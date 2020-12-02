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
        # Một filname có dạng "Screenshot 2020-11-13 105547.jpg", lấy [22:-4] để bỏ ".jpg" và "Screenshot 2020-11-13"
def Check(img,ID, sobel):
    Sus = []
    dem = 0

    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    if sobel == 'X':
        gray = cv.GaussianBlur(gray, (5,5), 0)
        sobelX = cv.Sobel(gray, cv.CV_8U, 1, 0, ksize= 3)
        ret, thresh = cv.threshold(sobelX, 110, 255, cv.THRESH_BINARY)
    if sobel == 'Y':
        sobelX = cv.Sobel(gray, cv.CV_8U, 0, 1, ksize=1)
        ret, thresh = cv.threshold(sobelX, 70, 255, cv.THRESH_BINARY)
    # Do những ảnh như 110119 hay 105547 có các đường biên dọc quá sáng và khá gần biển số nên lúc này cần phải sobel Y để tách các đường ấy ra khỏi biển số
    close_img = cv.morphologyEx(thresh, cv.MORPH_CLOSE, np.ones((5, 19)))
    contours, hiearchy = cv.findContours(close_img, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    for cnt in contours:

        x,y,w,h = cv.boundingRect(cnt)
        if(w*h >1500 and w*h <6500 and w> 2*h and w<5.25*h and x > 5 and y>5 and w > 80):
            #Ở đây e không muốn đặt điều kiện cho diện tích khoảng nghi vấn là biển số ta tìm được gần bằng với cv,ContourArea(cnt) vì yêu cầu là tìm khoanh vùng được biển số trong một tập ảnh
            #nhưng mà tập ảnh này có những chụp khác nhau nên khi em dùng cv.morphologyEx để close lại thì diện tích contour này sẽ rất nhỏ so vs khung mà ta nghi ngờ là biển số
            #file Case1.py sẽ hiển thị các biển số khi được close
            crop = img[y-5:y+h+5,x-5:x+w+5]
            #Crop khoảng với tọa đốj  hơn hình chữ nhật ta tim đc 5 pixellớn nên phải đặt điều kiện x,y phải lớn 5 để tránh trường hợp x, y về âm
            Sus.append(crop)

    #Sus là mảng chứa  các vùng mà ta nghi ngờ đó là biển số được crop lại
    if len(Sus) == 1:
        #Nếu mảng chứa các vùng nghi ngờ có 1 phần tử thì đó là biển số cần tìm

        cv.imwrite(os.path.join("Save", ID + ".jpg"), Sus[0])
        dem  += 1
    if len(Sus) > 1:
        #Nếu lớn hơn 1 lúc này e sử dụng pytest để kiểm tra chắc chắn xem cái nào chứa dãy kí tự thì đó là biển số. Trong quá trình làm thì e có sử dụng hiearchy nhưng mà nó khá bất cập vì cần xét nhiều điều kiện cấp với dãy số nằm trong khung hay không có đường kẻ khung ngoài biển số.
        for check_crop in Sus:
            if CheckStr(check_crop) == True:
                cv.imwrite(os.path.join("Save", ID + ".jpg" ),check_crop)
                dem +=1
    #dem để ảnh sau khi đi qua cả len > 1 và len = 1 mà chưa tìm được biển số đến bước này
    if len(Sus) == 0 or dem == 0:
        Spc.append(img)
        #ảnh chưa tìm được sẽ đc lưu vào mảng này
        Spc_ID.append(ID)


def CheckStr(img):

    img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    img = cv.equalizeHist(img)

    img = cv.Sobel(img, cv.CV_8U, 1, 0, ksize = 3)
    #Đây chỉ là mảng để kiểm tra đây có phải biển số không nên là em muốn lọc hết các trường hợp bằng cách loại bỏ hầu hết các trường hợp chẳng may có dãy kí tự
    #Bằng việc gray sau đó sobelX thì sobel X sẽ xóa các đường ngang khỏi ảnh lúc này mặc dù kí tự trong biển só khi đọc được sẽ khác nhưng mà vẫn là một chuỗi kí tự để em có thể xdd đây là biển số
    image_to_text = pytesseract.image_to_string(img, lang='eng')

    if len(image_to_text) >3:
        #Do khi pytes trả về chuỗi rỗng (chuỗi rỗng của pytes có dạng [F]  ) với len là 3 nên em chỉ cần tìm được một chuỗi có len lớn hơn 3 là được
        return True
    return False



#Phần chính
for i in range(len(Images)):
    Check(Images[i], ID_img[i], 'X')
if len(Spc) != 0:
    for i in range(len(Spc)):
        Check(Spc[i], Spc_ID[i], 'Y')
cv.waitKey(0)