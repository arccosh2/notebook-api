from fastapi import APIRouter, HTTPException, Request, Response
from fastapi.encoders import jsonable_encoder
from database import db_create_todo
from schemas import Todo, TodoBody
from starlette.status import HTTP_201_CREATED

router = APIRouter()

@router.post('/api/todo', response_model=Todo)
async def create_todo(request: Request, response: Response, data: TodoBody):
  todo = jsonable_encoder(data)
  res = await db_create_todo(todo)
  response.status_code = HTTP_201_CREATED
  if res:
    return res
  raise HTTPException(
    status_code = 404, detail='Create task failed'
  )
