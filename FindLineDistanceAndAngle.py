import cv2
import numpy as np
import sys
import argparse
import pickle
import math


PixToDegree = 12.07
counter = 0
def best_contour(image):
    global counter
    img, contours, _ = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    img_color = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
    output = img_color
    cont = None
    minDiffer = sys.maxsize
    cont_area = 0
    bestBox = None
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
            bestBox = box
    output = cv2.drawContours(img_color, cont, -1, (0, 0, 255), 4) 
    output = cv2.drawContours(img_color, [bestBox], -1, (0, 0, 255), 4) 
    cv2.imshow("output" + str(counter), output)
    counter=counter+1
    maxY = 0
    secondMaxY = 0
    for x, y in bestBox:
        if y > secondMaxY:
            if y >= maxY:
                maxY, secondMaxY = y, maxY            
            else:
                secondMaxY = y
    print(maxY)
    print(secondMaxY)
    print(42.8/math.tan(math.radians(((maxY + secondMaxY)/2)/PixToDegree)))
    print(bestBox)
    return (cont, cont_area)

parser = argparse.ArgumentParser(
        description='An image white line will be detected in')
parser.add_argument(
        'image',
        help='the path of the image'
    )
args = parser.parse_args()
image = cv2.imread(args.image)
objpoints =  pickle.load(open('objpoints.pkl', 'rb'))
imgpoints =  pickle.load(open('imgpoints.pkl', 'rb'))
ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, (640,480),None,None)
h,  w = image.shape[:2]
newcameramtx, roi=cv2.getOptimalNewCameraMatrix(mtx, dist, (w, h), 1, (w, h))

mapx,mapy = cv2.initUndistortRectifyMap(mtx,dist,None,newcameramtx,(w,h),5)
dst = cv2.remap(image, mapx, mapy, cv2.INTER_LINEAR)

# crop the image
x,y,w,h = roi
dst = dst[y:y+h, x:x+w]

image = dst
cv2.imshow("base image", image)

image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
cv2.imshow("grayscale image", image)

image_half_y = int(image.shape[0] / 2)
roi = image[image_half_y:image.shape[0], 0:image.shape[1]]
ret, roi = cv2.threshold(roi, 210, 255, cv2.THRESH_BINARY)
cv2.imshow("lower half after threshold", roi)

kernel = np.ones((5, 5), np.uint8)
roi_morphed = cv2.erode(roi, kernel, iterations = 1)
roi_morphed = cv2.dilate(roi_morphed, kernel, iterations= 1)
cv2.imshow("lower half after threshold and open", roi_morphed)

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
