# main_window.py
from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QPushButton,
    QFileDialog,
    QSplitter,
)
from PySide6.QtCore import QFile, Qt, QThread
from configs import globals

from components.video_streamer import VideoStreamer
from components.info_table import VideoInfoTable
from modules.video_engine import VideoEngine


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(globals.APP_TITLE)
        self.resize(globals.WINDOW_WIDTH, globals.WINDOW_HEIGHT)

        # create the main widget
        self.central_widget = QWidget()
        self.main_layout = QVBoxLayout()

        # File selector
        self.open_button = QPushButton("Open Video")
        self.open_button.setFixedSize(150, 40)
        self.open_button.clicked.connect(self.selectAndBuild)
        self.main_layout.addWidget(self.open_button, alignment=Qt.AlignCenter)

        # add the layout to the central widget
        self.central_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.central_widget)

        # apply global stylesheet
        file = QFile("styles/global.qss")
        if file.open(QFile.ReadOnly | QFile.Text):
            self.setStyleSheet(file.readAll().data().decode())

        # close VideoEngine Thread when window gets closed unexpected
        # self.aboutToQuit.connect(self.video_engine_thread.stop)
        # self.aboutToQuit.connect(self.video_engine_thread.quit)
        # self.aboutToQuit.connect(self.video_engine_thread.wait)

    def closeEvent(self, event):
        """
        Override the closeEvent from the MainWindow
        """

        self.video_engine.stop()
        self.video_engine_thread.quit()
        self.video_engine_thread.wait()
        event.accept()

    def selectAndBuild(self) -> None:
        """
        Opens a file dialog to select a video file and loads the main layout.
        """

        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Video File",
            "",
            "Video Files (*.mp4 *.avi *.mov *.mkv);;All Files (*)",
        )

        # remove the open button from the layout
        self.main_layout.removeWidget(self.open_button)
        self.open_button.setParent(None)
        self.open_button.deleteLater()

        # create a thread for the video engine
        self.video_engine_thread = QThread()
        self.video_engine = VideoEngine(file_path)
        self.video_engine.moveToThread(self.video_engine_thread)

        # ---------------- Left Split screen ------------------
        left_splitter = QSplitter(Qt.Vertical)

        # add a VideoStreamer component to the left pane
        self.video_streamer = VideoStreamer(self.video_engine)
        left_splitter.addWidget(self.video_streamer)

        # add a VideoInfoTable component to the left pane
        self.video_info_table = VideoInfoTable(self.video_engine)
        left_splitter.addWidget(self.video_info_table)

        left_splitter.setSizes([3, 1])
        self.main_layout.addWidget(left_splitter)

        # --------- Rigth Tab Bar --------
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)

        # # add a tabbar
        # tab_widget = QTabWidget()

        # # First tab
        # tab1 = QWidget()
        # tab1.setLayout(VideoEditor())

        # # Second tab
        # tab2 = QWidget()
        # layout2 = QVBoxLayout()
        # layout2.addWidget(QLabel("This is the second tab"))
        # tab2.setLayout(VideoExtractor())

        # # Add tabs
        # tab_widget.addTab(tab1, "Video Editor")
        # tab_widget.addTab(tab2, "Video Extractor")

        # right_layout.addWidget(tab_widget)

        # ------------ Vertical Split screen -------------------
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(left_splitter)
        splitter.addWidget(right_widget)
        splitter.setSizes([2, 1])
        self.main_layout.addWidget(splitter)

        # emit the first frame after the layout is built
        self.video_engine_thread.started.connect(self.video_engine.initialize)
        # start the video engine thread after the layout is built
        self.video_engine_thread.start()
