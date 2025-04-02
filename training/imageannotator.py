#https://www.youtube.com/watch?v=Bzv58L6xYGc
import cv2
import tkinter as tk
from tkinter import filedialog
#import threading
from PIL import Image, ImageTk
from ultralytics import YOLO
import dataset

class ImageAnnotator:
    def __init__(self, master, image):
        self.image = image
        self.resizedImage = None
        self.roiAreas = []
        self.mouse_over_roi = None
        self.mouse_clicked_roi = None
        self.label_centerX = -1
        self.label_centerY = -1

        self.root = tk.Toplevel(master)
        self.root.title("Image annotator")
        self.root.geometry(f"{self.root.winfo_screenwidth()}x{self.root.winfo_screenheight()}")

        self.frameAnnotation = tk.Frame(self.root)
        self.frameAnnotation.pack(pady=20)

        self.reload_button = tk.Button(self.frameAnnotation, text="Reload", command=self.show_image)
        self.reload_button.pack(side=tk.LEFT, pady=20)
        
        self.annotate_button = tk.Button(self.frameAnnotation, text="Find players", command=self.find_players)
        self.annotate_button.pack(side=tk.LEFT, pady=20)

        self.annotation_coordinates_entry = tk.Entry(self.frameAnnotation, width=50)
        self.annotation_coordinates_entry.pack(side=tk.LEFT, padx=10)

        self.image_label = tk.Label(self.root, text="Image", bg="red")
        self.image_label.pack(fill=tk.BOTH, expand=True)
        self.image_label.bind("<Motion>", self.mouse_over)
        self.image_label.bind("<Button-1>", self.mouse_click)

        self.root.after_idle(self.on_screen_ready)

        self.yolo = YOLO('yolov8s.pt')
        #self.yolo = YOLO('best.pt')

    def mouse_over(self, event):
        x = event.x
        y = event.y
        self.mouse_over_roi = None
        for roi_x1, roi_y1, roi_x2, roi_y2 in self.roiAreas:
            x1 = roi_x1 * self.resizeFactor
            y1 = roi_y1 * self.resizeFactor
            x2 = roi_x2 * self.resizeFactor
            y2 = roi_y2 * self.resizeFactor
            if(x >= x1 and x <= x2 and y >= y1 and y <= y2):
                self.mouse_over_roi = (roi_x1, roi_y1, roi_x2, roi_y2)                
                break
        self.show_image()
                

    def mouse_click(self, event):
        x = event.x
        y = event.y
        self.mouse_over_roi = None
        roiIndex = 0
        found = False
        for roi_x1, roi_y1, roi_x2, roi_y2 in self.roiAreas:
            x1 = roi_x1 * self.resizeFactor
            y1 = roi_y1 * self.resizeFactor
            x2 = roi_x2 * self.resizeFactor
            y2 = roi_y2 * self.resizeFactor
            if(x >= x1 and x <= x2 and y >= y1 and y <= y2):
                self.mouse_clicked_roi = (roi_x1, roi_y1, roi_x2, roi_y2)
                self.annotationCoordinates = self.createAnnotation(roiIndex)
                self.annotation_coordinates_entry.delete(0, tk.END)
                self.annotation_coordinates_entry.insert(0, self.annotationCoordinates) 

                self.dataset = dataset.Dataset(self.root, self.image,self.annotationCoordinates)                  
                self.dataset.start()       
                found = True
                break
            roiIndex = roiIndex + 1

        if(found == False):
            self.annotationCoordinates = ""
            self.annotation_coordinates_entry.delete(0, tk.END)
            self.annotation_coordinates_entry.insert(0, self.annotationCoordinates) 

            self.dataset = dataset.Dataset(self.root, self.image,self.annotationCoordinates)  
            self.dataset.start()

        self.show_image()
            
    def createAnnotation(self, roiIndex):
        annotation = ""
        x1, y1, x2, y2 = self.roiAreas[roiIndex]
        imageHeight, imageWidth, channels = self.image.shape

        centerX = ((x1 + x2) / 2) / imageWidth
        centerY = ((y1 + y2) / 2) / imageHeight
        width = abs(x2 - x1) / imageWidth
        height = abs(y2 - y1) / imageHeight
        annotation = "0 " + str(centerX) + " " + str(centerY) + " " + str(width) + " " + str(height)
        
        return annotation


    def on_screen_ready(self):
        self.root.update_idletasks()
        self.root.after(1000, self.resize_image)
        self.root.after(2000, self.show_image)

    def resize_image(self):
        self.resizedImage = None
        self.imageheight, self.imageWidth, channels = self.image.shape
        self.label_width = self.image_label.winfo_width()
        self.label_height = self.image_label.winfo_height()
        if(self.label_centerX < 0 and self.label_centerY < 0):
            self.label_centerX = int(self.image_label.winfo_x() + self.label_width  / 2)
            self.label_centerY = int(self.image_label.winfo_y() + self.label_height  / 2)
        
        if self.label_width  > 2 and self.label_height > 2 and (self.imageheight > self.label_height or self.imageWidth > self.label_width):
            widthFactor = self.label_width  / self.imageWidth
            heightFactor = self.label_height / self.imageheight
            if(heightFactor < widthFactor):
                imageHeight = int(heightFactor * self.imageheight)
                imageWidth = int(heightFactor * self.imageWidth)              
            else:
                imageHeight = int(widthFactor * self.imageheight)
                imageWidth = int(widthFactor * self.imageWidth)

            self.resizeFactor = (imageHeight / self.imageheight)
            
            new_x = int(self.label_centerX - imageWidth / 2)
            new_y = int(self.label_centerY - imageHeight / 2)
            self.image_label.place(x = new_x, y = new_y, width=imageWidth, height=imageHeight)
            #self.image_label.place(width=100, height=100)
            #self.yAnnotationFactor = (imageHeight - 2) / self.imageheight
            #self.xAnnotationFactor = (imageWidth - 2) / self.imageWidth
            self.resizedImage = cv2.resize(self.image, (imageWidth, imageHeight))
            self.root.mainloop()
            print(f"width:{imageWidth} height:{imageHeight} lw:{self.label_width} lh:{self.label_height}")
            #self.xFactor = int(abs(self.label_width - imageWidth)/2)
            #self.yFactor = int(abs(self.label_height - imageHeight)/2)

    def start(self):
        print("ImageAnnotator started")
        self.root.mainloop()

    def show_image(self):       
        if(self.resizedImage is not None):
            colorCorrectedImage = cv2.cvtColor(self.resizedImage, cv2.COLOR_BGR2RGB)

            for x1, y1, x2, y2 in self.roiAreas:
                x1 = int(x1 * self.resizeFactor)
                y1 = int(y1 * self.resizeFactor)
                x2 = int(x2 * self.resizeFactor)
                y2 = int(y2 * self.resizeFactor)
                
                colour = (255,0,0)
                cv2.rectangle(colorCorrectedImage, (x1, y1), (x2, y2), colour, 2)

            if(self.mouse_over_roi is not None):
                colour = (0,255,0)
                x1, y1, x2, y2 = self.mouse_over_roi
                x1 = int(x1 * self.resizeFactor)
                y1 = int(y1 * self.resizeFactor)
                x2 = int(x2 * self.resizeFactor)
                y2 = int(y2 * self.resizeFactor)

                cv2.rectangle(colorCorrectedImage, (x1, y1), (x2, y2), colour, 2)

            if(self.mouse_clicked_roi is not None):
                colour = (0,0,255)
                x1, y1, x2, y2 = self.mouse_clicked_roi
                x1 = int(x1 * self.resizeFactor)
                y1 = int(y1 * self.resizeFactor)
                x2 = int(x2 * self.resizeFactor)
                y2 = int(y2 * self.resizeFactor)
                cv2.rectangle(colorCorrectedImage, (x1, y1), (x2, y2), colour, 2)

            img = Image.fromarray(colorCorrectedImage)
            imgtk = ImageTk.PhotoImage(image=img)

            self.image_label.imgtk = imgtk
            self.image_label.configure(image=imgtk)

    def find_players(self):
        self.roiAreas.clear()
        results = self.yolo.track(self.image, stream=True)

        for result in results:
            classes_names = result.names

            for box in result.boxes:
                if box.conf[0] > 0.4 and int(box.cls[0]) == 0:
                    [x1, y1, x2, y2] = box.xyxy[0]
                    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                    self.roiAreas.append((x1,y1,x2,y2))
                    #cls = int(box.cls[0])
                    #class_name = classes_names[cls]
                    #colour = (255,0,0)
                    #cv2.rectangle(self.resizedImage, (x1, y1), (x2, y2), colour, 2)
                    #cv2.putText(self.resizedImage, f'{classes_names[int(box.cls[0])]} {box.conf[0]:.2f}', (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 1, colour, 2)

                    #colorCorrectedImage = cv2.cvtColor(self.resizedImage, cv2.COLOR_BGR2RGB)
                    #img = Image.fromarray(colorCorrectedImage)
                    #imgtk = ImageTk.PhotoImage(image=img)

                    #self.image_label.imgtk = imgtk
                    #self.image_label.configure(image=imgtk)
        self.show_image()


