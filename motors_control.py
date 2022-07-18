import RPi.GPIO as GPIO
from time import sleep

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


resolution_dict = {1: [0,0,0],
                   2: [1,0,0],
                   4: [0,1,0],
                   8: [1,1,0],
                  16: [1,1,1],}


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


X_MAX = 2700
Y_MAX = 3100

x_stepper_motor = StepperMotor("x", X_STEP_PIN, X_DIRECTION_PIN, X_MS1_Pin, X_MS2_Pin, X_MS3_Pin, Y_MS1_Pin, Y_MS2_Pin, Y_MS3_Pin, 0.0005)
y_stepper_motor = StepperMotor("y", Y_STEP_PIN, Y_DIRECTION_PIN, X_MS1_Pin, X_MS2_Pin, X_MS3_Pin, Y_MS1_Pin, Y_MS2_Pin, Y_MS3_Pin, 0.0005)


GPIO.cleanup()
print("Finish!")
