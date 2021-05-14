# Correction 1 cannot go below the start of Wave 1
# Wave 2 cannot be shorter than 1 and 3
# Correction 2 cannot go below the top of Wave 1
# Wave 3 needs to end with momentum divergence

# Fibonacci Levels

wave_1_start = None
wave_1_end = None
wave_1_length = None
wave_1_bars = 0
wave_2_start = None
wave_2_end = None
wave_2_length = None

up = False

wave_1 = False
correction_1 = False
wave_2 = False
correction_2 = False
wave_3 = False

elliot_wave = False

rows = bars.shape[0]

for i in range(rows):
    
    if i > 0:
        
        date = bars.index[i].strftime('%d-%m-%Y')
        close = bars.loc[bars.index[i], 'Close']
        up = True if close > bars.loc[bars.index[i-1], 'Open'] else False
        
        if elliot_wave:
            
            if wave_1:
                
                if up:
                    print('{} - WAVE 1 - UP - {}'.format(date, close))
                else:
                    wave_1 = False
                    wave_1_end = close
                    wave_1_length = wave_1_end - wave_1_start
                    wave_1_bars = 0
                    correction_1 = True
                    print('{} - WAVE 1 - ENDED - {} - LENGTH - {}'.format(date, close, wave_1_length))
                    
            elif correction_1:
                
                if not up:
                    if close < wave_1_start:
                          correction_1 = False
                          elliot_wave = False
                          print('{} - CORRECTION 1 THROUGH START OF WAVE 1 - {}'.format(date, close))
                    else:
                        print('{} - CORRECTION 1 DOWN - {}'.format(date, close))
                else:
                    correction_1 = False
                    wave_2 = True
                    wave_2_start = close
                    print('{} - CORRECTION 1 ENDED - {}'.format(date, close))
                    
            elif wave_2:
                
                if up:
                    print('{} - WAVE 2 - UP - {}'.format(date, close))
                else:
                    wave_2 = False
                    wave_2_end = close
                    wave_2_length = wave_2_end - wave_2_start
                    print('{} - WAVE 2 - ENDED - {} - LENGTH - {}'.format(date, close, wave_2_length))
                          
                    if wave_2_length < wave_1_length:
                        elliot_wave = False
                        print('{} - WAVE 2 LENGTH < WAVE 1 LENGTH - {} < {}'.format(date, wave_1_length, wave_2_length))
                    else:
                        correction_2 = True
                    
            elif correction_2:
                
                if not up:
                    if close < wave_1_end:
                        correction_2 = False
                        elliot_wave = False
                        print('{} - CORRECTION 2 THROUGH END OF WAVE 1 - {}'.format(date, close))
                    else:
                        print('{} - CORRECTION 2 DOWN - {}'.format(date, close))
                else:
                    correction_2 = False
                    wave_3 = True
                    print('{} - CORRECTION 2 ENDED - {}'.format(date, close))
                    print('------------------LAUNCH!!!------------------')
                    
            elif wave_3:
                
                if up:
                    print('{} - WAVE 3 - UP - {}'.format(date, close))
                else:
                    wave_3 = False
                    elliot_wave = False
                    print('END OF ELLIOT WAVE')
                    
        else:
            
            if up:
                wave_1_bars += 1
                
                if wave_1_bars > 2:
                    wave_1 = True
                    wave_1_start = close
                    elliot_wave = True
                    print('{} - WAVE 1 STARTED - {}'.format(date, close))
