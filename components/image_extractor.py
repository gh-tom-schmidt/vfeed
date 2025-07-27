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
    QDialog,
)
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtCore import QSize, Qt

from modules.video_engine import VideoEngine


class ImageExtractor(QWidget):
    """ImageExtractor component to manage image extraction from video frames.

    Methods:
        select_output_folder(): Opens a dialog to select the output folder for images.
        load_output_images(): Loads images from the selected output folder into the list.
        save(): Saves the current active frame as an image in the selected output folder.
        show_full_image(item): Displays the full image in a dialog when an item is clicked.
    """

    def __init__(self, video_engine: VideoEngine, parent=None) -> None:
        """
        Set up the layout
        Args:
            video_engine (VideoEngine): The video engine instance to interact with video frames.
            parent: Parent widget for this component.
        """

        super().__init__(parent)

        self.video_engine = video_engine
        self.output_path = ""

        self.main_layout = QVBoxLayout(self)

        top_bar = QHBoxLayout()

        # Save button
        bt_save = QPushButton("Save")
        bt_save.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        bt_save.clicked.connect(self.save)
        top_bar.addWidget(bt_save)

        # Output path selector
        select_folder_btn = QPushButton("Select Output Folder")
        select_folder_btn.clicked.connect(self.select_output_folder)
        select_folder_btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        top_bar.addWidget(select_folder_btn)

        self.output_path_label = QLabel("No folder selected")
        self.output_path_label.setStyleSheet("color: white")
        top_bar.addWidget(self.output_path_label)

        self.main_layout.addLayout(top_bar)

        # Image list
        self.image_list = QListWidget()
        self.image_list.setViewMode(QListWidget.IconMode)
        self.image_list.setIconSize(QSize(100, 100))
        self.image_list.setResizeMode(QListWidget.Adjust)
        self.image_list.setSpacing(10)
        self.image_list.itemClicked.connect(self.show_full_image)
        self.main_layout.addWidget(self.image_list)

        self.setLayout(self.main_layout)

    # ---------------------------- FUNCTIONS ------------------------------------

    def select_output_folder(self):
        """
        Opens a dialog to select the output folder for images
        and loads existing images
        """

        folder = QFileDialog.getExistingDirectory(self, "Select Output Folder")
        if folder:
            self.output_path = folder
            self.output_path_label.setText(folder)
            self.load_output_images()

    def load_output_images(self):
        """
        Loads images from the selected output folder into the list widget.
        """

        # clear the current list
        self.image_list.clear()

        if not self.output_path or not os.path.exists(self.output_path):
            return

        # for each file that is an image
        for filename in os.listdir(self.output_path):
            if filename.lower().endswith((".png", ".jpg", ".jpeg")):
                full_path = os.path.join(self.output_path, filename)

                # create an icon from that image and add it to the list
                icon = QIcon(
                    QPixmap(full_path).scaled(
                        100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation
                    )
                )
                item = QListWidgetItem(icon, filename)
                item.setData(Qt.UserRole, full_path)
                self.image_list.addItem(item)

    def save(self):
        """
        Saves the frame to the selected output folder.
        """

        if self.output_path:
            self.video_engine.save(self.output_path)
            # update the list
            self.load_output_images()

    def show_full_image(self, item):
        """
        Displays the full image in a dialog when an item is clicked.

        Args:
            item (QListWidgetItem): The item clicked in the list.
        """

        full_path = item.data(Qt.UserRole)
        pixmap = QPixmap(full_path)

        # create the dialog
        dialog = QDialog(self)
        dialog.setWindowTitle(item.text())
        dialog.setMinimumSize(820, 600)
        dialog.setStyleSheet("background-color: black;")

        # image label
        image_label = QLabel()
        image_label.setPixmap(pixmap.scaledToWidth(800, Qt.SmoothTransformation))
        image_label.setAlignment(Qt.AlignCenter)

        # layout
        layout = QVBoxLayout()
        layout.addWidget(image_label)
        dialog.setLayout(layout)

        dialog.exec()
