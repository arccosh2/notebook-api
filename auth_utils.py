from datetime import datetime, timedelta
from fastapi import HTTPException
import jwt
from passlib.context import CryptContext
from decouple import config

JWT_KEY = config('JWT_KEY')

class AuthJwtCsrf():
  pwd_ctx = CryptContext(schemes=['bcrypt'], deprecated='auto')
  secret_key = JWT_KEY

  def generate_hashed_password(self, password) -> str:
    return self.pwd_ctx.hash(password)

  def verify_password(self, plain_password, hashed_password) -> bool:
    return self.pwd_ctx.verify(plain_password, hashed_password)

  def encode_jwt(self, email) -> str:
    payload = {
      'exp': datetime.utcnow() + timedelta(days=0, minutes=5),
      'iat': datetime.utcnow(),
      'sub': email
    }
    
    return jwt.encode(
      payload,
      self.secret_key,
      algorithm='HS256'
    )
    
  def decode_jwt(self, token) -> str:
    try:
      payload = jwt.decode(token, self.secret_key, algorithms=['HS256'])
      return payload['sub']
    except jwt.ExpiredSignatureError:
      raise HTTPException(
        status_code=401, detail="The JWT has expired"
      )
    except jwt.InvalidTokenError as e:
      raise HTTPException(
        status_code=401, detail="JWT is not valid"
      )
