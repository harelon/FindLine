import cv2
import numpy as np
import sys
import argparse

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
        if cv2.contourArea(box) <= 200 or cv2.contourArea(contour)==0 :
            continue
        if cv2.contourArea(box) / cv2.contourArea(contour) < minDiffer:
            minDiffer =  cv2.contourArea(box) / cv2.contourArea(contour)
            cont = contour
            cont_area = cv2.contourArea(contour)
    output = cv2.drawContours(img_color, cont, -1, (0, 0, 255), 4) 
    cv2.imshow("output" + str(counter), output)
    counter=counter+1
    return (cont, cont_area, is_single)

parser = argparse.ArgumentParser(
        description='An image white line will be detected in')
parser.add_argument(
        'image',
        help='the path of the image'
    )
args = parser.parse_args()
image = cv2.imread(args.image)
cv2.imshow("base image", image)

image = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
cv2.imshow("grayscale image", image)

image_half_y = int(image.shape[0] / 2)
roi = image[image_half_y:image.shape[0], 0:image.shape[1]]
ret, roi = cv2.threshold(roi, 200, 255, cv2.THRESH_BINARY)
cv2.imshow("lower half after threshold", roi)

kernel = np.ones((5, 5), np.uint8)
roi_morphed = cv2.erode(roi, kernel, iterations = 1)
roi_morphed = cv2.dilate(roi_morphed, kernel, iterations = 1)
cv2.imshow("lower half after threshold and 3 erodes 1 dilate", roi_morphed)

roi_morphed_result = best_contour(roi_morphed)
img_color = cv2.cvtColor(roi_morphed,cv2.COLOR_GRAY2BGR)
try:
    output = cv2.drawContours(img_color,[roi_morphed_result[0]],-1,(0,0,255),4)
except:
    output=roi
    pass
cv2.imshow("output", output)
cv2.waitKey(0)
cv2.destroyAllWindows()
