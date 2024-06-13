from concurrent import futures
import time
import logging
import grpc
import model_pb2
import model_pb2_grpc
from app.inference import detect_yolov8_obb

logging.getLogger().setLevel(logging.INFO)


class ImageProcessorServicer(model_pb2_grpc.ImageProcessorServicer):
    def ProcessImage(self, request, context):
        input_s3_uri = request.input_s3_uris
        output_s3_uri = self.run_model(input_s3_uri)
        return model_pb2.ImageResponse(  # pylint: disable=E1101
            output_s3_uri=output_s3_uri
        )

    def run_model(self, input_s3_uri):
        results = detect_yolov8_obb(input_s3_uri)
        return results


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    model_pb2_grpc.add_ImageProcessorServicer_to_server(
        ImageProcessorServicer(), server
    )
    server.add_insecure_port("[::]:8061")
    server.start()
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == "__main__":
    serve()
