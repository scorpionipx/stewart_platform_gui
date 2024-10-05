import math
import sys

from pathlib import Path

from threading import Thread
from time import sleep

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QSlider
from PyQt5.QtGui import QPixmap, QTransform


from stewart_platform_gui import LOGGER
from stewart_platform_gui.settings import SETTINGS
from stewart_platform_gui.utils.gui.widgets.servo import Servo

from stewart_platform_gui.stm_driver import STMDriver

IMG_DIR = Path(__file__).parent.joinpath('utils').joinpath('img')
SERVO_ON_IMG = IMG_DIR.joinpath('servo_sq_on.png')
SERVO_OFF_IMG = IMG_DIR.joinpath('servo_sq_off.png')


class StewartPlatformGUI(QMainWindow):
    """
    StewartPlatformGUI
    """
    def __init__(self):
        LOGGER.info('init')
        super(StewartPlatformGUI, self).__init__()

        self.status_label = QLabel(self)

        self.servos = []

        self.__set_status('Ready')

        self.value = 90
        self.__refresh_rate = 0.001
        self.control_thread_enabled = False
        self.__init_gui()

        self.__buffer = []

        self.load_csv('')

    def load_csv(self, csv):
        csv = Path(__file__).parent.joinpath('utils').joinpath('csv').joinpath('servo_dummy_data.csv')
        with open(csv, 'r') as fh:
            content = fh.read()
        for index, line in enumerate(content.split()[1:]):
            self.__buffer.extend(map(int, line.split(',')))

    def __init_gui(self):
        """
        __init_gui
        """
        self.setStyleSheet("QMainWindow {background: '#4E5254'; border-radius: 0px; color: 'yellow'; }")
        self.setFixedSize(SETTINGS['width'], SETTINGS['height'])
        self.setWindowTitle(SETTINGS['title'])

        self.status_label.setText(' Idle')
        self.status_label.setStyleSheet("QLabel {color: '#BABBBB'; background-color: '#3C3F41'}")
        self.status_label.setFixedWidth(SETTINGS['width'])
        self.status_label.move(0, 0)
        self.status_label.show()

        servo_holder = QLabel(self)
        servo_holder.setScaledContents(True)
        servo_holder.resize(SETTINGS['holder']['size'], SETTINGS['holder']['size'])
        servo_holder_pixmap = QPixmap(r"D:\projects\stewart_platform_gui\stewart_platform_gui\utils\img\holder.png")
        servo_holder.setPixmap(servo_holder_pixmap)
        servo_holder.move(
            40,
            (SETTINGS['height'] - servo_holder.height()) // 2 + self.status_label.height() // 2
        )
        servo_holder.show()

        scale = int(SETTINGS['servo']['size']/math.sqrt(2))
        servo_on_pixmap = QPixmap(SERVO_ON_IMG.as_posix()).scaled(scale, scale)
        servo_off_pixmap = QPixmap(SERVO_OFF_IMG.as_posix()).scaled(scale, scale)

        self.servo_1 = Servo(
            parent=self,
            servo_holder=servo_holder,
            rotation_angle=0,
            on_pixmap=servo_on_pixmap,
            off_pixmap=servo_off_pixmap,
            uid=1,
        )

        self.servo_2 = Servo(
            parent=self,
            servo_holder=servo_holder,
            rotation_angle=60,
            on_pixmap=servo_on_pixmap,
            off_pixmap=servo_off_pixmap,
            uid=2,
        )

        self.servo_3 = Servo(
            parent=self,
            servo_holder=servo_holder,
            rotation_angle=120,
            on_pixmap=servo_on_pixmap,
            off_pixmap=servo_off_pixmap,
            uid=3,
        )

        self.servo_4 = Servo(
            parent=self,
            servo_holder=servo_holder,
            rotation_angle=180,
            on_pixmap=servo_on_pixmap,
            off_pixmap=servo_off_pixmap,
            uid=4,
        )

        self.servo_5 = Servo(
            parent=self,
            servo_holder=servo_holder,
            rotation_angle=240,
            on_pixmap=servo_on_pixmap,
            off_pixmap=servo_off_pixmap,
            uid=5,
        )

        self.servo_6 = Servo(
            parent=self,
            servo_holder=servo_holder,
            rotation_angle=300,
            on_pixmap=servo_on_pixmap,
            off_pixmap=servo_off_pixmap,
            uid=6,
        )

        self.slider = QSlider(self)
        self.slider.setRange(0, 180)
        self.slider.setValue(90)
        self.slider.resize(80, 800)
        self.slider.move(SETTINGS['width'] - self.slider.width() * 2, 100)
        self.slider.valueChanged.connect(self.slider_value_changed)
        self.slider.show()
        slider_label = QLabel(self)
        slider_label.resize(40, 40)
        slider_label.move(self.slider.x(), self.slider.y() + self.slider.height() + 20)
        slider_label.setText('090')
        slider_label.show()
        self.slider.label = slider_label

        self.stm_driver = STMDriver(com_port='COM4')

        self.start_control_thread()

    def slider_value_changed(self, value):
        """
        slider_value_changed
        """
        self.value = int(value)
        self.slider.label.setText(f'{self.value:03d}')

    def start_control_thread(self):
        self.control_thread_enabled = True
        thread = Thread(target=self.control_thread)
        thread.start()

    def control_thread(self):
        sleep(2)
        # return
        loop_counter = 0
        buffer_index = 0
        buffer_len = len(self.__buffer)
        while True:
            loop_counter += 1
            cmd_bytes = [182, ]
            cmd_bytes.extend(self.__buffer[buffer_index:buffer_index+6])
            buffer_index += 6
            if buffer_index >= buffer_len:
                buffer_index = 0

            cmd = bytearray(cmd_bytes)
            # for b in cmd_bytes:
            #     print(hex(b))
            self.stm_driver.send_bytes(cmd)


            # for servo in Servo.__all__:
            #     servo: Servo
            #     val = self.__buffer[buffer_index] * 2
            #     if val > 180:
            #         val //= 2
            #     cmd = bytearray(f'{servo.uid}={self.__buffer[buffer_index]:03d}', encoding='utf-8')
            #     buffer_index += 1
            #     if buffer_index >= buffer_len:
            #         buffer_index = 0
            #
            #     self.stm_driver.send_bytes(cmd)
            #     sleep(.0001)
            #     # if servo.state:
            #     #     cmd = bytearray(f'{servo.uid}={self.value:03d}', encoding='utf-8')
            #     #     self.stm_driver.send_bytes(cmd)
            #     #     sleep(.001)
            # self.__set_status(f'{loop_counter:08d}')
            sleep(self.__refresh_rate)
            # input('press any key to go to the next loop')  # TODO: remove e after HW fix

    def __set_status(self, text, level=None):
        """
        __set_status
        """
        self.status_label.setText(f' {text}')
        
    def __connect(self):
        """
        
        """


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = StewartPlatformGUI()
    win.show()
    sys.exit(app.exec_())

