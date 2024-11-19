from connections.mongo import MongoConnection
from fastapi import Request, HTTPException

class ImageTagSyncingService:

    async def save_tags_to_mongo(reference_data: dict):

        if reference_data["referenceType"] == "post":
            db_posts = MongoConnection.execute("posts")
            postID = reference_data["referenceID"]
            result = reference_data["result"]
            
            try:
                array_filters = []
                set_statements = {}

                for i, res in enumerate(result):
                    referenceID = res["referenceID"]
                    referenceTag = res["referenceTag"]

                    array_filters.append({f"ref{i}.referenceID": referenceID})
                    set_statements[f"content.references.$[ref{i}].referenceTag"] = referenceTag

                db_posts.update_one(
                    { "postID": postID },
                    { "$set": set_statements },
                    array_filters=array_filters
                )

            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
        
        if reference_data["referenceType"] == "message":
            db_messages = MongoConnection.execute("messages")

            messageID = reference_data["referenceID"]
            result = reference_data["result"]
            referenceTag = result[0]["referenceTag"]

            db_messages.update_one({
                "messageID": messageID
            }, {
                "$set": {
                    "referenceTag": referenceTag
                }
            })
        
        return None