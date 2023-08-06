import urllib.parse
from itertools import islice
from typing import Tuple

import numpy as np
from IPython.display import display, HTML


class URLString(str):
    """A subclass of strings that displays urls as links in ipython"""

    def _ipython_display_(self):
        url = str(self)
        return display(HTML(f"<a href='{url}'>{url}</a>"))


def parse_query_url(url):
    return urllib.parse.quote_plus(url, safe="=&")


def change_sampling_frequency(timestamp_to_fpath_series, min_time_between_samples):
    timestamps = timestamp_to_fpath_series.index.astype("int64") / 10 ** 9  # convert to sec from nanosec

    # Re-sample in order to get sampling frequency at most (1 / min_time_passed_between_samples) Hz
    _, kept_indices = filter_close_points_from_sequence(
        timestamps, min_distance=min_time_between_samples, keep_last_point=False
    )
    return timestamp_to_fpath_series.iloc[kept_indices]


def filter_close_points_from_sequence(
    coordinates_sequence: np.array, min_distance: float, keep_last_point: bool = True
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Function goes over `coordinates_sequence` and accepts each coordinate that is at least `min_distance` units away
    from the previously accepted coordinate.

    TODO:
        This approach could be improved by sampling interesting points, rather than points that are a min.
        distance apart. One approach to look into is the Ramer–Douglas–Peucker algorithm
    Args:
        coordinates_sequence: Series of relative coordinates in meters indexed in time order.
        min_distance: Minimum accepted distance between two subsequent coordinates. The larger
            the value the more points will be removed from the `coordinates_sequence`.
        keep_last_point: Will keep the last point in the sequence even though the distance to it
            from the second last point is smaller than `min_distance`

    Returns:
        Tuple with two arrays: similar to `coordinates_sequence`, with some of the coordinates removed.
    """
    if min_distance < 0:
        raise ValueError("`min_distance` should be a positive number")

    if len(coordinates_sequence) == 0:
        return np.array([]), np.array([])

    last_accepted_point = coordinates_sequence[0]
    cleaned_coordinates_sequence = [last_accepted_point]
    kept_indices = [0]

    for index, next_point_candidate in enumerate(islice(coordinates_sequence, 1, None), start=1):
        distance = np.linalg.norm(np.subtract(next_point_candidate, last_accepted_point))

        if distance >= min_distance:
            cleaned_coordinates_sequence.append(next_point_candidate)
            kept_indices.append(index)
            last_accepted_point = next_point_candidate

    if keep_last_point and np.all(cleaned_coordinates_sequence[-1] != coordinates_sequence[-1]):
        cleaned_coordinates_sequence.append(coordinates_sequence[-1])
        kept_indices.append(index)

    return np.array(cleaned_coordinates_sequence), np.array(kept_indices)
