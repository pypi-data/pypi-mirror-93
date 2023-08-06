import json
from typing import Dict

from .frames import Frames
from .urls import URLS
from .constants import TIME_STRING_FORMAT


class ModelEvaluationObjectDetection:
    """Get bounding box evaluation results for :class:`.Frames`

    Args:
        frames: The frames to evaluate on
        model_pred: Name of the model to use as the predictions when evaluating bounding boxes
        model_true: Name of the model to use as (ground) truth when evaluating bounding boxes

    Returns:
        A dictionary containing the average precision per class and the mean average precision

    Examples:
        >>> sia = SiaSearch.login("http://custom-domain.siasearch.de", "user@example.com", "password")
        >>> sequences = sia.query("dataset_name = 'kitti' AND curved_trajectory = 'LEFT_BEND'").all()
        >>> model_eval = ModelEvaluationObjectDetection(sequences.frames(), "ground-truth", "yolo-v3")
        Evaluation object for models `yolo-v3` (pred) and `ground-truth` (true) for 1585 frames
    """

    def __init__(self, frames: Frames, model_true: str, model_pred: str):
        # Use intersection of where model_true and model_pred have labels
        self._frames = frames
        self._model_true = model_true
        self._model_pred = model_pred
        # Should this be a parameter? Possibly makes more sense to pass it along
        self._metrics = {}
        self._models = None

        self._session = frames._session

    def __repr__(self):
        return (
            f"Evaluation object for models `{self._model_pred}` (pred) and "
            f"`{self._model_true}` (true) for {len(self._frames)} frames"
        )

    def evaluate(self, iou_threshold: float) -> dict:
        """Evaluate the given :class:`.Frames` and the given model at a specific `iou_threshold`

        Args:
            iou_threshold: The iou threshold to use when matching bounding boxes for evaluation

        Returns:
            Dictionary with average precision values per class, mean average precision and the number of frames used
            for the evaluation

        Examples:
            >>> sia = SiaSearch.login("http://custom-domain.siasearch.de", "user@example.com", "password")
            >>> sequences = sia.query("dataset_name = 'kitti' AND curved_trajectory = 'LEFT_BEND'").all()
            >>> model_eval = ModelEvaluationObjectDetection(sequences.frames(), "ground-truth", "yolo-v3")
            >>> model_eval.evaluate(iou_threshold=0.5)
            {
                'ap': {'Car': 0.38785485446284634, 'Pedestrian': 0.2549019607843137, 'Truck': 0.6367521367521367},
                'mean_ap': 0.23850401725240808,
                'num_frames': 20
            }
        """
        if iou_threshold in self._metrics:
            return self._metrics[iou_threshold]

        df_segments = self._frames.to_pandas().copy()
        df_segments = df_segments.reset_index("timestamp")
        df_segments = df_segments.drop(columns="image_fpath")
        df_segments["timestamp"] = df_segments["timestamp"].dt.strftime(TIME_STRING_FORMAT)
        json_df = df_segments.to_dict(orient="list")

        eval_val = self._session.post(
            URLS.frames_ap,
            json_body={
                "model_pred": self._model_pred,
                "model_true": self._model_true,
                "iou_threshold": iou_threshold,
                "timestamp_match_threshold": 0.0,
                "df_frames": json_df,
            },
        )
        # TODO(robert): This should be handled in `Session`
        eval_val = json.loads(eval_val.text)
        self._metrics[iou_threshold] = eval_val
        return eval_val


def available_models(frames: Frames) -> Dict[str, int]:
    """Fetch all available models for the given frames

    Args:
        frames: The frames for which to check the models

    Returns:
        Dictionary of available models for evaluation with the model names as keys and the number of frames that have
        been evaluated using that particular model as values.

    Examples:
        >>> sia = SiaSearch.login("http://custom-domain.siasearch.de", "user@example.com", "password")
        >>> sequences = sia.query("dataset_name = 'kitti' AND curved_trajectory = 'LEFT_BEND'").all()
        >>> sia.model_evaluation.available_models(sequences.frames())
        {'ground-truth': 20, 'yolo-608-0-3': 1585, 'yolo-608-0-5': 1585, 'yolo-928-0-3': 1585, 'yolo-928-0-5': 1585}
    """
    df_segments = frames.to_pandas().copy()
    df_segments = df_segments.reset_index("timestamp")
    df_segments = df_segments.drop(columns="image_fpath")
    df_segments["timestamp"] = df_segments["timestamp"].dt.strftime(TIME_STRING_FORMAT)
    json_df = df_segments.to_dict(orient="records")
    eval_val = frames._session.post(URLS.models, json_body={"df_frames": json_df})
    eval_val = json.loads(eval_val.text)
    return eval_val


class SiaSearchModelEvaluation:
    @staticmethod
    def object_detection(frames: Frames, model_true: str, model_pred: str):
        return ModelEvaluationObjectDetection(frames, model_true, model_pred)

    @staticmethod
    def available_models(frames: Frames):
        return available_models(frames)
