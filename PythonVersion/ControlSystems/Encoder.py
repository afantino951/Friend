import Jetson.GPIO as GPIO
import math
import time


class Encoder:

    LEFT_PIN_A = 15
    LEFT_PIN_B = 16

    RIGHT_PIN_A = 11
    RIGHT_PIN_B = 13

    def __init__(self, pin_a, pin_b):
        self.pin_a = pin_a
        self.pin_b = pin_b

        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.pin_a, GPIO.IN)
        GPIO.setup(self.pin_b, GPIO.IN)

        self.last_delta = 0
        self.r_seq = self.rotation_sequence()
        self.count = 0

        self.steps_per_cycles = 4*4*298
        self.remainder = 0

    def rotation_sequence(self):
        a_state = GPIO.input(self.pin_a)
        b_state = GPIO.input(self.pin_b)

        r_seq = (a_state ^ b_state) | b_state << 1
        return r_seq

    def get_delta(self):
        delta = 0
        r_seq = self.rotation_sequence()

        if r_seq != self.r_seq:
            delta = (r_seq - self.r_seq) % 4

            if delta == 3:
                delta = -1
            elif delta == 2:
                delta = int(math.copysign(delta, self.last_delta))

            self.last_delta = delta
            self.r_seq = r_seq
        
        return delta
    
    def get_cycles(self):
        self.remainder += self.get_delta()
        cycles = self.remainder // self.steps_per_cycles
        self.remainder %= self.steps_per_cycles

        return cycles

    def set_value(self, val):
        pass

    def reset_encoder_value(self):
        pass


if __name__ == "__main__":
    l_cycles = 0
    r_cycles = 0
    l_t = time.time()
    r_t = time.time()

    left_encoder = Encoder(15, 16)
    right_encoder = Encoder(11, 13)

    while True:
        l_tmp = left_encoder.get_cycles()
        r_tmp = right_encoder.get_cycles()

        if l_tmp == 0:
            continue
        if (l_tmp*l_cycles) < 0:
            l_t = time.time()
            l_cycles = 0

        if r_tmp == 0:
            continue
        elif (r_tmp*r_cycles) < 0:
            r_t = time.time()
            r_cycles = 0

        l_cycles += l_tmp
        r_cycles += r_tmp

        print("%d cycles in %f seconds \t\t %d cycles in %f seconds"
              % (l_cycles, (time.time() - l_t), r_cycles, (time.time() - r_t)))
