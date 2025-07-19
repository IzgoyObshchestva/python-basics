import json
from datetime import datetime
from collections import deque
import os
import platform

class Task:
    def __init__(self):
        self._start_task = True
        self._q = TodoManager()

    @staticmethod
    def _clear_consol():
        sistem = platform.system()
        if sistem == "Windows":
            os.system("cls")
        else:
            os.system("clear")

    def start(self):
        while self._start_task:
            self._clear_consol()
            value = self._function_selection()
            match value:
                case "1":
                    self._show_task()
                case "2":
                    self._add_task()
                case "3":
                    self._delete_task()
                case "4":
                    self._mark_done_task()
                case "5":
                    self._clear_consol()
                    self._q.save_to_file()
                    print("Программа успешно завершина")
                    break
                case _:
                    self._clear_consol()
                    print(f'Не верный выбор')
            input('Нажмите Enter чтобы продолжить...')

    def _show_task(self):
        self._clear_consol()
        self._q.show_tasks()

    def _add_task(self):
        self._clear_consol()
        valus = input("Введите название задачи: ")
        self._q.add_task(valus)

    def _delete_task(self):
        self._clear_consol()
        valus = input("Для удаления введите нормер задачи: ")
        self._q.delete_task(valus)

    def _mark_done_task(self):
        self._clear_consol()
        valus = input("Для изменения статуса введите нормер задачи: ")
        self._q.mark_done(valus)

    @staticmethod
    def _function_selection():
        print(f"Выберите что хотите сделать:\n1. Показать список задач\n2. Добавить задачу\n3. Удалить задачу\n4. Изменнить статус задачи\n5. Выход")
        return input('Введи число: ')



class TodoManager:
    def __init__(self):
        self._todo_list = self._load_from_file()

    #Добавление задачи
    def add_task(self, title: str):
        last_id = self._get_last_id()
        self._todo_list[last_id] = {"title": title,
        "status": "pending",
        "created_at": datetime.now().strftime('%d.%m.%Y')}
        print("Успешно добавлено")

    #Отметка выполнения задачи
    def mark_done(self, task_id: int):
        todo = self._todo_list
        if task_id in todo:
            if todo[task_id]["status"] == "pending":
                todo[task_id]["status"] = "done"
            else:
                todo[task_id]["status"] = "pending"
            print(f"Задача №{task_id} изменила свой статус")
        else:
            print("Такой задачи нет")

    #Удаление задачи
    def delete_task(self, task_id: int):
        if task_id in self._todo_list:
            del self._todo_list[task_id]
            print(f"Задача №{task_id} удалена")
        else:
            print("Такой задачи нет")

    #Показать задачи
    def show_tasks(self):
        for key, value in self._todo_list.items():
            stats = "✔️  " if value["status"] == "done" else "❌ "
            print(f"{stats}№{key}. {value["title"]} {value["created_at"]}")
        if self._todo_list == {}:
            print("Нет задач")
    
    #Сохранить в файл
    def save_to_file(self):
        with open('todo/todo.json', 'w', encoding='utf-8') as f:
            json.dump(self._todo_list, f, ensure_ascii=False, indent=4)

    #Загрузить из файла
    @staticmethod
    def _load_from_file():
        try:
            with open('todo/todo.json', 'r', encoding='utf-8') as f:
                date = json.load(f)
        except FileNotFoundError:
            print(1)
            with open('todo/todo.json', "w", encoding='utf-8') as f:
                date = {}
        except:
            date = {}
        return date
    
    def _get_last_id(self):
        if self._todo_list == {}:
            return "0"
        else:
            [last] = deque(self._todo_list, maxlen=1)
            return str(int(last)+1)


s = Task()

if __name__ == '__main__':
    s.start()