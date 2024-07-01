import os
import colorsys
import grpc
import pytest
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
            input_image_paths=[
                "/data/patch_250.tif",
                "/data/patch_420.tif",
            ]
        )
    )
    assert response.entries[0].processed is not None
    assert response.entries[1].processed is not None
    print("Output file: " + response.entries[0].result_path)
    print("Output file: " + response.entries[1].result_path)
    for res in response.entries:
        result_path = res.result_path
        print(result_path)
        if result_path:
            fname = os.path.basename(result_path)
            local_result_path = os.path.join(
                "test-data", os.path.relpath(result_path, "/data")
            )
            print(local_result_path)
            img_path = os.path.join("test-data", fname.split(".")[0] + ".tif")
            output_path = os.path.join("test-data", fname.split(".")[0] + ".png")
            visualize_annotations(img_path, local_result_path, output_path)
