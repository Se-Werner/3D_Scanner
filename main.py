from machine import Pin
import utime
import component_classes


y_motor = component_classes.StepperMotor((10, 11, 12, 13))
x_motor = component_classes.StepperMotor((21, 20, 19, 18))

range_sensor = component_classes.LidarSensor(0, 0, 1)

y_button = Pin(17, Pin.IN)
x_button = Pin(16, Pin.IN)

def home_motor(motor, button):

    while True:
        if button.value() == 1:
            motor.set_current_position()
            break
        elif button.value() == 0:
            motor.step(-1, 20, 0.01)

        utime.sleep(0.01)

    motor.step(1, 100, 0.01)

    while True:
        if button.value() == 1:
            motor.set_max_position()
            break
        elif button.value() == 0:
            motor.step(1, 20, 0.01)

        utime.sleep(0.01)

    motor.step(-1, 100, 0.01)


home_motor(y_motor, y_button)
home_motor(x_motor, x_button)

y_motor.move_to_position(50, 0.01)
x_motor.move_to_position(50, 0.01)

range_sensor.set_zero()

y_motor.release_stepper()
x_motor.release_stepper()

