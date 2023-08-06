# fmt: off

API_BASE_URL = "/public_api/v1"


class Urls:
    login        = API_BASE_URL + "/auth/login"
    query        = API_BASE_URL + "/query"

    columns_info = API_BASE_URL + "/columns_info"

    frames_url   = API_BASE_URL + "/frames/all"

    bboxes       = API_BASE_URL + "/evaluation/bboxes"
    models       = API_BASE_URL + "/evaluation/frames/models"
    frames_ap    = API_BASE_URL + "/evaluation/frames/average_precision"

    sensor_names = API_BASE_URL + "/sequences/<drive_id>/sensor_names"

    data         = API_BASE_URL + "/sequences/<drive_id>/data"

# fmt: on


URLS = Urls()
