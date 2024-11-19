from pydantic import BaseModel
from typing import List, Optional, Any

class ReferenceTagSchema(BaseModel):
    tag: Any
    confidence: Any

class MessageDate(BaseModel):
    date: Any
    time: Any

class MessageModel(BaseModel):
    messageID: Any
    conversationID: Any
    pendingID: Any
    sender: Any
    receivers: List[Any]
    seeners: List[Any]
    content: Any
    referenceTag: Optional[List[ReferenceTagSchema]] = []
    messageDate: MessageDate
    isReply: bool
    replyingTo: Optional[Any] = None
    reactions: List[Any]
    isDeleted: bool
    messageType: Any
    conversationType: Any