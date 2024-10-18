from concurrent import futures
import threading
import logging
import grpc
from upload import app_run
import model_pb2
import model_pb2_grpc
from app.inference import detect_yolov8_obb

logging.getLogger().setLevel(logging.INFO)


class ImageProcessorServicer(model_pb2_grpc.ImageProcessorServicer):
    def ProcessImage(self, request, context):
        print(request)
        input_image_path = request.input_image_paths
        result = self.run_model(input_image_path)
        return model_pb2.ImageResponse(entries=result)  # pylint: disable=E1101

    def run_model(self, input_image_path):
        # Pass the image path to your model inference function
        result = detect_yolov8_obb(input_image_path)
        return result


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    model_pb2_grpc.add_ImageProcessorServicer_to_server(
        ImageProcessorServicer(), server
    )
    server.add_insecure_port("[::]:8061")
    server.start()
    threading.Thread(target=app_run).start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
