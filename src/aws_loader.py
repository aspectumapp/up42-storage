import json
import math
import os
import uuid
from typing import List

import boto3
import botocore
from geojson import FeatureCollection, Feature
from shapely.geometry import Polygon, mapping

from blockutils.common import (
    load_query,
    save_metadata,
    ensure_data_directories_exist,
)
from blockutils.logging import get_logger
from blockutils.stac import STACQuery

logger = get_logger(__name__)


class AWSAspectum:
    DEFAULT_ZOOM_LEVEL = 9
    AWS_ACCESS_KEY = os.environ.get('AWS_ACCESS_KEY')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
    AWS_REGION = os.environ.get('AWS_REGION')
    BUCKET_NAME = os.environ.get('AWS_BUCKET_NAME')
    TIF_FILES = 'up42_storage'

    @staticmethod
    def __convert_size(size_bytes):
        if size_bytes == 0:
            return "0B"
        size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
        i = int(math.floor(math.log(size_bytes, 1024)))
        p = math.pow(1024, i)
        s = round(size_bytes / p, 2)
        return f"{s} {size_name[i]}"

    @staticmethod
    def run():
        query: STACQuery = load_query()
        ensure_data_directories_exist()
        query.set_param_if_not_exists(
            "zoom_level", AWSAspectum.DEFAULT_ZOOM_LEVEL
        )
        output_features: List[Feature] = []

        file_path = f'{AWSAspectum.TIF_FILES}/{query.file_name}'
        feature_id: str = str(uuid.uuid4())
        out_path = f'/tmp/output/{feature_id}.tif'

        logger.debug(f"File output will be {out_path}")

        poly = Polygon([
            [query.bbox[0], query.bbox[1]],
            [query.bbox[2], query.bbox[1]],
            [query.bbox[2], query.bbox[3]],
            [query.bbox[0], query.bbox[3]]
        ])
        geom = json.loads(json.dumps(mapping(poly)))

        feature = Feature(
            id=feature_id,
            bbox=query.bbox,
            geometry=geom,
            properties={
                'up42.data.aoiclipped': f'{feature_id}.tif'
            }
        )

        s3 = boto3.client(
            's3',
            aws_access_key_id=AWSAspectum.AWS_ACCESS_KEY,
            aws_secret_access_key=AWSAspectum.AWS_SECRET_ACCESS_KEY,
            region_name=AWSAspectum.AWS_REGION,

        )

        try:
            response = s3.head_object(
                Bucket=AWSAspectum.BUCKET_NAME,
                Key=file_path
            )
            logger.debug(
                f'[FILE SIZE ON S3] - '
                f'{AWSAspectum.__convert_size(response["ContentLength"])}'
            )
            with open(out_path, 'wb') as f:
                s3.download_fileobj(AWSAspectum.BUCKET_NAME, file_path, f)
            output_features.append(feature)
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == "404":
                logger.error("The object does not exist.")
            else:
                raise
        logger.debug(
            f'[FILE SIZE AFTER DOWNLOAD] - '
            f'{AWSAspectum.__convert_size(os.path.getsize(out_path))}'
        )
        result = FeatureCollection(list(output_features))

        logger.debug("Saving %s result features", len(result.get("features")))
        save_metadata(result)
