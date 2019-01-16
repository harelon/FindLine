import cv2
import numpy as np

image = cv2.imread(".\output 23cm\d100ccd0lcr0.jpg")
cv2.imshow("base image", image)

image = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
cv2.imshow("grayscale image", image)

image_half_y = int(image.shape[0] / 2)
roi = image[image_half_y:image.shape[0], 0:image.shape[1]]
ret, roi = cv2.threshold(roi, 210, 255, cv2.THRESH_BINARY)
cv2.imshow("lower half after threshold", roi)

kernel = np.ones((5, 5), np.uint8)
roi = cv2.morphologyEx(roi, cv2.MORPH_CLOSE, kernel)
cv2.imshow("lower half after threshold and open", roi)

img, contours, hierarchy = cv2.findContours(roi, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
img_color = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
output = img_color
cont = None
minDiffer = 1000000
rects = None
for contour in contours:
    rect = cv2.minAreaRect(contour)
    box = cv2.boxPoints(rect)
    box = np.int0(box)
    print(box)
    if cv2.contourArea(box) == 0:
        continue
    if cv2.contourArea(box) - cv2.contourArea(contour) < minDiffer:
        minDiffer = cv2.contourArea(contour) -  cv2.contourArea(box)
        cont = contour
    # rects = cv2.drawContours(img_color, [box], -1, (0, 0, 255), 4)
print(minDiffer)
# cv2.imshow("rects", rects)
output = cv2.drawContours(img_color, cont, -1, (0, 0, 255), 4)   
cv2.imshow("output", output)

cv2.waitKey(0)
cv2.destroyAllWindows()
