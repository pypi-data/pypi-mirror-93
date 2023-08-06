from typing import List

import pandas as pd

from .mixins import DisplaysUrl
from .segment import Segment
from .session import Session
from .utils import parse_query_url


class Segments(DisplaysUrl):
    """Segments interface that holds multiple segments and allows a user to manipulate them in different ways

     Examples:
        >>> sia = Siasearch("http://redfish-development.merantix.de", "user@example.com", "password")
        >>> segments: Segments = sia.query_clips("dataset_name = 'kitti")
        >>> segments.df_segments()
    """

    _ordered_columns = ["drive_id", "start_timestamp", "end_timestamp", "dataset_name"]

    def __init__(self, df_segments: pd.DataFrame, query: str, session: Session):
        """Holds query results in the form of drive Segments.

        Args:
            df_segments:
            query: SiaSearch query associated with the data
        """
        self._query = query
        self._df_segments = self._format_df_segments(df_segments)
        self._segments = None
        self._session = session

    def _format_df_segments(self, df):
        if df.shape[0] > 0:
            df = df[self._ordered_columns]
            df = df.sort_values(by="drive_id")
            df = df.reset_index(drop=True)

        return df

    @property
    def segments(self) -> List[Segment]:
        """Returns list of drive Segments corresponding to a query"""
        if self._segments is None:
            self._segments = [
                Segment(
                    row.drive_id, row.start_timestamp, row.end_timestamp, row.dataset_name, self._session, self._query
                )
                for row in self._df_segments.itertuples()
            ]
        return self._segments

    @property
    def df_segments(self) -> pd.DataFrame:
        """Returns pd.DataFrame with Segments corresponding to a query

        Args:


        Returns:
          pandas DataFrame with segments
        """
        return self._df_segments

    def get_url(self) -> str:
        """Get the URL for the results of a query to view it via web browser in the SiaSearch frontend

        Returns:
            The URL corresponding to the query results
        """
        query = parse_query_url(self._query)
        return f"{self._session.viewer_server}/search?query={query}&submit=true"

    def __str__(self):
        return f"{self.__class__.__name__} for query `{self._query}`"

    def __repr__(self):
        return self.__str__()
