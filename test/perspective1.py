import cv2
import numpy as np

x1 = x2 = x3 = x4 = -1
y1 = y2 = y3 = y4 = -1
def mouse_click_handler(event, x, y, flags, param):
    global x1, x2, x3, x4, y1, y2, y3, y4

    if event == cv2.EVENT_LBUTTONUP:
        if(y4 != -1 and x4 != -1):
            x1 = x2 = x3 = x4 = -1
            y1 = y2 = y3 = y4 = -1  

        if(x1 == -1 and y2 == -1):
            x1 = x
            y1= y
        elif(y1 != -1 and x1 != -1 and y2 == -1 and x2 == -1):
            x2 = x
            y2= y
        elif(y2 != -1 and x2 != -1 and y3 == -1 and x3 == -1):
            x3 = x
            y3= y
        elif(y3 != -1 and x3 != -1 and y4 == -1 and x4 == -1):
            x4 = x
            y4= y


while True: 
    image = cv2.imread('perspective.png')

    if(x1 != -1 and y1 != -1 and x2 != -1 and y2 != -1 and x3 != -1 and y3 != -1 and x4 != -1 and y4 != -1):
        src_points = np.float32([[x1, y1], [x2, y2], [x4, y4], [x3, y3]])
        dst_points = np.float32([[0, 0], [300, 0], [0, 300], [300, 300]])
        matrix = cv2.getPerspectiveTransform(src_points, dst_points)

        result = cv2.warpPerspective(image, matrix, (300, 300))
        cv2.imshow('result', result)


    if(x1 != -1 and y1 != -1):
        cv2.circle(image, (x1, y1), 2, (0,255,0), thickness=2)  
    if(x2 != -1 and y2 != -1):
        cv2.circle(image, (x2, y2), 2, (255,0,0), thickness=2) 
    if(x3 != -1 and y3 != -1):
        cv2.circle(image, (x3, y3), 2, (0,0,255), thickness=2)   
    if(x4 != -1 and y4 != -1):
        cv2.circle(image, (x4, y4), 2, (255,255,255), thickness=2)           

    cv2.imshow('image', image)
    cv2.setMouseCallback('image', mouse_click_handler)

    if cv2.waitKey(1) == ord('q'):
        break

cv2.destroyAllWindows()
