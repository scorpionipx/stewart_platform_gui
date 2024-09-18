import sys

from threading import Thread
from time import sleep

from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QSlider
from PyQt5.QtGui import QPixmap


from stewart_platform_gui import LOGGER
from stewart_platform_gui.settings import SETTINGS

from stewart_platform_gui.stm_driver import STMDriver


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
        self.__refresh_rate = 0.2
        self.control_thread_enabled = False
        self.__init_gui()
    
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
        servo_holder.resize(500, 500)
        servo_holder.setPixmap(QPixmap(r"D:\projects\stewart_platform_gui\stewart_platform_gui\utils\imgs\holder.png"))
        servo_holder.move(
            (SETTINGS['width'] - servo_holder.width()) // 2,
            (SETTINGS['height'] - servo_holder.height()) // 2 + self.status_label.height() // 2
        )
        servo_holder.show()

        slider = QSlider(self)
        slider.setRange(0, 180)
        slider.setValue(90)
        slider.resize(40, 400)
        slider.move(1100, 100)
        slider.valueChanged.connect(self.slider_value_changed)
        slider.show()

        self.servo_1 = QLabel(self)
        self.servo_1.setScaledContents(True)
        self.servo_1.resize(100, 220)
        self.servo_1.setPixmap(QPixmap(r"D:\projects\stewart_platform_gui\stewart_platform_gui\utils\imgs\servo.png"))
        self.servo_1.move((SETTINGS['width'] - self.servo_1.width()) // 2, 100)
        self.servo_1.show()

        servo_1_label = QLabel(self.servo_1)
        servo_1_label.move(12, 100)
        servo_1_label.resize(80, 30)
        servo_1_label.setStyleSheet("QLabel {color: '#BABBBB'; font-weight: bold; font-size: 24px}")
        servo_1_label.setText('   S1')
        servo_1_label.show()

        servo_1_angle_label = QLabel(self.servo_1)
        servo_1_angle_label.move(10, 170)
        servo_1_angle_label.resize(80, 30)
        servo_1_angle_label.setStyleSheet("QLabel {color: '#BABBBB'}")
        servo_1_angle_label.setText('     N/A')
        servo_1_angle_label.show()
        self.servo_1.servo_1_angle_label = servo_1_angle_label

        self.stm_driver = STMDriver(com_port='COM3')

        self.stm_driver.send_bytes(bytearray('1=100', encoding='utf-8'))

        self.start_control_thread()

    def slider_value_changed(self, value):
        """
        slider_value_changed
        """
        self.value = int(value)

    def start_control_thread(self):
        self.control_thread_enabled = True
        thread = Thread(target=self.control_thread)
        thread.start()

    def control_thread(self):
        loop_counter = 0
        while True:
            loop_counter += 1
            cmd = bytearray(f'1={self.value:03d}', encoding='utf-8')
            self.stm_driver.send_bytes(cmd)
            self.__set_status(f'1={self.value:03d}')
            self.servo_1.servo_1_angle_label.setText(f'     {self.value:03d}')
            sleep(self.__refresh_rate)

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

