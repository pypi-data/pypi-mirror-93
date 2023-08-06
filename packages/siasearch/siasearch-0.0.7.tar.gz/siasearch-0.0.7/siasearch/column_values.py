from typing import Dict

import pandas as pd


class ColumnValues:
    """Wraps the data from columns

    Usually the results of :meth:`.Sequence.column_values`
    """

    def __init__(self, data: pd.DataFrame):
        self._data = data

    def __repr__(self):
        return f"Raw values for: {list(self._data.columns)}"

    def __getitem__(self, item) -> pd.Series:
        return self._data[item]

    def to_dict(self) -> Dict[str, pd.Series]:
        """Returns values as a dict"""
        d = self._data.to_dict()
        return d

    def to_pandas(self) -> pd.DataFrame:
        """Returns a pandas representation of the data"""
        return self._data
