from typing import Optional
from pydantic import BaseModel
from decouple import config
from pydantic import BaseSettings

CSRF_KEY = config("CSRF_KEY")

class CsrfSettings(BaseSettings):
  secret_key: str = CSRF_KEY
  cookie_samesite: str = "none"

class Todo(BaseModel):
  id: str
  title: str
  description: str


class TodoBody(BaseModel):
  title: str
  description: str
  
class SuccessMessage(BaseModel):
  message: str


class UserBody(BaseModel):
  email: str
  password: str

class UserInfo(BaseModel):
  id: Optional[str] = None
  email: str

class Csrf(BaseModel):
  csrf_token: str
