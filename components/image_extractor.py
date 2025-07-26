


        # output path and folder selection
        path_layout = QHBoxLayout()
        self.output_path_label = QLabel("No folder selected")
        self.output_path_label.setStyleSheet("color: white")
        select_folder_btn = QPushButton("Select Output Folder")
        select_folder_btn.clicked.connect(self.select_output_folder)
        path_layout.addWidget(select_folder_btn)
        path_layout.addWidget(self.output_path_label)
        right_layout.addLayout(path_layout)

        # image list
        self.image_list = QListWidget()
        self.image_list.setViewMode(QListWidget.IconMode)
        self.image_list.setIconSize(QSize(100, 100))
        self.image_list.setResizeMode(QListWidget.Adjust)
        self.image_list.setSpacing(10)
        self.image_list.itemClicked.connect(self.show_full_image)
        right_layout.addWidget(self.image_list)

        # Split screen
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(left_widget)
        splitter.addWidget(right_widget)
        splitter.setSizes([2, 1])  # 2/3 left, 1/3 right
        self.main_layout.addWidget(splitter)


    def show_full_image(self, item):
        full_path = item.data(Qt.UserRole)
        pixmap = QPixmap(full_path)

        dialog = QDialog(self)
        dialog.setWindowTitle(item.text())
        layout = QVBoxLayout(dialog)
        label = QLabel()
        label.setPixmap(pixmap.scaledToWidth(800, Qt.SmoothTransformation))
        layout.addWidget(label)
        dialog.exec()

    def load_output_images(self):
        self.image_list.clear()
        if not hasattr(self, "output_path"):
            return

        for filename in os.listdir(self.output_path):
            if filename.lower().endswith((".png", ".jpg", ".jpeg")):
                full_path = os.path.join(self.output_path, filename)
                pixmap = QPixmap(full_path)
                icon = QIcon(
                    pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                )
                item = QListWidgetItem(icon, filename)
                item.setData(Qt.UserRole, full_path)
                self.image_list.addItem(item)



    def select_output_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Output Folder")
        if folder:
            self.output_path = folder
            self.output_path_label.setText(folder)
            self.load_output_images()



bt_save = QPushButton("Save")
        bt_save.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        bt_save.clicked.connect(lambda: self.save())
        control_layout.addWidget(bt_save)


    def save(self):
        self.video.save(self.output_path)
        self.load_output_images()