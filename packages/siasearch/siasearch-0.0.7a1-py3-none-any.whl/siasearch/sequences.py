from collections import namedtuple, Sequence as AbstractSequence
from typing import Iterable, List, Optional, Union

import pandas as pd

from .column_values import ColumnValues
from .constants import TIME_STRING_FORMAT
from .frames import Frames
from .session import Session
from .urls import URLS
from .util import parse_query_url, URLString

SegmentTuple = namedtuple("SegmentTuple", "drive_id, start_timestamp, end_timestamp")


def listify(p: Union[None, str, Iterable]):
    if p is None:
        return []
    elif isinstance(p, str):
        return [p]
    elif isinstance(p, Iterable):
        return list(p)
    else:
        raise ValueError(f"Unsupported type for listify {type(p)}")


class Sequence:
    """
    A sequence defined by a `drive_id`, `start_timestamp` and `end_timestamps` and associated. Usually one "row" (item)
    from from a query results (represented as a :class:`.Sequences` object)
    """

    def __init__(self, session: Session, drive_id: str, start_timestamp: pd.Timestamp, end_timestamp: pd.Timestamp):
        self.drive_id = drive_id

        if not end_timestamp >= start_timestamp:
            raise ValueError(
                f"Expected end_timestamp to be later than start_timestamp. Got {end_timestamp} and {start_timestamp}"
            )
        self.start_timestamp = start_timestamp
        self.end_timestamp = end_timestamp

        self._session = session
        self._frames = None

    @property
    def duration(self):
        return self.end_timestamp - self.start_timestamp

    def __repr__(self):
        content = f"drive_id='{self.drive_id}', start_timestamp='{self.start_timestamp}', duration='{self.duration}'"

        return f"<{self.__class__.__name__}({content})>"

    def sensor_names(self):
        """Get available cameras for the particular Sequence"""
        url_filled = URLS.sensor_names.replace("<drive_id>", self.drive_id)
        return self._session.get(url_filled, format="json")

    def column_values(self, names: Union[str, Iterable[str]]) -> ColumnValues:
        """Get the data in columns for this particular Sequence

        Args:
            names: Names of the columns to fetch

        Returns:
            The data from the columns wrapped in `ColumnValues` object
        """
        names = listify(names)
        # TODO(robert): Check here for valid columns

        url_filled = URLS.data.replace("<drive_id>", self.drive_id)
        df = self._session.get(
            url_filled,
            params={
                "start_timestamp": self.start_timestamp,
                "end_timestamp": self.end_timestamp,
                "metrics": str(names),
            },
            format="parquet",
        )
        col_values = ColumnValues(df)
        return col_values

    def to_pandas(self) -> pd.Series:
        """Returns a pandas representation of the data"""
        return pd.Series(
            [self.drive_id, self.start_timestamp, self.end_timestamp],
            index=["drive_id", "start_timestamp", "end_timestamp"],
        )

    def to_tuple(self) -> SegmentTuple:
        return SegmentTuple(
            drive_id=self.drive_id, start_timestamp=self.start_timestamp, end_timestamp=self.end_timestamp
        )

    def frames(self):
        """Get a Frames representation of the sequences"""
        if self._frames is None:
            self._frames = Frames.from_sequences(Sequences(self._session, [self]))
        return self._frames

    def view(self) -> URLString:
        """Get the URL corresponding to the segment in the frontend"""
        query_url = (
            f"start_timestamp={self.start_timestamp.strftime(TIME_STRING_FORMAT)}&"
            f"end_timestamp={self.end_timestamp.strftime(TIME_STRING_FORMAT)}"
        )

        query_url = parse_query_url(query_url)
        return URLString(f"{self._session.viewer_server}/drives/{self.drive_id}?{query_url}")


class Sequences(AbstractSequence):
    """
    A collection of Sequence objects. Usually the results of a :class:`.Query`. Can be treated like a
    `collections.Sequence` i.e. slicing, getting items etc.
    """

    REQUIRED_COLS = ["drive_id", "start_timestamp", "end_timestamp"]

    def __init__(self, session: Session, segments_list: List[Sequence], query: Optional[str] = None):
        self._session = session
        if not isinstance(segments_list, list):
            raise TypeError(f"Expected input to be a list, got {type(segments_list)}")
        self._check_all_segment(segments_list)
        self._segments = segments_list
        self._frames = None
        self._query = query

    @classmethod
    def from_pandas(cls, session: Session, df: pd.DataFrame, query: Optional[str] = None):
        if not all(c in df for c in cls.REQUIRED_COLS):
            raise ValueError("Expected")
        segments = [Sequence(session, row.drive_id, row.start_timestamp, row.end_timestamp) for row in df.itertuples()]
        return cls(session, segments, query)

    def to_pandas(self) -> pd.DataFrame:
        """Returns a pandas representation of the data"""
        return pd.DataFrame(seg.to_tuple() for seg in self._segments)

    def view(self) -> Optional[URLString]:
        """If a query is available, return a link to the frontend to view the query that generated the Sequences"""
        if self._query:
            query = parse_query_url(self._query)
            return URLString(f"{self._session.viewer_server}/search?query={query}&submit=true")
        return None

    def frames(self):
        """Get a Frames representation of the sequences"""
        if self._frames is None:
            self._frames = Frames.from_sequences(self)
        return self._frames

    @staticmethod
    def _check_all_segment(data) -> None:
        if isinstance(data, Sequence):
            return
        elif isinstance(data, list):
            if not all(isinstance(d, Sequence) for d in data):
                raise TypeError(f"Expected all elements in the input list to be of type {Sequence.__class__.__name__}")
        else:
            raise TypeError(f"Unsupported type {type(data)}, expected {Sequence.__class__.__name__}")

    def __repr__(self):
        return f"<{self.__class__.__name__} class with {len(self._segments)} segments>,\n{self.to_pandas().__repr__()}"

    def __len__(self) -> int:
        return len(self._segments)

    def __getitem__(self, i: Union[int, slice]) -> Union["Sequences", Sequence]:
        if isinstance(i, int):
            return self._segments[i]
        elif isinstance(i, slice):
            return Sequences(self._session, self._segments[i])
        else:
            raise TypeError(f"{self.__class__.__name__} indices must be integers or slices, not {type(i)}")

    def __add__(self, other: "Sequences"):
        return Sequences(self._session, self._segments + other._segments)
