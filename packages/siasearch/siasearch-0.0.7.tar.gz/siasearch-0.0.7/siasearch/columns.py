from typing import Optional

import pandas as pd
from dataclasses import dataclass


@dataclass
class Column:
    name: str
    description: str
    display_name: str


@dataclass
class CategoricalColumn(Column):
    """Stores categorical values e.g. `is_lane_change`"""

    levels: list


@dataclass
class NumericColumn(Column):
    """Stores numerical (float) values e.g. `velocity`"""

    unit: str


@dataclass
class CountingColumn(Column):
    """Stores counts e.g. `num_pedestrians`"""

    pass


@dataclass
class OrdinalColumn(Column):
    """Stores ordinal values e.g. `velocity_level`"""

    levels: list


@dataclass
class TextColumn(Column):
    """Stores text values e.g. `drive_id`"""

    pass


@dataclass
class GenericColumn(Column):
    """Stores generic values"""

    levels: list
    unit: str


class Columns:
    """Class that wraps the information on available columns

    Information about each column is wrapped in a dataclass. The type of the dataclass corresponds to the type
    of values in the column:

        - `range_double`
        - `range_integer`
        - `ordinal`
        - `categorical`
        - `slider`
        - `map`

    The attributes of the class are populated with the names of the columns. This happens dynamically so it is well
    suited for interaction in `ipython` or in a jupyter notebook after it has been created.

    Examples:
        >>> sia = SiaSearch.login("http://custom-domain.siasearch.de", "user@example.com", "password")
        >>> cols = sia.columns()
        <Columns object containing columns: ['acceleration_level', 'being_overtaken', 'country_name', 'cut_in',
        'dataset_name', 'drive_id', 'forward_velocity', 'num_pedestrians', 'tag_road_type', 'velocity_level']>
        >>> cols.forward_velocity
        NumericColumn(name='forward_velocity', unit='m/s', description='Float. Queries for clips in which the
        velocity lies continuously within a specified range (in m/s).', display_name='Forward Velocity')
        >>> cols.cut_in
        CategoricalColumn(name='cut_in', levels=["'left_cut_in'", "'no_cut_in'", "'right_cut_in'"],
        description='Scenarios in which another vehicle cuts into the ego lane.', display_name='Cut In')
    """

    def __init__(self, data: pd.DataFrame):
        self._data = data
        self._metrics = []
        for row in self._data.itertuples():
            row_dict = row._asdict()
            name = row_dict["Index"]
            if row_dict["type_value"] == "categorical":
                col = CategoricalColumn(
                    name=name,
                    levels=row_dict["levels"],
                    description=row_dict["description"],
                    display_name=row_dict["display_name"],
                )
            elif row_dict["type_value"] == "range_double":
                col = NumericColumn(
                    name=name,
                    unit=row_dict["unit"],
                    description=row_dict["description"],
                    display_name=row_dict["display_name"],
                )
            elif row_dict["type_value"] == "range_integer":
                col = CountingColumn(
                    name=name, description=row_dict["description"], display_name=row_dict["display_name"],
                )
            elif row_dict["type_value"] == "ordinal":
                col = OrdinalColumn(
                    name=name,
                    levels=row_dict["levels"],
                    description=row_dict["description"],
                    display_name=row_dict["display_name"],
                )
            elif row_dict["type_value"] == "text":
                col = TextColumn(name=name, description=row_dict["description"], display_name=row_dict["display_name"])
            elif row_dict["type_value"] == "slider" or row_dict["type_value"] == "map":
                col = GenericColumn(
                    name=name,
                    unit=row_dict["unit"],
                    levels=row_dict["levels"],
                    description=row_dict["description"],
                    display_name=row_dict["display_name"],
                )
            else:
                raise ValueError(f"Unknown column type {row_dict['type_value']}")
            setattr(self, name, col)
            self._metrics.append(name)

    def __repr__(self) -> str:
        return f"<Columns object containing columns: {str(self._metrics)}>"

    def __len__(self):
        return len(self._metrics)

    def __getitem__(self, item):
        return self.__dict__[item]

    def to_pandas(self) -> pd.DataFrame:
        """Returns a pandas representation of the data"""
        return self._data

    def filter(self, keep: Optional[str] = None, remove: Optional[str] = None) -> "Columns":
        """Gets a new `Metric` object that has been filtered based on criteria

        Args:
            keep: Substring matching columns to keep (inclusive filter)
            remove: Substring matching columns to remove (exclusive filter)

        Returns:
            Columns object with columns filtered out corresponding to the input parameters
        """
        data = []
        for t in self._data.itertuples():
            if remove is not None and remove in t.Index:
                continue

            if keep is None:
                data.append(t)
            else:
                if keep in t.Index:
                    data.append(t)

        df = pd.DataFrame(data)
        df = df.set_index("Index")
        return Columns(df)