# yolo = YOLO('yolov8s.pt')

# image = None
# image_label = None


# def annotate_image(frame):
#     global image_label, image
#     image = frame

#     root = tk.Tk()
#     root.title("Image annotator")
#     root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}")

#     frameAnnotation = tk.Frame(root)
#     frameAnnotation.pack(pady=20)
        
#     open_button = tk.Button(frameAnnotation, text="Annotate")#, command=open_file)
#     open_button.pack(side=tk.LEFT, pady=20)

#     videoFilename_entry = tk.Entry(frameAnnotation, width=50)
#     videoFilename_entry.pack(side=tk.LEFT, padx=10)

#     image_label = tk.Label(root, text="Image", bg="red")
#     image_label.pack(fill=tk.BOTH, expand=True)

#     root.after_idle(on_screen_ready)

#     root.mainloop()

# def find_players(image):
#     global image_label
#     height, width, channels = image.shape
#     label_width = image_label.winfo_width()
#     label_height = image_label.winfo_height()
    
#     if label_width > 0 and label_height > 0 and (height > label_height or width > label_width):
#         newWidth = label_width / width
#         newHeight = label_height / height
#         if(newHeight < newWidth):
#             imageHeight = int(newHeight * height)
#             imageWidth = int(newHeight * width)
#         else:
#             imageHeight = int(newWidth * height)
#             imageWidth = int(newWidth * width)
#         resizedImage = cv2.resize(image, (imageWidth - 2, imageHeight - 2))
#         print(f"width:{imageWidth} height:{imageHeight} lw:{label_width} lh:{label_height}") 

    
#     resizedImage = cv2.cvtColor(resizedImage, cv2.COLOR_BGR2RGB)
#     img = Image.fromarray(resizedImage)
#     imgtk = ImageTk.PhotoImage(image=img)

#     image_label.imgtk = imgtk
#     image_label.configure(image=imgtk)

#     # results = yolo.track(resizedframe, stream=True)

#     # for result in results:
#     #     classes_names = result.names

#     #     for box in result.boxes:
#     #         if box.conf[0] > 0.4:
#     #             [x1, y1, x2, y2] = box.xyxy[0]
#     #             x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
#     #             cls = int(box.cls[0])
#     #             class_name = classes_names[cls]
#     #             colour = (255,0,0)
#     #             cv2.rectangle(resizedframe, (x1, y1), (x2, y2), colour, 2)
#     #             cv2.putText(resizedframe, f'{classes_names[int(box.cls[0])]} {box.conf[0]:.2f}', (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 1, colour, 2)
                
