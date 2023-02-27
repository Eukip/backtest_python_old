from typing import Optional

import jwt
from fastapi import HTTPException, Security, Header
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from passlib.context import CryptContext
from datetime import datetime, timedelta

from core.config import settings




class AuthHandler:
    security = HTTPBearer()
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def get_password_hash(self, password):
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    def encode_token(self, user_id):
        payload = {
            'exp': datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
            'iat': datetime.utcnow(),
            'sub': user_id
        }
        return jwt.encode(
            payload,
            settings.SECRET_KEY,
            algorithm=settings.ALGORITHM
        )

    def decode_token(self, token):
        if token:
            try:
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
                return payload['sub']
            except jwt.ExpiredSignatureError:
                raise HTTPException(status_code=401, detail='Signature has expired')
            except jwt.InvalidTokenError as e:
                raise HTTPException(status_code=401, detail='Invalid token')
        else:
            raise HTTPException(status_code=401, detail='Invalid token')


    def parse_bearer_token(self, raw_token: str):
        scheme, _, token = raw_token.partition(" ")
        if scheme.lower() != 'bearer':
            raise HTTPException(status_code=401, detail='Invalid token scheme')
        return token


    def auth_wrapper(self, auth: HTTPAuthorizationCredentials = Security(security)):
        return self.decode_token(auth.credentials)

    def auth_wrapper_optional_secure(self, authorization: Optional[str] = Header(None)):
        if authorization:
            token = self.parse_bearer_token(authorization)
            auth_user_id = self.decode_token(token)
            return auth_user_id
        return None


auth_handler = AuthHandler()
