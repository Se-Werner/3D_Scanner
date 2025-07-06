from machine import Pin, I2C
import utime
from vl53l0x import VL53L0X


class StepperMotor:
    def __init__(self, pins):
        self.pin_out = [Pin(pins[0], Pin.OUT),
                        Pin(pins[1], Pin.OUT),
                        Pin(pins[2], Pin.OUT),
                        Pin(pins[3], Pin.OUT)]

        self.step_sequence = [[1, 0, 0, 1],
                              [1, 1, 0, 0],
                              [0, 1, 1, 0],
                              [0, 0, 1, 1]]

        self.current_position = 1_000_000
        self.max_position = 2_000_000
        self.step_index = 0

    def step(self, direction, steps, speed):

        if self.max_position < self.current_position + (steps * direction):
            steps = self.max_position - self.current_position
        elif self.current_position + (steps * direction) < 0:
            steps = self.current_position

        for i in range(steps):
            self.step_index = (self.step_index + direction) % len(self.step_sequence)
            self.current_position += direction
            for pin_index in range(len(self.pin_out)):
                pin_value = self.step_sequence[self.step_index][pin_index]
                self.pin_out[pin_index].value(pin_value)
            utime.sleep(speed)

    def set_current_position(self):
        self.current_position = 0

    def set_max_position(self):
        self.max_position = self.current_position

    def release_stepper(self):
        for pin in self.pin_out:
            pin.value(0)

    def move_to_position(self, position, speed):

        target_position = round(self.max_position * (position / 100), 0)

        steps_needed = target_position - self.current_position
        if steps_needed < 0:
            direction = -1
        elif steps_needed > 0:
            direction = 1

        self.step(direction, steps_needed, speed)


class LidarSensor:
    def __init__(self, i2c_id, sda_pin, scl_pin):

        self.i2c = I2C(id=i2c_id, sda=Pin(sda_pin), scl=Pin(scl_pin))

        self.sensor = VL53L0X(self.i2c)
        self.sensor.set_measurement_timing_budget(40_000)
        self.sensor.set_Vcsel_pulse_period(self.sensor.vcsel_period_type[0], 12)
        self.sensor.tof.set_Vcsel_pulse_period(self.sensor.vcsel_period_type[1], 8)

        self.zero = 0

    def read(self):
        measurement_value = self.zero - self.sensor.ping()
        return measurement_value

    def set_zero(self):
        self.zero = self.sensor.ping()
