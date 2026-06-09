from fastapi import FastAPI, UploadFile, File, HTTPException, Query
from fastapi.responses import JSONResponse, StreamingResponse
from PIL import Image
import numpy as np
import io
import cv2                                      # ← Added this
from pathlib import Path
from fastapi.middleware.cors import CORSMiddleware
from app.model import TableDetector
from app.utils import draw_detections, save_json_result, save_annotated_image

app = FastAPI(
    title="Table Structure Detection API",
    description="YOLO model for detecting tables, column headers, and projected row headers",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load model once
detector = TableDetector("best.pt")

class_names = ["table", "table column header", "table projected row header"]

# Output directory
OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)

@app.post("/predict")
async def predict(
    file: UploadFile = File(...),
    conf: float = Query(0.25, ge=0.0, le=1.0, description="Confidence threshold"),
    iou: float = Query(0.45, ge=0.0, le=1.0, description="IOU threshold"),
    save_output: bool = Query(True, description="Save JSON and annotated image to output/ folder"),
    return_image: bool = Query(False, description="Return image with bounding boxes (instead of JSON)")
):
    # Validate file type
    if not file.content_type.startswith("image/"):
        raise HTTPException(400, detail="Only image files (jpg, png, jpeg, etc.) are allowed")

    # Read uploaded image
    contents = await file.read()
    image = Image.open(io.BytesIO(contents)).convert("RGB")
    image_np = np.array(image)

    # Run YOLO prediction
    result = detector.predict(image_np, conf=conf, iou=iou)

    # Parse detections
    detections = []
    if result.boxes is not None:
        for box in result.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
            confidence = float(box.conf[0])
            class_id = int(box.cls[0])

            detections.append({
                "class": class_names[class_id],
                "confidence": round(confidence, 4),
                "confidence_percent": f"{round(confidence * 100, 2)}%",
                "bbox": [x1, y1, x2, y2],
                "bbox_normalized": [
                    round(x1 / image_np.shape[1], 4),
                    round(y1 / image_np.shape[0], 4),
                    round((x2 - x1) / image_np.shape[1], 4),
                    round((y2 - y1) / image_np.shape[0], 4)
                ]
            })

    response_data = {
        "filename": file.filename,
        "num_detections": len(detections),
        "detections": detections,
        "model_info": {
            "confidence_threshold": conf,
            "iou_threshold": iou
        }
    }

    # Save results to output folder
    if save_output:
        base_name = Path(file.filename).stem
        json_path = OUTPUT_DIR / f"{base_name}_result.json"
        annotated_path = OUTPUT_DIR / f"{base_name}_annotated.jpg"
        
        save_json_result(json_path, response_data)
        
        annotated_img = draw_detections(image_np, detections)
        save_annotated_image(annotated_path, annotated_img)
        
        response_data["saved_files"] = {
            "json": str(json_path),
            "annotated_image": str(annotated_path)
        }

    # Return annotated image if requested
    if return_image:
        annotated_img = draw_detections(image_np, detections)
        _, buffer = cv2.imencode('.jpg', annotated_img)
        return StreamingResponse(io.BytesIO(buffer.tobytes()), media_type="image/jpeg")

    return JSONResponse(content=response_data)




@app.get("/")
async def root():
    return {
        "message": "Table YOLO Detection API is running ",
        "docs_url": "/docs",
        "usage": "POST image to /predict"
    }

@app.get("/health")
def health():
    return {"status": "ok"}