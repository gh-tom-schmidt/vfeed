from PySide6.QtWidgets import QTableWidget, QTableWidgetItem
from PySide6.QtCore import Qt

from components.video_engine import VideoEngine


class VideoInfoTable(QTableWidget):
    """
    Show video information in a table format.
    Methods:
        updateInfo(video_engine): Updates the table with the current video information.
    """

    def __init__(self, video_engine: VideoEngine, parent=None) -> None:
        """
        Set the layout.
        """

        super().__init__(9, 1, parent)

        self.video_engine = video_engine

        self.setVerticalHeaderLabels(
            [
                "Current Frame",
                "Width",
                "Height",
                "FPS",
                "Max Frames",
                "Crop Top",
                "Crop Bottom",
                "Crop Left",
                "Crop Right",
            ]
        )

        self.horizontalHeader().setVisible(False)
        self.setEditTriggers(QTableWidget.NoEditTriggers)
        self.setStyleSheet("QTableWidget { background-color: #333; color: white; }")

        self.update_info(video_engine)

    def update_info(self) -> None:
        """
        Updates the table with the current video information.
        """

        croped_values = self.video_engine.getCropValues()

        self.setItem(
            0, 0, QTableWidgetItem(str(self.video_engine.getVideoReaderPosition()))
        )
        self.setItem(1, 0, QTableWidgetItem(str(self.video_engine.width)))
        self.setItem(2, 0, QTableWidgetItem(str(self.video_engine.height)))
        self.setItem(3, 0, QTableWidgetItem(str(self.video_engine.fps)))
        self.setItem(4, 0, QTableWidgetItem(str(self.video_engine.max_frames)))
        self.setItem(5, 0, QTableWidgetItem(str(croped_values[2])))
        self.setItem(6, 0, QTableWidgetItem(str(croped_values[3])))
        self.setItem(7, 0, QTableWidgetItem(str(croped_values[0])))
        self.setItem(8, 0, QTableWidgetItem(str(croped_values[1])))
