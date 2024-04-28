from datetime import datetime

# ---------------------------------------------
# Constants for the backend
# ---------------------------------------------

# AWS Constants
AWS_S3_BUCKET = "hectre-journals"
TEST_S3_BUCKET = "hectre-journals-test"
REGION_NAME = "us-east-2"

# Service Constants
DATETIME_FMT = "%Y-%m-%d-%H:%M:%S"
S3_FOLDER_INPUT = f"uploads-{datetime.now().strftime(DATETIME_FMT)}"
S3_FOLDER_OUTPUT = f"output-{datetime.now().strftime(DATETIME_FMT)}"
TEMP_DIR = "temp"
