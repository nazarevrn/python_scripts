# -*- coding:utf-8 -*-

from Tkinter import *
import time
 
def get_window(): 
#окно
    tk=Tk()
    tk.geometry("100x75+800+400")
    '''
    #кнопка 
    button = Button(tk, text="Хорошо!")
    button.pack(expand='YES')
    button.bind("<Button-1>", tk.destroy)
    '''
    #поверх всех окон
    tk.wm_attributes('-topmost',1)
    Label(text="Посмотри в окно!", width=20, height=3).pack(expand='YES')
    Button(tk, text = "OK", command = tk.destroy).pack(expand='YES')
    tk.mainloop()
    
i = 5
while i == 5:
    time.sleep(3600)
    get_window()

