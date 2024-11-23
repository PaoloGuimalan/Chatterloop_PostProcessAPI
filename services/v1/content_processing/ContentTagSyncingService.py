from connections.mongo import MongoConnection
from fastapi import HTTPException
from schemas.UserPostSchema import UserPosts
from schemas.UserMessageSchema import UserMessage
from models.UserPostsModel import PostModel
from models.UserMessageModel import MessageModel
from helpers.formatter import DataFormatter

class ContentTagSyncingService:

    async def save_tags_to_mongo(reference_data: dict):
        remove_and_total_tag_duplicates = DataFormatter.remove_and_total_tag_duplicates

        if reference_data != None:

            if reference_data["referenceType"] == "post":
                db_posts = MongoConnection.execute("posts")
                post_data: PostModel = UserPosts(db_posts.find_one({ "postID": reference_data["referenceID"] }))

                pendingDataTags = list()
                pendingReferenceTags = list()

                pendingDataTags = post_data["content"]["dataTag"]
                pendingReferenceTags = [
                    { 
                            "referenceID": x["referenceID"], 
                            "caption": x["caption"],
                            "referenceTag": x["referenceTag"]
                    } for x in post_data["content"]["references"]
                ]

                if len(reference_data["dataTag"]) > 0:
                    pendingDataTags.extend(reference_data["dataTag"])
                    pendingDataTags = remove_and_total_tag_duplicates(pendingDataTags)

                if len(reference_data["references"]) > 0:
                        for tag in reference_data["references"]:
                            for current_reference in pendingReferenceTags:
                                if current_reference["referenceID"] == tag["referenceID"]:
                                    current_reference["referenceTag"].extend(tag["referenceTag"])

                try:
                    array_filters = []
                    set_statements = {
                        "content.dataTag": pendingDataTags
                    }

                    for i, res in enumerate(pendingReferenceTags):
                        referenceID = res["referenceID"]
                        referenceTag = res["referenceTag"]

                        array_filters.append({f"ref{i}.referenceID": referenceID})
                        set_statements[f"content.references.$[ref{i}].referenceTag"] = remove_and_total_tag_duplicates(referenceTag)

                    db_posts.update_one(
                        { "postID": reference_data["referenceID"] },
                        { "$set": set_statements },
                        array_filters=array_filters
                    )

                except Exception as e:
                    raise HTTPException(status_code=500, detail=str(e))

                return None
            
            if reference_data["referenceType"] == "message":
                if len(reference_data["referenceTag"]) > 0:
                    db_messages = MongoConnection.execute("messages")
                    message_data: MessageModel = UserMessage(db_messages.find_one({ "messageID": reference_data["referenceID"] }))

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