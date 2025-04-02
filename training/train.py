import ultralytics
from ultralytics import YOLO


print(f"Versio v{ultralytics.__version__}")


model = YOLO('yolov8n.pt')  # voi käyttää myös 'yolov8m.pt' tai 'yolov8l.pt'
model.train(data='dataset.yaml', epochs=50, imgsz=640)
#model.train(data='/home/centria/projects/machinevision/training/dataset.yaml', epochs=50, imgsz=640)
#model.train(data='/home/centria/projects/machinevision/training/dataset.yaml', epochs=50, imgsz=640, project='/your/custom/path')
