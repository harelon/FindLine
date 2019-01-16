import cv2
import numpy as np
frame=None
def pick_color(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        pixel = frame[y,x]
        print(pixel)


cap=cv2.VideoCapture(1)
cv2.namedWindow("frame")
cv2.setMouseCallback("frame", pick_color)
while True:
    ret, frame=cap.read()
    cv2.imshow("frame", frame)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV_FULL)
    if cv2.waitKey(1)&0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
