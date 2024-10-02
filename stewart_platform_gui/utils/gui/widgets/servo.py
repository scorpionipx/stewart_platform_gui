import math

from pathlib import Path

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage, QPixmap, QTransform
from PyQt5.QtWidgets import QLabel, QPushButton


from stewart_platform_gui.settings import SETTINGS


SERVO_STYLESHEET = ''


CENTER_OFFSET = SETTINGS['holder']['size'] * .4  # value got from trial & error to get best visuals
VERTICAL_VISUAL_OFFSET = SETTINGS['height'] // 160  # rotating image results in some strange size deformations


BUTTON_SIZE = SETTINGS['height'] // 18
br = BUTTON_SIZE // 2
BUTTON_STATE_ON_STYLESHEET = f'border-radius : {br}; border : 4px solid black; background-color: darkorange'
BUTTON_STATE_OFF_STYLESHEET = f'border-radius : {br}; border : 4px solid black; background-color: grey'

cos_30 = math.cos(30 * math.pi / 180)
sin_30 = math.sin(30 * math.pi / 180)


class Servo:
    """
    Servo
    """
    __all__ = []
    
    def __init__(self, parent, servo_holder, rotation_angle, on_pixmap, off_pixmap, uid):
        """
        __init__
        """
        Servo.__all__.append(self)
        self.__on_pixmap = on_pixmap
        self.__off_pixmap = off_pixmap

        self.__state = False  # off
        self.__uid = uid

        self.parent = parent
        self.rotation_angle = rotation_angle

        self.body = QLabel(parent)
        self.body.setAlignment(Qt.AlignCenter)
        self.body.setStyleSheet(SERVO_STYLESHEET)
        self.body.resize(SETTINGS['servo']['size'], SETTINGS['servo']['size'])
        self.body.setPixmap(off_pixmap.transformed(QTransform().rotate(rotation_angle)))

        # fk trigonometry
        if self.rotation_angle == 0:
            self.body.move(
                servo_holder.x() + (servo_holder.width() - self.body.width()) // 2,
                servo_holder.y() + (servo_holder.height() - self.body.height()) // 2
                - CENTER_OFFSET + VERTICAL_VISUAL_OFFSET,
            )
        elif self.rotation_angle == 60:
            self.body.move(
                servo_holder.x() + (servo_holder.width() - self.body.width()) // 2
                + CENTER_OFFSET * cos_30,
                servo_holder.y() + (servo_holder.height() - self.body.height()) // 2
                - CENTER_OFFSET * sin_30,
            )
        elif self.rotation_angle == 120:
            self.body.move(
                servo_holder.x() + (servo_holder.width() - self.body.width()) // 2
                + CENTER_OFFSET * cos_30,
                servo_holder.y() + (servo_holder.height() - self.body.height()) // 2
                + CENTER_OFFSET * sin_30,
            )
        elif self.rotation_angle == 180:
            self.body.move(
                servo_holder.x() + (servo_holder.width() - self.body.width()) // 2,
                servo_holder.y() + (servo_holder.height() - self.body.height()) // 2
                + CENTER_OFFSET - VERTICAL_VISUAL_OFFSET,
            )
        elif self.rotation_angle == 240:
            self.body.move(
                servo_holder.x() + (servo_holder.width() - self.body.width()) // 2
                - CENTER_OFFSET * cos_30,
                servo_holder.y() + (servo_holder.height() - self.body.height()) // 2
                + CENTER_OFFSET * sin_30,
            )
        elif self.rotation_angle == 300:
            self.body.move(
                servo_holder.x() + (servo_holder.width() - self.body.width()) // 2
                - CENTER_OFFSET * cos_30,
                servo_holder.y() + (servo_holder.height() - self.body.height()) // 2
                - CENTER_OFFSET * sin_30,
            )
        self.body.show()

        self.toggle_button = QPushButton(parent)
        self.toggle_button.resize(BUTTON_SIZE, BUTTON_SIZE)
        self.toggle_button.setStyleSheet(BUTTON_STATE_OFF_STYLESHEET)
        self.toggle_button.clicked.connect(self.__toggle)
        self.toggle_button.move(
            self.body.x() + (self.body.width() - self.toggle_button.width()) // 2,
            self.body.y() + (self.body.height() - self.toggle_button.height()) // 2,
        )
        self.toggle_button.show()

    @property
    def state(self):
        return self.__state

    @property
    def uid(self):
        return self.__uid

    def __toggle(self):
        if self.__state:
            self.__state = False
            self.toggle_button.setStyleSheet(BUTTON_STATE_OFF_STYLESHEET)
            self.body.setPixmap(self.__off_pixmap.transformed(QTransform().rotate(self.rotation_angle)))
        else:
            self.__state = True
            self.toggle_button.setStyleSheet(BUTTON_STATE_ON_STYLESHEET)
            self.body.setPixmap(self.__on_pixmap.transformed(QTransform().rotate(self.rotation_angle)))
