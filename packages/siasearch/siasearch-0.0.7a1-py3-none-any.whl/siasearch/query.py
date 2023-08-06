from typing import Union
import pandas as pd

from .sequences import Sequences
from .session import Session
from .urls import URLS


class Query:
    """Allows for querying for specific :class:`.Sequences`

    Examples:
        >>> sia = SiaSearch.login("http://custom-domain.siasearch.de", "user@example.com", "password")
        >>> query = sia.query("dataset_name = 'kitti' AND curved_trajectory = 'LEFT_BEND'")
        Query("dataset_name = 'kitti' AND curved_trajectory = 'LEFT_BEND'")
        >>> query.all()
        <Sequences class with 54 segments>
    """

    def __init__(self, session: Session, query_value: str):
        if not isinstance(query_value, str):
            raise ValueError(
                f"Currently there is only support for raw string queries, got query of type {type(query_value)}"
            )
        self.query_str = query_value
        self._session = session

    def all(self) -> Sequences:
        """Fetches the query results and returns the corresponding :class:`.Sequences`"""
        request_format = "parquet"
        params = {"query": self.query_str, "query_source": "python_api", "format": request_format}
        df_segments = self._session.get(URLS.query, params, request_format)
        if df_segments.empty:
            df_segments = pd.DataFrame([], columns=["drive_id", "start_timestamp", "end_timestamp", "dataset_name"])
        df_segments["start_timestamp"] = pd.to_datetime(df_segments["start_timestamp"])
        df_segments["end_timestamp"] = pd.to_datetime(df_segments["end_timestamp"])

        df_segments = df_segments.sort_values(["drive_id", "start_timestamp"])

        segments = Sequences.from_pandas(self._session, df_segments, query=self.query_str)
        return segments

    def __repr__(self):
        return f'{self.__class__.__name__}("{self.query_str}")'

    def and_(self, statement: Union[str, "Query"]) -> "Query":
        """Dot notation to combine different queries

        Examples:
            >>> query1 = sia.query("dataset_name = 'mxa' AND curved_trajectory = 'LEFT_BEND'")
            >>> query2 = sia.query("forward_velocity > 5")
            >>> query1.and_(query2)
            Query("dataset_name = 'mxa' AND curved_trajectory = 'LEFT_BEND' AND forward_velocity > 5")
            >>> query2.and_("forward_acceleration > 1")
            Query("forward_velocity > 5 AND forward_acceleration > 1")
        """
        if isinstance(statement, str):
            query_new = self.query_str + " AND " + statement
        elif isinstance(statement, Query):
            query_new = self.query_str + " AND " + statement.query_str
        else:
            raise ValueError(f"Unsupported query type {statement}")

        return Query(self._session, query_new)
