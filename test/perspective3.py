import cv2
import numpy as np
import tkinter as tk
from tkinter import ttk
import threading

class LineFunction:
    slope : float
    minSlope: float
    maxSlope: float
    constant: float
    minConstant : float
    maxConstant : float
    similarLineFunctions = []

    def __init__(self, slope, constant):
            self.slope = slope
            self.constant = constant
            slopeDifference = (slope * 0.1)
            self.minSlope = slope - slopeDifference
            self.maxSlope = slope + slopeDifference
            constantDifference = (constant * 0.1)
            self.minConstant = constant - constantDifference
            self.maxConstant = constant + constantDifference

    def isNew(self, slope, constant):
        lineFunction = LineFunction(slope, constant)
        if(lineFunction.slope >= self.minSlope and lineFunction.slope <= self.maxSlope):
            self.similarLineFunctions.append(lineFunction)
            lineFunction = None
        elif(lineFunction.minSlope >= self.minSlope and lineFunction.minSlope <= self.maxConstant):
            self.similarLineFunctions.append(lineFunction)
            lineFunction = None
        elif(lineFunction.maxSlope >= self.minSlope and lineFunction.maxSlope <= self.maxConstant):
            self.similarLineFunctions.append(lineFunction)
            lineFunction = None

        return lineFunction
    



def line_intersection(line1, line2):
    x1, y1, x2, y2 = line1
    x3, y3, x4, y4 = line2

    # Laske viivojen yhtälöt (y = mx + b)
    m1 = (y2 - y1) / (x2 - x1) if x2 != x1 else float('inf')
    b1 = y1 - m1 * x1 if m1 != float('inf') else x1

    m2 = (y4 - y3) / (x4 - x3) if x4 != x3 else float('inf')
    b2 = y3 - m2 * x3 if m2 != float('inf') else x3

    # Tarkista, ovatko viivat yhdensuuntaiset
    if m1 == m2:
        return None  # Viivat eivät leikkaa

    # Laske leikkauspiste
    if m1 == float('inf'):
        x = b1
        y = m2 * x + b2
    elif m2 == float('inf'):
        x = b2
        y = m1 * x + b1
    else:
        x = (b2 - b1) / (m1 - m2)
        y = m1 * x + b1

    return (int(x), int(y))

stop_thread = False
def opencv_loop():
    global threshold1slider, threshold2slider, threshold3slider, threshold1valuelabel, threshold2valuelabel, threshold3valuelabel
    while not stop_thread:
        threshold1Value = int(threshold1slider.get())
        threshold2Value = int(threshold2slider.get())
        threshold3Value = int(threshold3slider.get())

        threshold1valuelabel['text'] = str(threshold1Value)
        threshold2valuelabel['text'] = str(threshold2Value)
        threshold3valuelabel['text'] = str(threshold3Value)


        image = cv2.imread('perspective.png')
        height, width, channels = image.shape
        grayimage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blurredimage = cv2.GaussianBlur(grayimage, (15, 15), 0)
        #edges = cv2.Canny(blurredimage,threshold1Value,threshold2Value, 3)
        ret, maskedImage = cv2.threshold(blurredimage, threshold1Value, threshold2Value, cv2.THRESH_BINARY)

        kernel = np.ones((threshold3Value, threshold3Value), np.uint8)
        closedImage = cv2.morphologyEx(maskedImage, cv2.MORPH_CLOSE, kernel)
  

        cv2.imshow('maskedImage', maskedImage)
        cv2.imshow('grayimage', grayimage)
        cv2.imshow('blurredimage', blurredimage)
        cv2.imshow('image', image)
        cv2.imshow('closedImage', closedImage)

        if cv2.waitKey(100) == 27:
            print('ended')
            root.quit()
            break

    print('while loop ended')
    cv2.destroyAllWindows()


def on_closing():
    global stop_thread
    stop_thread = True
    root.quit()

root = tk.Tk()
root.geometry("400x300+100+200")
root.title("Tkinter ja OpenCV")

threshold1 = 100
threshold2 = 200
threshold3 = 50

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

threshold3label = tk.Label(root, text="Closing size:")
threshold3label.pack()
threshold3slider = ttk.Scale(root, from_=0, to=255, orient='horizontal')
threshold3slider.set(threshold3)
threshold3slider.pack(pady=10)
threshold3valuelabel = tk.Label(root, text="-")
threshold3valuelabel.pack()




opencv_thread = threading.Thread(target=opencv_loop)
opencv_thread.start()

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
opencv_thread.join()
print('program ended')
