import time

print('enter the amount of time you want to countdown')

time_Hour = int(input('enter the hours: '))
time_Minute = int(input('enter the minutes: '))
time_Second = int(input('enter the seconds: '))

countdown_Time = time_Hour*3600 + time_Minute*60 + time_Second

def countdown(t):
    while t:
        mins, secs = divmod(t,60)
        hours, mins = divmod(mins,60)
        timer = '{:02d}:{:02d}:{:02d}'.format(hours,mins,secs)
        print(timer, end = '\r')
        time.sleep(1)
        t-=1
    
    print('DONE DONE DONE DONE')

countdown(countdown_Time)