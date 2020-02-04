import json
import os
import pathlib
from enum import Enum

from geojson import FeatureCollection, Feature

from .stac import STACQuery
from .logging import get_logger

logger = get_logger(__name__)


def ensure_data_directories_exist():
    pathlib.Path("/tmp/input/").mkdir(parents=True, exist_ok=True)
    pathlib.Path("/tmp/output/").mkdir(parents=True, exist_ok=True)
    pathlib.Path("/tmp/quicklooks/").mkdir(parents=True, exist_ok=True)


def load_query(validator=lambda x: True) -> STACQuery:
    """
    Get the query for the current task directly from the task parameters.
    """
    data: str = os.environ.get("UP42_TASK_PARAMETERS", "{}")
    logger.debug("Raw task parameters from UP42_TASK_PARAMETERS are: %s", data)
    query_data = json.loads(data)
    return STACQuery.from_dict(query_data, validator)


def load_params() -> dict:
    """
    Get the parameters for the current task directly from the task parameters.
    """
    data: str = os.environ.get("UP42_TASK_PARAMETERS", "{}")
    logger.debug("Fetching parameters for this block: %s", data)
    if data == "":
        data = "{}"
    return json.loads(data)


def load_metadata() -> FeatureCollection:
    """
    Get the geojson metadata from the provided location
    """
    ensure_data_directories_exist()
    if os.path.exists("/tmp/input/data.json"):
        with open("/tmp/input/data.json") as json_file:
            data = json.loads(json_file.read())

        features = []
        for feature in data["features"]:
            features.append(Feature(**feature))

        return FeatureCollection(features)
    else:
        return FeatureCollection([])


def save_metadata(result: FeatureCollection):
    """
    Save the geojson metadata to the provided location
    """
    ensure_data_directories_exist()
    with open("/tmp/output/data.json", "w") as json_file:
        json_file.write(json.dumps(result))


class BlockModes(Enum):
    DRY_RUN = "DRY_RUN"
    DEFAULT = "DEFAULT"


def get_block_mode() -> str:
    """
    Gets the task mode from environment variables. If no task mode is set, DEFAULT
    mode will be returned.
    """
    value = os.environ.get("UP42_JOB_MODE", BlockModes.DEFAULT.value)
    if value not in [mode.value for mode in BlockModes]:
        value = "DEFAULT"
    return value
