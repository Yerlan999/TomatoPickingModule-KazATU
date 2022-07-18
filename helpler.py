# All fonts in Tkinter viewer

from tkinter import *
from tkinter import font

win = Tk()
win.geometry("750x350")
win.title('Font List')

fonts=list(font.families())
fonts.sort()
def fill_frame(frame):
   for f in fonts:
      label = Label(frame,text=f,font=(f, 14)).pack()

def onFrameConfigure(canvas):
   canvas.configure(scrollregion=canvas.bbox("all"))

canvas = Canvas(win,bd=1, background="white")
frame = Frame(canvas, background="white")
scroll_y = Scrollbar(win, orient="vertical", command=canvas.yview)
canvas.configure(yscrollcommand=scroll_y.set)
scroll_y.pack(side="right", fill="y")
canvas.pack(side="left", expand=1, fill="both")
canvas.create_window((5,4), window=frame, anchor="n")
frame.bind("<Configure>", lambda e, canvas=canvas: onFrameConfigure(canvas))
fill_frame(frame)
win.mainloop()

# Multiprocessing

from multiprocessing import Process
import sys

rocket = 0

def func1():
    global rocket
    print 'start func1'
    while rocket < sys.maxint:
        rocket += 1
    print 'end func1'

def func2():
    global rocket
    print 'start func2'
    while rocket < sys.maxint:
        rocket += 1
    print 'end func2'

# if __name__=='__main__':
#     p1 = Process(target = func1)
#     p1.start()
#     p2 = Process(target = func2)
#     p2.start()
