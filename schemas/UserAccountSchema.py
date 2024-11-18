def UserAccount(user: dict) -> dict:
    if user == None:
        return {}

    return {
        "_id": str(user.get("_id")),
        "userID": user.get("userID"),
        "fullname": {
            "firstName": user.get("fullname", {}).get("firstName"),
            "middleName": user.get("fullname", {}).get("middleName"),
            "lastName": user.get("fullname", {}).get("lastName")
        },
        "birthdate": {
            "month": user.get("birthdate", {}).get("month"),
            "day": user.get("birthdate", {}).get("day"),
            "year": user.get("birthdate", {}).get("year")
        },
        "profile": user.get("profile"),
        "coverphoto": user.get("coverphoto"),
        "gender": user.get("gender"),
        "email": user.get("email"),
        "password": user.get("password"),  # Should be hashed in real applications
        "dateCreated": {
            "date": user.get("dateCreated", {}).get("date"),
            "time": user.get("dateCreated", {}).get("time")
        },
        "isActivated": user.get("isActivated"),
        "isVerified": user.get("isVerified")
    }

def List_UserAccounts(users) -> list:
    return [UserAccount(user) for user in users]