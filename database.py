import pandas as pd
import yfinance as yf
from datetime import datetime
from sqlalchemy import create_engine
from dateutil.relativedelta import relativedelta


def update_database(table, tickers, db_con, columns):

    up_to_date = False
    end = datetime.today().date()

    try:
        db_response = pd.read_sql('SELECT * FROM {}'.format(table), con=db_con)

    except Exception as e:
        start = datetime(2021,1,1)
        start_str = start.strftime('%Y-%m-%d')
        db_response = None

    else:
        db_response.set_index('Date', inplace=True)
        db_response.index = pd.to_datetime(db_response.index)
        max_date = db_response.index.max()
        start = (max_date + relativedelta(days=1)).date()
        if start < end:
            start_str = start.strftime('%Y-%m-%d')
        else:
            up_to_date = True
            
    finally:
        if not up_to_date:
            end_str = end.strftime('%Y-%m-%d')
            new_prices = yf.download(tickers, start=start_str, end=end_str, rounding=True)[columns]
            new_prices.fillna(method='ffill', inplace=True)
            new_prices = new_prices[(new_prices.index >= pd.to_datetime(start))]
            if db_response is not None:
                updated_prices = pd.concat([db_response, new_prices])
            else:
                updated_prices = new_prices.copy()
            updated_prices.to_sql(table, con=db_con, if_exists='replace')
        else:
            updated_prices = db_response.copy()

        return updated_prices


if __name__ == '__main__':

    updated_prices = dict() 
    columns = 'Close' 
    tables = {
        'EQUITIES':['^GSPC','^FTSE'],
        'CRYPTO':['ETH-USD','XRP-USD'],
        'CURRENCIES':['EURUSD=X','AUDUSD=X'] 
    } 
    
    db_con = create_engine('sqlite:///Database/prices.db', echo=False)

    for table, ticker_list in tables.items():
        tickers = ' '.join(tables[table])
        updated_prices[table] = update_database(table, tickers, db_con, columns)