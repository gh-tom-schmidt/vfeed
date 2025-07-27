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


class VideoEditor(QWidget):
    def __init__(self, crop_values, on_apply_callback=None, parent=None):
        super().__init__(parent)

        self.crop_values = (
            crop_values  # Dict like {"top":0, "bottom":0, "left":0, "right":0}
        )
        self.on_apply_callback = on_apply_callback

        layout = QVBoxLayout(self)

        # Form layout
        form_layout = QFormLayout()
        self.crop_top = QLineEdit(str(crop_values.get("top", 0)))
        self.crop_bottom = QLineEdit(str(crop_values.get("bottom", 0)))
        self.crop_left = QLineEdit(str(crop_values.get("left", 0)))
        self.crop_right = QLineEdit(str(crop_values.get("right", 0)))

        form_layout.addRow("Crop Top:", self.crop_top)
        form_layout.addRow("Crop Bottom:", self.crop_bottom)
        form_layout.addRow("Crop Left:", self.crop_left)
        form_layout.addRow("Crop Right:", self.crop_right)
        layout.addLayout(form_layout)

        # Buttons
        button_layout = QHBoxLayout()
        apply_btn = QPushButton("Apply")
        reset_btn = QPushButton("Reset")
        button_layout.addWidget(apply_btn)
        button_layout.addWidget(reset_btn)
        layout.addLayout(button_layout)

        # Button actions
        apply_btn.clicked.connect(self.apply_changes)
        reset_btn.clicked.connect(self.reset_fields)

    def apply_changes(self):
        values = {
            "top": int(self.crop_top.text()),
            "bottom": int(self.crop_bottom.text()),
            "left": int(self.crop_left.text()),
            "right": int(self.crop_right.text()),
        }
        self.crop_values.update(values)
        if self.on_apply_callback:
            self.on_apply_callback(values)

    def reset_fields(self):
        self.crop_top.setText(str(self.crop_values.get("top", 0)))
        self.crop_bottom.setText(str(self.crop_values.get("bottom", 0)))
        self.crop_left.setText(str(self.crop_values.get("left", 0)))
        self.crop_right.setText(str(self.crop_values.get("right", 0)))
