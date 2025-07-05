from machine import Pin
import utime
import component_classes


y_motor = component_classes.StepperMotor([10, 11, 12, 13])
x_motor = component_classes.StepperMotor([21, 20, 19, 18])

range_sensor = component_classes.LidarSensor(0, 0, 1)

y_button = Pin(17, Pin.IN)
x_button = Pin(16, Pin.IN)

def home_y_axis():

    while True:
        if y_button.value() == 1:
            y_motor.set_current_position()
            break
        elif y_button.value() == 0:
            y_motor.step(-1, 20, 0.01)

        utime.sleep(0.01)

    y_motor.step(1, 100, 0.01)

    while True:
        if y_button.value() == 1:
            y_motor.set_max_position()
            break
        elif y_button.value() == 0:
            y_motor.step(1, 20, 0.01)

        utime.sleep(0.01)

    y_motor.step(-1, 100, 0.01)

def home_x_axis():

    while True:
        if x_button.value() == 1:
            x_motor.set_current_position()
            break
        elif x_button.value() == 0:
            x_motor.step(-1, 20, 0.01)

        utime.sleep(0.01)

    x_motor.step(1, 100, 0.01)

    while True:
        if x_button.value() == 1:
            x_motor.set_max_position()
            break
        elif x_button.value() == 0:
            x_motor.step(1, 20, 0.01)

        utime.sleep(0.01)

    x_motor.step(-1, 100, 0.01)

home_y_axis()
home_x_axis()

y_motor.move_to_position(50, 0.01)
x_motor.move_to_position(50, 0.01)

y_motor.release_stepper()
x_motor.release_stepper()

