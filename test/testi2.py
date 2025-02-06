import cv2

# Open the default camera
cap = cv2.VideoCapture(0)
#cap = cv2.VideoCapture("/home/centria/projects/machinevision/test vid.mp4")



if not cap.isOpened():
    print("Cannot open camera")
    exit()
while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
 
    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    # Our operations on the frame come here
    #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Display the resulting frame
    #cv2.imshow('frame', gray)
    cv2.imshow("testi", frame);
    if cv2.waitKey(1) == ord('q'):
        break
 
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()