import numpy as np
import cv2 as cv
import os

Images = []
ID_img = []
for filename in os.listdir("image"):
    img = cv.imread(os.path.join("image", filename))
    if img is not None:
        Images.append(img)
        ID_img.append(filename[22:-4])

def Check(img,ID):

    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    gray = cv.GaussianBlur(gray, (5,5), 0)
    sobelX = cv.Sobel(gray, cv.CV_8U, 1, 0, ksize= 3)
    ret, thresh = cv.threshold(sobelX, 110, 255, cv.THRESH_BINARY)

    close_img = cv.morphologyEx(thresh, cv.MORPH_CLOSE, np.ones((5, 19)))
    contours, hiearchy = cv.findContours(close_img, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    for cnt in contours:

        x,y,w,h = cv.boundingRect(cnt)
        if(w*h >1500 and w*h <6500 and w> 2*h and w<5.25*h and x > 5 and y>5 and w > 80):
            crop = img[y-5:y+h+5,x-5:x+w+5]
            cv.rectangle(close_img, (x,y), (x+w,y+h), (0,255,0))
    cv.imshow(ID, close_img)

for img in range(len(Images)):
    Check(Images[img], ID_img[img])

cv.waitKey(0)




