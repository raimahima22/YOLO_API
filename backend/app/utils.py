import cv2
import numpy as np
import json
from pathlib import Path

def draw_detections(image_np: np.ndarray, detections: list) -> np.ndarray:
    annotated = image_np.copy()
    colors = {
        "table": (0, 255, 0),
        "table column header": (0, 165, 255),
        "table projected row header": (255, 100, 0)
    }
    
    for det in detections:
        x1, y1, x2, y2 = det["bbox"]
        color = colors.get(det["class"], (0, 255, 255))
        
        cv2.rectangle(annotated, (x1, y1), (x2, y2), color, 3)
        label = f"{det['class']} {det['confidence']:.2f}"
        cv2.putText(annotated, label, (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
    return annotated


def save_json_result(output_path: Path, data: dict):
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)


def save_annotated_image(output_path: Path, image_np: np.ndarray):
    cv2.imwrite(str(output_path), image_np)