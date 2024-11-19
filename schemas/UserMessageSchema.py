def UserMessage(message: dict) -> dict:
    if message == None:
        return {}

    return {
        "messageID": message.get("messageID"),
        "conversationID": message.get("conversationID"),
        "pendingID": message.get("pendingID"),
        "sender": message.get("sender"),
        "receivers": message.get("receivers", []),
        "seeners": message.get("seeners", []),
        "content": message.get("content"),
        "referenceTag": message.get("referenceTag", []),
        "messageDate": {
            "date": message.get("messageDate", {}).get("date"),
            "time": message.get("messageDate", {}).get("time")
        },
        "isReply": message.get("isReply"),
        "replyingTo": message.get("replyingTo"),
        "reactions": message.get("reactions", []),
        "isDeleted": message.get("isDeleted"),
        "messageType": message.get("messageType"),
        "conversationType": message.get("conversationType")
    }

def List_UserMessage(messages: list) -> list:
    return [UserMessage(message) for message in messages]