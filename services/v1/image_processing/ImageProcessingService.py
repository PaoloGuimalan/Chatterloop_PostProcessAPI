from connections.mongo import MongoConnection
from schemas.UserPostSchema import UserPosts
from schemas.UserMessageSchema import UserMessage

class ImageProcessingService:

    async def fetch_image_src(
            referenceID: str, 
            referenceType: str
        ):

        if(referenceType == "post"):
            db_post = MongoConnection.execute("posts")
            post_data = UserPosts(db_post.find_one({ "postID": referenceID }))

            return post_data
        
        if(referenceType == "message"):
            db_message = MongoConnection.execute("messages")
            message_data = UserMessage(db_message.find_one({ "messageID": referenceID }))

            return message_data
        
        return {}