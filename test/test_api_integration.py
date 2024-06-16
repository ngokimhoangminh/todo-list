import requests
from uuid import uuid4

API = 'https://qyhn475cesi4fkcbvysiy6446u0imidk.lambda-url.us-east-1.on.aws/'

def test_can_create_and_get_task():
    user_id = f"user_{uuid4().hex}"
    content = f"content_{uuid4().hex}"
    create_response = create_task(user_id, content)

    assert create_response.status_code == 200

    # get task
    task_id = create_response.json()['task']['id']
    get_response = get_task(task_id)

    assert get_response.status_code == 200
    assert get_response.json()['user_id'] == user_id
    assert get_response.json()['content'] == content

def test_can_list_tasks():
    user_id = f"user_{uuid4().hex}"

    for i in range(3):
        create_task(user_id, f"task_{i}")

    # List the tasks for this user.
    response = list_tasks(user_id)

    assert response.status_code == 200
    tasks = response.json()["tasks"]
    assert len(tasks) == 3

def test_can_update_task():
    # Create a new user for this test.
    user_id = f"user_{uuid4().hex}"
    create_response = create_task(user_id, "task content")
    task_id = create_response.json()["task"]["id"]

    # Update the task with new content.
    new_task_content = f"updated task content"
    payload = {
        "id": task_id,
        "content": new_task_content,
        "is_done": True,
    }

    update_task_response = update_task(payload)
    assert update_task_response.status_code == 200

    get_task_response = get_task(task_id)

    assert get_task_response.status_code == 200
    assert get_task_response.json()["content"] == new_task_content
    assert get_task_response.json()["is_done"] == True


def test_can_delete_task():
    user_id = f"user_{uuid4().hex}"
    create_response = create_task(user_id, "task1")
    task_id = create_response.json()["task"]["id"]

    # Delete the task.
    delete_task(task_id)

    # We shouldn't be able to get the task anymore.
    get_task_response = get_task(task_id)
    assert get_task_response.status_code == 404

def create_task(user_id: str, content: str) -> dict:
    payload = {
        "user_id": user_id,
        "content": content
    }

    return requests.post(f"{API}/create-task", json=payload)

def list_tasks(user_id: str) -> dict:
    return requests.get(f"{API}/list-tasks/{user_id}")

def get_task(id: str) -> dict:
    return requests.get(f"{API}/get-task/{id}")


def delete_task(id: str) -> dict:
    return requests.delete(f"{API}/delete-task/{id}")


def update_task(payload: dict) -> dict:
    return requests.put(f"{API}/update-task", json=payload)