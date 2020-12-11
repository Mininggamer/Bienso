import cv2 as cv
from os import path, listdir
import numpy as np

temp = 0
Error = []
def CheckImg(img):
    Sus = []

    gray  = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    gray = cv.GaussianBlur(gray, (5, 5), 0)
    sobelX = cv.Sobel(gray, cv.CV_8U, 1, 0, ksize=3)
    ret, thresh = cv.threshold(sobelX, 127, 255, cv.THRESH_BINARY)
    close_img = cv.morphologyEx(thresh, cv.MORPH_CLOSE, np.ones((5, 21)))
    contours, hiearchy = cv.findContours(close_img, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        x,y,w,h = cv.boundingRect(cnt)
        if (w * h > 2000 and w * h < 6500 and w > 3 * h and w < 5.25 * h and x > 5 and y > 5 and w > 90 and h>15):
            crop = img[y - 5:y + h + 5, x - 5:x + w + 5]
            Sus.append(crop)
            #cv.rectangle(img, (x,y), (x+w,y+h), (0,0,255))
    if len(Sus) ==1:
        return (Sus[0], True)
    else:
        return (None, False)

for filename in listdir("image"):
    img = cv.imread(path.join("image",filename))
    if img is not None:
        s = CheckImg(img)
        if s[1] == True:
            cv.imwrite(path.join("Save", str(temp)+".jpg"),s[0])
            temp +=1
