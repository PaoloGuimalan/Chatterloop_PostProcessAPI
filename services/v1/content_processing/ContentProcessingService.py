import spacy
import tf_keras as keras
from transformers import pipeline
from connections.mongo import MongoConnection
from schemas.UserPostSchema import UserPosts
from schemas.UserMessageSchema import UserMessage
from models.UserPostsModel import PostSchema
from models.UserMessageModel import MessageModel

class ContentProcessingService:

    def __init__(self):
        self.nlp = None
        self.ner_pipeline = None

    def load_model(self):
        # if self.nlp == None:
        #     self.nlp = spacy.load("xx_sent_ud_sm") #xx_ent_wiki_sm

        if self.ner_pipeline == None:
            self.ner_pipeline = pipeline("ner", model="dbmdz/bert-large-cased-finetuned-conll03-english", grouped_entities=True) #xlm-roberta-large-finetuned-conll03-english, xlm-roberta-base

    async def content_check(self, referenceID: str, referenceType: str):
        if referenceType == "post":
            db_posts = MongoConnection.execute("posts")
            post_data: PostSchema = UserPosts(db_posts.find_one({ "postID": referenceID }))
            
            if post_data != {}:
                main_content = post_data["content"]["data"]
                references = [
                    { 
                        "referenceID": reference["referenceID"], 
                        "caption": reference["caption"],
                        "referenceTag": reference["referenceTag"]
                    } for reference in post_data["content"]["references"] if reference["referenceMediaType"] != "shared_post" and reference["caption"] != ""
                ]

                # doc_main_content = self.nlp(main_content)
                results = self.ner_pipeline(main_content)
                parsed_results = [
                    {
                        "tag": entity["word"],
                        "confidence": f"{entity['score'] * 100:.2f}"
                    } for entity in results
                ]

                referenceTagFromCaption = []

                for reference in references:
                    pendingReferenceTag = reference["referenceTag"]
                    captionToProcess = self.ner_pipeline(reference["caption"])

                    for entity in captionToProcess:
                        pendingReferenceTag.append({
                            "tag": entity["word"],
                            "confidence": f"{entity['score'] * 100:.2f}"
                        } )

                    referenceTagFromCaption.append({
                        "referenceID": reference["referenceID"],
                        "caption": reference["caption"],
                        "referenceTag": pendingReferenceTag
                    })
                    
                return {
                    "referenceID": referenceID,
                    "referenceType": referenceType,
                    "dataTag": parsed_results,
                    "references": referenceTagFromCaption
                }
            
            return None

        if referenceType == "message":
            db_messages = MongoConnection.execute("messages")
            message_data: MessageModel = UserMessage(db_messages.find_one({ "messageID": referenceID }))

            if message_data != {}:
                content = message_data["content"]
                results = self.ner_pipeline(content)
                parsed_results = [
                    {
                        "tag": entity["word"],
                        "confidence": f"{entity['score'] * 100:.2f}"
                    } for entity in results
                ]

                return {
                    "referenceID": referenceID,
                    "referenceType": referenceType,
                    "referenceTag": parsed_results
                }
            
            return None

        # print(referenceID, referenceType)
        return None

content_processing = ContentProcessingService()
content_processing.load_model()
