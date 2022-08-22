import os
import shutil
from tkinter import *
from tkinter import messagebox
from time import sleep
from multiprocessing import Process
import RPi.GPIO as GPIO


# class DummyStepperMotor():

#     def __init__(self, which, step_pin, direction_pin, X_MS1_Pin, X_MS2_Pin, X_MS3_Pin, Y_MS1_Pin, Y_MS2_Pin, Y_MS3_Pin, delay=0.208, resolution = 1):
#         self.which = which
#         self.step_pin = step_pin
#         self.direction_pin = direction_pin
#         self.delay = delay
#         self.current_step = 0

#         self.current_position = 0

#     def move(self, step):
#         print(f"Moving {step} step")

class StepperMotor():
    def __init__(self, which, step_pin, direction_pin, X_MS1_Pin, X_MS2_Pin, X_MS3_Pin, Y_MS1_Pin, Y_MS2_Pin, Y_MS3_Pin, delay=0.208, resolution = 1):
        self.which = which
        self.step_pin = step_pin
        self.direction_pin = direction_pin
        self.delay = delay
        self.current_step = 0

        self.current_position = 0

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.step_pin, GPIO.OUT)
        GPIO.setup(self.direction_pin, GPIO.OUT)

        if (which == "x"):
            GPIO.setup(X_MS1_Pin, GPIO.OUT)
            GPIO.setup(X_MS2_Pin, GPIO.OUT)
            GPIO.setup(X_MS3_Pin, GPIO.OUT)

            GPIO.output(X_MS1_Pin, resolution_dict[resolution][0])
            GPIO.output(X_MS2_Pin, resolution_dict[resolution][1])
            GPIO.output(X_MS3_Pin, resolution_dict[resolution][2])
        else:
            GPIO.setup(Y_MS1_Pin, GPIO.OUT)
            GPIO.setup(Y_MS2_Pin, GPIO.OUT)
            GPIO.setup(Y_MS3_Pin, GPIO.OUT)

            GPIO.output(Y_MS1_Pin, resolution_dict[resolution][0])
            GPIO.output(Y_MS2_Pin, resolution_dict[resolution][1])
            GPIO.output(Y_MS3_Pin, resolution_dict[resolution][2])


    def move(self, steps_to_take):
        GPIO.output(self.direction_pin, int(steps_to_take > 0))

        for x in range(abs(steps_to_take)):
            GPIO.output(self.step_pin, GPIO.HIGH)
            self.current_step += 1
            sleep(self.delay)
            GPIO.output(self.step_pin, GPIO.LOW)
            sleep(self.delay)

        return True


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
        #self.is_seleced = False

    def reach_me(self):
        print()
        print("Going to this cell")
        read_current_positoin()

        print(f"Moving to the x={self.midpoint_coord[0]}, y={self.midpoint_coord[1]}")
        print(f'X diff: {self.midpoint_coord[0] - x_stepper_motor.current_position}, Y diff: {self.midpoint_coord[1] - y_stepper_motor.current_position}')

        if __name__ == "__main__":
            p1 = Process(target = x_stepper_motor.move, args=(self.midpoint_coord[0] - x_stepper_motor.current_position,))
            p2 = Process(target = y_stepper_motor.move, args=(self.midpoint_coord[1] - y_stepper_motor.current_position,))
            p1.start()
            p2.start()
            p1.join()
            p2.join()

        # x_stepper_motor.move(self.midpoint_coord[0] - x_stepper_motor.current_position)
        # y_stepper_motor.move(self.midpoint_coord[1] - y_stepper_motor.current_position)

        self.capture_me()

        x_stepper_motor.current_position = self.midpoint_coord[0]
        y_stepper_motor.current_position = self.midpoint_coord[1]

        save_current_position()
        print()

    def capture_me(self):
        sleep(int(wait_time.get()))
        photo_name = f"{self.cell_index}_cell_photo.jpeg"
        os.chdir("cell_photos/")
        os.system(f"LD_PRELOAD=/usr/lib/arm-linux-gnueabihf/libv4l/v4l1compat.so fswebcam --no-banner {photo_name}")
        print(f"Taking picture {photo_name} with WEB camera")
        os.chdir("/home/pi")

