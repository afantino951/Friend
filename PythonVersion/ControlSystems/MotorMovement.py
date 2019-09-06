from SerialSender import SerialSender
import time


class Motor:

    def __init__(self):
        self.serial = SerialSender('/dev/ttyACM0')

    def move_forward(self, speed):
        arr = [str(speed), str(speed), "11", "11", "1", "1"]
        self.serial.set_message_vals(arr)

        return arr

    def move_backwards(self, speed):
        arr = [str(speed), str(speed), "10", "10", "1", "0"]
        self.serial.set_message_vals(arr)

        return arr

    def turn_left(self, speed):
        arr = [str(speed), str(speed), "10", "01", "5", "0"]
        self.serial.set_message_vals(arr)

        return arr

    def turn_right(self, speed):
        arr = [str(speed), str(speed), "01", "10", "0", "5"]
        self.serial.set_message_vals(arr)

        return arr

    def stop_all_motors(self):
        arr = SerialSender.EMPTY_MSG_ARR
        self.serial.set_message_vals(arr)

        return arr


if __name__ == "__main__":
    start_time = time.time()
    m = Motor()

    while (time.time() - start_time) <= 5:
        m.move_forward(10)
