import cv2
import os
from PySide6.QtCore import QObject, Signal, Slot, QTimer


class VideoEngine(QObject):
    """
    This class provides the backend for video processing and control with OpenCV.

    Methods:
        load(path): Loads a video file and initializes the VideoEngine capture properties.
        updateCropValues(left, right, top, bottom): Updates the crop values for the video
        getCropValues(): Gets the current crop values for the video.
        setVideoReaderPosition(frame_number): Update the current position of the video reader.
        getVideoReaderPosition(): Gets the current position of the video reader.
        changeVideoReaderPosition(delta): Update the current position of the video reader by a delta value.
        getNextFrame(): Gets the next frame from the video source.
        save(output_path): Save the current active frame to the specified output path.
    """

    # emiters for UI update
    emit_new_frame = Signal(object)
    emit_new_frame_index = Signal(int)

    def __init__(self, path: str) -> None:
        """
        Initializes the VideoEngine with default values.

        Args:
            path(str): Path to the video source

        Attributes:
            source (cv2.VideoCapture): The video source.
            file_name (str): The name of the video file without extension.
            width (int): The width of the video frames.
            height (int): The height of the video frames.
            fps (float): The frames per second of the video.
            max_frames (int): The total number of frames in the video.
            crop_values (dict): The crop values for the video.
            active_frame (cv2.Mat): The currently active frame from the video.
        """

        super().__init__()

        # Load the video
        # check if the file exists
        if not os.path.exists(path):
            raise ValueError(f"Video file does not exist: {path}")

        # load the video file and check if it can be opened
        self.source = cv2.VideoCapture(path)
        if not self.source.isOpened():
            raise ValueError(f"Unable to open video file: {path}")

        # set globals
        self.file_name = os.path.splitext(os.path.basename(path))[0]
        self.width = int(self.source.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.source.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.fps = self.source.get(cv2.CAP_PROP_FPS)
        self.max_frames = int(self.source.get(cv2.CAP_PROP_FRAME_COUNT))
        self.active_frame = None

        # this values are used to crop the video
        self.crop_values = {
            "left": 0,
            "right": 0,
            "top": 0,
            "bottom": 0,
        }

        # add a timer for the video playback
        self.state_playing = False
        self.timer = QTimer()
        self.timer.timeout.connect(self._playStep)

    @Slot()
    def initialize(self) -> None:
        """
        Initializes the video engine by generating the first frame.
        This method is called when the video engine thread starts.
        """

        # generate the first frame
        self.generateFrame()

    @Slot()
    def stop(self) -> None:
        """
        Cleanup if thread is closed.
        """

        if self.source is not None:
            self.source.release()

    #
    # ------------------------------- VIDEO EDITIONG -------------------------------
    #

    @Slot(int, int, int, int)
    def updateCropValues(
        self, left: int = None, right: int = None, top: int = None, bottom: int = None
    ) -> None:
        """
        Updates the crop values for the video.

        Args:
            left (int, optional): The left crop value.
            right (int, optional): The right crop value.
            top (int, optional): The top crop value.
            bottom (int, optional): The bottom crop value.

        """

        # only update the values if they are changed
        if left is not None:
            self.crop_values["left"] = left
        if right is not None:
            self.crop_values["right"] = right
        if top is not None:
            self.crop_values["top"] = top
        if bottom is not None:
            self.crop_values["bottom"] = bottom

    def getCropValues(self) -> tuple[int, int, int, int]:
        """
        Gets the current crop values for the video.

        Returns:
            tuple[int, int, int, int]: The left, right, top, and bottom crop values.
        """

        return (
            self.crop_values["left"],
            self.crop_values["right"],
            self.crop_values["top"],
            self.crop_values["bottom"],
        )

    #
    # ------------------------------- VIDEO CONTROL -------------------------------
    #

    # caution: this slows down over time when playing a video, so use this only
    # for per-frame changes and not for playback
    @Slot(int)
    def setVideoReaderPosition(self, frame_number: int) -> None:
        """
        Update the current position of the video reader.

        Args:
            frame_number (int): The frame number to set the position to.

        """

        # set the current position of the video reader when in bounds
        if 0 <= frame_number < self.max_frames:
            self.source.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
            self.generateFrame()

    def getVideoReaderPosition(self) -> int:
        """
        Gets the current position of the video reader.

        Returns:
            int: The current frame number of the video reader.
        """
        return int(self.source.get(cv2.CAP_PROP_POS_FRAMES))

    @Slot(int)
    def changeVideoReaderPosition(self, delta: int) -> None:
        """
        Update the current position of the video reader by a delta value.

        Args:
            delta (int): The delta value to change the position by.

        """

        # set the new position of the video reader
        # the -1 is compensate the +1 from opencv.read()
        new_pos = self.getVideoReaderPosition() + delta - 1
        # check if the new position is within the bounds of the video
        if 0 <= new_pos < self.max_frames:
            self.setVideoReaderPosition(new_pos)

    @Slot()
    def generateFrame(self) -> None:
        """
        Generates the frame from the video source.
        """

        # get the next frame from the video source
        # Note: this automatically updates the position of the video reader
        ret, frame = self.source.read()
        if not ret:
            return None

        # apply the crop values to the frame
        # left and right are reversed because the crop values are from the left side
        left = self.crop_values["left"]
        right = self.width - self.crop_values["right"]
        top = self.crop_values["top"]
        bottom = self.height - self.crop_values["bottom"]

        # save it as the active frame
        self.active_frame = frame[top:bottom, left:right]

        # emit frame
        self.emit_new_frame.emit(cv2.cvtColor(self.active_frame, cv2.COLOR_BGR2RGB))
        self.emit_new_frame_index.emit(self.getVideoReaderPosition())

    def getFrame(self) -> None | cv2.Mat:
        """
        Returns  the current frame.

        Returns:
            cv2.Mat: The current active frame in RGB format, or None if no frame is available.
        """

        return cv2.cvtColor(self.active_frame, cv2.COLOR_BGR2RGB)

    def play(self, state: bool) -> None:
        """
        Play or pause the video playback.

        Args:
            state (bool): True to play the video, False to pause it.
        """

        self.state_playing = state

        if self.state_playing:
            # Start playing based on fps (interval in ms)
            interval = int(1000 / self.fps)
            self.timer.start(interval)
        else:
            self.timer.stop()

    def _playStep(self):
        """
        Helper function to play the video.
        """

        # called every frame interval
        self.generateFrame()

        # stop when video ends
        if self.getVideoReaderPosition() >= self.max_frames:
            self.play(False)

    #
    # ------------------------------------ MISC -----------------------------------
    #

    @Slot(str)
    def save(self, output_path: str):
        """
        Save the current active frame to the specified output path.

        Args:
            output_path (str): The path to save the frame to.

        """

        # save the current active frame to the output path when output path is valid
        if not os.path.exists(output_path):
            raise ValueError(f"Output path does not exist: {output_path}")
        cv2.imwrite(
            os.path.join(output_path, f"{self.source_name}_Frame-{self.getPos()}.jpg"),
            cv2.cvtColor(self.active_frame, cv2.COLOR_RGB2BGR),
        )