class Tasks():
    def __init__(self):
        self.list_of_tasks = []

    def add_or_remove_task(self, task):
        if (task in self.list_of_tasks):
            self.list_of_tasks.remove(task)
            task.configure(bg=unselected_cell_button_color)
        else:
            self.list_of_tasks.append(task)
            task.configure(bg=selected_cell_button_color)

    def execute_tasks(self):
        for task in self.list_of_tasks:
            task.reach_me()

    def clear_tasks(self):
        for task in self.list_of_tasks:
            task.configure(bg=unselected_cell_button_color)
        self.list_of_tasks.clear()


    def select_all(self):
        for task in grid_frame.winfo_children():
            if (task in self.list_of_tasks):
                continue
            else:
                self.list_of_tasks.append(task)
                task.configure(bg=selected_cell_button_color)

def to_initial_position():
    if not is_initial_position_set:
        messagebox.showerror(title="Внимание!", message="Необходимо для начала назначить начальную точку.")
        return

    print("Going back")
    answer = messagebox.askyesno(title="Внимание!", message="Хотите вернуться в исходную точку?")

    if answer:
        read_current_positoin()
        print(f'(Back) X diff: {-abs(x_stepper_motor.current_position)}, Y diff: {-abs(y_stepper_motor.current_position)}')

        if __name__ == "__main__":
            p1 = Process(target = x_stepper_motor.move, args=(-abs(x_stepper_motor.current_position),))
            p2 = Process(target = y_stepper_motor.move, args=(-abs(y_stepper_motor.current_position),))
            p1.start()
            p2.start()
            p1.join()
            p2.join()

        # x_stepper_motor.move(-abs(x_stepper_motor.current_position))
        # y_stepper_motor.move(-abs(y_stepper_motor.current_position))

        x_stepper_motor.current_position = 0
        y_stepper_motor.current_position = 0

        save_current_position()
        print('Reached the initial point!')

        messagebox.showwarning(title="Сообщение", message="Возвращен на исходную точку")

    tasks.list_of_tasks.clear()

def chosen_by(index):
    chosen = grid_frame.winfo_children()[index-1]
    tasks.add_or_remove_task(chosen)
    print(chosen.midpoint_coord)
    print("Tasks count: ", len(tasks.list_of_tasks))

def choose_all():
    if them_all.get():
        tasks.select_all()
    else:
        tasks.clear_tasks()

def run_process():
    if not is_initial_position_set:
        messagebox.showerror(title="Внимание!", message="Необходимо для начала назначить начальную точку.")
        return

    print("Tasks count: ", len(tasks.list_of_tasks))
    print()
    
    create_photos_folder()
    
    for task in tasks.list_of_tasks:
        task.reach_me()
        task.configure(bg=unselected_cell_button_color)

    sleep(int(wait_time.get()))
    messagebox.showinfo(title="Сообщение", message="Процесс завершен")
    to_initial_position()

def create_photos_folder():
    if not (os.path.exists("cell_photos/")):
        os.makedirs("cell_photos/")
    elif len(os.listdir("cell_photos/")) > 0:
        shutil.rmtree("cell_photos/")
        os.makedirs("cell_photos/")
        
def create_grid():
    global grid

    if not calculate_max_steps():
        return

    try:
        assert width.get() != ""; checking_width = int(width.get())
        assert height.get() != ""; checking_height = int(height.get())
        assert wait_time.get() != ""; checking_wait = int(height.get())
    except:
        print("No or invalid data for grid creation")
        messagebox.showerror("Внимание!", "Введите корректные данные о сетке")
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

                cell_button = ButtonCell(cell_count, (cell_x_coord, cell_y_coord), grid_frame, text = str(cell_count), bg=unselected_cell_button_color, activebackground=pressed_cell_button_color, command= lambda ztemp= cell_count : chosen_by(ztemp), font=main_font)
                cell_button.grid(row = i, column = j, sticky="WENS")

                cell_button.bind("<Enter>", cell_on_enter)
                cell_button.bind("<Leave>", cell_on_leave)

        all_cells = Checkbutton(footer_frame, text='Все ячейки',variable=them_all, onvalue=1, offvalue=0, command=choose_all, font=main_font)
        all_cells.grid(row = grid.number_of_cols+3, column = 0, pady = 5, sticky="WENS")

        execute_button = Button(footer_frame, text = "Начать", command = run_process, font=main_font, bg=start_button_color, activebackground=pressed_start_button_color)
        execute_button.grid(row = grid.number_of_cols+4, column = 0, pady = 5, sticky="WENS")

        execute_button.bind("<Enter>", on_enter)
        execute_button.bind("<Leave>", on_leave)

        grid_frame.grid_columnconfigure(list(range(grid.number_of_cols)), weight=1)
        grid_frame.grid_rowconfigure(list(range(grid.number_of_rows)), weight=1)

        grid_frame.pack(expand=True, fill=BOTH)
        footer_frame.pack(expand=True, fill=BOTH)



