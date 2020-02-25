"""
STAC query according to https://github.com/radiantearth/stac-spec
"""

from __future__ import annotations

import json
from decimal import Decimal
from typing import Union, Tuple, Iterable, cast, Optional, Callable

import shapely.geometry
from geojson.geometry import Geometry

from .logging import get_logger

logger = get_logger(__name__)

Number = Union[int, Decimal, float]
Coordinates = Iterable[Number]
BoundingBox = Tuple[Number, Number, Number, Number]


class STACQuery:
    """
    Object representing a STAC query as used by data blocks.
    """

    def __init__(
            self,
            bbox: Optional[BoundingBox] = None,
            file_path: Optional[str] = None,
            **kwargs
    ):  # pylint: disable=too-many-arguments

        if not bbox:
            raise ValueError(
                """Only one of the following query parameters is
                allowed at a query at any given time:
                * bbox """
            )

        self.__dict__.update(
            kwargs
        )  # At the front so we do not accidentally overwrite some members
        self.file_path = file_path
        self.bbox = bbox

    def bounds(self) -> BoundingBox:
        """
        Get the bounding box of the query AOI(s) as a GeoJson Polygon object.
        """
        if self.bbox:
            return self.bbox
        else:
            raise ValueError(
                """STACQuery does not contain any of the following query 
                parameters:
                * bbox """
            )

    def geometry(self) -> Geometry:
        if self.bbox:
            return shapely.geometry.box(*self.bbox)
        else:
            raise ValueError(
                """STACQuery does not contain any of the following query 
                parameters:
                * bbox """
            )

    def set_param_if_not_exists(self, key, value):
        if key not in self.__dict__:
            self.__dict__[key] = value

    @classmethod
    def from_json(cls, json_data: str) -> STACQuery:
        return STACQuery.from_dict(json.loads(json_data))

    @classmethod
    def from_dict(
            cls, dict_data: dict,
            validator: Callable[[dict], bool] = lambda x: True
    ) -> STACQuery:

        if not validator(dict_data):
            raise ValueError(
                """Input Query did not pass validation. Please refer
                to the official block documentation or block specification."""
            )

        bbox: Optional[BoundingBox] = cast(BoundingBox,
                                           dict_data.get("bbox")) if not (
                dict_data.get("bbox") is None
                or dict_data.get("bbox") == ""
                or dict_data.get("bbox") == {}
        ) else None

        file_path: Optional[str] = dict_data.get("file_path") \
            if not dict_data.get("time") == "" else None

        known_filters = [
            "bbox",
            "file_path",
        ]

        truncated_dict_data = {
            key: dict_data[key] for key in dict_data if
            key not in known_filters
        }

        return STACQuery(
            bbox=bbox,
            file_path=file_path,
            **truncated_dict_data
        )
