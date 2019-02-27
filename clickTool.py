import cv2
import numpy as np
import sys
import os

def get_file_names(data_dir):
    file_names = [os.path.join(data_dir, f) for f in os.listdir(data_dir)]
    return file_names

def callBack(event, x, y, flags, userdata):
    if  ( event == cv2.EVENT_LBUTTONDOWN ):
        print("Left button of the mouse is clicked - position ( %i ,  %i )" %(x,y) )
        # centroids[0,0] = x
        # centroids[0,1] = y

        tips.append(x)
        tips.append(y)
        print("tips: ")
        print(tips)

        img[ y, x ] = [255, 0, 0]
        cv2.imshow(origNames[idx[i]], img)
        # cv2.waitKey(0)

dataset_path = raw_input("Input image dataset path: ")
im_paths = get_file_names(dataset_path)
im_names = os.listdir(dataset_path)
origNames = im_names[:]
# print("before: ")
# print(im_names)
idx = sorted(range(len(im_names)), key=lambda k: im_names[k])
im_names.sort()
# print("after: ")
# print(im_names)
# print("idx: ")
# print(idx)

num_of_data = len(im_paths)

tips = []

for i in range(num_of_data):
    img = cv2.imread(im_paths[idx[i]])

    cv2.namedWindow(origNames[idx[i]], cv2.WINDOW_NORMAL)
    cv2.resizeWindow(origNames[idx[i]], 1200,900)

    cv2.setMouseCallback(origNames[idx[i]], callBack)
    cv2.imshow(origNames[idx[i]], img)
    cv2.waitKey(0)
    cv2.destroyWindow(origNames[idx[i]])
