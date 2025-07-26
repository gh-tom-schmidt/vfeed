import cv2
import os


class VideoEngine:
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

    def __init__(self) -> None:
        """
        Initializes the VideoEngine with default values.

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

        self.source = None
        self.file_name = None

        self.width = None
        self.height = None
        self.fps = None
        self.max_frames = None

        # this values are used to crop the video
        self.crop_values = {
            "left": 0,
            "right": 0,
            "top": 0,
            "bottom": 0,
        }

        self.active_frame = None

    def load(self, path: str) -> None:
        """
        Loads a video file and initializes the VideoEngine capture properties.

        Args:
            path (str): The path to the video file.

        """

        # check if the file exists
        if not os.path.exists(path):
            raise ValueError(f"Video file does not exist: {path}")

        # load the video file and check if it can be opened
        self.source = cv2.VideoCapture(path)
        if not self.source.isOpened():
            raise ValueError(f"Unable to open video file: {path}")

        # set global properties
        self.file_name = os.path.splitext(os.path.basename(path))[0]
        self.width = int(self.source.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.source.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.fps = self.source.get(cv2.CAP_PROP_FPS)
        self.max_frames = int(self.source.get(cv2.CAP_PROP_FRAME_COUNT))

    #
    # ------------------------------- VIDEO EDITIONG -------------------------------
    #

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
    def setVideoReaderPosition(self, frame_number: int) -> None:
        """
        Update the current position of the video reader.

        Args:
            frame_number (int): The frame number to set the position to.

        """

        # set the current position of the video reader when in bounds
        if 0 <= frame_number < self.max_frames:
            self.source.set(cv2.CAP_PROP_POS_FRAMES, frame_number)

    def getVideoReaderPosition(self) -> int:
        """
        Gets the current position of the video reader.

        Returns:
            int: The current frame number of the video reader.
        """
        return int(self.source.get(cv2.CAP_PROP_POS_FRAMES))

    def changeVideoReaderPosition(self, delta: int) -> None:
        """
        Update the current position of the video reader by a delta value.

        Args:
            delta (int): The delta value to change the position by.

        """

        # set the new position of the video reader
        # the -1 is compensate the +1 from opencv.read()
        new_pos = self.getPos() + delta - 1
        # check if the new position is within the bounds of the video
        if 0 <= new_pos < self.max_frames:
            self.setPos(new_pos)

    def getNextFrame(self) -> None | cv2.Mat:
        """
        Gets the next frame from the video source.

        Returns:
            None | cv2.Mat: The next frame from the video source or None if there are no more frames.
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
        # convert this from the opencv standard BGR to RGB before returning
        return cv2.cvtColor(self.active_frame, cv2.COLOR_BGR2RGB)

    #
    # ------------------------------------ MISC -----------------------------------
    #

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
