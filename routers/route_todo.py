from typing import List
from fastapi import APIRouter, Depends, HTTPException, Request, Response
from fastapi.encoders import jsonable_encoder
from auth_utils import AuthJwtCsrf
from database import db_create_todo, db_delete_todo, db_get_todos, db_get_todo_detail, db_update_todo
from schemas import SuccessMessage, Todo, TodoBody
from starlette.status import HTTP_201_CREATED
from fastapi_csrf_protect import CsrfProtect

router = APIRouter()
auth = AuthJwtCsrf()

@router.post('/api/todo', response_model=Todo)
async def create_todo(request: Request, response: Response, data: TodoBody, csrf_protect: CsrfProtect = Depends()):
  new_token = auth.verify_csrf_update_jwt(
    request, csrf_protect, request.headers
  )
  todo = jsonable_encoder(data)
  res = await db_create_todo(todo)
  response.status_code = HTTP_201_CREATED
  response.set_cookie(
    key='access_token', value=f'Bearer {new_token}', httponly=True, samesite='none', secure=True
  )
  if res:
    return res
  raise HTTPException(
    status_code=404, detail='Create task failed'
  )

@router.get('/api/todo', response_model=List[Todo])
async def get_todos(request: Request):
  auth.verify_jwt(request)
  res = await db_get_todos()
  return res

@router.get('/api/todo/{id}', response_model=Todo)
async def get_todo_detail(request: Request, response: Response, id: str):
  new_token, _ = auth.verify_update_jwt(request)
  res = await db_get_todo_detail(id)
  response.set_cookie(
    key='access_token', value=f'Bearer {new_token}', httponly=True, samesite='none', secure=True
  )
  if res:
    return res
  raise HTTPException(
    status_code=404, detail=f"Task of ID: {id} doesn't exist"
  )

@router.put('/api/todo/{id}', response_model=Todo)
async def update_todo(request: Request, response: Response, id: str, data: TodoBody, csrf_protect: CsrfProtect = Depends()):
  new_token = auth.verify_csrf_update_jwt(
    request, csrf_protect, request.headers
  )
  todo = jsonable_encoder(data)
  res = await db_update_todo(id, todo)
  response.set_cookie(
    key='access_token', value=f'Bearer {new_token}', httponly=True, samesite='none', secure=True
  )
  if res:
    return res
  raise HTTPException(
    status_code=404, detail="Update task failed"
  )

@router.delete('/api/todo/{id}', response_model=SuccessMessage)
async def delete_todo(requset: Request, response: Response, id: str, csrf_protect: CsrfProtect = Depends()):
  new_token = auth.verify_csrf_update_jwt(
    requset, csrf_protect, requset.headers
  )
  res = await db_delete_todo(id)
  response.set_cookie(
    key='accsess_token', value=f'Bearer {new_token}', httponly=True, samesite='none', secure=True
  )
  if res:
    return {'message': 'Successfully deleted'}
  raise HTTPException(
    status_code=404, detail="Delete task failed"
  )
