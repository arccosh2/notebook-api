from typing import List
from fastapi import APIRouter, HTTPException, Request, Response
from fastapi.encoders import jsonable_encoder
from database import db_create_todo, db_get_todos, db_get_todo_detail
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
    status_code=404, detail='Create task failed'
  )

@router.get('/api/todo', response_model=List[Todo])
async def get_todos():
  res = await db_get_todos()
  return res

@router.get('/api/todo/{id}', response_model=Todo)
async def get_todo_detail(id: str):
  res = await db_get_todo_detail(id)
  if res:
    return res
  raise HTTPException(
    status_code=404, detail=f"Task of ID: {id} doesn't exist"
  )
