def UserPosts(post: dict) -> dict:
    if post == None:
        return {}
    
    return {
        "_id": str(post.get("_id")),
        "postID": post.get("postID"),
        "userID": post.get("userID"),
        "content": {
            "isShared": post.get("content", {}).get("isShared"),
            "references": [
                {
                    "name": reference.get("name"),
                    "referenceID": reference.get("referenceID"),
                    "reference": reference.get("reference"),
                    "caption": reference.get("caption"),
                    "referenceMediaType": reference.get("referenceMediaType"),
                    "referenceTag": [{ "tag": referenceTag.get("tag"), "confidence": referenceTag.get("confidence") } for referenceTag in reference.get("referenceTag", [])]
                } for reference in post.get("content", {}).get("references", [])
            ],
            "data": post.get("content", {}).get("data"),
            "dataTag": post.get("content", {}).get("dataTag", [])
        },
        "type": {
            "fileType": post.get("type", {}).get("fileType"),
            "contentType": post.get("type", {}).get("contentType")
        },
        "tagging": {
            "isTagged": post.get("tagging", {}).get("isTagged"),
            "users": post.get("tagging", {}).get("users", [])
        },
        "privacy": {
            "status": post.get("privacy", {}).get("status"),
            "users": post.get("privacy", {}).get("users", [])
        },
        "onfeed": post.get("onfeed"),
        "isSponsored": post.get("isSponsored"),
        "isLive": post.get("isLive"),
        "isOnMap": {
            "status": post.get("isOnMap", {}).get("status"),
            "isStationary": post.get("isOnMap", {}).get("isStationary")
        },
        "fromSystem": post.get("fromSystem"),
        "dateposted": post.get("dateposted")
    }

def List_UserPosts(posts: list) -> list:
    return [UserPosts(post) for post in posts]
