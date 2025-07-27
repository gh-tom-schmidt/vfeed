from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QFormLayout,
    QLineEdit,
    QPushButton,
    QHBoxLayout,
    QLabel,
)
from PySide6.QtCore import Qt

from modules.video_engine import VideoEngine


class VideoEditor(QWidget):
    def __init__(self, video_engine: VideoEngine, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)

        self.video_engine = video_engine

        crop_values = self.video_engine.getCropValues()

        # form layout for each crop value
        form_layout = QFormLayout()
        self.crop_top = QLineEdit(str(crop_values[2]))
        self.crop_bottom = QLineEdit(str(crop_values[3]))
        self.crop_left = QLineEdit(str(crop_values[0]))
        self.crop_right = QLineEdit(str(crop_values[1]))

        form_layout.addRow("Crop Top:", self.crop_top)
        form_layout.addRow("Crop Bottom:", self.crop_bottom)
        form_layout.addRow("Crop Left:", self.crop_left)
        form_layout.addRow("Crop Right:", self.crop_right)
        layout.addLayout(form_layout)

        # buttons
        button_layout = QHBoxLayout()
        apply_btn = QPushButton("Apply")
        apply_btn.clicked.connect(self.applyChanges)
        button_layout.addWidget(apply_btn)
        layout.addLayout(button_layout)

    def applyChanges(self):
        self.video_engine.updateCropValues(
            int(self.crop_left.text()),
            int(self.crop_right.text()),
            int(self.crop_top.text()),
            int(self.crop_bottom.text()),
        )
