from ultralytics import YOLO
from PIL import Image
from io import BytesIO
import numpy as np
import requests

class InputReader:

    def __init__(self):
        self.model = None

    def load_model(self):
        self.model = YOLO("yolov5su.pt")  # "yolov5s, yolov5s.pt" is a lightweight model

    async def read_image_src(self, url: str):
        response = requests.get(url)
        if response.status_code == 200:
            # Open the image from the content of the response
            img = Image.open(BytesIO(response.content))
            return img;
        return None
    
    async def image_preprocess(self, image: Image.Image):
        input_shape = (800, 800)

        if image.mode != 'RGB':
            image = image.convert('RGB')

        image = image.resize(input_shape)
        image = np.asarray(image, dtype=float)
        image = image / 255.0
        image = np.expand_dims(image, 0)

        return image
    
    async def yolo_process(self, image: Image.Image):
        if self.model == None:
            self.model = YOLO("yolov5su.pt")  # "yolov5s, yolov5s.pt" is a lightweight model

        model = self.model
        # Run inference
        results = model(image)
        # results.show()
        if len(results[0]) > 0:
            probs = results[0].probs 
            cls = results[0].boxes.cls
            names = results[0].names

            cls = cls.cpu().numpy() 

            detected_items = {}

            for i in range(len(cls)):
                class_idx = int(cls[i])
                class_name = names[class_idx]
                confidence = results[0].boxes.conf[i].cpu().numpy()

                if class_name not in detected_items:
                    detected_items[class_name] = confidence
                else:
                    if confidence > detected_items[class_name]:
                        detected_items[class_name] = confidence

            final_detected_items = [{"tag": tag, "confidence": f"{conf:.2f}"} for tag, conf in detected_items.items()]

            return final_detected_items
        return []
    
input_reader = InputReader()