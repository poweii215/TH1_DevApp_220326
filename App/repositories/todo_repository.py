from datetime import datetime


class TodoRepository:
    def __init__(self):
        self._todos = []
        self._next_id = 1

    def create(self, title: str, is_done: bool):
        todo = {
            "id": self._next_id,
            "title": title,
            "is_done": is_done,
            "created_at": datetime.utcnow()
        }
        self._todos.append(todo)
        self._next_id += 1
        return todo

    def get_all(self):
        return self._todos.copy()

    def get_by_id(self, todo_id: int):
        return next((t for t in self._todos if t["id"] == todo_id), None)

    def update(self, todo_id: int, title: str, is_done: bool):
        todo = self.get_by_id(todo_id)
        if todo:
            todo["title"] = title
            todo["is_done"] = is_done
        return todo

    def delete(self, todo_id: int):
        for i, todo in enumerate(self._todos):
            if todo["id"] == todo_id:
                self._todos.pop(i)
                return True
        return False
