# DeployAI Object Detection

This repository contains a deep learning model for detecting objects from very high resolution optical remote sensing images using `YOLOv8 Oriented Bounding Box`.

## Key features

The model allows detecting the following objects

```python
{
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
```

## Input Format

The input image should be of size $1024\times1024\times3$, which means RGB images. The image extension can be `tif, png, and jpg`.

## Output Format

The output is a text file that contains one or multiple lines. Each line is associated with one detected object. A line starts with the object ID, the coordinates of the bounding box in as floats and the final float number is the confidence of the model for this detected object. The following is an example of an output file

```powershell
10 0.769302 0.0571918 0.771534 0.0672572 0.792736 0.0625548 0.790504 0.0524893 0.76106
10 0.616684 0.486967 0.617148 0.478474 0.597924 0.477423 0.59746 0.485916 0.750721
10 0.688043 0.250695 0.688133 0.239724 0.666332 0.239545 0.666242 0.250515 0.748338
10 0.791213 0.0233559 0.793775 0.0334864 0.814816 0.0281648 0.812254 0.0180343 0.742376
10 0.920348 0.259305 0.921118 0.250443 0.899601 0.248574 0.898831 0.257436 0.741958
10 0.587494 0.0695165 0.589827 0.0792789 0.611123 0.0741892 0.60879 0.0644268 0.740567
10 0.389937 0.87311 0.402007 0.87338 0.402523 0.850284 0.390453 0.850015 0.734022
10 0.660951 0.249243 0.661426 0.238898 0.639115 0.237874 0.63864 0.248219 0.729625
10 0.756774 0.252888 0.75691 0.243747 0.735853 0.243432 0.735717 0.252574 0.727624
10 0.779803 0.25355 0.780564 0.244453 0.761168 0.242829 0.760406 0.251926 0.727543
10 0.839222 0.49564 0.839412 0.486096 0.820622 0.485721 0.820432 0.495266 0.724032
10 0.818512 0.0460792 0.821328 0.0566282 0.843585 0.0506866 0.840769 0.0401376 0.718547
10 0.794084 0.0536486 0.796465 0.06351 0.816973 0.0585586 0.814592 0.0486972 0.71648
10 0.410527 0.990634 0.421791 0.991873 0.424142 0.970501 0.412879 0.969262 0.716345
10 0.949887 0.153857 0.960255 0.154084 0.960727 0.132494 0.950359 0.132267 0.712833
10 0.731965 0.251506 0.732028 0.240369 0.70949 0.24024 0.709427 0.251378 0.695606
10 0.952913 0.118352 0.962452 0.11878 0.963257 0.100856 0.953718 0.100428 0.690941
10 0.930095 0.630377 0.942441 0.630199 0.942102 0.60675 0.929756 0.606928 0.680457
10 0.899142 0.52734 0.899547 0.515103 0.87483 0.514285 0.874425 0.526521 0.679904
10 0.748125 0.0643654 0.750111 0.0733148 0.768692 0.0691932 0.766707 0.0602438 0.679206
10 0.542528 0.72823 0.542866 0.719201 0.522363 0.718433 0.522024 0.727462 0.671653
10 0.542875 0.09504 0.545214 0.104361 0.56727 0.0988264 0.564931 0.0895057 0.670565
10 0.514469 0.241546 0.514625 0.231891 0.495045 0.231573 0.494888 0.241228 0.659224
10 0.411977 0.107108 0.421696 0.10315 0.412963 0.0817091 0.403245 0.0856669 0.658168
10 0.688186 0.047754 0.690909 0.0580302 0.711969 0.0524495 0.709246 0.0421734 0.652222
10 0.815344 0.496517 0.815647 0.484862 0.79277 0.484267 0.792467 0.495922 0.646563
10 0.402369 0.158664 0.413241 0.155916 0.407498 0.13319 0.396626 0.135938 0.640109
10 0.410532 0.235188 0.421777 0.234454 0.420403 0.213409 0.409158 0.214143 0.638257
10 0.575733 0.247085 0.576258 0.23622 0.554647 0.235175 0.554121 0.24604 0.629506
10 0.690261 0.241132 0.690296 0.24971 0.704803 0.249651 0.704768 0.241073 0.629367
10 0.42136 0.810876 0.432653 0.811612 0.43393 0.792007 0.422638 0.791271 0.623552
10 0.896587 0.25795 0.896931 0.247696 0.875841 0.246989 0.875497 0.257243 0.620359
10 0.665811 0.0532124 0.668573 0.0631043 0.688284 0.0576016 0.685522 0.0477097 0.606935
10 0.491674 0.240513 0.491788 0.230942 0.471246 0.230698 0.471133 0.240269 0.589916
10 0.846418 0.256734 0.846858 0.245675 0.824892 0.244802 0.824452 0.25586 0.586082
10 0.880364 0.497953 0.880778 0.486231 0.857944 0.485425 0.85753 0.497147 0.584526
10 0.865397 0.0376271 0.867868 0.0468694 0.888878 0.0412524 0.886407 0.03201 0.576995
10 0.424943 0.584658 0.435262 0.585262 0.436446 0.565055 0.426127 0.564451 0.576027
10 0.533221 0.486 0.533473 0.477197 0.514317 0.476649 0.514066 0.485453 0.57352
10 0.717181 0.0691708 0.719289 0.0788939 0.745109 0.0732945 0.743 0.0635713 0.569721
10 0.9483 0.185812 0.959756 0.185702 0.959535 0.162561 0.94808 0.162671 0.562052
10 0.966552 0.483726 0.977363 0.483707 0.977327 0.462491 0.966516 0.46251 0.55568
10 0.928987 0.528518 0.929515 0.516924 0.906123 0.515859 0.905595 0.527453 0.555298
10 0.823349 0.256009 0.823735 0.245357 0.803351 0.244619 0.802965 0.255271 0.55416
10 0.868114 0.256894 0.868223 0.247538 0.849274 0.247317 0.849165 0.256673 0.550512
10 0.510295 0.481979 0.510747 0.471428 0.490472 0.470558 0.490019 0.481109 0.548859
10 0.522158 0.0857164 0.524665 0.095236 0.546002 0.0896183 0.543495 0.0800987 0.545464
10 0.132021 0.358989 0.143523 0.356336 0.138069 0.332698 0.126568 0.335351 0.537943
10 0.376703 0.0544178 0.385392 0.0520741 0.379585 0.030545 0.370896 0.0328887 0.531255
10 0.439166 0.0871696 0.448514 0.0869721 0.448134 0.0690157 0.438787 0.0692132 0.526881
10 0.945528 0.260469 0.945641 0.248959 0.923987 0.248747 0.923874 0.260257 0.525446
10 0.948854 0.236979 0.957606 0.236679 0.956944 0.217387 0.948191 0.217688 0.514772
10 0.799053 0.254669 0.800043 0.245094 0.784531 0.24349 0.783541 0.253065 0.510273
10 0.971243 0.459011 0.981005 0.459456 0.981929 0.439142 0.972167 0.438698 0.490019
10 0.434593 0.646896 0.445607 0.647584 0.447104 0.623616 0.436089 0.622928 0.489712
10 0.546778 0.247995 0.547957 0.237888 0.521758 0.234832 0.520579 0.244939 0.480963
10 0.435081 0.670829 0.445528 0.671212 0.44624 0.651811 0.435792 0.651427 0.477593
10 0.939566 0.423276 0.949077 0.42386 0.950287 0.404175 0.940777 0.40359 0.474118
10 0.372622 0.106577 0.382082 0.103421 0.375114 0.0825353 0.365654 0.0856915 0.472688
10 0.397381 0.257077 0.409946 0.256133 0.408309 0.234358 0.395744 0.235303 0.4562
10 0.637246 0.248056 0.63752 0.239333 0.621149 0.23882 0.620875 0.247542 0.393989
10 0.531447 0.489119 0.53177 0.479934 0.512711 0.479263 0.512387 0.488448 0.385059
10 0.939789 0.450982 0.951764 0.450924 0.951652 0.42739 0.939676 0.427447 0.373513
10 1.00037 0.530977 1.00117 0.521119 0.986989 0.519975 0.986194 0.529833 0.370596
10 0.336085 0.024257 0.339086 0.0326989 0.355896 0.0267217 0.352894 0.0182798 0.369308
10 0.401825 0.0185187 0.412382 0.013623 0.405082 -0.00211815 0.394525 0.00277759 0.368418
10 0.686198 0.0780266 0.689156 0.0869896 0.709658 0.0802245 0.7067 0.0712615 0.361413
9 0.211506 0.220896 0.227521 0.216149 0.212085 0.164066 0.196069 0.168813 0.356888
10 0.565684 0.105703 0.567619 0.11296 0.584769 0.108388 0.582834 0.101131 0.351471
9 0.570139 0.719797 0.570226 0.732347 0.604308 0.732111 0.604221 0.719561 0.327334
10 0.930733 0.603296 0.941956 0.603665 0.94258 0.584695 0.931358 0.584326 0.317335
10 0.283544 0.659585 0.294072 0.659736 0.294374 0.638583 0.283846 0.638433 0.301854
10 0.792477 0.0173265 0.800817 0.0147654 0.79538 -0.00294156 0.78704 -0.000380462 0.300901
10 0.808204 0.0153187 0.815899 0.0122031 0.809846 -0.00274596 0.802151 0.000369608 0.294774
10 0.890847 0.281562 0.891716 0.273191 0.875498 0.271507 0.874628 0.279878 0.283491
10 0.989942 0.247576 0.999541 0.251096 1.00361 0.240008 0.994008 0.236487 0.27634
```

