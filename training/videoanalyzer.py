import cv2
import tkinter as tk
from tkinter import filedialog
#import threading
from PIL import Image, ImageTk
#from ultralytics import YOLO
import imageannotator


frameCount = 0
frameIndex = 0  
running = True
frame_label = None
videoFilename = ""
cap = None
frame = None
imageAnnotator = None



def open_file():
    global videoFilename
    videoFilename = ""
    videoFilename = filedialog.askopenfilename(
        title="Open video",
        filetypes=[("Video", "*.mp4"), ("All file types", "*.*")]
    )
    videoFilename_entry.delete(0, tk.END)
    videoFilename_entry.insert(0, videoFilename)

    open_video(videoFilename)
    set_current_frame_index(frameIndex)
    #if file_path:
    #    print(f"Valittu tiedosto: {file_path}")    

def annotate():
    global frame, imageAnnotator
    imageAnnotator = imageannotator.ImageAnnotator(root, frame)
    imageAnnotator.start()
 
def set_current_frame_index(val):  
    global frameIndex, cap, frame
    frameIndex = int(val)

    if( cap != None):
        cap.set(cv2.CAP_PROP_POS_FRAMES, frameIndex)
        ret, frame = cap.read()

        if ret:
            height, width, channels = frame.shape
            label_width = image_label.winfo_width()
            label_height = image_label.winfo_height()
            #self.label_centerX = int(image_label.winfo_x() + label_width / 2)
            #self.label_centerY = int(image_label.winfo_y() + label_height / 2)
            
            if label_width > 0 and label_height > 0 and (height > label_height or width > label_width):
                newWidth = label_width / width
                newHeight = label_height / height
                if(newHeight < newWidth):
                    imageHeight = int(newHeight * height)
                    imageWidth = int(newHeight * width)
                else:
                    imageHeight = int(newWidth * height)
                    imageWidth = int(newWidth * width)
                resizedframe = cv2.resize(frame, (imageWidth - 2, imageHeight - 2))
                print(f"width:{imageWidth} height:{imageHeight} lw:{label_width} lh:{label_height}") 

            
            resizedframe = cv2.cvtColor(resizedframe, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(resizedframe)
            imgtk = ImageTk.PhotoImage(image=img)

            image_label.imgtk = imgtk
            image_label.configure(image=imgtk)
        else:
            print("Can't receive frame (stream end?). Exiting ...")

def open_video(filename):
    global cap, slider
    if(cap != None):
        cap.release()
    cap = cv2.VideoCapture(filename)
    if cap.isOpened():
        frameCount = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) - 1
        slider.config(to=frameCount)
    else:
        print("Cannot open video")

        



root = tk.Tk()
root.title("Video analyzer")
root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}")

frameVideoFile = tk.Frame(root)
frameVideoFile.pack(pady=20)
    
open_button = tk.Button(frameVideoFile, text="Open Video", command=open_file)
open_button.pack(side=tk.LEFT, pady=20)

videoFilename_entry = tk.Entry(frameVideoFile, width=50)
videoFilename_entry.pack(side=tk.LEFT, padx=10)

image_label = tk.Label(root, text="Image", bg="lightblue")
image_label.pack(fill=tk.BOTH, expand=True)

frameVideoBrowser = tk.Frame(root)
frameVideoBrowser.pack(pady=20)

slider = tk.Scale(frameVideoBrowser, from_=0, to=frameCount, orient=tk.HORIZONTAL, command=set_current_frame_index)
slider.pack(side=tk.LEFT, pady=20)

annotate_button = tk.Button(frameVideoBrowser, text="Annotate", command=annotate)
annotate_button.pack(side=tk.LEFT, pady=20)

root.mainloop()

if(cap != None):
    cap.release()
    
cv2.destroyAllWindows()
print("Program ended")

