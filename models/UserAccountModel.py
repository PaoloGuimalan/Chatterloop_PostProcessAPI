from pydantic import BaseModel
from typing import Union

class UserFullname(BaseModel):
    firstName: Union[str, int]
    lastName: Union[str, int]
    middleName: Union[str, int]

class UserBirthdate(BaseModel):
    month: Union[str, int]
    day: Union[str, int]
    year: Union[str, int]

class UserDateCreated(BaseModel):
    date: Union[str, int]
    time: Union[str, int]

class UserAccount(BaseModel):
    userID: Union[str, int]
    fullname: UserFullname
    birthdate: UserBirthdate
    profile: Union[str, int]
    coverphoto: Union[str, int]
    gender: Union[str, int]
    email: Union[str, int]
    password: Union[str, int]
    dateCreated: UserDateCreated
    isActivated: bool
    isVerified: bool