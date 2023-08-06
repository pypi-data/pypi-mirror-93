import json
from collections import namedtuple, Sequence as AbstractSequence
from typing import Callable, List, Optional, Union

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from skimage import io as sk_io

from .constants import TIME_STRING_FORMAT
from .session import Session
from .urls import URLS
from .util import change_sampling_frequency

FrameTuple = namedtuple("FrameTuple", "timestamp drive_id image_fpath")
BboxTuple = namedtuple("BboxTuple", "x_min x_max y_min y_max")


class BoundingBoxes2D:
    """
    Class that holds 2D bounding boxes for images
    """

    REQUIRED_COLUMNS = {"confidence", "drive_id", "object_type", "timestamp", "x_max", "x_min", "y_max", "y_min"}

    def __init__(self, df: pd.DataFrame):
        self._validate_columns(df.columns)
        self._data = df

    def _validate_columns(self, columns: pd.Index):
        columns_set = set(columns)
        if not self.REQUIRED_COLUMNS.issubset(columns_set):
            raise ValueError(f"Some required columns are missing: {self.REQUIRED_COLUMNS.difference(columns_set)}")

    def __iter__(self):
        return self._data.itertuples()

    def __repr__(self):
        return f"<{self.__class__.__name__} object with {len(self._data)} bounding boxes>"

    def to_pandas(self) -> pd.DataFrame:
        """Returns a pandas representation of the data"""
        return self._data


class Frame:
    """
    Conceptually a Frame is a single point in time defined by data, a timestamp and a drive_id. In practice it is
    defined by the timestamp, filepath (and/or the actual data if it has been loaded data), and drive_id.
    """

    def __init__(self, session: Session, timestamp, f_path: str, drive_id: str):
        self._session = session
        self.timestamp = timestamp
        self.f_path = f_path
        self.drive_id = drive_id
        self._img = None
        self._bboxes = {}

    def __repr__(self):
        return f"{self.timestamp} - {self.drive_id} - {self.f_path.split('?')[0]}"

    def img_to_numpy(self, load_func: Callable = sk_io.imread) -> np.ndarray:
        """Load underlying image as numpy array using the given function

        Args:
            load_func: Function to load the image from path

        Returns:
            A numpy array corresponding to the Frame image
        """
        if self._img is None:
            self._img = load_func(self.f_path)
        return self._img

    def plot(self, bboxes: Optional[BoundingBoxes2D] = None) -> None:
        """Plot with the provided bounding boxes overlaid

        Args:
            bboxes: Bounding boxes to plot overlaid on the image, usually returned from Frame.bboxes
        """
        # TODO(robert): Support advanced plotting e.g. different colors for different classes
        plt.figure()
        plt.imshow(self.img_to_numpy())
        if bboxes is None:
            return

        for idx_obj, row in enumerate(bboxes):
            row_dict = row._asdict()
            data_bbox = BboxTuple(**{field: row_dict[field] for field in BboxTuple._fields})
            plt.plot(
                [data_bbox.x_min, data_bbox.x_max, data_bbox.x_max, data_bbox.x_min, data_bbox.x_min],
                [data_bbox.y_min, data_bbox.y_min, data_bbox.y_max, data_bbox.y_max, data_bbox.y_min],
                color="red",
                linewidth=2,
            )

    def bboxes(self, model_name) -> BoundingBoxes2D:
        """Fetch the bounding boxes for the Frame

        Args:
            model_name: The model that provides the bounding boxes e.g. `yolo-v3`

        Returns:
            The bounding boxes for the Frame
        """
        if model_name in self._bboxes:
            return self._bboxes[model_name]

        df = pd.DataFrame({"timestamp": [self.timestamp], "image_fpath": [self.f_path], "drive_id": [self.drive_id]})
        df_bboxes = self._session.get_bboxes(df, model_name)
        self._bboxes[model_name] = BoundingBoxes2D(df_bboxes)
        return self._bboxes[model_name]

    def view(self):
        raise NotImplementedError

    def to_tuple(self):
        """Return the Frame data as a namedtuple"""
        return FrameTuple(drive_id=self.drive_id, timestamp=self.timestamp, image_fpath=self.f_path)


DEFAULT_CAMERA = "camera_00"


