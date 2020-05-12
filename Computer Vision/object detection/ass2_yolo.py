import numpy as np
import matplotlib.pyplot as plt
import cv2
import seaborn as sns
import imutils
import os, time, math, sys
from collections import deque, defaultdict
import argparse
from tqdm import tqdm
from SORT import Sort
from functools import partial


#cap = cv2.VideoCapture('Pedestrian.avi')
LABELS_PATH = './labels.txt'
MOVIE_PATH = './sequence'
# change path according to your OS
MOBILE_NET_SSD_PROTOTEXT_PATH = './mobilenet_ssd/MobileNetSSD_deploy.prototxt'
MOBILE_NET_SSD_MODEL_PATH = './mobilenet_ssd/MobileNetSSD_deploy.caffemodel'


############ IMPORTANT!! ############
# Before running get YOLOv3 files from here and put them in subdir /YOLOv3
# https://github.com/pjreddie/darknet/blob/master/data/coco.names
YOLOv3_CLASSES_PATH = './YOLOv3/coco.names'
# https://github.com/pjreddie/darknet/blob/master/cfg/yolov3.cfg
YOLOv3_MODEL_CONF_PATH = './YOLOv3/yolov3.cfg'
# https://pjreddie.com/media/files/yolov3.weights
YOLOv3_MODEL_WEIGHTS_PATH = './YOLOv3/yolov3.weights'


# read and get labels of pedestrian count
def get_labels(path):
	f = open(path, "r")
	labels = []
	for line in f:
		labels.append(int(line.split('\t')[1].rstrip('\n')))
	return labels


labels = get_labels(LABELS_PATH)


# read and return list of frames
def get_movie(movie_path):
    # reading file names
    frame_names = []
    for f in os.listdir(movie_path):
        if os.path.isfile(os.path.join(movie_path, f)):
            frame_names.append(f)

    # sort the frames_names so the appear
    # in the correct sequence
    frame_names = sorted(frame_names)

    # reading frames
    frames = []
    for f in range(len(frame_names)):
        frame_path = os.path.join(movie_path, frame_names[f])
        frames.append(cv2.imread(frame_path, 1))

    return frames

def show_movie(f, s=180):
    '''
    @param f: list of images
    @param s: time between frames in ms
    '''
    movie_length = len(f)
    for i in range(movie_length):
        frame_cpy = f[i].copy()
        cv2.putText(frame_cpy, f'Frame: {i+1}/{movie_length}', (10, f[0].shape[0]-10), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 0), 1)
        cv2.imshow('Pedestrian tracking movie (ESC to close)', frame_cpy)
        k = cv2.waitKey(s)
        if k == 27: # checking ESC has been pressed
            cv2.destroyAllWindows()
            break
    cv2.destroyAllWindows()

# make a video file from set of frames
def make_video_file(f, fps=10, video_name='video.avi'):
	height, width, layers = f[0].shape
	codec = cv2.VideoWriter_fourcc('M','J','P','G')
	video = cv2.VideoWriter(video_name, codec, fps, (width,height))
	for i in range(len(f)):
		video.write(f[i])
	cv2.destroyAllWindows()
	video.release()



# getting mean values for 3 channels of all frames
def mean_bgr_frames(f):
    avg_color = []
    for i in range(len(f)):
        avg_color_per_row = np.average(f[i], axis=0)
        avg_color_per_img = np.average(avg_color_per_row, axis=0)
        avg_color.append(avg_color_per_img)
    return np.average(avg_color, axis=0)

# getting std for 3 channels of all frames
def std_bgr_frames(f):
    std = []
    for i in range(len(f)):
        std_temp = []
        _, std_img = cv2.meanStdDev(f[i])
        std_temp.append(std_img[0][0]); std_temp.append(std_img[1][0]); std_temp.append(std_img[2][0])
        std.append(std_temp)
    return np.average(std, axis=0)