def set_initial_position(event):
    create_grid_button.focus_set()

    global is_initial_position_set

    x_stepper_motor.current_position = 0
    y_stepper_motor.current_position = 0

    with open("current_position.txt", "w") as file:
        file.write(str(0) + "," + str(0))
    messagebox.showinfo("Сообщение", "Исходная точка назначена")
    is_initial_position_set = True

def save_current_position():
    with open("current_position.txt", "w") as file:
        file.write(str(x_stepper_motor.current_position) + "," + str(y_stepper_motor.current_position))

def read_current_positoin():
    with open("current_position.txt", "r") as file:
        x_read, y_read = file.readline().split(",")
        x_stepper_motor.current_position, y_stepper_motor.current_position = int(x_read), int(y_read)


def up(event):
    y_stepper_motor.move(manual_step)
    y_stepper_motor.current_position += manual_step
def down(event):
    y_stepper_motor.move(-manual_step)
    y_stepper_motor.current_position += -manual_step
def left(event):
    x_stepper_motor.move(-manual_step)
    x_stepper_motor.current_position += -manual_step
def right(event):
    x_stepper_motor.move(manual_step)
    x_stepper_motor.current_position += manual_step

resolution_dict = {1: [0,0,0],
                   2: [1,0,0],
                   4: [0,1,0],
                   8: [1,1,0],
                  16: [1,1,1],}


def calculate_max_steps():
    global X_MAX, Y_MAX

    try:
        assert workzone_width.get() != ""; checking_width = int(workzone_width.get())
        assert workzone_height.get() != ""; checking_height = int(workzone_height.get())
    except:
        print("No or invalid data for working zone")
        messagebox.showerror("Внимание!", "Введите корректные данные о рабочей зоне")
        return
    else:
        X_MAX = int(int(workzone_width.get())/x_one_revol_cm*one_revol_steps) # 2500
        Y_MAX = int(int(workzone_height.get())/y_one_revol_cm*one_revol_steps) # 1300

        return True

def on_enter(e):
    e.widget['background'] = '#7f997c'
def on_leave(e):
    e.widget['background'] = '#c1d6c4'

def cell_on_enter(e):
    if not (e.widget in tasks.list_of_tasks):
        e.widget['background'] = hover_cell_button_color

def cell_on_leave(e):
    if not (e.widget in tasks.list_of_tasks):
        e.widget['background'] = unselected_cell_button_color



X_STEP_PIN = 23
X_DIRECTION_PIN = 24

X_MS1_Pin = 14
X_MS2_Pin = 15
X_MS3_Pin = 18


Y_STEP_PIN = 16
Y_DIRECTION_PIN = 20

Y_MS1_Pin = 25
Y_MS2_Pin = 8
Y_MS3_Pin = 7

is_initial_position_set = False

x_one_revol_cm = 4
y_one_revol_cm = 3.8

one_revol_steps = 200

X_MAX = 0
Y_MAX = 0

manual_step = 50

master = Tk()

grid = None
tasks = Tasks()


x_stepper_motor = StepperMotor("x", X_STEP_PIN, X_DIRECTION_PIN, X_MS1_Pin, X_MS2_Pin, X_MS3_Pin, Y_MS1_Pin, Y_MS2_Pin, Y_MS3_Pin, 0.0005)
y_stepper_motor = StepperMotor("y", Y_STEP_PIN, Y_DIRECTION_PIN, X_MS1_Pin, X_MS2_Pin, X_MS3_Pin, Y_MS1_Pin, Y_MS2_Pin, Y_MS3_Pin, 0.0005)

