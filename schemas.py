from typing import Optional
from pydantic import BaseModel

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
