from fastapi import HTTPException
from connections.mongo import MongoConnection
from schemas.UserPostSchema import UserPosts
from schemas.UserMessageSchema import UserMessage
from PIL import Image # type: ignore
from io import BytesIO
import requests # type: ignore
import numpy as np # type: ignore
import tensorflow as tf # type: ignore
from tensorflow.keras.applications.imagenet_utils import decode_predictions # type: ignore
from tensorflow.keras.layers import GlobalAveragePooling2D, Dense # type: ignore

class Prediction:

    def __init__(self):
        self.model = None

    async def load_model(self):
        input_shape = (400, 400, 3)
        # self.model = tf.keras.applications.MobileNetV2(input_shape=input_shape, include_top=False, weights='imagenet')

        base_model = tf.keras.applications.MobileNetV2(input_shape=input_shape, include_top=False, weights='imagenet')
        
        x = base_model.output
        x = GlobalAveragePooling2D()(x)
        x = Dense(1000, activation='softmax')(x)
        self.model = tf.keras.models.Model(inputs=base_model.input, outputs=x)

    async def predict(self, image_data: np.ndarray):
        if self.model == None:
            await self.load_model()

        result = decode_predictions(self.model.predict(image_data), 10)[0]
        
        response = []
        for i, res in enumerate(result):
            resp = {}
            resp["tag"] = res[1]
            resp["confidence"] = f"{res[2]*100:0.2f}"

            response.append(resp)

        return response

class InputReader:

    async def read_image_src(url: str):
        response = requests.get(url)
        if response.status_code == 200:
            # Open the image from the content of the response
            img = Image.open(BytesIO(response.content))
            return img;
        return None
    
    async def image_preprocess(image: Image.Image):
        input_shape = (400, 400)

        if image.mode != 'RGB':
            image = image.convert('RGB')

        image = image.resize(input_shape)
        image = np.asarray(image, dtype=float)
        image = image / 255.0
        image = np.expand_dims(image, 0)

        return image

class ImageProcessingService:

    async def fetch_image_src(
            referenceID: str, 
            referenceType: str
        ):

        if(referenceType == "post"):
            db_post = MongoConnection.execute("posts")
            post_data = UserPosts(db_post.find_one({ "postID": referenceID }))

            if "content" in post_data and "references" in post_data["content"]:
                post_references = post_data["content"]["references"]
                filtered_post_references = [x for x in post_references if x["referenceMediaType"] == "image"]
                return { "referenceID": referenceID, "referenceType": referenceType, "result": filtered_post_references } 
            
            return { "referenceID": referenceID, "referenceType": referenceType, "result": [] }
        
        if(referenceType == "message"):
            db_message = MongoConnection.execute("messages")
            message_data = UserMessage(db_message.find_one({ "messageID": referenceID }))

            if "content" in message_data and message_data["messageType"] == "image":
                return { "referenceID": referenceID, "referenceType": referenceType, "result": [message_data["content"]] } 
            
            return { "referenceID": referenceID, "referenceType": referenceType, "result": [] }
        
        return { "referenceID": referenceID, "referenceType": referenceType, "result": [] }
    
    async def handle_images_pre_prediction(reference_data: dict):
        if "result" in reference_data and len(reference_data["result"]) > 0:
            image_list = reference_data["result"]

            read_image_src = InputReader.read_image_src
            preprocess_image = InputReader.image_preprocess

            prediction = Prediction()

            predictions_result = list()

            for img in image_list:
                try:
                    if reference_data["referenceType"] == "post":
                        loaded_img = await read_image_src(img["reference"])
                        processed_image = await preprocess_image(loaded_img)
                        result = await prediction.predict(processed_image)
                        predictions_result.append({ "referenceID": img["referenceID"], "prediction": result })
                        # print(result)
                    
                    if reference_data["referenceType"] == "message":
                        loaded_img = await read_image_src(img)
                        processed_image = await preprocess_image(loaded_img)
                        result = await prediction.predict(processed_image)
                        predictions_result.append({ "referenceID": reference_data["referenceID"], "prediction": result })
                        # print(result)
                except Exception as e:
                    raise HTTPException(status_code=400, detail=str(e))

            # reference_data["predictions"] = predictions_result

            reference_data_w_tags = [
                {
                    **({
                        "name": reference.get("name"),
                        "referenceID": reference.get("referenceID"),
                        "reference": reference.get("reference"),
                        "caption": reference.get("caption"),
                        "referenceMediaType": reference.get("image"),
                        "referenceTag": next(
                            (x.get("prediction") for x in predictions_result if x.get("referenceID") == reference.get("referenceID")),
                            None
                        )
                    } if reference_data["referenceType"] == "post" else {
                        "reference": reference,
                        "referenceTag": next(
                            (x.get("prediction") for x in predictions_result if x.get("referenceID") == reference_data["referenceID"]),
                            None
                        )
                    })
                } for reference in reference_data["result"]
            ]

            final_reference_data = {
                "referenceID": reference_data["referenceID"],
                "referenceType": reference_data["referenceType"],
                "result": reference_data_w_tags
            }

            return final_reference_data

        return reference_data