> [!IMPORTANT]  
> If not objects are detected for an image, no output file is produced.

## Repository Content

```markdown
.
├── .github/
│ └── workflows/
│     └── build-test-image.yaml
├── README.md
├── Dockerfile
├── model.proto (Ptorobuf v3 specs)
├── requirements.txt
├── serve.py (gRPC service)
├── .gitignore
├── .dockerignore
├── .pylintrc
└── app/ (DL model)
    ├── init.py
    ├── config.py
    ├── utils.py
    ├── inference.py
    └── weights/
        └── best.pt
```

## Local Development

- In a terminal, clone the repository

```powershell
git clone https://github.com/AlbughdadiM/depai-yolov8-obb.git
```

- Go to the repository directory

```powershell
cd depai-yolov8-obb
```

- If the files `model.proto` and `model_pb2.py` are not there, generate them using

```powershell
python3.10 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. model.proto
```

- Build the docker image

```
docker build . -t object-detection:v0.1
```

- Create a container from the built image

```powershell
docker run --name=test -p 8061:8061 object-detection:v0.1
```

- Run the pytest

```powershell
pytest test_image_processor.py
```

## Container Registry

- Generate a personal access token: Github account settings > Developer settings > Personal access tokens (classic). Generate a token with the `read:package` scope.