class Frames(AbstractSequence):
    """
    Holds a collection of individual frames e.g. camera frames. Can be derived from sequences or
    from another set of frames. Used for viewing data (e.g. images), subsampling (e.g. only 1 frame every 5 seconds)
    and evaluating models.
    """

    REQUIRED_COLS = ["image_fpath", "drive_id"]

    def __init__(self, session: Session, frames: List[Frame]):
        self._session = session
        self._bboxes = {}
        self._frames = frames
        self._data = None

    @classmethod
    def from_pandas(cls, session: Session, df: pd.DataFrame):
        """Initialize a Frames object from a dataframe

        Args:
            session: The current session used to connect to the API endpoints.
            df: DataFrame where each row corresponds to single Frame.

        Returns:
            A Frames object containing the frames in the input dataframe
        """
        if not all(c in df for c in cls.REQUIRED_COLS):
            raise ValueError("Expected")
        frames = [Frame(session, ts, row["image_fpath"], row["drive_id"]) for ts, row in df.iterrows()]
        return cls(session, frames)

    @classmethod
    def from_sequences(cls, sequences):
        """Initialize a Frames object from Sequences

        Args:
            sequences: Sequences in which the frame data should lie

        Returns:
            A Frames object containing the frames in the time ranges + drive_id defined by the Sequences
        """
        df = sequences.to_pandas().copy()
        df["start_timestamp"] = df["start_timestamp"].dt.strftime(TIME_STRING_FORMAT)
        df["end_timestamp"] = df["end_timestamp"].dt.strftime(TIME_STRING_FORMAT)
        json_df = df.to_dict(orient="list")

        frames_val = sequences._session.post(
            URLS.frames_url, json_body={"camera_id": DEFAULT_CAMERA, "df_clips": json_df}
        )

        frames_val = json.loads(frames_val.text)
        df_results = pd.DataFrame.from_dict(frames_val)
        df_results["timestamp"] = pd.to_datetime(df_results["timestamp"])
        df_results = df_results.set_index("timestamp")
        return cls.from_pandas(sequences._session, df_results)

    def __repr__(self):
        return str(self.to_pandas())

    def __len__(self):
        return len(self._frames)

    def __getitem__(self, i: Union[int, slice]):
        if isinstance(i, int):
            return self._frames[i]
        elif isinstance(i, slice):
            # TODO(robert): Some caching needed?
            return Frames(self._session, self._frames[i])
        else:
            raise ValueError("")

    def __add__(self, other: "Frames"):
        return Frames(self._session, self._frames + other._frames)

    def _subsample_time(self, min_time_between_samples_per_drive: float) -> "Frames":
        df = self.to_pandas()
        dfs = []
        for _, df_group in df.groupby("drive_id"):
            dfs.append(change_sampling_frequency(df_group, min_time_between_samples_per_drive))
        df = pd.concat(dfs)
        return self.from_pandas(self._session, df)

    def _subsample_num_samples(self, num_samples_per_drive: int) -> "Frames":
        df = self.to_pandas()
        dfs = []
        for _, df_group in df.groupby("drive_id"):
            dfs.append(
                df_group.take(np.linspace(0, len(df_group) - 1, num_samples_per_drive, endpoint=True, dtype=np.int))
            )
        df = pd.concat(dfs)
        return self.from_pandas(self._session, df)

    def subsample(
        self, num_samples_per_drive: int = None, min_time_between_samples_per_drive: float = None,
    ):
        """Subsample the Frames based on a criterion

        Can subsample
            1) In time (e.g. every 5 seconds)
            2) By specifying the number of samples included per drive, taken every n-samples including starting and
               endpoint.

        Only one mode is possible for each call, and if both parameters are specified sampling by number of frames
        per drive takes precedence.

        Args:
            num_samples_per_drive: Number of samples to keep per drive.
            min_time_between_samples_per_drive: Time (in seconds) between successive samples

        Returns:
            Re-sampled Frames object
        """
        if num_samples_per_drive is not None:
            return self._subsample_num_samples(num_samples_per_drive)
        elif min_time_between_samples_per_drive is not None:
            return self._subsample_time(min_time_between_samples_per_drive)
        else:
            raise ValueError("Please specify at least one parameter for subsampling")

    def img_to_numpy(self, load_func: Callable = sk_io.imread) -> List[np.ndarray]:
        """Load underlying images of the frames as a list of numpy arrays using the given function

        Args:
            load_func: Function to load the image from path

        Returns:
            A list of numpy arrays corresponding to the frames
        """
        # TODO(robert): This could be optimized by batch downloading
        imgs = []
        for frame in self._frames:
            imgs.append(frame.img_to_numpy(load_func))
        return imgs

    def to_pandas(self) -> pd.DataFrame:
        """Returns a pandas representation of the data"""
        if self._data is None:
            self._data = pd.DataFrame(frame.to_tuple() for frame in self._frames)
            self._data = self._data.set_index("timestamp")
        return self._data

    @property
    def drive_id(self):
        return self.to_pandas()["drive_id"]

    @property
    def image_fpaths(self):
        return self.to_pandas()["image_fpath"]

    @property
    def timestamp(self):
        return self.to_pandas().index

    def bboxes(self, model_name):
        """Fetch the bounding boxes for all the frames

        NOTE: Will only fetch bounding boxes for those frames that have bounding boxes associated with
              them by the model.

        Args:
            model_name: The model that provides the bounding boxes e.g. `yolo-v3`

        Returns:
            The bounding boxes for the frames
        """
        if model_name in self._bboxes:
            return self._bboxes[model_name]
        # This is optimized with a single call to the backend as opposed to multiple, one per frame
        df = self.to_pandas().copy()
        df = df.reset_index()
        self._bboxes[model_name] = self._session.get_bboxes(df, model_name)
        # TODO(robert): Cache this in the individual frames as well here?
        return self._bboxes[model_name]

    def plot(self, model_name: Optional[str] = None, force_plot: bool = False):
        """Plot frames with the provided bounding boxes overlaid

        If there are more than 10 frames to plot, by default the function does not plot because it might lead to memory
        problems.

        Args:
            model_name: Model for which to fetch the bounding boxes
            force_plot: Forces the plot even if there are more than 10 frames to plot
        """
        if len(self) > 10 and not force_plot:
            print(
                f"Attempting to plot {len(self)} frames which might cause performance issues. "
                f"If you are sure this is what you want to do, call `plot` with `force_plot=True`",
            )
            return

        for frame in self:
            frame.plot(frame.bboxes(model_name))

    def view(self):
        raise NotImplementedError
