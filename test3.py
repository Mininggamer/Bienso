import cv2 as cv
import os
import numpy as np

Error_Img = []
Error_ID = []
ID = []

path = "image"
images = []

for filename in os.listdir(path):
    img = cv.imread(os.path.join(path, filename))
    if img is not None:
        ID.append(filename[22:-4])
        images.append(img)




def detect_frame_label(img):
    img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    smooth = cv.GaussianBlur(img_gray, (7, 7), 0)

    sobelx = cv.Sobel(smooth, cv.CV_8U, 1, 0, ksize=3)
    # thresh  =  cv.adaptiveThreshold ( sobelx , 255 , cv . ADAPTIVE_THRESH_GAUSSIAN_C ,cv.THRESH_BINARY_INV, 11 , 2 )
    ret, thresh = cv.threshold(sobelx, 127, 255, cv.THRESH_BINARY)
    horizal = thresh
    vertical = thresh

    scale_height = 50  # Scale này để càng cao thì số dòng dọc xác định sẽ càng nhiều
    scale_long = 10

    long = int(img.shape[1] / scale_long)
    height = int(img.shape[0] / scale_height)

    horizalStructure = cv.getStructuringElement(cv.MORPH_RECT, (long, 1))
    horizal = cv.erode(horizal, horizalStructure, (-1, -1))

    horizal = cv.dilate(horizal, horizalStructure, (-1, -1))

    verticalStructure = cv.getStructuringElement(cv.MORPH_RECT, (1, height))
    vertical = cv.erode(vertical, verticalStructure, (-1, -1))
    cv.imshow('img', thresh)
    vertical = cv.dilate(vertical, verticalStructure, (-1, -1))

    mask = horizal + vertical

    cv.imshow('oto.jpg', thresh)
    #     thresh_gray = cv.morphologyEx(mask, cv.MORPH_CLOSE, cv.getStructuringElement(cv.MORPH_ELLIPSE, (61,61)))

    # # kernel = np.ones((3,3),np.uint8)
    # # dilation = cv.dilate(thresh, kernel, iterations = 1)
    #     # cv.imshow('img',thresh_gray)
    contours, hierarchy = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

#     max = 0
#     for cnt in contours:
#         x, y, w, h = cv.boundingRect(cnt)
#         if cv.contourArea(cnt) > max:
#             x_max, y_max, w_max, h_max = x, y, w, h
#             max = cv.contourArea(cnt)
#     frame_label = img[y_max+10:y_max+h_max-10, x_max+10:x_max+w_max-10]
#     # _, thresh = cv.threshold(frame_label, 110, 255, cv.THRESH_BINARY_INV)
#     return frame_label

for i in images:
    detect_frame_label(i)
cv.waitKey(0)
