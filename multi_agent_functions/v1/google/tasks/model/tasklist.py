from dataclasses import asdict, dataclass, field
from typing import Optional


@dataclass(frozen=True)
class TaskList:
    title: str
    kind: str = field(default="tasks#taskList")
    id: Optional[str] = None
    etag: Optional[str] = None
    updated: Optional[str] = None
    selfLink: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict) -> "TaskList":
        """
        Creates a TaskList object from a dictionary, typically received from the Google Tasks API.

        Args:
            data (dict): A dictionary containing task list data with the following possible keys:
                - 'kind' (str, optional): Type of the resource. Defaults to "tasks#taskList".
                - 'id' (str, optional): Task list identifier.
                - 'etag' (str, optional): ETag of the resource.
                - 'title' (str): Title of the task list.
                - 'updated' (str, optional): Last modification time of the task list (RFC 3339 timestamp).
                - 'selfLink' (str, optional): URL pointing to this task list.

        Returns:
            TaskList: A TaskList object populated with the provided data.
        """
        return TaskList(
            kind=data.get("kind", "tasks#taskList"),
            id=data.get("id"),
            etag=data.get("etag"),
            title=data["title"],
            updated=data.get("updated"),
            selfLink=data.get("selfLink"),
        )
    
    def to_dict(self) -> dict:
        """
        Converts the TaskList object to a dictionary.

        Returns:
            dict: A dictionary representation of the TaskList object.
        """
        return asdict(self)

    def __repr__(self):
        return f"TaskList(id={self.id}, title={self.title})"
