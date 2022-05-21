from tkinter import ACTIVE
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

from dns_client.dns_utils import process_dns_query

TEXT_COLOR = (255, 255, 255, 0.87)


class DNSWidget(QWidget):
    def __init__(self, parent: QWidget, fixed_size: QSize = None) -> None:
        super().__init__(parent)

        if fixed_size:
            self.setFixedSize(fixed_size)

        self.initUI()

    def initUI(self):
        self.__init_vertical_layout()
        self.__init_response_window()
        self.__init_layout()

        self.setStyleSheet(
            f"color: rgba({TEXT_COLOR[0]},{TEXT_COLOR[1]},{TEXT_COLOR[2]},{TEXT_COLOR[3]});"
        )
        self.setLayout(self.Layout)
        self.setGeometry(0, 0, self.size().width(), self.size().height())
        self.setFocus()
        self.show()

    def __init_layout(self):
        self.Layout = QGridLayout()

        self.Layout.addLayout(self.vLayout, 0, 0)
        self.Layout.addWidget(self.response, 0, 1, 4, 1)

    def __init_vertical_layout(self):
        self.vLayout = QVBoxLayout()
        self.vLayout.setSpacing(15)
        self.vLayout.setContentsMargins(25, 25, 25, 25)

        self.__init_domain_name()
        self.__init_many_check_box()
        self.__init_send_button()

        self.vLayout.addWidget(QLabel("Domain name:"))
        self.vLayout.addWidget(self.domain_name)
        self.vLayout.addWidget(self.many)
        self.vLayout.addWidget(self.button)

    def __init_domain_name(self):
        self.domain_name = QLineEdit(self)
        self.domain_name.setFont(QFont('Koulen', 11))
        self.domain_name.setPlaceholderText("www.example.com")
        self.domain_name.setStyleSheet(
            f"color: rgba({255-TEXT_COLOR[0]},{255-TEXT_COLOR[1]},{255-TEXT_COLOR[2]},{TEXT_COLOR[3] - 0.5});\
                border-radius: 5px;\
                padding: 10px"
        )
        self.domain_name.setFixedSize(200, self.domain_name.size().height() * 1.5)
        self.domain_name.textChanged.connect(self.__domain_name_changed)

    def __init_many_check_box(self):
        self.many = QCheckBox("Look for many IPs", self)
        self.many.setFont(QFont('Koulen', 9))
        self.many.setCheckable(True)
        self.many.setEnabled(True)
        self.many.setStyleSheet(
            "QCheckBox::indicator"
                "{"
                    "background-color: white;"
                    "border-radius: 5px;"
                "}"
            "QCheckBox::indicator::checked"
                "{"
                    "background-color: black;"
                "}"
        )

    def __init_send_button(self):
        self.button = QPushButton(self)
        self.button.setFont(QFont('Koulen', 11))
        self.button.setText("Get IP")
        self.button.setEnabled(False)
        self.button.setStyleSheet(
            f"background-color: rgba({255-TEXT_COLOR[0]},{255-TEXT_COLOR[1]},{255-TEXT_COLOR[2]},{TEXT_COLOR[3] - 0.5});\
                border-style: solid;\
                border-width: 2px;\
                border-radius: 5px;\
                padding: 5px;\
                border-color: rgba({255-TEXT_COLOR[0]},{255-TEXT_COLOR[1]},{255-TEXT_COLOR[2]},{TEXT_COLOR[3]});\
                color: rgba({TEXT_COLOR[0]},{TEXT_COLOR[1]},{TEXT_COLOR[2]},{TEXT_COLOR[3]});"
        )
        self.button.clicked.connect(self.__show_ips)

    def __init_response_window(self):
        self.response = QTextEdit()
        self.response.setFont(QFont('Koulen', 16))
        self.response.setReadOnly(True)
        self.response.setStyleSheet("border-radius: 30px;\
            background-clip: border;\
            background-color: rgb(220, 220,220);\
            color: rgba({TEXT_COLOR[0]},{TEXT_COLOR[1]},{TEXT_COLOR[2]},{TEXT_COLOR[3]});\
            padding: 50px")

    def __domain_name_changed(self):
        if self.domain_name.text() == '':
            self.button.setEnabled(False)
            self.domain_name.setStyleSheet(
                f"color: rgba({255-TEXT_COLOR[0]},{255-TEXT_COLOR[1]},{255-TEXT_COLOR[2]},{TEXT_COLOR[3] - 0.5});\
                    border-radius: 5px;\
                    padding: 10px"
            )
            self.button.setStyleSheet(
                f"background-color: rgba({255-TEXT_COLOR[0]},{255-TEXT_COLOR[1]},{255-TEXT_COLOR[2]},{TEXT_COLOR[3] - 0.5});\
                    border-style: solid;\
                    border-width: 2px;\
                    border-radius: 5px;\
                    padding: 5px;\
                    border-color: rgba({255-TEXT_COLOR[0]},{255-TEXT_COLOR[1]},{255-TEXT_COLOR[2]},{TEXT_COLOR[3]});\
                    color: rgba({TEXT_COLOR[0]},{TEXT_COLOR[1]},{TEXT_COLOR[2]},{TEXT_COLOR[3]});"
            )
        else:
            self.button.setEnabled(True)
            self.domain_name.setStyleSheet(
                f"color: rgba({255-TEXT_COLOR[0]},{255-TEXT_COLOR[1]},{255-TEXT_COLOR[2]},{TEXT_COLOR[3]});\
                    border-radius: 5px;\
                    padding: 10px"
            )
            self.button.setStyleSheet(
                f"background-color: rgba({255-TEXT_COLOR[0]},{255-TEXT_COLOR[1]},{255-TEXT_COLOR[2]},{TEXT_COLOR[3]});\
                    border-style: solid;\
                    border-width: 2px;\
                    border-radius: 5px;\
                    padding: 5px;\
                    border-color: rgba({255-TEXT_COLOR[0]},{255-TEXT_COLOR[1]},{255-TEXT_COLOR[2]},{TEXT_COLOR[3]});\
                    color: rgba({TEXT_COLOR[0]},{TEXT_COLOR[1]},{TEXT_COLOR[2]},{TEXT_COLOR[3]});"
            )

    def __get_ips(self) -> dict:
        return process_dns_query(
            domain_name=self.domain_name.text(),
            many=self.many.isChecked())

    def __show_ips(self):
        result = self.__get_ips()
        # Check for errors
        if result['errors']:
            self.response.setText(f"\n\
            There was an error while handling a dns query.\n\n\
            Error message: {result['errors']}")
        else:
            ip_text = 'IP address:'
            if len(result['ip_addresses']) > 1:
                ip_text = 'IP addresses:'
            
            ip_addresses = f'{result["ip_addresses"].pop()}\n                                    '
            ip_addresses += '\n                                    '.join(result["ip_addresses"])

            self.response.setText(f"\
            Success!\n\
            Domain name: {result['domain_name']}\n\
            {ip_text}   {ip_addresses}")