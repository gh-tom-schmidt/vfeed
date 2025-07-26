        bt_draw = QPushButton("Draw")
        bt_draw.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        bt_draw.clicked.connect(lambda: self.draw())
        control_layout.addWidget(bt_draw)





    def draw(self):
        # Placeholder for draw functionality
        print("Draw button clicked")
        # Implement drawing logic here
        pass