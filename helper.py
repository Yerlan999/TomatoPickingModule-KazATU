import cv2
from time import sleep


cam = cv2.VideoCapture(1)

if cam.isOpened():
    print("Camera opened")
    ret, image = cam.read()
    if ret:
        cv2.imwrite('testimage.jpg', image)
    else:
        print("Nothing found in a frame")
else:
    print("Camera not opened")
cam.release()




