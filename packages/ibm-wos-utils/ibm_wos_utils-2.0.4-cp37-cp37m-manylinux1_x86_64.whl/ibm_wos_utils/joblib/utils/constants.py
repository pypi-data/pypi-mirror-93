# ----------------------------------------------------------------------------------------------------
# IBM Confidential
# OCO Source Materials
# 5900-A3Q, 5737-H76
# Copyright IBM Corp. 2020, 2021
# The source code for this program is not published or other-wise divested of its trade
# secrets, irrespective of what has been deposited with the U.S.Copyright Office.
# ----------------------------------------------------------------------------------------------------

from enum import Enum
from http import HTTPStatus

SPARK_INSTANCE = 'BatchTestingInstance'
SPARK_VOLUME = 'aios'
IAE_SPARK_INTEGRATED_SYSTEM = 'watson_data_catalog'
IAE_JOB_FINISHED_STATE = 'FINISHED'
IAE_JOB_FAILED_STATE = 'FAILED'

LIVY_JOB_FINISHED_STATE = 'success'
LIVY_JOB_FAILED_STATE = 'error'
LIVY_JOB_DEAD_STATE = 'dead'
LIVY_JOB_KILLED_STATE = 'killed'

SYNC_JOB_MAX_WAIT_TIME = 300

ENTRY_JOB_FILE = 'main_job.py'
ENTRY_JOB_BASE_FOLDER = "job"
IAE_SPARK_JOB_NAME = "Watson Openscale IAE Spark Job"
IAE_VOLUME_MOUNT_PATH = "/openscale"

TIMESTAMP_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"
UPLOAD_FILE_RETRY_COUNT = 3
UPLOAD_FILE_RETRY_STATUS_CODES = [
    HTTPStatus.NOT_FOUND,
    HTTPStatus.BAD_GATEWAY,
    HTTPStatus.SERVICE_UNAVAILABLE,
    HTTPStatus.GATEWAY_TIMEOUT
]

DEFAULT_CONNECTION_TIMEOUT = 180 # Number of seconds to wait while connecting to database

class SparkType(Enum):
    REMOTE_SPARK = "custom"
    IAE_SPARK = "cpd_iae"

class StorageType(Enum):
    HIVE = "hive"
    JDBC = "jdbc"
