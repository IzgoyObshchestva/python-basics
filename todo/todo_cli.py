import json
from datetime import datetime
# from collections import deque
import os
import platform

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

class TodoCLI:
    def __init__(self, manager):
        self.manager = manager

    @staticmethod
    def _clear_consol():
        sistem = platform.system()
        if sistem == "Windows":
            os.system("cls")
        else:
            os.system("clear")

    def run(self):
        while True:
            self._clear_consol()
            self._show_menu()
            choice = input("Введите номер действия: ")
            match choice:
                case "1":
                    self._clear_consol()
                    self.manager.show_tasks()
                case "2":
                    self._clear_consol()
                    title = input("Введите название задачи: ")
                    res = self.manager.add_task(title)
                    print(res)
                case "3":
                    self._clear_consol()
                    try:
                        task_id = int(input("Введите ID задачи для удаления: "))
                        res = self.manager.delete_task(task_id)
                        print(res)
                    except ValueError:
                        print("Неверный ID.")
                case "4":
                    self._clear_consol()
                    try:
                        task_id = int(input("Введите ID задачи для смены статуса: "))
                        res = self.manager.mark_done(task_id)
                        print(res)
                    except ValueError:
                        print("Неверный ID.")
                case "5":
                    self._clear_consol()
                    print("Программа успешно завершина")
                    break
                case _:
                    self._clear_consol()
                    print(f'Неверный выбор')
            input('Нажмите Enter чтобы продолжить...')

    @staticmethod
    def _show_menu():
        print("Меню:")
        print("1. Показать задачи")
        print("2. Добавить задачу")
        print("3. Удалить задачу")
        print("4. Отметить задачу выполненной/невыполненной")
        print("5. Выход")

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


if __name__ == '__main__':
    path = "todo/todo.json"
    manager = TodoManager(path)
    app = TodoCLI(manager)
    app.run()