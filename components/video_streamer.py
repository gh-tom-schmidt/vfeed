from modules.video_engine import VideoEngine
import time
from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QSlider,
    QPushButton,
    QSizePolicy,
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QImage, QPixmap
from configs.globals import SLIDER_UPDATE_INTERVAL


class VideoStreamer(QWidget):
    """
    VideoStreamer component to control video playback and display.
    Methods:
        fileSelector(): Opens a file dialog to select a video file.
        changeFrame(delta): Changes the current frame by a specified delta.
        updateFrame(): Updates the displayed video frame.
        slided(value): Handles slider movement to change the video frame.
        lock(state): Locks or unlocks the control buttons based on playback state.
        play(): Toggles playback state between play and pause.
    """

    def __init__(self, video_engine: VideoEngine) -> None:
        """
        Define the layout for the video streamer component.
        Args:
            video_engine (VideoEngine): The video engine instance to control video playback.
        """

        super().__init__()

        # hook the video engine
        self.video_engine = video_engine

        layout = QVBoxLayout()

        # Video Frame
        self.video_display = QLabel("Video")
        self.video_display.setFixedHeight(600)
        self.video_display.setStyleSheet(
            "background-color: #444; border: 1px solid #666;"
        )
        self.video_display.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.video_display)

        # get the frame emitter to update the Video Frame
        self.video_engine.emit_new_frame.connect(self.updateFrame)

        # Slider
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0, self.video_engine.max_frames)
        self.slider.valueChanged.connect(self.slided)
        layout.addWidget(self.slider)

        # initialize the slider update interval
        self.last_slider_update = time.time()

        # get the current frame number for updating the slider form the video engine
        self.video_engine.emit_new_frame_index.connect(self.slider.setValue)

        # ---------------- Control Buttons -----------------------
        self.control_layout = QHBoxLayout()

        # change by -60 Frames
        bt_neg60 = QPushButton("-60")
        bt_neg60.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        bt_neg60.clicked.connect(lambda: self.changeFrame(-60))
        self.control_layout.addWidget(bt_neg60)

        # change by -30 Frames
        bt_neg30 = QPushButton("-30")
        bt_neg30.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        bt_neg30.clicked.connect(lambda: self.changeFrame(-30))
        self.control_layout.addWidget(bt_neg30)

        # change by -10 Frames
        bt_neg10 = QPushButton("-10")
        bt_neg10.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        bt_neg10.clicked.connect(lambda: self.changeFrame(-10))
        self.control_layout.addWidget(bt_neg10)

        # change by -1 Frame
        bt_neg1 = QPushButton("-1")
        bt_neg1.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        bt_neg1.clicked.connect(lambda: self.changeFrame(-1))
        self.control_layout.addWidget(bt_neg1)

        # the play / pause button
        bt_play = QPushButton("Play")
        bt_play.setObjectName("PlayButton")
        bt_play.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        bt_play.clicked.connect(self.stream)
        self.control_layout.addWidget(bt_play)

        # change by +1 Frame
        bt_plus1 = QPushButton("+1")
        bt_plus1.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        bt_plus1.clicked.connect(lambda: self.changeFrame(1))
        self.control_layout.addWidget(bt_plus1)

        # change by +10 Frames
        bt_plus10 = QPushButton("+10")
        bt_plus10.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        bt_plus10.clicked.connect(lambda: self.changeFrame(10))
        self.control_layout.addWidget(bt_plus10)

        # change by +30 Frames
        bt_plus30 = QPushButton("+30")
        bt_plus30.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        bt_plus30.clicked.connect(lambda: self.changeFrame(30))
        self.control_layout.addWidget(bt_plus30)

        # change by +60 Frames
        bt_plus60 = QPushButton("+60")
        bt_plus60.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        bt_plus60.clicked.connect(lambda: self.changeFrame(60))
        self.control_layout.addWidget(bt_plus60)

        layout.addLayout(self.control_layout)

        self.setLayout(layout)

    #
    # -------------------------------- FUNCTIONS --------------------------------------
    #

    def changeFrame(self, delta: int) -> None:
        """
        Change the frame by a given delta.
        Args:
            delta (int): The amount of change.
        """

        # set the video reader position
        self.video_engine.changeVideoReaderPosition(delta)

    def updateFrame(self, frame) -> None:
        """
        Update the frame in the video display.
        """

        h, w, ch = frame.shape
        bytes_per_line = ch * w

        # display the frame
        qt_image = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
        self.video_display.setPixmap(
            QPixmap.fromImage(qt_image).scaled(
                self.video_display.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
        )

    def slided(self, value: int) -> None:
        """
        Change the frame when the slider is moved.
        Args:
            value (int): The amount of change.
        """

        # only change the frame if the slider is down
        # so it not gets triggered by the video engine
        # when the slider is autmoatically updated
        if self.slider.isSliderDown():
            # set a time interval to avoid too many updates
            now = time.time()
            if now - self.last_slider_update >= SLIDER_UPDATE_INTERVAL:
                self.last_slider_update = now
                # self.video_engine.setVideoReaderPosition(value)

    def lock(self, state: bool) -> None:
        """
        Lock the skip buttons when video is playing.
        Args:
            state (bool): The state of the look.
        """

        # get all buttons in the control_layout
        for i in range(self.control_layout.count()):
            widget = self.control_layout.itemAt(i).widget()
            # if the is the PlayButton
            if widget.objectName() == "PlayButton":
                continue

            # enable / disable the button
            widget.setEnabled(not state)

    def stream(self) -> None:
        """
        Play / Pause the video.
        Args:
            state (bool): The state of the look.
        """

        # get the PlayButton
        button = self.control_layout.itemAt(4).widget()  # Play button

        # if it says: "Play", so the video is stopped
        if button.text() == "Play":
            # lock the skip buttons
            self.lock(True)
            # change the text on the button
            button.setText("Pause")

            self.video_engine.play(True)

        # if it says: "Pause", stop  the video
        else:
            # unlock the skip buttons
            self.lock(False)

            # set the button back to play
            button.setText("Play")

            self.video_engine.play(False)
