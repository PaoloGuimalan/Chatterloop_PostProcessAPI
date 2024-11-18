from fastapi import Request, HTTPException
from configs.env_exports import envs
from schemas.UserAccountSchema import List_UserAccounts
from connections.mongo import MongoConnection

class JWTChecker:

    async def check_user_token(request: Request):
        x_access_token = request.headers.get("x-access-token")

        db = MongoConnection.execute("useraccount")
        user = List_UserAccounts(db.find())

        print(user)
        
        if x_access_token == None:
            raise HTTPException(401, "No token found")