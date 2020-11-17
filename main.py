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
        k = ts1
        v = ts2
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

Bs = []
id = []
done = 0
for filename in os.listdir("Detected"):
    img = cv.imread(os.path.join("Detected", filename))
    if img is not None:
        Bs.append(img)
        id.append(filename)
chiu_chiu = []
for j in range(len(Bs)):
    #img = cv.imread(r'Save/110034 save.jpg')
    img = Bs[j]

    img_cp = img.copy()
    Count_Contour_drawn = 0
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    ret, thresh = cv.threshold(gray, 127, 255, cv.THRESH_BINARY)
    contours, hierachy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    max = 0
    for i in range(hierachy.shape[1]):
        leftmost = tuple(contours[i][contours[i][:, :, 0].argmin()][0])
        rightmost = tuple(contours[i][contours[i][:, :, 0].argmax()][0])
        a = rightmost[0] - leftmost[0]
        if (a > max):
            max = a
            b = i
        # if (hierachy[0, i][0] != -1 or (hierachy[0, i][3] == 0 and hierachy[0, i][0] == -1)):
        # cv.drawContours(img_cp, contours, i, (0, 255, 0))
    bien = hierachy[0, b][2]
    while (bien != -1):
        leftmost = tuple(contours[bien][contours[bien][:, :, 0].argmin()][0])
        rightmost = tuple(contours[bien][contours[bien][:, :, 0].argmax()][0])
        a = rightmost[0] - leftmost[0]

        if(cv.contourArea(contours[bien]) > 30 and a < 20):
            cv.drawContours(img_cp, contours, bien, (0, 255, 0), 1)
            Count_Contour_drawn+=1

        bien = hierachy[0, bien][0]
    chiu_chiu.append(img_cp)

    if(Count_Contour_drawn >= 7 ):
        cv.imwrite(os.path.join("Done", id[j] + ".jpg"),img_cp)
        print(id[j])
        done +=1
#cv.drawContours(img_cp, contours, 15, (0,255,0))
for k in range(len(chiu_chiu)):
    cv.imshow(id[k], chiu_chiu[k])
print(done)

cv.waitKey(0)

#lấy số từ biển


