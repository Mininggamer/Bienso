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


def Find(ts1,ts2,tsThresh, TupleClose, AreA,ts3, Blur_or_not, ArrayImg, ArrayID, ts4, ts5,SobelX,SobelY):
    Special = []
    Spc_ID = []

    for img in range(len(ArrayImg)):
        gray = cv.cvtColor(ArrayImg[img], cv.COLOR_BGR2GRAY)
        gray = cv.GaussianBlur(gray, (5, 5), 0)
        if(Blur_or_not == True):

            gray = cv.equalizeHist(gray)
        sobelX = cv.Sobel(gray, cv.CV_8U, SobelX, SobelY, ksize = 3)
        ret,thresh1 = cv.threshold(sobelX, tsThresh,255, cv.THRESH_BINARY)
        closeImg = cv.morphologyEx(thresh1, cv.MORPH_CLOSE, kernel= np.ones(TupleClose))
        copyImg = ArrayImg[img]


        contours, hiearchy = cv.findContours(closeImg, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        scale_height = 50  # Scale này để càng cao thì số dòng dọc xác định sẽ càng nhiều
        scale_long = 10
        k = int(ArrayImg[img].shape[1] / scale_long)
        v = ts2
        long = int(ArrayImg[img].shape[1] / scale_long)
        height = int(ArrayImg[img].shape[0] / scale_height)

        j = 0
        for i in contours:
            x,y,w,h = cv.boundingRect(i)

            if (w*h > AreA) and (w>=ts3*h and w<=7*h)and (cv.arcLength(i,True) >= ts5) and (2*(w+h) >= ts4):
                if (w*h >= cv.contourArea(i) - k) and (w*h <= cv.contourArea(i) +k):
                    if (cv.arcLength(i,True) <= (2*(w+h) + v)) and (cv.arcLength(i,True) > (2*(w+h) -v)):
                        #cv.rectangle(ArrayImg[img], (x,y),(x+w,y+h), (0,0,255), 3)
                        crop = copyImg[y-7:y+h+7,x-7:x+w+7]
                        j+=1

        if j == 1:
            cv.imwrite(os.path.join("Save", ArrayID[img] + " save.jpg"), crop)

            #cv.imwrite("Save" + Loaded_Img[img].name, CroppedImg[0])
        if(j >1 or j == 0):
            Special.append(ArrayImg[img])
            Spc_ID.append(ArrayID[img])

    return (Special,Spc_ID)
print(len(ID))
Error_Img, Error_ID = Find(2500, 20, 160, (5,25), 500, 3, False, images, ID,0, 200, 1,0)
if(len(Error_Img) >0):
    #Tuơng phản kém
    Error_Img, Error_ID = Find(3800, 25, 127,(7,19), 650, 2, True, Error_Img, Error_ID,0,200,1,0)
    #Biển số bị lệch(ảnh chụp chéo)
    Error_Img, Error_ID = Find(2800, 50, 127, (3, 25), 500, 2, False, Error_Img, Error_ID, 200,100,1,0)
    #hoa văn cạnh biển có quá nhiều trục dọc
    Error_Img, Error_ID = Find(3500, 50, 147, (7, 35), 700, 2, False, Error_Img, Error_ID, 300, 300,0,1)


for img in range(len(Error_Img)):
    cv.imwrite(os.path.join("Special", "Screenshot 2020-11-13 " + Error_ID[img] + ".jpg"), Error_Img[img])

print("ảnh chụp từ quá xa, biển số lẫn vào cảnh vật ko thể detect (xem trong thư mục Special))")

print(Error_ID)



#lấy số từ biển


