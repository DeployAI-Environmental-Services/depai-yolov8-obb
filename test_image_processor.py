import os
import json
import colorsys
from urllib.parse import urlparse
import grpc
import pytest
import requests
from matplotlib import pyplot as plt
import matplotlib.patches as patches
import tifffile as tiff
import model_pb2
import model_pb2_grpc


def generate_class_colors(num_classes):
    hsv_colors = [(x * 1.0 / num_classes, 1.0, 1.0) for x in range(num_classes)]
    rgb_colors = [
        tuple(int(255 * y) for y in colorsys.hsv_to_rgb(*color)) for color in hsv_colors
    ]
    return rgb_colors


colors = generate_class_colors(18)
normalized_colors = [(r / 255.0, g / 255.0, b / 255.0) for r, g, b in colors]


def download_file_from_url(url, ouput_path):
    response = requests.get(url, stream=True)  # pylint:disable=W3101
    if response.status_code == 200:
        with open(ouput_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"File downloaded successfully as {ouput_path}")
    else:
        print(f"Failed to download file. Status code: {response.status_code}")


def get_filename_from_url(url):
    parsed_url = urlparse(url)
    filename = os.path.basename(parsed_url.path)
    return filename


def read_annotations(file_path):
    with open(file_path, "r") as file:  # pylint:disable=W1514
        annotations = []
        for line in file:
            values = line.strip().split()
            x1, y1, x2, y2, x3, y3, x4, y4 = map(
                lambda val: float(val) * 1025, values[1:-1]
            )

            category = values[0]
            annotations.append(
                {
                    "x1": x1,
                    "y1": y1,
                    "x2": x2,
                    "y2": y2,
                    "x3": x3,
                    "y3": y3,
                    "x4": x4,
                    "y4": y4,
                    "category": category,
                }
            )
    return annotations


def visualize_annotations(img_path, annotation_path, output_path):
    img = tiff.imread(img_path)
    fig, ax = plt.subplots(1)
    ax.imshow(img)
    annotations = read_annotations(annotation_path)
    for annotation in annotations:
        polygon = patches.Polygon(
            [
                (annotation["x1"], annotation["y1"]),
                (annotation["x2"], annotation["y2"]),
                (annotation["x3"], annotation["y3"]),
                (annotation["x4"], annotation["y4"]),
            ],
            closed=True,
            edgecolor=normalized_colors[int(annotation["category"])],
            linewidth=2,
            fill=False,
        )
        ax.add_patch(polygon)
        # ax.text(
        #     annotation["x1"],
        #     annotation["y1"],
        #     f"{int(annotation['category'])}",
        #     color="white",
        #     bbox=dict(facecolor=colors[int(annotation["category"])], alpha=0.5),
        # )

        # Remove axes for better visualization
        ax.axis("off")
    plt.savefig(output_path)


@pytest.fixture(scope="module")
def grpc_stub():
    channel = grpc.insecure_channel("localhost:8061")
    stub = model_pb2_grpc.ImageProcessorStub(channel)
    yield stub
    channel.close()


def test_process_image(grpc_stub):  # pylint: disable=W0621
    response = grpc_stub.ProcessImage(
        model_pb2.ImageRequest(  # pylint: disable=E1101
            input_s3_uris=[
                "s3://MoBucket/obj-det/patch_250.tif",
                "s3://MoBucket/obj-det/patch_420.tif",
            ]
        )
    )
    assert response.output_s3_uri is not None
    assert response.output_s3_url is not None
    print("Output S3 URI: " + response.output_s3_uri)
    print("Output S3 URL: " + response.output_s3_url)
    output_file_path = "test-data/output.json"
    download_file_from_url(response.output_s3_url, output_file_path)
    with open(output_file_path, "r") as file:  # pylint: disable=W1514
        data = json.load(file)
    for result in data:
        result_url = result["result_url"]
        fname = get_filename_from_url(result_url)
        file_path = os.path.join("test-data", fname)
        download_file_from_url(result_url, file_path)
        img_path = os.path.join("test-data", fname.split(".")[0] + ".tif")
        output_path = os.path.join("test-data", fname.split(".")[0] + ".png")
        visualize_annotations(img_path, file_path, output_path)
