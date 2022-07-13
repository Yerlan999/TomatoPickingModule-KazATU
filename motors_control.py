import RPi.GPIO as GPIO
from time import sleep

class StepperHandler():

    __CLOCKWISE = 1
    __ANTI_CLOCKWISE = 0

    def __init__(self, which, step_pin, direction_pin, delay=0.208, resolution = 1, steps_per_revolution=200,):

        self.which = which
        self.CLOCKWISE = self.__CLOCKWISE
        self.ANTI_CLOCKWISE = self.__ANTI_CLOCKWISE
        self.step_pin = step_pin
        self.direction_pin = direction_pin
        self.delay = delay
        self.revolution_steps = steps_per_revolution
        self.current_direction = self.CLOCKWISE
        self.current_step = 0

        self.current_position = tuple()

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.step_pin, GPIO.OUT)
        GPIO.setup(self.direction_pin, GPIO.OUT)

        if (which == "x"):
            GPIO.setup(X_MS1_pin, GPIO.OUT)
            GPIO.setup(X_MS2_pin, GPIO.OUT)
            GPIO.setup(X_MS3_pin, GPIO.OUT)
        else:
            GPIO.setup(Y_MS1_pin, GPIO.OUT)
            GPIO.setup(Y_MS2_pin, GPIO.OUT)
            GPIO.setup(Y_MS3_pin, GPIO.OUT)

        if (resolution == 1):
            pass
        else if (resolution == 2):
            pass
        else if (resolution == 4):
            pass
        else if (resolution == 8):
            pass
        else if (resolution == 16):
            pass

    def Step(self, steps_to_take, direction = __CLOCKWISE):

        print("Step pin: " + str(self.step_pin) + " direction pin: " + str(self.direction_pin) + " delay: " + str(self.delay))
        print("Taking " + str(steps_to_take) + " steps.")

        GPIO.output(self.direction_pin, direction)

        for x in range(steps_to_take):
            print("Step " + str(x))
            GPIO.output(self.step_pin, GPIO.HIGH)
            self.current_step += 1
            sleep(self.delay)
            GPIO.output(self.step_pin, GPIO.LOW)
            sleep(self.delay)



X_STEP_PIN = 23
X_DIRECTION_PIN = 24

Y_STEP_PIN = 16
Y_DIRECTION_PIN = 20

X_MAX = 3000
Y_MAX = 3100

X_MS1_Pin = 14
X_MS2_Pin = 15
X_MS3_Pin = 18

Y_MS1_Pin = 25
Y_MS2_Pin = 8
Y_MS3_Pin = 7


x_stepperHandler = StepperHandler("x", X_STEP_PIN, X_DIRECTION_PIN, 0.0025)

x_stepperHandler.Step(200)

x_stepperHandler.Step(200, x_stepperHandler.ANTI_CLOCKWISE)
