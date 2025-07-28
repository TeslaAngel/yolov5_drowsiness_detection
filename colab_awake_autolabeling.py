# install autodistill
!pip install -q \
  autodistill \
  autodistill-grounded-sam \
  autodistill-yolov8 \
  roboflow \
  supervision==0.24.0

import os
HOME = os.getcwd()
print(HOME)

# NOW LABELING AWAKE IMAGES

# directory for "awake" images (#SUBJECT_TO_CHANGE)
IMAGE_DIR_PATH = f"{HOME}/DDD_dataset/NonDrowsy/images"
#!mkdir {HOME}/images
#IMAGE_DIR_PATH = f"{HOME}/images"

# clone github repo (including the dataset)
!git clone https://github.com/TeslaAngel/yolov5_drowsiness_detection.git

# display image sample
import supervision as sv

image_paths = sv.list_files_with_extensions(
    directory=IMAGE_DIR_PATH,
    extensions=["png", "jpg", "jpg"])

print('image count:', len(image_paths))

# autolabel the dataset
# define ontology
from autodistill.detection import CaptionOntology

ontology=CaptionOntology({
    "person": "awake",
    # "drowsy person": "drowsy"
})

# initiate dataset
DATASET_DIR_PATH = f"{HOME}/dataset"
#DATASET_DIR_PATH = f"{HOME}/DDD_dataset/NonDrowsy/images"

# initiate base model and autolabel
from autodistill_grounded_sam import GroundedSAM

base_model = GroundedSAM(ontology=ontology)
dataset = base_model.label(
    input_folder=IMAGE_DIR_PATH,
    extension=".png",
    output_folder=DATASET_DIR_PATH)

# display dataset sample
ANNOTATIONS_DIRECTORY_PATH = f"{HOME}/dataset/train/labels"
IMAGES_DIRECTORY_PATH = f"{HOME}/dataset/train/images"
DATA_YAML_PATH = f"{HOME}/dataset/data.yaml"

import supervision as sv

dataset = sv.DetectionDataset.from_yolo(
    images_directory_path=IMAGES_DIRECTORY_PATH,
    annotations_directory_path=ANNOTATIONS_DIRECTORY_PATH,
    data_yaml_path=DATA_YAML_PATH)

len(dataset)

import supervision as sv
from pathlib import Path

mask_annotator = sv.MaskAnnotator()
box_annotator = sv.BoxAnnotator()
label_annotator = sv.LabelAnnotator()

images = []
image_names = []
for i, (image_path, image, annotation) in enumerate(dataset):
    if i == SAMPLE_SIZE:
        break
    annotated_image = image.copy()
    annotated_image = mask_annotator.annotate(
        scene=annotated_image, detections=annotation)
    annotated_image = box_annotator.annotate(
        scene=annotated_image, detections=annotation)
    annotated_image = label_annotator.annotate(
        scene=annotated_image, detections=annotation)

    image_names.append(Path(image_path).name)
    images.append(annotated_image)

sv.plot_images_grid(
    images=images,
    titles=image_names,
    grid_size=SAMPLE_GRID_SIZE,
    size=SAMPLE_PLOT_SIZE)

# target training model
%cd {HOME}

from autodistill_yolov8 import YOLOv8

target_model = YOLOv8("yolov8n.pt")
target_model.train(DATA_YAML_PATH, epochs=50)

# Fix intermittent Colab bug. You may not need this.
# NotImplementedError: A UTF-8 locale is required. Got ANSI_X3.4-1968
import locale
locale.getpreferredencoding = lambda: "UTF-8"

!ls {HOME}/runs/detect/train/

# evaluate target model
# display confusion matrix
%cd {HOME}

from IPython.display import Image

Image(filename=f'{HOME}/runs/detect/train/confusion_matrix.png', width=600)

# display results
%cd {HOME}

from IPython.display import Image

Image(filename=f'{HOME}/runs/detect/train/results.png', width=600)

# display training samples
%cd {HOME}

from IPython.display import Image

Image(filename=f'{HOME}/runs/detect/train/val_batch0_pred.jpg', width=600)