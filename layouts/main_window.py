# main_window.py
from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout
from PySide6.QtCore import QFile
from configs import globals

from components.video_streamer import VideoStreamer
from components.info_table import VideoInfoTable
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

        # -------- left pane --------
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)

        # add a VideoStreamer component to the left pane
        self.video_streamer = VideoStreamer(self.video_engine)
        left_layout.addWidget(self.video_steamer)

        # add a VideoInfoTable compenent to the left pane
        self.video_info_table = VideoInfoTable(self.video_engine)
        left_layout.addWidget(video_info_table)

        # --------- right pane --------
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)

        # add a tabbar
        tab_widget = QTabWidget()

        # First tab
        tab1 = QWidget()
        tab1.setLayout(VideoEditor())

        # Second tab
        tab2 = QWidget()
        layout2 = QVBoxLayout()
        layout2.addWidget(QLabel("This is the second tab"))
        tab2.setLayout(VideoExtractor())

        # Add tabs
        tab_widget.addTab(tab1, "Video Editor")
        tab_widget.addTab(tab2, "Video Extractor")

        right_layout.addWidget(tab_widget)

        # ------------------ Split screen -------------------
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(left_widget)
        splitter.addWidget(right_widget)
        splitter.setSizes([2, 1])
        layout.addWidget(splitter)

        # add the layout to the central widget
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # apply global stylesheet
        file = QFile("styles/global.qss")
        if file.open(QFile.ReadOnly | QFile.Text):
            self.setStyleSheet(file.readAll().data().decode())
