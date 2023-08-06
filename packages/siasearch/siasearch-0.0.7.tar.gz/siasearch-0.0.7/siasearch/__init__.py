from typing import Optional

from .columns import Columns
from .evaluation import SiaSearchModelEvaluation
from .query import Query
from .session import Session
from .urls import URLS


class SiaSearch:
    """Interface that maintains login credentials for backend connection and allows to query

    Args:
        server: Server to connect to
        api_key: Log in token fetched from the frontend
        viewer_server: Server to view results on. If not specified, uses `server`

    Examples:
        >>> sia = SiaSearch("http://custom-domain.siasearch.de", "my_api_key")
        >>> sia
        <SiaSearch object connected to `http://custom-domain.siasearch.de`>

        >>> sia = SiaSearch.login("http://custom-domain.siasearch.de", "user@example.com", "password")
        >>> sia
        <SiaSearch object connected to `http://custom-domain.siasearch.de`>
    """

    def __init__(self, server: str, api_key: str, viewer_server: Optional[str] = None):
        self.server = server.rstrip("/")
        self._session = Session(server, jwt_token=api_key, viewer_server=viewer_server)
        self.model_evaluation = SiaSearchModelEvaluation()

    @classmethod
    def login(cls, server: str, email: str, password: str, viewer_server: Optional[str] = None) -> "SiaSearch":
        """Fetch a `SiaSearch` object logging in using an email and a password

        Args:
            server: Server to connect to
            email: Login email
            password: Password corresponding to the login email
            viewer_server: Server to view results on. If not specified, uses `server`

        Returns:
            A `SiaSearch` object with the user logged in, whose credentials were passed to the function
        """
        try:
            data = {"email": email, "password": password}
            json_res = Session(server, viewer_server).post_json(URLS.login, data)
            api_key = json_res["access_token"]
        except RuntimeError as e:
            print("Login failed:")
            raise e
        return cls(server, api_key, viewer_server)

    def __str__(self):
        if self._session is None:
            return f"Connection to {self.server} was not established"
        return f"<{self.__class__.__name__} object connected to `{self.server}`>"

    def __repr__(self):
        return self.__str__()

    def query(self, query_str: str) -> Query:
        """Get a query object corresponding to the input query. See :class:`.Query`

        Args:
            query_str: The query statements to execute

        Returns:
            Query object containing the results of the query

        Examples:
            >>> sia = SiaSearch.login("http://custom-domain.siasearch.de", "user@example.com", "password")
            >>> query = sia.query("dataset_name = 'kitti' AND curved_trajectory = 'LEFT_BEND'")
            Query("dataset_name = 'kitti' AND curved_trajectory = 'LEFT_BEND'")
            >>> query.all()
            <Sequences class with 54 segments>
        """
        return Query(self._session, query_str)

    def columns(self) -> Columns:
        """Fetches information on all available columns of data. See :class:`.Columns`.

        Examples:
            >>> sia = SiaSearch.login("http://custom-domain.siasearch.de", "user@example.com", "password")
            >>> sia.columns()
            <Columns object containing columns: ['acceleration_level', 'being_overtaken', 'country_name', 'cut_in',
            'dataset_name', 'drive_id', 'num_pedestrians', 'tag_road_type', 'velocity_level']>
        """
        df = self._session.get(URLS.columns_info, format="json_df")
        df = df.set_index(["name"]).sort_index()

        m = Columns(df)
        return m
