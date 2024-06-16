import os
import time
import boto3
from fastapi import FastAPI, HTTPException
from mangum import Mangum
from pydantic import BaseModel
from typing import Optional
from uuid import uuid4
from boto3.dynamodb.conditions import Key

class Task(BaseModel):
    id: Optional[str] = None
    user_id: Optional[str] = None
    content: str
    is_done: bool = False

app = FastAPI()
handler = Mangum(app)

@app.get("/")
def root():
    return {"message": "Wellcome to Todo list"}

@app.post("/create-task")
def create_task(request: Task):
    created_at = int(time.time())
    item = {
        "id": uuid4().hex,
        "user_id": request.user_id,
        "content": request.content,
        "created_time": created_at,
        "is_done": False,
        "ttl": int(created_at + 86400) # Exprie after 24 hours
    }

    # Put item into table
    table = _get_table()
    table.put_item(Item=item)

    return {"task" : item}

@app.get("/get-task/{id}")
def get_task(id: str):
    table = _get_table()
    response = table.get_item(Key={"id": id})
    item = response.get("Item")

    if not item:
        raise HTTPException(status_code=404, detail=f"Task {id} not found")
    return item

@app.get("/list-tasks/{user_id}")
def list_task(user_id: str):
    table = _get_table()
    response = table.query(
        IndexName="user-index",
        KeyConditionExpression=Key("user_id").eq(user_id),
        ScanIndexForward=False,
        Limit=10,
    )

    tasks = response.get("Items")

    return {"tasks": tasks}

@app.put("/update-task")
def update_task(request: Task):
    table = _get_table()
    response = table.update_item(
                Key={"id": request.id},
                UpdateExpression="SET content = :content, is_done = :is_done",
                ExpressionAttributeValues={
                    ":content": request.content,
                    ":is_done": request.is_done
                },
                ReturnValues="UPDATED_NEW",
            )

    return {"attribute" : response["Attributes"], "updated task  id successfully": request.id}

@app.delete("/delete-task/{id}")
def delete_task(id: str):
    table = _get_table()
    table.delete_item(Key={"id": id})

    return {"deleted task id successfully": id}

# configure a connection to a DynamoDB table in Python, via the boto3 library
def _get_table():
    table_name = os.environ.get("TABLE_NAME")
    return boto3.resource("dynamodb").Table(table_name)
