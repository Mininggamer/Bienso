import cv2 as cv
import os
Bs = []
id = []
for filename in os.listdir("Save"):
    img = cv.imread(os.path.join("Save", filename))
    if img is not None:
        Bs.append(img)
        id.append(filename)
chiu_chiu = []


img = cv.imread(r'Save/110224 save.jpg')
#110109
img_cp = img.copy()

gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
gray = cv.GaussianBlur(gray, (5,5) , 0)
#gray = cv.equalizeHist(gray)
ret, gray = cv.threshold(gray, 200, 255, cv.THRESH_BINARY)
contours, hierachy = cv.findContours(gray, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
max = 0
for i in range(hierachy.shape[1]):
    leftmost = tuple(contours[i][contours[i][:, :, 0].argmin()][0])
    rightmost = tuple(contours[i][contours[i][:, :, 0].argmax()][0])
    a = rightmost[1] - leftmost[1]
    if (a > max):
        max = a
        b = i
    # if (hierachy[0, i][0] != -1 or (hierachy[0, i][3] == 0 and hierachy[0, i][0] == -1)):
    # cv.drawContours(img_cp, contours, i, (0, 255, 0))
print(hierachy)
print(b)
bien = hierachy[0, b][2]


while (bien != -1 ):

    cv.drawContours(img_cp, contours, bien, (0, 255, 0), 1)
    bien = hierachy[0, bien][0]

cv.drawContours(img_cp,contours, -1, (0,255,0))
cv.imshow('s',img_cp)
cv.waitKey(0)

