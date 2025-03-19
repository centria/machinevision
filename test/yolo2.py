import cv2
from ultralytics import YOLO

yolo = YOLO('yolov8n.pt') #https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&ved=2ahUKEwjv9a-K7M-LAxUlExAIHarULt0QFnoECBEQAQ&url=https%3A%2F%2Fgithub.com%2Fultralytics%2Fassets%2Freleases%2Fdownload%2Fv8.1.0%2Fyolov8n.pt&usg=AOvVaw0xT1jI0XjDZI-PC-WWmzci&opi=89978449
# Open the default camera
#cap = cv2.VideoCapture(0)
cap = cv2.VideoCapture("/home/centria/projects/machinevision/test vid.mp4")


colour = (0,255,0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()
while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    results = yolo.track(frame, stream=True)


    for result in results:
        # get the classes names
        classes_names = result.names

        # iterate over each box
        for box in result.boxes:
            # check if confidence is greater than 40 percent
            if box.conf[0] > 0.3:
                # get coordinates
                [x1, y1, x2, y2] = box.xyxy[0]
                # convert to int
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

                # get the class
                cls = int(box.cls[0])

                # get the class name
                class_name = classes_names[cls]

                # get the respective colour
                

                # draw the rectangle
                cv2.rectangle(frame, (x1, y1), (x2, y2), colour, 2)

                # put the class name and confidence on the image
                cv2.putText(frame, f'{classes_names[int(box.cls[0])]} {box.conf[0]:.2f}', (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 1, colour, 2)
                

    cv2.imshow("testi", frame);
    if cv2.waitKey(1) == ord('q'):
        break
 
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()