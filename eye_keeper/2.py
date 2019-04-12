# -*- coding:utf-8 -*-

from Tkinter import *
import time
import datetime

def get_window(message): 
    tk=Tk()
    tk.geometry("200x75+800+400")
    #поверх всех окон
    tk.wm_attributes('-topmost',1)
    Label(text=message, width=20, height=3).pack(expand='YES')
    Button(tk, text = "OK", command = tk.destroy).pack(expand='YES')
    tk.mainloop()
    
# i = 5
# while i == 5:
#     time.sleep(3600)
#     get_window('123')

#get_window('123')

#datetime.datetime.today().weekday()
#0-Monday
#6-Sunday
def checkTime():
    now = datetime.datetime.today();
    #now = datetime.datetime(2019, 4, 12, 7, 59, 29, 787016);
    dayOfWeek = now.weekday();
    hour = now.hour;
    minute = now.minute;

    if (0 <= dayOfWeek <= 4):
        if (hour == 12 and minute == 59) or (hour == 7 and minute == 59) :
            get_window('Запусти задачу!')
        elif (hour == 12 and minute == 0) or (hour == 17 and minute == 0) :
            get_window('Останови задачу!')
        elif (minute == 0) :
            get_window('Посмотри в окно!')
        elif (minute %2 == 0) :
            get_window('Тест')



#exit();
i = 5
while i == 5:
    checkTime()
    time.sleep(60)
    
