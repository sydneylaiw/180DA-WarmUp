'''
Section 6: Camera exercises

References:
OpenCV color filtering:
https://medium.com/featurepreneur/colour-filtering-and-colour-pop-effects-using-opencv-python-3ce7d4576140
https://ckyrkou.medium.com/color-thresholding-in-opencv-91049607b06d

Video capture:
https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_gui/py_video_display/py_video_display.html

Bounding box:
https://docs.opencv.org/4.4.0/d3/dc0/group__imgproc__shape.html#gadf1ad6a0b82947fa1fe3c3d497f260e0

Finding dominant color in image:
https://code.likeagirl.io/finding-dominant-colour-on-an-image-b4e075f98097
https://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html
'''

import argparse
import numpy as np
import cv2 as cv
from collections import Counter
from sklearn.cluster import KMeans

# only used blue for laboratory assignment
def get_bounds(color_scheme):
    if color_scheme == 'hsv':
        lower_bounds = np.array([110, 50, 50], np.uint8)
        upper_bounds = np.array([130, 255, 255], np.uint8)
    else:
        # ucla blue rgb approx: (45,104,96), (39, 116, 174)
        lower_bounds = np.array([30, 80, 80], np.uint8)
        upper_bounds = np.array([60, 120, 190], np.uint8)
    return lower_bounds, upper_bounds

# get range in cluster (assume hsv)
def get_range(reshaped_frame, cluster_labels, max_cluster):
    lower_bounds = np.array([180, 255, 255], np.uint8)
    upper_bounds = np.array([0, 0, 0], np.uint8)
    print(lower_bounds, upper_bounds)
    for i in range(len(reshaped_frame)):
        label = cluster_labels[i]
        if label == max_cluster:
            for j in range(3):
                if reshaped_frame[i][j] < lower_bounds[j]:
                    lower_bounds[j] = reshaped_frame[i][j]
                if reshaped_frame[i][j] > upper_bounds[j]:
                    upper_bounds[j] = reshaped_frame[i][j]
    return lower_bounds, upper_bounds

def get_bounds_kmeans(frame):
    # reshape for correct k-means dimensions
    reshaped_frame = frame.reshape((frame.shape[0] * frame.shape[1], 3))
    clusters = KMeans(n_clusters=10).fit(reshaped_frame)
    # get max-frequency cluster
    cluster_cnt = Counter(clusters.labels_)
    max_cluster = cluster_cnt.most_common(1)[0][0]
    # get hsv bounds from cluster
    lower_bounds, upper_bounds = get_range(reshaped_frame, clusters.labels_, max_cluster)
    return lower_bounds, upper_bounds
    

def get_mask(frame, k_means, color_scheme):
    if not k_means:
        lower_bounds, upper_bounds = get_bounds(color_scheme)
    else:
        lower_bounds, upper_bounds = get_bounds_kmeans(frame)
    return cv.inRange(frame, lower_bounds, upper_bounds)

def convert_color_scheme(frame, color_scheme):
    if color_scheme == 'hsv':
        return cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    elif color_scheme == 'rgb':
        return cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    else:
        return frame

if __name__ == '__main__':

    # usage: python3 camera_exercises.py -c [hsv|rgb|bgr] --kmeans
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--color_scheme', type=str, default='bgr')
    parser.add_argument('--kmeans', dest='kmeans', action='store_true')
    args = parser.parse_args()
    color_scheme = args.color_scheme
    k_means = args.kmeans
    if k_means is None:
        k_means = False

    # capture video stream
    capture = cv.VideoCapture(0)
    
    while True:
        ret, frame = capture.read()
        # frame not read
        if not ret:
            break
        
        frame = convert_color_scheme(frame, color_scheme)

        mask = get_mask(frame, k_means, color_scheme)

        contours, _ = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
        if contours is not None and len(contours) > 0:
            # get largest contour by area
            largest_contour = max(contours, key=cv.contourArea)
            # print(largest_contour)
            # draw rectangle enclosing object
            x, y, w, h = cv.boundingRect(largest_contour)
            cv.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

        # display frame
        cv.imshow('frame', frame)
        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    capture.release()
    cv.destroyAllWindows()