# x_stepper_motor = DummyStepperMotor("x", X_STEP_PIN, X_DIRECTION_PIN, X_MS1_Pin, X_MS2_Pin, X_MS3_Pin, Y_MS1_Pin, Y_MS2_Pin, Y_MS3_Pin, 0.0005)
# y_stepper_motor = DummyStepperMotor("y", Y_STEP_PIN, Y_DIRECTION_PIN, X_MS1_Pin, X_MS2_Pin, X_MS3_Pin, Y_MS1_Pin, Y_MS2_Pin, Y_MS3_Pin, 0.0005)


master.title("Image Taker")
main_font = ("Terminal", 14)

start_button_color = "#c1d6c4"
create_grid_button_color = "#c1d6c4"
to_initial_position_button_color = "#c1d6c4"

pressed_start_button_color = "#647a62"
pressed_create_grid_button_color = "#647a62"
pressed_to_initial_position_button_color = "#647a62"


hover_cell_button_color = "#c2c2c2"
selected_cell_button_color = "#609e64"
pressed_cell_button_color = "#9e9e9e"
unselected_cell_button_color = "#d9d9d9"


main_frame = Frame(master)
grid_frame = Frame(master)
footer_frame = Frame(master)

main_frame.grid_columnconfigure(list(range(2)), weight=1)
main_frame.grid_rowconfigure(list(range(5)), weight=1)

footer_frame.grid_columnconfigure(0, weight=1)
footer_frame.grid_rowconfigure(list(range(3)), weight=1)

workzone_width = StringVar()
workzone_height = StringVar()
width = StringVar()
height = StringVar()
them_all = BooleanVar()
wait_time = StringVar()


workzone_width_label = Label(main_frame, text = "Ширина раб.зоны (см):", anchor=CENTER, relief=RIDGE, font=main_font)
workzone_height_label = Label(main_frame, text = "Длина раб.зоны (см):", anchor=CENTER, relief=RIDGE, font=main_font)
width_label = Label(main_frame, text = "Кол. строк:", anchor=CENTER, relief=RIDGE, font=main_font)
height_label = Label(main_frame, text = "Кол. столб:", anchor=CENTER, relief=RIDGE, font=main_font)
wait_label = Label(main_frame, text = "Ожидание (сек):", anchor=CENTER, relief=RIDGE, font=main_font)

workzone_width_label.grid(row = 0, column = 0, pady = 2, sticky="WENS")
workzone_height_label.grid(row = 1, column = 0, pady = 2, sticky="WENS")
width_label.grid(row = 2, column = 0, pady = 2, sticky="WENS")
height_label.grid(row = 3, column = 0, pady = 2, sticky="WENS")
wait_label.grid(row = 4, column = 0, pady = 2, sticky="WENS")


workzone_height_entry = Entry(main_frame, textvariable = workzone_height)
workzone_width_entry = Entry(main_frame, textvariable = workzone_width)
height_entry = Entry(main_frame, textvariable = height)
width_entry = Entry(main_frame, textvariable = width)
wait_entry = Entry(main_frame, textvariable = wait_time)

workzone_height_entry.grid(row = 0, column = 1, pady = 2, sticky="WENS")
workzone_width_entry.grid(row = 1, column = 1, pady = 2, sticky="WENS")
height_entry.grid(row = 2, column = 1, pady = 2, sticky="WENS")
width_entry.grid(row = 3, column = 1, pady = 2, sticky="WENS")
wait_entry.grid(row = 4, column = 1, pady = 2, sticky="WENS")

create_grid_button = Button(main_frame, height = 2, text = "Создать сетку", command = create_grid, font=main_font, bg=create_grid_button_color, activebackground=pressed_create_grid_button_color)
create_grid_button.grid(row = 5, column = 0, columnspan = 2, pady = 5, sticky="WENS")

back_button = Button(main_frame, height = 2, text = "На исходную точку", command = to_initial_position, font=main_font, bg=to_initial_position_button_color, activebackground=pressed_to_initial_position_button_color)
back_button.grid(row = 6, column = 0, columnspan = 2, pady = 5, sticky="WENS")

main_frame.pack(expand=True, fill=BOTH)


create_grid_button.bind("<Enter>", on_enter)
create_grid_button.bind("<Leave>", on_leave)

back_button.bind("<Enter>", on_enter)
back_button.bind("<Leave>", on_leave)

master.bind("<Return>", set_initial_position)

master.bind("<Up>", up)
master.bind("<Down>", down)
master.bind("<Left>", left)
master.bind("<Right>", right)

mainloop()

GPIO.cleanup()
print()
print("Finish!")
