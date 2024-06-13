import errno
import json
import logging
import os
import shutil
import boto3
import requests
from botocore.exceptions import ClientError
from app.config import (
    ACCESS_KEY,
    BUCKET_NAME,
    END_POINT,
    SECRECT_ACCESS_KEY,
    TMP_PATH,
)


def clean_temp_directory(folder_name: str):
    try:
        shutil.rmtree(folder_name)
    except OSError as e:
        logging.error("Error: %s - %s.", e.filename, e.strerror)


def download_file(url: str, dst_name: str):
    try:
        data = requests.get(url, stream=True)  # pylint: disable=W3101
        with open(dst_name, "wb") as out_file:
            for chunk in data.iter_content(chunk_size=100 * 100):
                out_file.write(chunk)
    except:  # pylint: disable=W0702
        logging.error("\t ... %s FAILED!", url.split("/")[-1])  # pylint: disable=W0702
    return


def create_directory(folder_name: str):
    if not os.path.exists(folder_name):
        try:
            os.mkdir(folder_name)
        except OSError as exc:
            if exc.errno != errno.EEXIST:
                raise


def initiate_s3_client(end_point: str, access_key: str, secret_access_key: str):
    s3_client = boto3.client(
        "s3",
        endpoint_url=end_point,
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_access_key,
    )
    return s3_client


def upload_file(file_name: str, bucket_name: str, prefix: str):
    s3_client = initiate_s3_client(END_POINT, ACCESS_KEY, SECRECT_ACCESS_KEY)
    object_name = os.path.basename(file_name)
    try:
        s3_client.upload_file(
            Filename=file_name,
            Bucket=bucket_name,
            Key="{0}/{1}".format(prefix, object_name),  # pylint:disable=C0209
            ExtraArgs={"ACL": "public-read"},
        )
    except ClientError as exce:
        logging.error(exce)
        return False, None
    return True, os.path.join("s3://", bucket_name, prefix, object_name)


def create_presigned_post(bucket_name: str, object_name: str, expiration: int = 3600):
    s3_client = initiate_s3_client(END_POINT, ACCESS_KEY, SECRECT_ACCESS_KEY)
    try:
        url = s3_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": bucket_name, "Key": object_name},
            ExpiresIn=expiration,
        )

    except ClientError as e:
        logging.error(e)
        return None
    return url


def get_json_file(task_id: str):
    s3_client = initiate_s3_client(END_POINT, ACCESS_KEY, SECRECT_ACCESS_KEY)
    file_name = os.path.join(task_id, task_id + ".json")
    local_file_path = os.path.join(TMP_PATH, task_id + ".json")
    with open(local_file_path, "wb") as myf:
        s3_client.download_fileobj(BUCKET_NAME, file_name, myf)
    try:
        with open(local_file_path, "r") as json_file:  # pylint: disable=W1514
            # Load the JSON data
            data = json.load(json_file)
        os.remove(local_file_path)
        return data
    except FileNotFoundError:
        logging.info("File %s not downloaded", file_name)
        return None


def download_file_from_bucket(file_uri: str, local_file_path: str):
    s3_client = initiate_s3_client(END_POINT, ACCESS_KEY, SECRECT_ACCESS_KEY)
    bucket_name = file_uri.split("//")[1].split("/")[0]
    file_name = file_uri.split(bucket_name)[1][1:]
    try:
        s3_client.download_file(bucket_name, file_name, local_file_path)
    except Exception:  # pylint: disable=W0718
        logging.info("File %s not downloaded", file_name)
