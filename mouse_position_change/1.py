from ctypes import windll, Structure, c_long, byref
import time, win32api, win32con

class POINT(Structure):
    _fields_ = [("x", c_long), ("y", c_long)]

def queryMousePosition():
    pt = POINT()
    windll.user32.GetCursorPos(byref(pt))
    return { "x": pt.x, "y": pt.y}

def click(x,y):
    win32api.SetCursorPos((x,y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)


i = 5
while i == 5:
    pos_begin = queryMousePosition()
    time.sleep(300)
    pos_end = queryMousePosition()
    try:
        if ( pos_begin['x'] - pos_end['x'] == 0 ) or ( pos_begin('y') - pos_end['y'] == 0 ):
            x_new = pos_end['x'] + 1
            y_new = pos_end['y'] + 1
            click(x_new, y_new)
            print "Mouse has been moved!"
    except TypeError:
        print "No need to move mouse"
        continue
