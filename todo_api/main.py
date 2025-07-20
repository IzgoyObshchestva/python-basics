from fastapi import FastAPI, HTTPException
from storage import TodoManager, Task

app = FastAPI()
store = TodoManager("todo_api/data.json")

@app.get("/tasks")
def get_tasks():
    return [task.to_dict() for task in store.tasks]

@app.post("/tasks")
def add_task(title: str):
    new_id = max((t.id for t in store.tasks), default=0) + 1
    task = Task(id=new_id, title=title)
    store.add_task(task)
    return task.to_dict()

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    success = store.delete_task(task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task deleted"}