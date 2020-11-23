import cv2 as cv
import numpy as np
import os
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'
Images = []
ID_img = []
Spc = []
Spc_ID = []
for filename in os.listdir("image"):
    img = cv.imread(os.path.join("image", filename))
    if img is not None:
        Images.append(img)
        ID_img.append(filename[22:-4])
def Check(img,ID, sobel):
    Sus = []
    dem = 0

    dem = 0
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    if sobel == 'X':
        gray = cv.GaussianBlur(gray, (5,5), 0)
        sobelX = cv.Sobel(gray, cv.CV_8U, 1, 0, ksize= 3)
        ret, thresh = cv.threshold(sobelX, 110, 255, cv.THRESH_BINARY)
    if sobel == 'Y':
        sobelX = cv.Sobel(gray, cv.CV_8U, 0, 1, ksize=1)
        ret, thresh = cv.threshold(sobelX, 70, 255, cv.THRESH_BINARY)
    close_img = cv.morphologyEx(thresh, cv.MORPH_CLOSE, np.ones((5, 19)))
    contours, hiearchy = cv.findContours(close_img, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    for cnt in contours:

        x,y,w,h = cv.boundingRect(cnt)
        if(w*h >1500 and w*h <6500 and w> 2*h and w<5.25*h and x > 5 and y>5 and w > 80):
            # Điều kiện x, y để ngăn việc phải raise exception khi crop mà tọa độ âm
            crop = img[y-5:y+h+5,x-5:x+w+5]

            Sus.append(crop)
    if len(Sus) == 1:
        cv.imwrite(os.path.join("Save", ID + ".jpg"), Sus[0])
        dem  += 1
    if len(Sus) > 1:
        for check_crop in Sus:
            if CheckStr(check_crop) == True:
                cv.imwrite(os.path.join("Save", ID + ".jpg" ),check_crop)
                dem +=1
    if len(Sus) == 0 or dem == 0:
        Spc.append(img)
        Spc_ID.append(ID)


def CheckStr(img):

    img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    img = cv.equalizeHist(img)

    img = cv.Sobel(img, cv.CV_8U, 1, 0, ksize = 3)

    image_to_text = pytesseract.image_to_string(img, lang='eng')

    if len(image_to_text) >3:
        return True
    return False
for i in range(len(Images)):
    Check(Images[i], ID_img[i], 'X')
print(len(Spc))
print(Spc_ID)
if len(Spc) != 0:
    for i in range(len(Spc)):
        Check(Spc[i], Spc_ID[i], 'Y')
cv.waitKey(0)