#/usr/bin/python2.7
# -*- coding:utf-8 -*-

from Tkinter import *
import time
import sys
 
def get_window(): 
    tk=Tk()
    tk.geometry("200x75+800+400")
    #поверх всех окон
    tk.wm_attributes('-topmost',1)
    Label(text=sys.argv[1], width=20, height=3).pack(expand='YES')
    Button(tk, text = "OK", command = tk.destroy).pack(expand='YES')
    tk.mainloop()
    

get_window()

