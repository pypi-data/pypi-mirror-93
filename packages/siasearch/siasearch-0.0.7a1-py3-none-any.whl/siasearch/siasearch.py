from typing import Optional

import pandas as pd

from .results import Segments
from .session import Session
from .urls import API_LOGIN_URL, API_QUERY_URL, METRICS_INFO_URL


class Siasearch:
    """Siasearch interface that maintains login credentials for backend connection and allows to query for drive
    segments of interest

     Examples:
         >>> sia = Siasearch("http://redfish-development.merantix.de", "user@example.com", "password")
         >>> sia
         'Siasearch object with user `user@example.com` connected to `http://redfish-development.merantix.de`'
         >>> sia.query_clips("dataset_name = 'kitti_raw'")
         "Results for query `dataset_name = 'kitti_raw'`"
    """

    def __init__(self, server: str, email: str, password: str, viewer_server: Optional[str] = None):
        self.server = server.rstrip("/")
        self.email = email
        self.session = Session(server, viewer_server=viewer_server)
        self.session.set_jwt_token(self._login(self.email, password))

    def __str__(self):
        return f"{self.__class__.__name__} object with user `{self.email}` connected to `{self.server}`"

    def __repr__(self):
        return self.__str__()

    def _login(self, email, password):
        data = {"email": email, "password": password}
        json_res = self.session.post_json(API_LOGIN_URL, data)
        return json_res["access_token"]

    def query(self, query: str) -> Segments:
        """Query SiaSearch platform for segments

        Args:
            query: The query statements to execute

        Returns:
            `Results` object containing the results of the query

        Examples:
            >>> sia = Siasearch("http://redfish-development.merantix.de", "user@example.com", "password")
            >>> sia.query_clips("dataset_name = 'kitti' AND curved_trajectory = 'LEFT_BEND'")
            "Results for query `dataset_name = 'kitti' AND curved_trajectory = 'RIGHT_BEND'`"

        """
        # TODO (timopheym): Preprocess query: enforce space before and after operator
        request_format = "parquet"
        params = {"query": query, "query_source": "python_api", "format": request_format}
        df_segments = self.session.get(API_QUERY_URL, params, request_format)
        return Segments(df_segments, query, self.session)

    def get_metrics_info(self) -> pd.DataFrame:
        """Fetches information on all implemented metrics

        Returns:
            A pandas dataframe where the index corresponds to the metric name. The dataframe has the following
            columns:

            - type_value: The type of values for that particular metric. One of:
                - `range_double`
                - 'range_integer'
                - `ordinal`
                - `categorical`
                - `slider`
                - `map`

            - levels: For categorical and ordinal metrics shows the discrete values they can take

            - unit: Holds the unit of the metric if the metric has a unit e.g. m/s for `forward_velocity`

            - description: Description of the metric

            - display_name: Pretty-printable metric name

        Examples:
            >>> sia = Siasearch("http://redfish-development.merantix.de", "user@example.com", "password")
            >>> df = sia.get_metrics_info()
            >>> df.columns
            Index(['type_value', 'levels', 'unit', 'description', 'display_name'], dtype='object')
            >>> df.loc["curved_trajectory"].levels
            ["'LEFT_BEND'", "'NO_BEND'", "'RIGHT_BEND'"]
            >>> df.loc["curved_trajectory"].description
            'Categorical. `LEFT_BEND` / `RIGHT_BEND` for clips in which the vehicle trajectory monotonically changes
            its angle by at least 60 degrees. `NO_BEND` otherwise. '
            >>> df.loc["forward_velocity"].unit
            'm/s'

        """
        # TODO(robert): This dataframe is quite cluttered with all kinds of columns. Think of a way to
        #               allow the user to filter for specific types of columns that are relevant.
        df = self.session.get(METRICS_INFO_URL, format="json_df")
        df = df.set_index(["name"]).sort_index()
        df = df[["type_value", "levels", "unit", "description", "display_name"]]

        return df
