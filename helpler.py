import tkinter as tk

master = tk.Tk()

frame = tk.Frame(master, width=40, height=40) #their units in pixels
button1 = tk.Button(frame, text="btn")


frame.grid_propagate(False) #disables resizing of frame
frame.columnconfigure(0, weight=1) #enables button to fill frame
frame.rowconfigure(0,weight=1) #any positive number would do the trick

frame.grid(row=0, column=1) #put frame where the button should be
button1.grid(sticky="wens") #makes the button expand

tk.mainloop()
