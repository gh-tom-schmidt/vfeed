from modules.video_engine import VideoEngine


class VideoStreamer(QWidget):
    def __init__(self, video_engine):
        super().__init__()

        # hook the video engine
        self.video = video_engine

        layout = QHBoxLayout()



        # File selector
        self.open_button = QPushButton("Open Video")
        self.open_button.setFixedSize(150, 40)
        self.open_button.clicked.connect(self.init_editor)
        self.main_layout.addWidget(self.open_button, alignment=Qt.AlignCenter)

        # Video Frame
        video_display = QLabel("Video")
        video_display.setFixedHeight(600)
        video_display.setStyleSheet("background-color: #444; border: 1px solid #666;")
        video_display.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.video_display)

        # Slider
        slider = QSlider(Qt.Horizontal)
        slider.setRange(0, 100)  # inital values
        slider.valueChanged.connect(self.slided)
        layout.addWidget(slider)

        # Control Buttons
        control_layout = QHBoxLayout()

        # change by -60 Frames
        bt_neg60 = QPushButton("-60")
        bt_neg60.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        bt_neg60.clicked.connect(self.changeFrame(-60))
        control_layout.addWidget(bt_neg60)

        # change by -30 Frames
        bt_neg30 = QPushButton("-30")
        bt_neg30.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        bt_neg30.clicked.connect(self.changeFrame(-30))
        control_layout.addWidget(bt_neg30)

        # change by -10 Frames
        bt_neg10 = QPushButton("-10")
        bt_neg10.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        bt_neg10.clicked.connect(self.changeFrame(-10))
        control_layout.addWidget(bt_neg10)

        # change by -1 Frame
        bt_neg1 = QPushButton("-1")
        bt_neg1.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        bt_neg1.clicked.connect(self.changeFrame(-1))
        control_layout.addWidget(bt_neg1)

        # the play / pause button
        bt_play = QPushButton("Play")
        bt_play.setObjectName("PlayButton")
        bt_play.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        bt_play.clicked.connect(self.stream)
        control_layout.addWidget(bt_play)

        # change by +1 Frame
        bt_plus1 = QPushButton("+1")
        bt_plus1.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        bt_plus1.clicked.connect(self.changeFrame(1))
        control_layout.addWidget(bt_plus1)

        # change by +10 Frames
        bt_plus10 = QPushButton("+10")
        bt_plus10.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        bt_plus10.clicked.connect(self.changeFrame(10))
        control_layout.addWidget(bt_plus10)

        # change by +30 Frames
        bt_plus30 = QPushButton("+30")
        bt_plus30.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        bt_plus30.clicked.connect(self.changeFrame(30))
        control_layout.addWidget(bt_plus30)

        # change by +60 Frames
        bt_plus60 = QPushButton("+60")
        bt_plus60.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        bt_plus60.clicked.connect(self.changeFrame(60))
        control_layout.addWidget(bt_plus60)

        layout.addLayout(self.control_layout)

        self.setLayout(layout)

    #
    # -------------------------------- FUNCTIONS --------------------------------------
    #

    def fileSelector(self) -> str:
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Video File",
            "",
            "Video Files (*.mp4 *.avi *.mov *.mkv);;All Files (*)",
        )

        return file_path

    def changeFrame(self, delta: int) -> None:
                frame = self.video.getNextFrame()
        h, w, ch = frame.shape
        bytes_per_line = ch * w
        qt_image = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
        self.video_display.setPixmap(
            QPixmap.fromImage(qt_image).scaled(
                self.video_display.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
        )

        self.slider.setValue(self.video.getPos())
        self.info_table.setItem(0, 0, QTableWidgetItem(str(self.video.getPos())))

    def slided(self, value: int) -> None:
        now = time.time()
        if now - self.last_slider_update >= self.slider_update_interval:
            self.last_slider_update = now
            self.video.setPos(value - 1)
            self.displayNextFrame()
        else:
            # Skip update if moving too fast
            pass
    
    def lock(self, state, control_layout):
        for i in range(control_layout.count()):
            widget = control_layout.itemAt(i).widget()
            if widget.objectName() == "PlayButton":
                continue
            if isinstance(widget, QPushButton):
                widget.setEnabled(not state)

        def play(self):
        button = self.control_layout.itemAt(5).widget()  # Play button
        if button.text() == "Play":
            self.lock(True, self.control_layout)
            button.setText("Pause")

            self.worker = video_player.VideoPlayerWorker(self.video)
            self.thread = QThread()

            self.worker.moveToThread(self.thread)
            # FFmpeg (used internally by OpenCV) doesn't like multithreaded decoding without proper locking
            # so we use signals to control the playback and generate the next frame from the main thread
            self.worker.next_frame.connect(lambda: self.displayNextFrame())
            self.worker.finished.connect(self.thread.quit)

            self.thread.started.connect(self.worker.run)
            self.thread.start()
        else:
            button.setText("Play")
            self.lock(False, self.control_layout)

            if self.worker:
                self.worker.playing = False  # Signal the worker to stop
                self.thread.quit()  # Ask the thread to exit
                self.thread.wait()  # Block until it’s done