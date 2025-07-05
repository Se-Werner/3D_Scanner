from machine import Pin
import utime


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

        for i in range(steps):
            self.step_index = (self.step_index + direction) % len(self.step_sequence)
            self.current_position += direction
            for pin_index in range(len(self.pin_out)):
                pin_value = self.step_sequence[self.step_index][pin_index]
                self.pin_out[pin_index].value(pin_value)
            utime.sleep(speed)

    def set_current_position(self, position):
        self.current_position = position

    def set_max_position(self, position):
        self.max_position = position

    def release_stepper(self):
        for pin in self.pin_out:
            pin.value(0)