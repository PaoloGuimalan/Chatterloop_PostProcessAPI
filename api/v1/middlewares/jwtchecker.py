from fastapi import Request, HTTPException

class JWTChecker:

    async def check_user_token(request: Request):
        x_access_token = request.headers.get("x-access-token")
        
        if x_access_token == None:
            raise HTTPException(401, "No token found")