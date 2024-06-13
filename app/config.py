import os

TMP_PATH = "/tmp"
ACCESS_KEY = os.environ.get("ACCESS_KEY")
SECRECT_ACCESS_KEY = os.environ.get("SECRET_ACCESS_KEY")
END_POINT = os.environ.get("END_POINT")
BUCKET_NAME = os.environ.get("BUCKET_NAME")
API_KEY = "PFbUcE0/kAIYuYr1Q6xUiIekq7C0qMceyNmyN/pHZVU="
DEBUG = True
NODATAVALUE = -1000
CONFIDENCE = 0.25
STREAM = True
BATCH_SIZE = 1
ISZ = 1025
DICT_CLASSES = {
    "plane": 0,
    "ship": 1,
    "storage-tank": 2,
    "baseball-diamond": 3,
    "tennis-court": 4,
    "basketball-court": 5,
    "ground-track-field": 6,
    "harbor": 7,
    "bridge": 8,
    "large-vehicle": 9,
    "small-vehicle": 10,
    "helicopter": 11,
    "roundabout": 12,
    "soccer-ball-field": 13,
    "swimming-pool": 14,
    "container-crane": 15,
    "airport": 16,
    "helipad": 17,
}
