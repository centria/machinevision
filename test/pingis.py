import cv2
from time import sleep
import numpy as np

# x1 = 0
# y1 = 0

# def mouse_callback(event, x, y, flags, param):
#     if event == cv2.EVENT_LBUTTONDOWN:
#         global x1, y1
#         x1 = x
#         y1 = y

# image = cv2.imread("/home/centria/projects/machinevision/test.png")

# while True:
#     cv2.putText(image, f"({x1}, {y1})", (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
#     #cv2.putText(image, "testi", (x1,y1), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
#     cv2.imshow('image', image)
#     cv2.setMouseCallback('image', mouse_callback)
#     if cv2.waitKey(1) == ord('q'):
#         break

# cv2.destroyAllWindows()
#############################################################
# Open the default camera
#cap = cv2.VideoCapture(0)
cap = cv2.VideoCapture("/home/centria/projects/machinevision/short_pingis_ball.mp4")



if not cap.isOpened():
    print("Cannot open camera")
    exit()
while True:
    
    sleep(0.1)
    # Capture frame-by-frame
    ret, frame = cap.read()
 
    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    #cv2.imshow('hsv', hsv)

    lower_orange = np.array([5, 150, 150])
    upper_orange = np.array([15, 255, 255])

    # # Luo maski oranssille värille
    mask = cv2.inRange(hsv, lower_orange, upper_orange)
    cv2.imshow('mask', mask)
    result = cv2.bitwise_and(frame, frame, mask=mask)

    # # Näytä alkuperäinen kuva ja tulos
    # cv2.imshow('frame', frame)
    cv2.imshow('result', result)


    if cv2.waitKey(1) == ord('q'):
        break
    elif cv2.waitKey(1) == ord('s'):
        cv2.imwrite("/home/centria/projects/machinevision/test.png", frame)
 
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()