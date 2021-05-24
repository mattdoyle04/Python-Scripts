class ElliotWave:
    
    
    def __init__(self, df=None):
        
        self.potential_waves = []
        self.reset()
        self.bars = df
        self.rows = df.shape[0]
        
    
    def reset(self):
        
        self.start_date = None
        
        self.wave_1 = False
        self.wave_1_start = None
        self.wave_1_end = None
        self.wave_1_high = None
        self.wave_1_length = None
        self.wave_1_bars = 0
        
        self.wave_2 = False
        self.wave_2_start = None
        self.wave_2_end = None
        self.wave_2_high = None
        self.wave_2_length = None

        self.wave_3 = False
        self.wave_3_start = None
        self.wave_3_end = None
        self.wave_3_length = None
        
        self.correction_1 = False
        self.correction_2 = False
    
        self.elliott_wave = False
        

    def wave_length(self, end, start):
        
        return (end - start) / start
    
    
    def end_wave_one(self):
        
        self.wave_1 = False
        self.wave_1_bars = 0
        self.correction_1 = True
        
    
    def end_correction_one(self, close):
        
        self.correction_1 = False
        self.wave_2 = True
        self.wave_2_start = close
        
    
    def end_wave_two(self):
        
        self.wave_2 = False
        self.correction_2 = True
        
    
    def end_correction_two(self, close):
        
        self.correction_2 = False
        self.wave_3 = True
        self.wave_3_start = close
        
    
    def iterate_rows(self):

        for i in range(self.rows):

            if i > 0:

                date = self.bars.index[i].strftime('%d-%m-%Y')
                high = self.bars.loc[self.bars.index[i], 'High']
                low = self.bars.loc[self.bars.index[i], 'Low']
                close = self.bars.loc[self.bars.index[i], 'Close']
                prior_close = self.bars.loc[self.bars.index[i-1], 'Close']

                up = True if close > prior_close else False

                if self.elliott_wave:

                    if self.wave_1:

                        if up:
                            self.wave_1_high = high
                            print('{} - WAVE 1 - UP - {}'.format(date, high))
                            pass
                        else:
                            self.wave_1_length = self.wave_length(prior_close, self.wave_1_start)
                            self.end_wave_one()
                            print('{} - WAVE 1 - ENDED - {} - LENGTH - {}'.format(date, prior_close, self.wave_1_length))

                    elif self.correction_1:
                        
                        # Volume should be lower during wave two than during wave one 
                        # Prices usually do not retrace more than 61.8% of the wave one gains
                        # Prices should fall in a three wave pattern

                        if not up:
                            if close < self.wave_1_start:
                                self.reset()
                                print('{} - CORRECTION 1 GONE TOO FAR | E.O.W. - {}'.format(date, close))
                            else:
                                print('{} - CORRECTION 1 DOWN - {}'.format(date, close))
                                pass
                        else:
                            self.end_correction_one(prior_close)
                            print('{} - CORRECTION 1 ENDED - {}'.format(date, close))

                    elif self.wave_2:
                        
                        # Wave three often extends wave one by a ratio of 1.618:1.

                        if up:
                            self.wave_2_high = high
                            print('{} - WAVE 2 - UP - {}'.format(date, close))
                            pass
                        else:
                            self.wave_2_length = self.wave_length(prior_close, self.wave_2_start)

                            if self.wave_2_length < self.wave_1_length:
                                self.reset()  
                                print('{} - WAVE 2 LENGTH < WAVE 1 LENGTH | E.O.W. - {} < {}'.format(date, self.wave_1_length, self.wave_2_length))
                            else:
                                self.end_wave_two()
                                print('{} - WAVE 2 - ENDED - {} - LENGTH - {}'.format(date, close, self.wave_2_length))

                    elif self.correction_2:
                        
                        # Wave four typically retraces less than 38.2% of wave three
                        # Volume is well below that of wave three

                        if not up:
                            if low < self.wave_1_high:
                                self.reset()
                                print('{} - CORRECTION 2 THROUGH TOP OF WAVE 1 | E.O.W. - {}'.format(date, close))
                            else:
                                print('{} - CORRECTION 2 DOWN - {}'.format(date, close))
                                pass
                        else:
                            self.end_correction_two(prior_close)
                            print('{} - CORRECTION 2 ENDED - {}'.format(date, close))
                            print('------------------LAUNCH!!!------------------')

                    elif self.wave_3:
                        
                        # Volume is often lower in wave five than in wave three 
                        # Momentum indicators start to show divergences (prices higher but indicators not)
                        
                        if up:
                            print('{} - WAVE 3 - UP - {}'.format(date, close))
                            pass
                        else:
                            self.wave_3_length = self.wave_length(prior_close, self.wave_3_start)
                            self.potential_waves.append({'start':self.start_date, 'end':self.bars.index[i]})
                            print('END OF ELLIOT WAVE - {}'.format(self.wave_3_length))
                            self.reset()

                else:

                    if up:
                        self.wave_1_bars += 1

                        if self.wave_1_bars > 2:
                            self.wave_1 = True
                            self.wave_1_start = self.bars.loc[self.bars.index[i-3], 'Close']
                            self.elliott_wave = True
                            self.start_date = self.bars.index[i]
                            print('{} - WAVE 1 STARTED - {}'.format(date, close))
                        else:
                            print('UP'.format(date, close))
                            pass
                            
                    else:
                        print('DOWN'.format(date, close))
                        pass
