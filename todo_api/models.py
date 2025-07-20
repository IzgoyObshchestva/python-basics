from pydantic import BaseModel
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