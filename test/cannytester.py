import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
from time import sleep
import tkinter as tk
from tkinter import ttk
import threading

stop_thread = False
def opencv_loop():
    while not stop_thread:
        img = cv.imread('test.png',0)
        edges = cv.Canny(img,100,200)

        cv.imshow('img', img)
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

opencv_thread = threading.Thread(target=opencv_loop)
opencv_thread.start()

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
opencv_thread.join()
print('program ended')