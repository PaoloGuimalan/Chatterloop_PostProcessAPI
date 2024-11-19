from pydantic import BaseModel, Field
from typing import List, Optional, Any

class ReferenceTagSchema(BaseModel):
    tag: Any
    confidence: Any

class ReferenceSchema(BaseModel):
    name: Any  # Replace `Any` with `str` or another specific type if possible
    referenceID: Any
    reference: Any
    caption: Any
    referenceMediaType: Any
    referenceTag: Optional[List[ReferenceTagSchema]] = []

class ContentSchema(BaseModel):
    isShared: Optional[bool] = False
    references: Optional[List[ReferenceSchema]] = []
    data: Any

class TypeSchema(BaseModel):
    fileType: Any
    contentType: Any

class TaggingSchema(BaseModel):
    isTagged: Optional[bool] = False
    users: Optional[List[Any]] = []

class PrivacySchema(BaseModel):
    status: Any
    users: Optional[List[Any]] = []  # Assuming this stores user IDs for filtering

class IsOnMapSchema(BaseModel):
    status: Optional[bool] = False
    isStationary: Optional[bool] = False

class PostSchema(BaseModel):
    postID: Any
    userID: Any
    content: ContentSchema
    type: TypeSchema
    tagging: Optional[TaggingSchema] = TaggingSchema()
    privacy: PrivacySchema
    onfeed: Any
    isSponsored: Optional[bool] = False
    isLive: Optional[bool] = False
    isOnMap: Optional[IsOnMapSchema] = IsOnMapSchema()
    fromSystem: Optional[bool] = False
    dateposted: Any

    class Config:
        orm_mode = True
