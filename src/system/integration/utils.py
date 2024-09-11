import os
from jose import jwt
from fastapi import HTTPException, status
class SecurityCore():
    def __init__(self) -> None:
        self.ALGORITHM = os.environ.get("ALGORITHM", "HS256")
        self.SECRET_KEY = os.environ.get("SECRET_KEY", "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7")
        
    async def token_access_decode(self,token: str):
        try:
            data = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])            
            return data
        except Exception as error:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Unathorizad",
                headers={"WWW-Authenticate": "Bearer"},
            )  
    async def token_access_decode(self,token: str):
        try:
            data = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])            
            return data
        except Exception as error:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Unathorizad",
                headers={"WWW-Authenticate": "Bearer"},
            )  