import tkinter as tk

def on_enter(e):
    e.widget['background'] = 'green'

def on_leave(e):
    e.widget['background'] = 'SystemButtonFace'

root = tk.Tk()
myButton = tk.Button(root,text="Click Me")
myButton.grid()


myButton.bind("<Enter>", on_enter)
myButton.bind("<Leave>", on_leave)

myButton2 = tk.Button(root,text="Click Me")
myButton2.grid()


myButton2.bind("<Enter>", on_enter)
myButton2.bind("<Leave>", on_leave)

root.mainloop()
