# main_window.py
from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout
from PySide6.QtCore import QFile
from components.header import Header
from components.sidebar import Sidebar
from components.content import Content
from config import globals


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(globals.APP_TITLE)
        self.resize(globals.WINDOW_WIDTH, globals.WINDOW_HEIGHT)
        self.init_ui()
        self.load_global_styles()

    def init_ui(self):
        central_widget = QWidget()
        layout = QVBoxLayout()

        self.header = Header()
        self.sidebar = Sidebar()
        self.content = Content()

        layout.addWidget(self.header)
        layout.addWidget(self.sidebar)
        layout.addWidget(self.content)

        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def load_global_styles(self):
        file = QFile("resources/global.qss")
        if file.open(QFile.ReadOnly | QFile.Text):
            self.setStyleSheet(file.readAll().data().decode())
