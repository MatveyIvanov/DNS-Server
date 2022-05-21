import sys
from PySide6.QtWidgets import QApplication
import sys
from gui.Window import Window


if __name__ == "__main__":
    app = QApplication([])

    window = Window()
    window.show()

    sys.exit(app.exec_())
