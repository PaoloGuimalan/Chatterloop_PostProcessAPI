from fastapi import Request, HTTPException
from configs.env_exports import envs
from schemas.UserAccountSchema import List_UserAccounts
from connections.mongo import MongoConnection
from jose import jwt # type: ignore
from configs.env_exports import envs

class JWTChecker:

    async def check_user_token(request: Request):
        x_access_token = request.headers.get("x-access-token")
        
        if x_access_token == None:
            raise HTTPException(401, "No token found")
        else:
            try:
                decode_token = jwt.decode(x_access_token, envs.jwt_secret)
                userID = decode_token["userID"]

                db = MongoConnection.execute("useraccount")
                user = List_UserAccounts(db.find({ "userID": userID }))

                if len(user) == 0:
                    raise HTTPException(401, "No user found")
                elif len(user) > 1:
                    raise HTTPException(401, "Duplicate accounts error have occured")
                else:
                    request.state.userID = user[0]["userID"]
            except Exception as e:
                print(e)
                raise HTTPException(401, "Invalid token")