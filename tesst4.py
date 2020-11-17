import cv2 as cv
import os


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