- In a terminal, login to container registry using

```powershell
docker login ghcr.io -u USERNAME -p PAT 
```

- Pull the image
  
```powershell
docker pull ghcr.io/albughdadim/depai-yolov8-obb:v0.1
```

- Create a container

```powershell
docker run --name=test -p 8061:8061 ghcr.io/albughdadim/depai-yolov8-obb:v0.1
```

> [!WARNING]  
> The current implementation receives the input from S3 cloud storage and sends the output to S3 cloud storage. For input, this makes more sense to avoid sending large image (in bytes) to the service. This is also more adequate for cloud environments. This current implementation uses an EWC bucket. Please don't distribute this code to avoid exposing the credentials. This will be replaced from cloud resources of the DeployAI project.

## How TO Use Example

```python
import grpc
import model_pb2
import model_pb2_grpc


def run():
    channel = grpc.insecure_channel("localhost:8061")
    stub = model_pb2_grpc.ImageProcessorStub(channel)
    # As we can see, the model accepts multiple images in a list
    response = stub.ProcessImage(
        model_pb2.ImageRequest(  # pylint: disable=E1101
            input_s3_uris=[
                "s3://MoBucket/obj-det/patch_250.tif",
                "s3://MoBucket/obj-det/patch_420.tif",
            ]
        )
    )
    # There are two outputs, the URI, which is the location of the output on S3 and the URL, which is a signed URL to download the output directly without having access to the bucket
    print("Output S3 URI: " + response.output_s3_uri)
    print("Output S3 URL: " + response.output_s3_url)


if __name__ == "__main__":
    run()
```

The output file looks like this

```json
[
   {
      "image_uri":"s3://MoBucket/obj-det/patch_250.tif",
      "processed":true,
      "result_url":"https://object-store.os-api.cci1.ecmwf.int/MoBucket/df7bf521-6c7f-4d5d-9c53-ae1ee7d60dca/patch_250.txt?AWSAccessKeyId=e850aff0dd5749a0a8df9f909014049c&Signature=2Ipi65KTZN2ij7QTK1JRBlb0Ugc%3D&Expires=1718308170",
      "result_uri":"s3://MoBucket/df7bf521-6c7f-4d5d-9c53-ae1ee7d60dca/patch_250.txt"
   },
   {
      "image_uri":"s3://MoBucket/obj-det/patch_420.tif",
      "processed":true,
      "result_url":"https://object-store.os-api.cci1.ecmwf.int/MoBucket/df7bf521-6c7f-4d5d-9c53-ae1ee7d60dca/patch_420.txt?AWSAccessKeyId=e850aff0dd5749a0a8df9f909014049c&Signature=M2RHh4APNGS%2B7dj%2BltT8apgJDC0%3D&Expires=1718308171",
      "result_uri":"s3://MoBucket/df7bf521-6c7f-4d5d-9c53-ae1ee7d60dca/patch_420.txt"
   }
]
```

This is a list that has the same length of the input one. In each element of the list, there is a dictinary with three keys:

- `image_uri`: S3 location of the input image.
- `result_url`: Signed URL of the results of the input image.
- `result_uri`: S3 location of the results of the input image.
