import logging
import numpy as np
import rasterio
from rasterio.warp import calculate_default_transform, reproject, Resampling
from PIL import Image, ImageDraw
import folium
import os
from rasterio.io import MemoryFile

category_colors = {
    0: "red",  # plane
    1: "gray",  # ship
    2: "green",  # storage-tank
    3: "yellow",  # baseball-diamond
    4: "cyan",  # tennis-court
    5: "magenta",  # basketball-court
    6: "orange",  # ground-track-field
    7: "purple",  # harbor
    8: "pink",  # bridge
    9: "brown",  # large-vehicle
    10: "blue",  # small-vehicle
    11: "lime",  # helicopter
    12: "navy",  # roundabout
    13: "teal",  # soccer-ball-field
    14: "gold",  # swimming-pool
    15: "olive",  # container-crane
    16: "indigo",  # airport
    17: "black",  # helipad
}


def read_annotations(file_path):
    with open(file_path, "r") as file:
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


def read_image_bands_as_array(img_path, bands=[1, 2, 3]):
    with rasterio.open(img_path) as src:
        band_arrays = [src.read(band) for band in bands]
        stacked_array = np.stack(band_arrays, axis=-1)
        transform = src.transform
        crs = src.crs
    return stacked_array, transform, crs


def draw_annotations_on_image(image, annotations):
    img_pil = Image.fromarray(image)
    draw = ImageDraw.Draw(img_pil)

    for annotation in annotations:
        polygon = [
            (annotation["x1"], annotation["y1"]),
            (annotation["x2"], annotation["y2"]),
            (annotation["x3"], annotation["y3"]),
            (annotation["x4"], annotation["y4"]),
        ]

        category = int(annotation["category"])
        color = category_colors.get(category, "white")

        # Draw the polygon onto the image with the specific color
        draw.polygon(polygon, outline=color, width=3)

    return np.array(img_pil)


def reproject_annotated_image(src, annotated_image):
    dst_crs = "EPSG:4326"
    transform, width, height = calculate_default_transform(
        src.crs, dst_crs, src.width, src.height, *src.bounds
    )

    reprojected_image = np.empty(
        (height, width, annotated_image.shape[2]), dtype=annotated_image.dtype
    )

    # Create a memory file and write the annotated image to it
    with MemoryFile() as memfile:
        with memfile.open(
            driver="GTiff",
            height=annotated_image.shape[0],
            width=annotated_image.shape[1],
            count=annotated_image.shape[2],
            dtype="uint8",
            crs=src.crs,
            transform=src.transform,
        ) as dataset:
            for i in range(annotated_image.shape[2]):
                dataset.write(annotated_image[:, :, i], i + 1)

            for i in range(annotated_image.shape[2]):
                reproject(
                    source=dataset.read(i + 1),
                    destination=reprojected_image[:, :, i],
                    src_transform=dataset.transform,
                    src_crs=dataset.crs,
                    dst_transform=transform,
                    dst_crs=dst_crs,
                    resampling=Resampling.nearest,
                )

    return reprojected_image, transform


def calculate_map_center(bounds_list):
    min_lat = float("inf")
    min_lon = float("inf")
    max_lat = float("-inf")
    max_lon = float("-inf")
    for bounds in bounds_list:
        bottom_left = bounds[0]
        top_right = bounds[1]
        min_lat = min(min_lat, bottom_left[0])
        min_lon = min(min_lon, bottom_left[1])
        max_lat = max(max_lat, top_right[0])
        max_lon = max(max_lon, top_right[1])
    center_lat = (min_lat + max_lat) / 2
    center_lon = (min_lon + max_lon) / 2
    return center_lat, center_lon


def visualize_on_map(list_img_path, list_annotation_path, output_map_path):
    image_list = []
    bounds_list = []
    name_list = []
    for img_path, annotation_path in zip(list_img_path, list_annotation_path):
        with rasterio.open(img_path) as src:
            original_image, transform, crs = read_image_bands_as_array(img_path)
            annotations = read_annotations(annotation_path)
            annotated_image = draw_annotations_on_image(original_image, annotations)
            reprojected_image, transform = reproject_annotated_image(
                src, annotated_image
            )
            bounds = rasterio.transform.array_bounds(
                reprojected_image.shape[0], reprojected_image.shape[1], transform
            )
            logging.info(bounds)
            reprojected_image = reprojected_image / np.max(reprojected_image) * 5.5
            image_list.append(reprojected_image)
            bounds_list.append([[bounds[1], bounds[0]], [bounds[3], bounds[2]]])
            name_list.append(os.path.basename(img_path).split(".")[0])

    map_center = calculate_map_center(bounds_list)
    m = folium.Map(location=map_center, zoom_start=12)
    folium.TileLayer(
        tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
        attr="Esri",
        name="Esri Satellite",
        overlay=False,
        control=True,
    ).add_to(m)
    for img, bound, name in zip(image_list, bounds_list, name_list):
        folium.raster_layers.ImageOverlay(
            image=img,
            bounds=bound,
            opacity=1,
            name=name,
        ).add_to(m)
    folium.LayerControl().add_to(m)
    m.save(output_map_path)
