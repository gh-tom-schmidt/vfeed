# main_window.py
from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout
from PySide6.QtCore import QFile
from config import globals

from components.video_streamer import VideoStreamer
from modules.video_engine import VideoEngine
from components.image_extractor import ImageExtractor


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(globals.APP_TITLE)
        self.resize(globals.WINDOW_WIDTH, globals.WINDOW_HEIGHT)

        self.video_engine = VideoEngine()

        central_widget = QWidget()
        layout = QVBoxLayout()

        # Left pane
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)

        left_layout.addWidget(VideoStreamer(self.video_engine))

        # Right pane
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)

        right_layout.addWidget(ImageExtractor(self.video_engine))

        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        file = QFile("resources/global.qss")
        if file.open(QFile.ReadOnly | QFile.Text):
            self.setStyleSheet(file.readAll().data().decode())
