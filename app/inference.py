import json
import logging
import os
from typing import List
import uuid
from ultralytics import YOLO
from app.config import (
    BUCKET_NAME,
    CONFIDENCE,
    STREAM,
    DICT_CLASSES,
    TMP_PATH,
)
from app.utils import (
    create_directory,
    create_presigned_post,
    download_file_from_bucket,
    clean_temp_directory,
    upload_file,
)


def detect_yolov8_obb(list_images: List[str]):
    task_id = str(uuid.uuid4())
    logging.info("worker_init")
    logging.info("Initialization YOLOv8")
    model = YOLO("/object-detection/app/weights/best.pt")
    temp_path = os.path.join(TMP_PATH, task_id)
    create_directory(temp_path)
    processing_status = []
    for image_uri in list_images:
        list_classes = list(DICT_CLASSES.values())
        res_output = {
            "image_uri": image_uri,
            "processed": False,
            "result_url": None,
            "result_uri": None,
        }
        img_filename = os.path.basename(image_uri)
        downloaded_img_path = os.path.join(temp_path, img_filename)
        download_file_from_bucket(image_uri, downloaded_img_path)
        result = model(
            downloaded_img_path,
            classes=list_classes,
            # imgsz=ISZ,
            conf=CONFIDENCE,
            stream=STREAM,
        )
        result = [res for res in result][0]
        logging.info("Save results of %s", result.path)
        res_output_path = os.path.join(
            temp_path, os.path.basename(result.path).split(".tif")[0] + ".txt"
        )
        result.save_txt(res_output_path, save_conf=True)
        try:
            upload_file(res_output_path, BUCKET_NAME, task_id)
            object_name = os.path.join(task_id, os.path.basename(res_output_path))
            signed_url = create_presigned_post(
                BUCKET_NAME, object_name, expiration=36000
            )
            os.remove(res_output_path)
            os.remove(downloaded_img_path)
            res_output = {
                "image_uri": image_uri,
                "processed": True,
                "result_url": signed_url,
                "result_uri": os.path.join("s3://" + BUCKET_NAME, object_name),
            }
        except FileNotFoundError:
            os.remove(downloaded_img_path)
            res_output = {
                "image_uri": image_uri,
                "processed": True,
                "result_url": None,
                "result_uri": None,
            }
        processing_status.append(res_output)
    clean_temp_directory(temp_path)
    json_file_name = os.path.join(TMP_PATH, task_id + ".json")
    json_data = json.dumps(processing_status)
    # Write JSON data to a local file
    with open(json_file_name, "w") as json_file:  # pylint: disable=W1514
        json_file.write(json_data)
    _, output_s3_uri = upload_file(json_file_name, BUCKET_NAME, task_id)
    if os.path.exists(json_file_name):
        os.remove(json_file_name)
    return output_s3_uri
