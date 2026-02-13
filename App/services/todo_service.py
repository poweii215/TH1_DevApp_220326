class TodoService:
    def __init__(self, repository):
        self.repository = repository

    def create_todo(self, data):
        return self.repository.create(data.title, data.is_done)

    def get_todo(self, todo_id: int):
        return self.repository.get_by_id(todo_id)

    def update_todo(self, todo_id: int, data):
        return self.repository.update(todo_id, data.title, data.is_done)

    def delete_todo(self, todo_id: int):
        return self.repository.delete(todo_id)

    def list_todos(self, is_done=None, q=None, sort="created_at", limit=10, offset=0):
        data = self.repository.get_all()

        # Filter
        if is_done is not None:
            data = [t for t in data if t["is_done"] == is_done]

        # Search
        if q:
            q_lower = q.lower()
            data = [t for t in data if q_lower in t["title"].lower()]

        # Sort
        reverse = sort.startswith("-")
        data.sort(key=lambda x: x["created_at"], reverse=reverse)

        total = len(data)

        # Pagination
        items = data[offset: offset + limit]

        return items, total
