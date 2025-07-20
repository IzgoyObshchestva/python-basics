import json
import os
from datetime import datetime

class Task:
    def __init__(self, id, title, status="peding", created_at=None):
        self.id = id
        self.title = title
        self.status = status
        self.created_at = created_at or datetime.now().isoformat()

    def toggle_status(self):
        self.status = "done" if self.status == "pending" else "pending"

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "status": self.status,
            "created_at": self.created_at,
        }

    @staticmethod
    def from_dict(data):
        return Task(
            id=data["id"],
            title=data["title"],
            status=data.get("status", "pending"),
            created_at=data.get("created_at")
        )


class TodoManager:
    def __init__(self, path):
        self.path = path
        self.tasks = self.load_from_file()

    #Добавление задачи
    def add_task(self, title: str):
        new_id = self._get_next_id()
        task = Task(id=new_id, title=title)
        self.tasks.append(task)
        self.save_to_file()
        return "Задача добавлена."

    #Отметка выполнения задачи
    def mark_done(self, task_id: int):
        for task in self.tasks:
            if task.id == task_id:
                task.toggle_status()
                self.save_to_file()
                return f"Статус задачи №{task_id} изменён"
        return "Такой задачи нет"

    #Удаление задачи
    def delete_task(self, task_id: int):
        for task in self.tasks:
            if task.id == task_id:
                self.tasks.remove(task)
                self.save_to_file()
                return f"Задача №{task_id} удалена"
        return "Такой задачи нет"

    #Показать задачи
    def show_tasks(self):
        if not self.tasks:
            print("Нет задач")
        for task in self.tasks:
            status = "✔️  " if task.status == "done" else "❌ "
            print(f"{status} №{task.id}. {task.title} ({task.created_at})")
        
    
    #Сохранить в файл
    def save_to_file(self):
        data = [task.to_dict() for task in self.tasks]
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        with open(self.path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    #Загрузить из файла
    def load_from_file(self):
        try:
            with open(self.path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return [Task.from_dict(item) for item in data]
        except (FileNotFoundError, json.JSONDecodeError):
            return []
    
    def _get_next_id(self):
        if not self.tasks:
            return 1
        return max(task.id for task in self.tasks) + 1