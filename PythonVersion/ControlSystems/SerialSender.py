from serial import Serial
import time


class SerialSender:

    EMPTY_MSG_ARR = ["000", "000", "00", "00", "0", "0"]
    EMPTY_MSG_STR = "000000000000"

    def __init__(self, port):
        self.ser = Serial(port, 9600)
        self.message_arr = SerialSender.EMPTY_MSG_ARR

        self.__get_arduino_ready()
        self.__wait_for_initialization()

    def set_message_vals(self, msg):
        self.message_arr = msg

    def message_to_serial(self):
        serial_str = ""       

        if len(self.message_arr) != 12:
            serial_str = SerialSender.EMPTY_MSG_STR
            print("There was a problem with the length of the string")
        else:
            for i, string in enumerate(self.message_arr):
                serial_str = string + self.message_arr[i]

        self.ser.write(serial_str)
        return serial_str

    def __get_arduino_ready(self):
        msg = ""
        while msg.find("ready") == -1:
            if self.ser.inWaiting() > 0:
                c = self.ser.read()
                msg += c.decode('utf-8')

        print("Arduino " + msg)

    def __wait_for_initialization(self):
        time.sleep(1)
        while self.__check_reset():
            print('Kill Switch Off')
            time.sleep(1)

        self.ser.write(SerialSender.EMPTY_MSG_STR.encode())
        time.sleep(8.5)

    def __check_reset(self):
        val = False
        if self.ser.inWaiting() > 0:
            c = self.ser.read()
            num = int(str(c.decode('utf-8')))
        else:
            num = 0
        if num is 1:
            val = True
        self.ser.reset_input_buffer()
        return val
    

if __name__ == "__main__":
    s = SerialSender("/dev/ttyACM0")

    message = input("What do you want to send to the arduino?")

    s.set_message_vals(message)
    s.message_to_serial()
