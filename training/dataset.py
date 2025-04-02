import cv2
import tkinter as tk
from tkinter import filedialog
import os
import re  # Lisätään re-moduuli tiedostonimien käsittelyä varten

class Dataset:
    def __init__(self, master, image, annotation):
        self.image = image
        self.annotation = tk.StringVar(value=annotation)
        self.imageNumber = 0
        
        self.root = tk.Toplevel(master)
        self.root.title("Annotation dataset")
        self.root.geometry("900x400")  # Asetetaan ikkunan leveys kolminkertaiseksi
        self.root.grid_columnconfigure(0, weight=1)  # Ensimmäinen sarake venyy täyttämään tilan
        
        self.label_folder = tk.Label(self.root, text="Dataset folder:")
        self.label_folder.grid(row=0, column=0, padx=10, pady=(10, 0), sticky='w')

        self.folder = tk.StringVar(value=str(os.getcwd()) + "/dataset/")
        self.entry_folder = tk.Entry(self.root, textvariable = self.folder)
        self.entry_folder.grid(row=1, column=0, columnspan=2, padx=10, pady=(0, 10), sticky='ew')
        self.button_folder = tk.Button(self.root, text="Set")
        self.button_folder.grid(row=1, column=2, padx=10, pady=(0, 10))

        self.label_imagename = tk.Label(self.root, text="Image basic name:")
        self.label_imagename.grid(row=2, column=0, padx=10, pady=(10, 0), sticky='w')

        self.imagename = tk.StringVar(value="image")
        self.entry_imagename = tk.Entry(self.root, textvariable = self.imagename)
        self.entry_imagename.grid(row=3, column=0, columnspan=2, padx=10, pady=(0, 10), sticky='ew')
        self.button_imagename = tk.Button(self.root, text="Set")
        self.button_imagename.grid(row=3, column=2, padx=10, pady=(0, 10))

        # Lisätään annotaation merkintätiedoston tekstikenttä
        self.label_annotation = tk.Label(self.root, text="Annotation:")
        self.label_annotation.grid(row=4, column=0, padx=10, pady=(10, 0), sticky='w')

        self.entry_annotation = tk.Entry(self.root, text=self.annotation)
        self.entry_annotation.grid(row=5, column=0, columnspan=2, padx=10, pady=(0, 10), sticky='ew')

        # Lisätään "Create"-nappi ikkunan vasempaan alalaitaan
        self.button_create = tk.Button(self.root, text="Create", command=self.createAnnotation)
        self.button_create.grid(row=6, column=0, padx=10, pady=10, sticky='w')

        self.root.mainloop()

    def getLatestImageNumber(self):
        train_images_path = os.path.join(self.folder, "images", "train")
        if not os.path.exists(train_images_path):
            return 0  # Palautetaan 0, jos hakemistoa ei ole

        max_number = 0
        for filename in os.listdir(train_images_path):
            match = re.search(r"_(\d+)\.jpg$", filename)
            if match:
                number = int(match.group(1))
                max_number = max(max_number, number)

        return max_number

    def createAnnotation(self):
        # Haetaan kansiopolku entry-kentästä        # Luodaan alihakemistot 'images' ja 'labels', jos niitä ei ole olemassa
        # Luodaan pääkansio, jos sitä ei ole olemassa
        self.folder = self.entry_folder.get()
        if not os.path.exists(self.folder):
            os.makedirs(self.folder)
            print(f"Created folder: {self.folder}")

        # Luodaan alihakemistot 'images' ja 'labels', jos niitä ei ole olemassa
        images_path = os.path.join(self.folder, "images")
        labels_path = os.path.join(self.folder, "labels")

        if not os.path.exists(images_path):
            os.makedirs(images_path)
            print(f"Created subfolder: {images_path}")

        if not os.path.exists(labels_path):
            os.makedirs(labels_path)
            print(f"Created subfolder: {labels_path}")

        # Luodaan 'train' ja 'val' alihakemistot molempiin
        for subfolder in [images_path, labels_path]:
            train_path = os.path.join(subfolder, "train")
            val_path = os.path.join(subfolder, "val")

            if not os.path.exists(train_path):
                os.makedirs(train_path)
                print(f"Created subfolder: {train_path}")

            if not os.path.exists(val_path):
                os.makedirs(val_path)
                print(f"Created subfolder: {val_path}")

        # Päivitetään imageNumber viimeisimmän kuvan numeron perusteella
        self.imageNumber = self.getLatestImageNumber() + 1

        # Tallennetaan kuva images/train-hakemistoon
        train_images_path = os.path.join(images_path, "train")
        image_filename = f"{self.imagename.get()}_{self.imageNumber}.jpg"
        image_path = os.path.join(train_images_path, image_filename)

        # Tallennetaan kuva OpenCV:n avulla
        cv2.imwrite(image_path, self.image)
        print(f"Saved image: {image_path}")

        # Tallennetaan annotaatio labels/train-hakemistoon
        train_labels_path = os.path.join(labels_path, "train")
        annotation_filename = f"{self.imagename.get()}_{self.imageNumber}.txt"
        annotation_path = os.path.join(train_labels_path, annotation_filename)

        with open(annotation_path, "w") as annotation_file:
            annotation_file.write(self.entry_annotation.get())
        print(f"Saved annotation: {annotation_path}")

        self.imageNumber = self.imageNumber + 1