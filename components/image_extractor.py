import os
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QFileDialog,
    QSizePolicy,
    QSplitter,
)
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtCore import QSize, Qt


class OutputViewerTab(QWidget):
    def __init__(self, video=None, parent=None):
        super().__init__(parent)
        self.video = video
        self.output_path = ""

        self.main_layout = QVBoxLayout(self)
        self.setup_ui()

    def setup_ui(self):
        # LEFT SIDE (can be used for future controls)
        self.left_widget = QWidget()
        self.left_layout = QVBoxLayout(self.left_widget)

        # Save button
        bt_save = QPushButton("Save")
        bt_save.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        bt_save.clicked.connect(self.save)
        self.left_layout.addWidget(bt_save)
        self.left_layout.addStretch()

        # RIGHT SIDE (path + image list)
        self.right_widget = QWidget()
        self.right_layout = QVBoxLayout(self.right_widget)

        # Output path selector
        path_layout = QHBoxLayout()
        self.output_path_label = QLabel("No folder selected")
        self.output_path_label.setStyleSheet("color: white")
        select_folder_btn = QPushButton("Select Output Folder")
        select_folder_btn.clicked.connect(self.select_output_folder)
        path_layout.addWidget(select_folder_btn)
        path_layout.addWidget(self.output_path_label)
        self.right_layout.addLayout(path_layout)

        # Image list
        self.image_list = QListWidget()
        self.image_list.setViewMode(QListWidget.IconMode)
        self.image_list.setIconSize(QSize(100, 100))
        self.image_list.setResizeMode(QListWidget.Adjust)
        self.image_list.setSpacing(10)
        self.image_list.itemClicked.connect(self.show_full_image)
        self.right_layout.addWidget(self.image_list)

    def show_full_image(self, item):
        full_path = item.data(Qt.UserRole)
        pixmap = QPixmap(full_path)

        dialog = QLabel()
        dialog.setWindowTitle(item.text())
        dialog.setPixmap(pixmap.scaledToWidth(800, Qt.SmoothTransformation))
        dialog.setMinimumSize(820, 600)
        dialog.setStyleSheet("background-color: black")
        dialog.setWindowFlags(Qt.Window)
        dialog.show()

    def load_output_images(self):
        self.image_list.clear()
        if not self.output_path or not os.path.exists(self.output_path):
            return

        for filename in os.listdir(self.output_path):
            if filename.lower().endswith((".png", ".jpg", ".jpeg")):
                full_path = os.path.join(self.output_path, filename)
                pixmap = QPixmap(full_path)
                if not pixmap.isNull():
                    icon = QIcon(
                        pixmap.scaled(
                            100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation
                        )
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

    def save(self):
        if self.video and self.output_path:
            self.video.save(self.output_path)
            self.load_output_images()
