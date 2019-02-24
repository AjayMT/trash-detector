
import os
import sys


TRASH = [
    'bottle',
    'cup',
    'fork',
    'knife',
    'spoon'
    'banana',
    'apple',
    'sandwich',
    'orange',
    'broccoli',
    'carrot',
    'hot dog',
    'pizza',
    'donut',
    'cake'
]


YOLO_PATH = os.path.join(sys.path[0], 'yc')
IMAGE_PATH = os.path.join(sys.path[0], 'input.jpg')
DEFAULT_CONFIDENCE = 0.5
DEFAULT_THRESHOLD = 0.3


import numpy as np
import argparse
import time
import cv2

from model_def import load_model
from keras import backend as K
import tensorflow as tf
import numpy as np
from keras.preprocessing.image import ImageDataGenerator, img_to_array, array_to_img, load_img
from slidingBox import boxCoordinates
from PIL import Image,ImageDraw



img_width, img_height = 256, 256

if K.image_data_format() == 'channels_first':
    input_shape = (3, img_width, img_height)
else:
    input_shape = (img_width, img_height, 3)

model = load_model(input_shape, "4.h5")
graph = tf.get_default_graph()


labelsPath = os.path.join(YOLO_PATH, 'coco.names')
LABELS = open(labelsPath).read().strip().splitlines()

# random list of colors for class labels
np.random.seed(42)
COLORS = np.random.randint(0, 255, size=(len(LABELS), 3), dtype='uint8')

weightsPath = os.path.join(YOLO_PATH, 'yolov3.weights')
configPath = os.path.join(YOLO_PATH, 'yolov3.cfg')

# load YOLO data
net = cv2.dnn.readNetFromDarknet(configPath, weightsPath)


def process_image(image):
    (H, W) = image.shape[:2]

    # determine only the *output* layer names that we need from YOLO
    ln = net.getLayerNames()
    ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]

    # construct blob from image
    blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (416, 416), swapRB=True, crop=False)
    net.setInput(blob)
    start = time.time()
    layerOutputs = net.forward(ln)
    end = time.time()

    # show timing information on YOLO
    print('took {:.6f} seconds'.format(end - start))

    boxes = []
    confidences = []
    classIDs = []

    for output in layerOutputs:
        for detection in output:
            # extract the class ID and confidence (i.e., probability) of
            # the current object detection
            scores = detection[5:]
            classID = np.argmax(scores)
            confidence = scores[classID]

            if confidence < DEFAULT_CONFIDENCE:
                continue

            # scale the bounding box coordinates back
            box = detection[0:4] * np.array([W, H, W, H])
            (centerX, centerY, width, height) = box.astype('int')
            x = int(centerX - (width / 2))
            y = int(centerY - (height / 2))
            boxes.append([x, y, int(width), int(height)])
            confidences.append(float(confidence))
            classIDs.append(classID)

    # apply non-maxima suppression to suppress weak, overlapping bounding
    # boxes
    idxs = cv2.dnn.NMSBoxes(boxes, confidences, DEFAULT_CONFIDENCE, DEFAULT_THRESHOLD)

    # ensure at least one detection exists
    if len(idxs) > 0:
        # loop over the indexes we are keeping
        for i in idxs.flatten():
            label = LABELS[classIDs[i]]
            if label not in TRASH:
                continue

            # extract the bounding box coordinates
            (x, y) = (boxes[i][0], boxes[i][1])
            (w, h) = (boxes[i][2], boxes[i][3])

            # draw a bounding box rectangle and label on the image
            color = [int(c) for c in COLORS[classIDs[i]]]
            cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)
            text = LABELS[classIDs[i]]
            cv2.putText(image, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX,
                        0.5, color, 2)

    return image


# Take a PIL image
def process_image_keras(image):
    width, height = image.size
    boxCoords = []
    boxSize = width / 5
    boxCoords = boxCoordinates(width, height, boxSize)
    subImageVals = []
    rectangleCoord = []
    for i in range(len(boxCoords)):
        boxX = boxCoords[i][0]
        boxY = boxCoords[i][1]
        subImage = image.crop((boxX,boxY ,boxX + boxSize, boxY + boxSize))
        subImage = subImage.resize((256, 256), Image.ANTIALIAS)

        foundTrash = process_subimage(subImage)
        if(foundTrash >= 0.92):
            # smallerSubImage = image.crop((boxCoords[i][0]+boxSize*0.15,boxCoords[i][1]+boxSize*0.15,boxCoords[i][0] + boxSize*0.85, boxCoords[i][1] + boxSize*0.85))
            # smallerSubImage = smallerSubImage.resize((256, 256), Image.ANTIALIAS)

            draw = ImageDraw.Draw(image)
            rectangleCoord.append((boxX,boxY))

            
            # val2 = process_subimage(smallerSubImage)
            # if (val2 >= 0.5):
            subImageVals.append((foundTrash,boxX,boxY))
    for j in range(len(rectangleCoord)):
        width = 3
        for k in range(width):
            draw.rectangle(((rectangleCoord[j][0] + k,rectangleCoord[j][1] + k), (rectangleCoord[j][0]+ boxSize - k, rectangleCoord[j][1] + boxSize-k)), outline = 'black')
    # open_cv_image = numpy.array(image) 
    # Convert RGB to BGR 
    # open_cv_image = open_cv_image[:, :, ::-1].copy() 
    image.show()
    return subImageVals

def process_subimage(image):
    with graph.as_default():
        x = img_to_array(image)  # this is a Numpy array with shape (3, 256, 256)
        x = x.reshape((1,) + x.shape)
        img_gen = ImageDataGenerator().flow(x)
        result = model.predict(x)
        # print(result)
        return result[0][0]






















