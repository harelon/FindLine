import cv2
import numpy as np
import sys

counter = 0
def best_contour(image):
    global counter
    img, contours, hierarchy = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    img_color = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
    output = img_color
    cont = None
    minDiffer = sys.maxsize
    cont_area = 0
    is_single=False
    if len(contours)==1:
        is_single = True
    for contour in contours:
        rect = cv2.minAreaRect(contour)
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        if cv2.contourArea(box) == 0:
            continue
        if cv2.contourArea(box) - cv2.contourArea(contour) < minDiffer and cv2.contourArea(box) > 100 and len(contour)<20:
            minDiffer =  cv2.contourArea(box) - cv2.contourArea(contour)
            cont = contour
            cont_area = cv2.contourArea(contour)
    output = cv2.drawContours(img_color, cont, -1, (0, 0, 255), 4) 
    cv2.imshow("output" + str(counter), output)
    counter=counter+1
    return (cont, cont_area, is_single)

image = cv2.imread(".\output 13.5cm\d200ccd-10lcr0.jpg")
cv2.imshow("base image", image)

image = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
cv2.imshow("grayscale image", image)

image_half_y = int(image.shape[0] / 2)
roi = image[image_half_y:image.shape[0], 0:image.shape[1]]
ret, roi = cv2.threshold(roi, 210, 255, cv2.THRESH_BINARY)
cv2.imshow("lower half after threshold", roi)

kernel = np.ones((5, 5), np.uint8)
roi_opened = cv2.morphologyEx(roi, cv2.MORPH_OPEN, kernel)
cv2.imshow("lower half after threshold and open", roi_opened)

roi_closed = cv2.morphologyEx(roi, cv2.MORPH_CLOSE, kernel)
cv2.imshow("lower half after threshold and close", roi_closed)

opened_result = best_contour(roi_opened)
closed_result = best_contour(roi_closed)
output = None
try:
    if(opened_result[1]<closed_result[1] or closed_result[2]) and not opened_result[2]:        
        img_color = cv2.cvtColor(roi_closed,cv2.COLOR_GRAY2BGR)
        output = cv2.drawContours(img_color,[closed_result[0]],-1,(0,0,255),4)
    else:
        img_color = cv2.cvtColor(roi_opened,cv2.COLOR_GRAY2BGR)
        output = cv2.drawContours(img_color,[opened_result[0]],-1,(0,0,255),4)    
except:
    output=roi
    pass
cv2.imshow("output", output)
cv2.waitKey(0)
cv2.destroyAllWindows()
