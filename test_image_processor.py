import grpc
import pytest
import model_pb2
import model_pb2_grpc


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
    print("Output S3 URI: " + response.output_s3_uri)
