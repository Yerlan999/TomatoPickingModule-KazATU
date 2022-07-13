from tkinter import *
from tkinter import messagebox


def save_current_position():
    with open("current_position.txt", "w") as file:
        file.write(str(M1x) + "," + str(M1y) + "," + str(M2x) + "," + str(M2y))

def read_current_positoin():
    with open("current_position.txt", "r") as file:
        all_line = file.readline()

class Grid():
    def __init__(self, x_max, y_max, number_of_rows, number_of_cols):
        self.x_max = x_max
        self.y_max = y_max
        self.number_of_rows = number_of_rows
        self.number_of_cols = number_of_cols

    def calculate_(self, ):
        pass


class Cell():
    def __init__(self, index, midpoint_coord):
        self.index = index
        self.midpoint_coord = midpoint_coord

class Tasks():
    def __init__(self, list_of_tasks):
        self.list_of_tasks = list_of_tasks

    def execute_tasks(self, ):
        pass


def to_initial_position():
    print("Going back")
    messagebox.showinfo("Сообщение", "На исходную точку")

list_of_tasks = []

def chosen_by(index):
    # print(index-1)
    # print(grid_frame.winfo_children()[index-1])

    chosen = grid_frame.winfo_children()[index-1]
    if (chosen in list_of_tasks):
        list_of_tasks.remove(chosen)
        chosen.configure(bg="white")
    else:
        list_of_tasks.append(chosen)
        chosen.configure(bg="green")

    # print(list_of_tasks)

def run_process():
    # print(len(list_of_tasks))
    print(width.get())
    print(height.get())


def create_grid():

    if not (width.get() == "" and height.get() == ""):
        grid_frame.grid_columnconfigure(list(range(int(height.get()))), weight=1)
        if (footer_frame.winfo_children()):
            for child in footer_frame.winfo_children():
                child.destroy()
        if (grid_frame.winfo_children()):
            for child in grid_frame.winfo_children():
                child.destroy()
        list_of_tasks.clear()
        cell_count = 0
        for i in range(int(height.get())):
            for j in range(int(width.get())):
                cell_count += 1
                print(cell_count, i, j)
                back_button = Button(grid_frame, text = str(cell_count), command= lambda ztemp= cell_count : chosen_by(ztemp), font=main_font)
                back_button.grid(row = i, column = j, sticky="WENS")

        all_cells = Checkbutton(footer_frame, text='Все ячейки',variable=them_all, onvalue=1, offvalue=0, command=choose_all, font=main_font)
        all_cells.grid(row = int(width.get())+3, column = 0, pady = 5, sticky="WENS")

        execute_button = Button(footer_frame, text = "Начать", command = run_process, font=main_font)
        execute_button.grid(row = int(width.get())+4, column = 0, pady = 5, sticky="WENS")

    else:
        print("No date for grid creation")
        messagebox.showinfo("Сообщение", "Введите данные о сетке")

    grid_frame.grid_columnconfigure(list(range(int(width.get()))), weight=1)
    grid_frame.grid_rowconfigure(list(range(int(height.get()))), weight=1)

    grid_frame.pack(expand=True, fill=BOTH)
    footer_frame.pack(expand=True, fill=BOTH)

def choose_all():
    if them_all.get():
        for child in grid_frame.winfo_children():
            if (child in list_of_tasks):
                continue
            else:
                list_of_tasks.append(child)
                child.configure(bg="green")
    else:
        for task in list_of_tasks:
            task.configure(bg="white")
        list_of_tasks.clear()





master = Tk()

master.title("Image Taker")
main_font = ("Terminal", 14)

main_frame = Frame(master)
grid_frame = Frame(master)
footer_frame = Frame(master)

main_frame.grid_columnconfigure(list(range(2)), weight=1)
main_frame.grid_rowconfigure(list(range(3)), weight=1)

footer_frame.grid_columnconfigure(0, weight=1)
footer_frame.grid_rowconfigure(list(range(3)), weight=1)

width = StringVar()
height = StringVar()
them_all = BooleanVar()
wait_time = StringVar()

width_label = Label(main_frame, text = "Кол. строк:", anchor=CENTER, relief=RIDGE, font=main_font)
height_label = Label(main_frame, text = "Кол. столб:", anchor=CENTER, relief=RIDGE, font=main_font)
wait_label = Label(main_frame, text = "Ожидание (сек):", anchor=CENTER, relief=RIDGE, font=main_font)

width_label.grid(row = 0, column = 0, pady = 2, sticky="WENS")
height_label.grid(row = 1, column = 0, pady = 2, sticky="WENS")
wait_label.grid(row = 2, column = 0, pady = 2, sticky="WENS")

height_entry = Entry(main_frame, textvariable = height)
width_entry = Entry(main_frame, textvariable = width)
wait_entry = Entry(main_frame, textvariable = wait_time)

height_entry.grid(row = 0, column = 1, pady = 2, sticky="WENS")
width_entry.grid(row = 1, column = 1, pady = 2, sticky="WENS")
wait_entry.grid(row = 2, column = 1, pady = 2, sticky="WENS")

create_grid_button = Button(main_frame, height = 2, text = "Создать сетку", command = create_grid, font=main_font)
create_grid_button.grid(row = 3, column = 0, columnspan = 2, pady = 5, sticky="WENS")

back_button = Button(main_frame, height = 2, text = "На исходную точку", command = to_initial_position, font=main_font)
back_button.grid(row = 4, column = 0, columnspan = 2, pady = 5, sticky="WENS")

main_frame.pack(expand=True, fill=BOTH)

mainloop()

print("Finish!")
