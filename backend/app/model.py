from ultralytics import YOLO
import torch

class TableDetector:
    def __init__(self, model_path: str = "best.pt"):
        self.device = "cpu"
        self.model = YOLO(model_path)
        self.model.to(self.device)
        # warm up the model
        self.model.predict("https://ultralytics.com/images/bus.jpg", verbose=False)
        print("Model loaded successfully")
    
    def predict(self, image, conf=0.5, iou=0.55):
        results = self.model.predict(
            image,
            conf=conf,
            iou=iou,
            verbose= False
        )
        return results[0]

