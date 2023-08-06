import io
import json
from typing import Dict, List, Optional, Union
from urllib.parse import urljoin

import pandas as pd
import requests
from requests.utils import requote_uri

from .urls import URLS
from .constants import TIME_STRING_FORMAT


def _decode_parquet_buffer(content):
    buffer = io.BytesIO()
    buffer.write(content)
    return pd.read_parquet(buffer, engine="pyarrow")


class Session:
    def __init__(self, server: str, jwt_token: Optional[str] = None, viewer_server: Optional[str] = None):
        self.server = server.rstrip("/")
        self.jwt_token = jwt_token
        self.viewer_server = viewer_server.rstrip("/") if viewer_server else self.server

    def set_jwt_token(self, jwt_token: str):
        self.jwt_token = jwt_token

    def get(
        self, rel_url: str, params: Optional[Dict[str, Union[str, List[str]]]] = None, format: Optional[str] = None,
    ):
        url = urljoin(self.server, rel_url)
        r = requests.get(requote_uri(url), params=params, headers={"Authorization": f"Bearer {self.jwt_token}"})
        if r.status_code == 500:
            raise RuntimeError(f"Server {self.server} encountered an error")
        if r.status_code != 200:
            raise RuntimeError(f"Server {self.server} returned status {r.status_code}. Response: {r.text}")
        if format:
            if format == "parquet":
                return _decode_parquet_buffer(r.content)
            elif format == "json_df":
                return pd.DataFrame.from_dict(json.loads(r.text))
            elif format == "json":
                return json.loads(r.text)
            else:
                raise ValueError(f"Unknown api format {format}")
        return r

    def post(self, rel_url, json_body: Dict, params: Optional[Dict] = None):
        url = urljoin(self.server, rel_url)
        r = requests.post(
            requote_uri(url), json=json_body, params=params, headers={"Authorization": f"Bearer {self.jwt_token}"}
        )
        if r.status_code != 200:
            raise RuntimeError(f"Server {self.server} returned status {r.status_code}. Response: {r.text}")
        return r

    def post_json(self, rel_url: str, params: Optional[Dict[str, str]]):
        return json.loads(self.post(rel_url, params).text)

    def get_bboxes(self, df_org, model_name):
        df = df_org.copy()
        df["timestamp"] = df["timestamp"].dt.strftime(TIME_STRING_FORMAT)
        json_df = df.to_dict(orient="records")

        eval_val = self.post(URLS.bboxes, json_body={"model_name": model_name, "df_frames": json_df})
        eval_val = json.loads(eval_val.text)
        df_results = pd.DataFrame.from_dict(eval_val)
        return df_results
