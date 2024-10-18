import os
import grpc
import logging
from flask import Flask, render_template, request, redirect, session, url_for, flash
from model_pb2_grpc import ImageProcessorStub
from model_pb2 import ImageRequest  # pylint:disable=E0611
from visualize_annotations import visualize_on_map


data_dir = os.getenv("SHARED_FOLDER_PATH")
channel = grpc.insecure_channel("localhost:8061")
stub = ImageProcessorStub(channel)
app = Flask(__name__, static_folder="/data")
app.secret_key = "7038c774900b84f40f6cae8927187da2"
app.config["UPLOAD_FOLDER"] = os.path.join(data_dir, "uploads/")
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # Max file size: 16MB


os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

ALLOWED_EXTENSIONS = {"tif", "png", "jpg", "jpeg"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def index():
    map_path = session.get("map_path")  # Retrieve single map path from session
    return render_template("index.html", map_path=map_path)


@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        flash("No file part")
        return redirect(request.url)

    files = request.files.getlist("file")

    if not files:
        flash("No selected file")
        return redirect(request.url)
    file_paths = []

    for file in files:
        if file.filename == "":
            flash("No selected file")
            continue

        if allowed_file(file.filename):
            filename = file.filename
            file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(file_path)
            file_paths.append(file_path)
        else:
            flash(f"Invalid file type for {file.filename}", "error")

    if file_paths:
        try:
            response = process_images_via_grpc(
                file_paths
            )  # Send the list of file paths to gRPC service
            flash(
                f"Processing results: {response.entries}", "success"
            )  # Adjust according to your response structure
            # Generate maps based on the processing results
            list_img_paths = []  # Store paths of generated maps
            list_annotation_paths = []
            if response.entries:
                for result in response.entries:
                    img_path = result.image_path
                    annotation_path = result.result_path
                    if annotation_path is not None:
                        list_img_paths.append(img_path)
                        list_annotation_paths.append(annotation_path)
                output_map_path = os.path.join(
                    os.path.dirname(annotation_path), "map_viz.html"
                )
                logging.info(list_img_paths)
                logging.info(list_annotation_paths)
                visualize_on_map(list_img_paths, list_annotation_paths, output_map_path)
                # Provide the paths to the generated maps in the response
                flash("Processing complete. Check the generated maps.", "success")
                session["map_path"] = output_map_path
                return redirect(url_for("index"))
        except Exception as e:
            flash(f"Error during processing: {str(e)}", "error")
    return redirect(url_for("index"))


def process_images_via_grpc(image_path):
    req = ImageRequest(input_image_paths=image_path)
    response = stub.ProcessImage(req)
    return response


def app_run():
    app.run(host="0.0.0.0", port=8062, debug=False)
