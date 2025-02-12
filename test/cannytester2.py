import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
from time import sleep
import tkinter as tk
from tkinter import ttk
import threading

cap = cv.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()

stop_thread = False
def opencv_loop():
    global threshold1slider, threshold2slider, threshold1valuelabel, threshold2valuelabel, cap, stop_thread
    while not stop_thread:
        threshold1Value = threshold1slider.get()
        threshold2Value = threshold2slider.get()

        threshold1valuelabel['text'] = str(threshold1Value)
        threshold2valuelabel['text'] = str(threshold2Value)


        #frame = cv.imread('test1.png',0)
        ret, frame = cap.read() 
        # if frame is read correctly ret is True
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            stop_thread = True

        width = int(frame.shape[1] * 0.5)
        height = int(frame.shape[0] * 0.5)
        new_size = (width, height)
        resized_frame = cv.resize(frame, new_size, interpolation=cv.INTER_AREA)


        edges = cv.Canny(resized_frame,threshold1Value,threshold2Value)

        cv.imshow('resized_frame', resized_frame)
        cv.imshow('edges', edges)

        if cv.waitKey(100) == 27:
            print('ended')
            root.quit()
            break
    print('while loop ended')
    cv.destroyAllWindows()


def on_closing():
    global stop_thread
    stop_thread = True
    root.quit()



root = tk.Tk()
root.title("Tkinter ja OpenCV")

threshold1 = 100
threshold2 = 200

threshold1label = tk.Label(root, text="Low Threshold:")
threshold1label.pack()
threshold1slider = ttk.Scale(root, from_=0, to=255, orient='horizontal')
threshold1slider.set(threshold1)
threshold1slider.pack(pady=10)
threshold1valuelabel = tk.Label(root, text="-")
threshold1valuelabel.pack()

threshold2label = tk.Label(root, text="High Threshold:")
threshold2label.pack()
threshold2slider = ttk.Scale(root, from_=0, to=255, orient='horizontal')
threshold2slider.set(threshold2)
threshold2slider.pack(pady=10)
threshold2valuelabel = tk.Label(root, text="-")
threshold2valuelabel.pack()




opencv_thread = threading.Thread(target=opencv_loop)
opencv_thread.start()

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
opencv_thread.join()
print('program ended')