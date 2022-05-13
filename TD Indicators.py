import pandas as pd
import yfinance as yf
from datetime import datetime
from dateutil.relativedelta import relativedelta

tickers = ['ETH-USD']
start = datetime(2021,1,1).strftime('%Y-%m-%d')
end = datetime.today().date().strftime('%Y-%m-%d')
prices = yf.download(tickers, start=start, end=end, rounding=True)
prices.fillna(method='ffill', inplace=True)
close = prices['Close']
high = prices['High']
low = prices['Low']

buy_setup = None
sell_setup = None
support_breached = False
resistance_breached = False

for i in range(4, close.shape[0]):
    
    date = close.index[i].date().strftime('%d-%b-%Y')
    high_0, low_0 = high.iloc[i].squeeze(), low.iloc[i].squeeze()
    t_0, t_1, t_2, t_3, t_4, t_5 = close.iloc[i].squeeze(), close.iloc[i-1].squeeze(), close.iloc[i-2].squeeze(), close.iloc[i-3].squeeze(), close.iloc[i-4].squeeze(), close.iloc[i-5].squeeze()
    
    if buy_setup:

        if t_0 < t_4:
            buy_setup_count += 1
            if t_0 < support:
                support_breached = True
            if buy_setup_count == 6:
                bar_6 = low_0
            elif buy_setup_count == 7:
                bar_7 = low_0
            elif buy_setup_count == 8:
                bar_8 = low_0
            elif buy_setup_count == 9:
                bar_9 = low_0
                if ((bar_8 < bar_6) or (bar_8 < bar_7)) or ((bar_9 < bar_6) or (bar_9 < bar_7)):
                    buy_setup = False
                    buy_setup_count = 0
                    resistance = temp_resistance
                    print(date, 'Buy Setup Complete', 'Resistance:', resistance, 'Support Breached:', support_breached)
                    support_breached = False
                else:
                    buy_setup_count = 8
                    print(date, 'Not Yet Perfect Buy Setup')
        else:
            buy_setup = False
            buy_setup_count = 0
            
    elif sell_setup:
        
        if t_0 > t_4:
            sell_setup_count += 1
            if t_0 > resistance:
                resistance_breached = True
            if sell_setup_count == 6:
                bar_6 = high_0
            elif sell_setup_count == 7:
                bar_7 = high_0
            elif sell_setup_count == 8:
                bar_8 = high_0
            elif sell_setup_count == 9:
                bar_9 = high_0
                if ((bar_8 > bar_6) or (bar_8 > bar_7)) or ((bar_9 > bar_6) or (bar_9 > bar_7)):     
                    sell_setup = False
                    sell_setup_count = 0
                    support = temp_support
                    print(date, 'Sell Setup Complete', 'Support:', support, 'Resistance Breached:', resistance_breached) 
                    resistance_breached = False
                else:
                    sell_setup_count = 8
                    print(date, 'Not Yet Perfect Sell Setup')
        else:
            sell_setup = False
            sell_setup_count = 0
            
    else:
        if (t_1 > t_5) & (t_0 < t_4):
            buy_setup = True
            buy_setup_count = 1
            temp_resistance = high_0
        elif (t_1 < t_5) & (t_0 > t_4):
            sell_setup = True
            sell_setup_count = 1
            temp_support = low_0
            
