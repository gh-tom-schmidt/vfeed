   # Video editing button
        edit_button = QPushButton("Edit Video")
        edit_button.clicked.connect(self.editVideo)
        layout.addWidget(edit_button, alignment=Qt.AlignLeft)



 def editVideo(self):
        dialog = QDialog(parent)
        dialog.setWindowTitle("Set Crop Values")
        dialog.setMinimumWidth(300)
        layout = QVBoxLayout(dialog)

        form_layout = QFormLayout()

        crop_top = QLineEdit(text=str(self.crop_values[""]))
        crop_bottom = QLineEdit(text=str(crop_values[1]))
        crop_left = QLineEdit(text=str(crop_values[2]))
        crop_right = QLineEdit(text=str(crop_values[3]))

        form_layout.addRow("Crop Top:", crop_top)
        form_layout.addRow("Crop Bottom:", crop_bottom)
        form_layout.addRow("Crop Left:", crop_left)
        form_layout.addRow("Crop Right:", crop_right)
        layout.addLayout(form_layout)

        button_layout = QHBoxLayout()
        ok_btn = QPushButton("OK")
        cancel_btn = QPushButton("Cancel")
        ok_btn.clicked.connect(dialog.accept)
        cancel_btn.clicked.connect(dialog.reject)

        button_layout.addWidget(ok_btn)
        button_layout.addWidget(cancel_btn)
        layout.addLayout(button_layout)

        if dialog.exec() == QDialog.Accepted:
            return {
                "top": int(crop_top.text()),
                "bottom": int(crop_bottom.text()),
                "left": int(crop_left.text()),
                "right": int(crop_right.text()),
            }