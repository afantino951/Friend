from ControlSystems.MotorMovement import Motor
import cv2


class Teleop:

    def __init__(self, speed):
        self.m = Motor()
        self.speed = speed

        self.m.stop_all_motors()

    def keyboard_forward(self):
        if (cv2.waitKey(1) & 0xFF) == ord('w'):
            self.m.move_forward(self.speed)

    def keyboard_backwards(self):
        if (cv2.waitKey(1) & 0xFF) == ord('s'):
            self.m.move_backwards(self.speed)

    def keyboard_left(self):
        if (cv2.waitKey(1) & 0xFF) == ord('a'):
            self.m.turn_left(self.speed)

    def keyboard_right(self):
        if (cv2.waitKey(1) & 0xFF) == ord('d'):
            self.m.turn_right(self.speed)


if __name__ == "__main__":
    t = Teleop(50)

    while True:
        t.keyboard_forward()
        t.keyboard_backwards()
        t.keyboard_left()
        t.keyboard_right()