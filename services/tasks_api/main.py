import uuid
from typing import Union

import jwt
from fastapi import FastAPI, Depends, Header, status
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum

from config import Config
from models import Task
from schemas import CreateTask, APITask, APITaskList, CloseTask
from store import TaskStore


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

config = Config()


def get_task_store():
    return TaskStore(config.TABLE_NAME, config.DYNAMODB_URL)


def get_user_email(authorization: Union[str, None] = Header(default=None)):
    if authorization:
        token = jwt.decode(authorization, verify=False)
        return token


@app.get("/api/health-check/")
def health_check():
    return {"message": "OK"}


@app.post(
    "/api/create-task", response_model=APITask, status_code=status.HTTP_201_CREATED
)
def create_task(
    task: CreateTask,
    user_email: str = Depends(get_user_email),
    task_store: TaskStore = Depends(get_task_store),
):
    task = Task.create(id_=uuid.uuid4(), title=task.title, owner=user_email)
    task_store.add(task)
    return task


handler = Mangum(app)


@app.get("/api/open-tasks", response_model=APITaskList)
def open_tasks(
    user_email: str = Depends(get_user_email),
    task_store: TaskStore = Depends(get_task_store),
):
    tasks = task_store.list_open(owner=user_email)
    return APITaskList(results=tasks)


@app.post("/api/close-task", response_model=APITask)
def close_task(
    parameters: CloseTask,
    user_email: str = Depends(get_user_email),
    task_store: TaskStore = Depends(get_task_store),
):
    task = task_store.get_by_id(task_id=parameters.id, owner=user_email)
    task.close()
    task_store.add(task)

    return task


@app.get("/api/closed-tasks", response_model=APITaskList)
def closed_tasks(
    user_email: str = Depends(get_user_email),
    task_store: TaskStore = Depends(get_task_store),
):
    return APITaskList(results=task_store.list_closed(owner=user_email))
