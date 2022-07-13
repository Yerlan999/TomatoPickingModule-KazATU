from tkinter import *
from tkinter import messagebox
from time import sleep

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
        self.cell_width = self.calculate_cell_width()
        self.cell_height = self.calculate_cell_height()

    def calculate_cell_width(self):
        return self.x_max/self.number_of_cols
    def calculate_cell_height(self):
        return self.y_max/self.number_of_rows


class ButtonCell(Button):
    def __init__(self, cell_index, midpoint_coord, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cell_index = cell_index
        self.midpoint_coord = midpoint_coord


class Tasks():
    def __init__(self):
        self.list_of_tasks = []

    def add_or_remove_task(self, task):
        if (task in self.list_of_tasks):
            self.list_of_tasks.remove(task)
            task.configure(bg="white")
        else:
            self.list_of_tasks.append(task)
            task.configure(bg="green")

    def execute_tasks(self):
        pass

    def clear_tasks(self):
        for task in self.list_of_tasks:
            task.configure(bg="white")
        self.list_of_tasks.clear()


    def select_all(self):
        for task in grid_frame.winfo_children():
            if (task in self.list_of_tasks):
                continue
            else:
                self.list_of_tasks.append(task)
                task.configure(bg="green")

def to_initial_position():
    print("Going back")
    messagebox.showinfo("Сообщение", "На исходную точку")

tasks = Tasks()

def chosen_by(index):
    # print(index-1)
    # print(grid_frame.winfo_children()[index-1])

    chosen = grid_frame.winfo_children()[index-1]
    tasks.add_or_remove_task(chosen)

def run_process():
    # print(len(list_of_tasks))
    print(len(tasks.list_of_tasks))
    for task in tasks.list_of_tasks:
        print(task.cell_index, task.midpoint_coord)


def create_grid():
    global grid
    try:
        assert width.get() != ""; checking_width = int(width.get())
        assert height.get() != ""; checking_height = int(height.get())
    except:
        print("No or invalid data for grid creation")
        messagebox.showinfo("Сообщение", "Введите корректные данные о сетке")
    else:
        grid = Grid(X_MAX, Y_MAX, int(height.get()), int(width.get()))

        grid_frame.grid_columnconfigure(list(range(grid.number_of_rows)), weight=1)
        if (footer_frame.winfo_children()):
            for child in footer_frame.winfo_children():
                child.destroy()
        if (grid_frame.winfo_children()):
            for child in grid_frame.winfo_children():
                child.destroy()
        tasks.list_of_tasks.clear()
        cell_count = 0
        for i in range(grid.number_of_rows):
            for j in range(grid.number_of_cols):
                cell_count += 1

                cell_x_coord = int( grid.x_max/grid.number_of_cols/2 + (grid.x_max/grid.number_of_cols)*(j))
                cell_y_coord = grid.y_max - int( grid.y_max/grid.number_of_rows/2 + (grid.y_max/grid.number_of_rows)*(i))

                # print(cell_count, i, j, (cell_x_coord, cell_y_coord))

                back_button = ButtonCell(cell_count, (cell_x_coord, cell_y_coord), grid_frame, text = str(cell_count), command= lambda ztemp= cell_count : chosen_by(ztemp), font=main_font)
                back_button.grid(row = i, column = j, sticky="WENS")

        all_cells = Checkbutton(footer_frame, text='Все ячейки',variable=them_all, onvalue=1, offvalue=0, command=choose_all, font=main_font)
        all_cells.grid(row = grid.number_of_cols+3, column = 0, pady = 5, sticky="WENS")

        execute_button = Button(footer_frame, text = "Начать", command = run_process, font=main_font)
        execute_button.grid(row = grid.number_of_cols+4, column = 0, pady = 5, sticky="WENS")

        grid_frame.grid_columnconfigure(list(range(grid.number_of_cols)), weight=1)
        grid_frame.grid_rowconfigure(list(range(grid.number_of_rows)), weight=1)

        grid_frame.pack(expand=True, fill=BOTH)
        footer_frame.pack(expand=True, fill=BOTH)

def choose_all():
    if them_all.get():
        tasks.select_all()
    else:
        tasks.clear_tasks()


X_MAX = 2700 # Steps to reach the endge of X axis (EXAMPLE)
Y_MAX = 3100 # Steps to reach the endge of Y axis (EXAMPLE)


master = Tk()
grid = None

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
