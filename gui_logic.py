from tkinter import *
from tkinter.ttk import *
import tkinter as tk
from tkinter import messagebox


def save_current_position():
    with open("current_position.txt", "w") as file:
        file.write(str(M1x) + "," + str(M1y) + "," + str(M2x) + "," + str(M2y))

def read_current_positoin():
    with open("current_position.txt", "r") as file:
        all_line = file.readline()

class Grid():
    def __init__(self, number_of_rows, number_of_cols):
        self.number_of_rows = number_of_rows
        self.number_of_cols = number_of_cols

class Cell():
    def __init__(self, midpoint_coord):
        pass

class Task():
    def __init__(self, ):
        pass

class Tasks():
    def __init__(self, ):
        pass


def to_initial_position():
    print("Going back")
    messagebox.showinfo("Сообщение", "На исходную точку")

list_of_tasks = set()

def chosen_by(index):
    print(index-1)
    print(grid_frame.winfo_children()[index-1])
    if (grid_frame.winfo_children()[index-1] in list_of_tasks):
        list_of_tasks.remove(grid_frame.winfo_children()[index-1])
    else:
        # grid_frame.winfo_children()[index-1].configure(bg="red", fg="yellow")
        list_of_tasks.add(grid_frame.winfo_children()[index-1])

    print(list_of_tasks)

def create_grid():
    if not (width.get() == "" and height.get() == ""):
        if (grid_frame.winfo_children()):
            for child in grid_frame.winfo_children():
                child.destroy()
        cell_count = 0
        for i in range(int(width.get())):
            for j in range(int(height.get())):
                cell_count += 1
                back_button = Button(grid_frame, text = str(cell_count), command= lambda ztemp= cell_count : chosen_by(ztemp))
                back_button.grid(row = i, column = j, sticky="wens")
    else:
        print("No date for grid creation")
        messagebox.showinfo("Сообщение", "Введите данные о сетке")

    grid_frame.pack()


master = Tk()

master.title("Image Taker")

main_frame = Frame(master)
grid_frame = Frame(master)

width = StringVar()
height = StringVar()
them_all = BooleanVar()
wait_time = StringVar()

width_label = Label(main_frame, text = "Кол. строк:")
height_label = Label(main_frame, text = "Кол. столб:")
wait_label = Label(main_frame, text = "Ожидание (сек):")

width_label.grid(row = 0, column = 0, sticky = W, pady = 2)
height_label.grid(row = 1, column = 0, sticky = W, pady = 2)
wait_label.grid(row = 2, column = 0, sticky = W, pady = 2)

width_entry = Entry(main_frame, textvariable = width)
height_entry = Entry(main_frame, textvariable = height)
wait_entry = Entry(main_frame, textvariable = wait_time)

width_entry.grid(row = 0, column = 1, pady = 2)
height_entry.grid(row = 1, column = 1, pady = 2)
wait_entry.grid(row = 2, column = 1, pady = 2)

create_grid_button = Button(main_frame, text = "Создать сетку", command = create_grid)
create_grid_button.grid(row = 3, column = 0, columnspan = 2, pady = 5)

back_button = Button(main_frame, text = "На исходную точку", command = to_initial_position)
back_button.grid(row = 4, column = 0, columnspan = 2, pady = 5)

main_frame.pack()

mainloop()

print("Finish!")
