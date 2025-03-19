import cv2
import time
import numpy as np

stitcher = cv2.Stitcher.create(cv2.Stitcher_PANORAMA)
stitcher.setCompositingResol(1.0)

cap1 = cv2.VideoCapture(2)
cap2 = None
if cap1.isOpened():
     time.sleep(2)
     cap2 = cv2.VideoCapture(0)


if cap1.isOpened() and cap2 != None and cap2.isOpened():   
    cap1.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)  
    cap1.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080) 
    cap2.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)  
    cap2.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080) 
    while True:
        ret1, frame1 = cap1.read()
        
        if ret1:
            ret2, frame2 = cap2.read()
            if ret2:
                if cv2.waitKey(1) == ord('q'):
                    break
                half_size_frame1 = cv2.resize(frame1, (0, 0), fx=0.5, fy=0.5)
                half_size_frame2 = cv2.resize(frame2, (0, 0), fx=0.5, fy=0.5)
                cv2.imshow('frame1', half_size_frame1)
                cv2.imshow("frame2", half_size_frame2)
                (status, panorama) = stitcher.stitch([frame1, frame2])

                if status == cv2.Stitcher_OK:
                    # # Määritä yhdistetyn kuvan koko
                    # height, width = panorama.shape[:2]
                    
                    # # Luo tyhjä kuva, jossa on kolme osaa
                    # final_panorama = np.zeros((height, width, 3), dtype=np.uint8)
                    
                    # # Kopioi vasemman kameran kuva
                    # final_panorama[:, :frame1.shape[1]] = frame1
                    
                    # # Kopioi yhteinen alue
                    # common_area_width = width - frame1.shape[1] - frame2.shape[1]
                    # final_panorama[:, frame1.shape[1]:frame1.shape[1] + common_area_width] = panorama[:, frame1.shape[1]:frame1.shape[1] + common_area_width]
                    
                    # # Kopioi oikean kameran kuva
                    # final_panorama[:, -frame2.shape[1]:] = frame2
                    
                    # #cv2.imwrite("final_panorama.jpg", final_panorama)
                    # cv2.imshow('final_panorama', final_panorama)
                    # print("Panorama yhdistetty onnistuneesti!")



                    half_size_panorama = cv2.resize(panorama, (0, 0), fx=0.5, fy=0.5)
                    cv2.imshow('half_size_panorama', half_size_panorama)
                else:
                    print('Kuvien yhdistäminen epäonnistui')
            else:
                print("Can't receive frame2. Exiting ...")
                break
        else:
                print("Can't receive frame1. Exiting ...")
                break        
    cap1.release()
    cap2.release()
    cv2.destroyAllWindows()
else:
    print("Cannot open cameras")
    exit()