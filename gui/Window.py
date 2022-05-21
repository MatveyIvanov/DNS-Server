import os
import sys
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

from gui.DNSWidget import DNSWidget


MIN_SIZE = (720, 360)
DARK_THEME_COLOR = (50, 50, 50)
CURRENT_DIRECTORY = os.path.dirname(os.path.realpath(__file__))

class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("DNS-Client")
        self.setFixedSize(MIN_SIZE[0], MIN_SIZE[1])

        font_path = os.path.join(CURRENT_DIRECTORY, "fonts", "Koulen-Regular.ttf")
        _id = QFontDatabase.addApplicationFont(font_path)
        if QFontDatabase.applicationFontFamilies(_id) == -1:
            print("Problem loading font")
            sys.exit(-1)

        self.setFont(QFont('Koulen', 12))
        p = self.palette()
        p.setColor(self.backgroundRole(), QColor(qRgb(*DARK_THEME_COLOR)))
        self.setPalette(p)

        self.dns_widget = DNSWidget(
            self, fixed_size=QSize(self.width(), self.height())
        )