def detect_pedestrians(frames):
    new_frames = []
    frame1 = frames[0]
    # maxlen = 8 if more than 8 dissapear
    pts = deque(maxlen=8)
    ptss = []
    for i in range(0,10):
        ptss.append(deque(maxlen=8))
    print(ptss)
    # using for loop to make 10 people place
    # then calculate
    for i in range(1,len(frames)):
        frame2 = frames[i]
        diff = cv2.absdiff(frame1, frame2)
        gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
        dialated = cv2.dilate(thresh, None, iterations=3)
        # dialated from diff
        items = cv2.findContours(dialated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(items)
        contours = items[0] if len(items) == 2 else items[1]
        center = None

        count = 0
        for contour in contours:
            # draw rectangle
            (x, y, w, h) = cv2.boundingRect(contour)
            # caluculate area , size
            if cv2.contourArea(contour) < 700:
                continue
            cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # c = max(cnts, key=cv2.contourArea)
            # # Find the Center of a Blob (Centroid)
            # M = cv2.moments(c)
            center = (int((x + x + w) / 2.0), int((y + y + h) / 2.0))
            #center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
            # update the points queue
            ptss[count].appendleft(center)

            # loop over the set of tracked points
            for pts in ptss:
                for i in range(1, len(pts)):
                    # if either of the tracked points are None, ignore
                    # them
                    if pts[i - 1] is None or pts[i] is None:
                        continue
                    # otherwise, compute the thickness of the line and
                    # draw the connecting lines
                    thickness = int(np.sqrt(8 / float(i + 1)) * 2.0)
                    cv2.line(frame1, pts[i - 1], pts[i], (0, 0, 255), thickness)

            count += 1

        if(count >= 1):
            cv2.putText(frame1, "Status: {} Count: {}".format('Movement', count), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

        # c = max(cnts, key=cv2.contourArea)
        # # Find the Center of a Blob (Centroid)
        # M = cv2.moments(c)
        # center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        # # update the points queue
        # pts.appendleft(center)
        #
        # # loop over the set of tracked points
        # for i in range(1, len(pts)):
        #     # if either of the tracked points are None, ignore
        #     # them
        #     if pts[i - 1] is None or pts[i] is None:
        #         continue
        #     # otherwise, compute the thickness of the line and
        #     # draw the connecting lines
        #     thickness = int(np.sqrt(8 / float(i + 1)) * 2.0)
        #     cv2.line(frame1, pts[i - 1], pts[i], (0, 0, 255), thickness)

        new_frames.append(frame1)
        frame1 = frame2
    return new_frames


# Mobilenet SSD detector + Centriod tracker
def detect_mobilenet_ssd_centroid(frames, con=0.5):
    CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
               "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
               "featuredog", "horse", "motorbike", "person", "pottedplant", "sheep",
               "sofa", "train", "tvmonitor"]

    ct = CentroidTracker()
    t1 = time.perf_counter()

    # mean color
    avg_color = mean_bgr_frames(frames)
    # std color
    std_color = std_bgr_frames(frames)
    # scale parameter = 1/std
    scale_bgr = 1 / std_color

    processed_frames = []
    (h, w) = frames[0].shape[:2]

    net = cv2.dnn.readNetFromCaffe(MOBILE_NET_SSD_PROTOTEXT_PATH, MOBILE_NET_SSD_MODEL_PATH)
    # iterate over frames
    for i in range(len(frames)):
        image = frames[i].copy()
        # customised params
        #         blob = cv2.dnn.blobFromImage(image, scale_bgr[0], (w, h), (avg_color[2], avg_color[1], avg_color[0]))
        # default params
        blob = cv2.dnn.blobFromImage(image, 0.007843, (w, h), 127.5)
        net.setInput(blob)
        detections = net.forward()
        rects = []
        # iterate over detections
        for j in np.arange(0, detections.shape[2]):
            confidence = detections[0, 0, j, 2]
            if confidence > con:
                idx = int(detections[0, 0, j, 1])
                label = CLASSES[idx]
                if idx == 15:
                    box = detections[0, 0, j, 3:7] * np.array([w, h, w, h])
                    rects.append(box.astype("int"))
        #                     (startX, startY, endX, endY) = box.astype("int")

        objects = ct.update(rects)

        for (objectID, centroid) in objects.items():
            text = "ID {}".format(objectID)
            cv2.circle(image, (centroid[0], centroid[1]), 4, (0, 255, 0), -1)
            cv2.putText(image, text, (centroid[0] - 10, centroid[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0),
                        2)
        #             cv2.rectangle(image, (startX, startY), (endX, endY), (0, 255, 0), 2)
        #             cv2.putText(image, text, (startX, startY - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

        processed_frames.append(image)

    t2 = time.perf_counter()
    r_t = round(t2 - t1, 2)
    print(f'Running time of processing {len(frames)} frames with MobileNet SSD is {r_t} sec {round(len(frames) / r_t, 2)} fps')

    return processed_frames


# Get the names of the output layers
def getOutputsNames(net):
    # Get the names of all the layers in the network
    layersNames = net.getLayerNames()
    # Get the names of the output layers, i.e. the layers with unconnected outputs
    return [layersNames[i[0] - 1] for i in net.getUnconnectedOutLayers()]


# Remove the bounding boxes with low confidence using non-maxima suppression
def postprocess(frame, tracker, outs, confThreshold, nmsThreshold, classes, label_num, ptss):
    frameHeight = frame.shape[0]
    frameWidth = frame.shape[1]

    classIds = []
    confidences = []
    boxes = []
    # Scan through all the bounding boxes output from the network and keep only the
    # ones with high confidence scores. Assign the box's class label as the class with the highest score.
    classIds = []
    confidences = []
    boxes = []
    for out in outs:
        for detection in out:
            scores = detection[5:]
            classId = np.argmax(scores)
            if classes[classId] != "person":
                continue
            confidence = scores[classId]
            if confidence > confThreshold:
                center_x = int(detection[0] * frameWidth)
                center_y = int(detection[1] * frameHeight)
                width = int(detection[2] * frameWidth)
                height = int(detection[3] * frameHeight)
                left = int(center_x - width / 2)
                top = int(center_y - height / 2)
                classIds.append(classId)
                confidences.append(float(confidence))
                boxes.append([left, top, width, height])

    # Perform non maximum suppression to eliminate redundant overlapping boxes with
    # lower confidences.
    indices = cv2.dnn.NMSBoxes(boxes, confidences, confThreshold, nmsThreshold)
    rects = np.empty((0, 5))
    frame_detections = 0
    for i in indices:
        i = i[0]
        box = np.array((boxes[i][0], boxes[i][1], boxes[i][0] + boxes[i][2], boxes[i][1] + boxes[i][3]))
        box = box.astype("float32")
        box = np.append(box, confidences[i])
        rects = np.vstack((rects, box))
        frame_detections += 1;

    cv2.putText(frame, "Detections: {}".format(frame_detections), (frame.shape[1] - 120, frame.shape[0] - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 0), 2)
    cv2.putText(frame, "True count: {}".format(labels[label_num]), (frame.shape[1] - 120, frame.shape[0] - 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 0), 2)

    objects = tracker.update(rects)
    for d in objects:
        d = d.astype(np.int32)
        startX = d[0]
        startY = d[1]
        endX = d[2]
        endY = d[3]
        id = d[4]

        # d4b is ID
        text = "ID {}".format(d[4])
        cv2.putText(frame, text, (startX, startY - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 0, 255), 1)

        center = (int((startX + endX) / 2.0), int((startY + endY) / 2.0))

        # update the points queue
        ptss[id].appendleft(center)

        # loop over the set of tracked points
        for i in range(1, len(ptss[id])):
            # if either of the tracked points are None, ignore
            # them
            if ptss[id][i - 1] is None or ptss[id][i] is None:
                continue
            # otherwise, compute the thickness of the line and
            # draw the connecting lines
            thickness = int(np.sqrt(12 / float(i + 1)) * 2.0)
            cv2.line(frame, ptss[id][i - 1], ptss[id][i], (0, 0, 255), thickness)


def detect_yolov3_sort(frames):
    # Initialize the parameters
    confThreshold = 0.5  # Confidence threshold
    nmsThreshold = 1  # Non-maximum suppression threshold
    inpWidth = 608  # Width of network's input image
    inpHeight = 608  # Height of network's input image

    # tracker object
    tr = Sort()

    # Load names of classes
    classesFile = YOLOv3_CLASSES_PATH
    classes = None
    with open(classesFile, 'rt') as f:
        classes = f.read().rstrip('\n').split('\n')

    # Give the configuration and weight files for the model and load the network using them.
    modelConfiguration = YOLOv3_MODEL_CONF_PATH
    modelWeights = YOLOv3_MODEL_WEIGHTS_PATH
    net = cv2.dnn.readNetFromDarknet(modelConfiguration, modelWeights)
    # backends = (cv.dnn.DNN_BACKEND_DEFAULT, cv.dnn.DNN_BACKEND_HALIDE, cv.dnn.DNN_BACKEND_INFERENCE_ENGINE, cv.dnn.DNN_BACKEND_OPENCV)
    net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
    # targets = (cv.dnn.DNN_TARGET_CPU, cv.dnn.DNN_TARGET_OPENCL, cv.dnn.DNN_TARGET_OPENCL_FP16, cv.dnn.DNN_TARGET_MYRIAD)
    net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

    processed_frames = []
    t1 = time.perf_counter()
    ptss = defaultdict(partial(deque, maxlen=12))
    for i in tqdm(range(len(frames))):
        image = frames[i].copy()
        # Create a 4D blob from a frame.
        blob = cv2.dnn.blobFromImage(image, 1 / 255, (inpWidth, inpHeight), [0, 0, 0], 1, crop=False)
        # Sets the input to the network
        net.setInput(blob)
        # Runs the forward pass to get output of the output layers
        outs = net.forward(getOutputsNames(net))
        # Remove the bounding boxes with low confidence
        postprocess(image, tr, outs, confThreshold, nmsThreshold, classes, i, ptss)
        # Put efficiency information. The function getPerfProfile returns the
        # overall time for inference(t) and the timings for each of the layers(in layersTimes)
        t, _ = net.getPerfProfile()
        label = 'Inference time: %.2f ms' % (t * 1000.0 / cv2.getTickFrequency())
        cv2.putText(image, label, (0, 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255))
        processed_frames.append(image)

    t2 = time.perf_counter()
    r_t = round(t2 - t1, 2)
    print(f'Running time of processing {len(frames)} frames with YOLOv3 is {r_t} sec {round(len(frames) / r_t, 2)} fps')

    return processed_frames



def main():
    cap = get_movie(MOVIE_PATH)
    #frames = detect_pedestrians(cap)
    frames = detect_yolov3_sort(cap[0:100])
    #frames = detect_mobilenet_ssd_centroid(cap)
    #show_movie(frames)
    make_video_file(frames)
    cap.reverse()

if __name__ == '__main__':
    main()