from connections.mongo import MongoConnection
from fastapi import HTTPException
from schemas.UserPostSchema import UserPosts
from schemas.UserMessageSchema import UserMessage
from models.UserPostsModel import PostModel
from models.UserMessageModel import MessageModel

class ContentTagSyncingService:

    async def save_tags_to_mongo(reference_data: dict):

        if reference_data["referenceType"] == "post":

            return None
        
        if reference_data["referenceType"] == "message":
            if len(reference_data["referenceTag"]) > 0:
                db_messages = MongoConnection.execute("messages")
                message_data = UserMessage(db_messages.find_one({ "messageID": reference_data["referenceID"] }))

                if message_data != {}:
                    message_tags = message_data["referenceTag"]
                    message_tags.extend(reference_data["referenceTag"])

                    db_messages.update_one({
                        "messageID": reference_data["referenceID"]
                    }, {
                        "$set": {
                            "referenceTag": message_tags
                        }
                    })

                    return True

                return None

            return None
        
        return None