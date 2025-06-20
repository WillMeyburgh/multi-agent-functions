from dataclasses import asdict
from typing import List, Optional, TypedDict


class Link(TypedDict, total=False):
    type: str
    description: Optional[str]
    link: Optional[str]

class Task(TypedDict, total=False):
    title: str
    kind: str
    id: Optional[str]
    etag: Optional[str]
    updated: Optional[str]
    selfLink: Optional[str]
    parent: Optional[str]
    position: Optional[str]
    notes: Optional[str]
    status: Optional[str]
    due: Optional[str]
    completed: Optional[str]
    deleted: Optional[bool]
    hidden: Optional[bool]
    links: Optional[List[Link]]

    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        """
        Creates a Task object from a dictionary, typically received from the Google Tasks API.

        Args:
            data (dict): A dictionary containing task data with the following possible keys:
                - 'kind' (str, optional): Type of the resource. Defaults to "tasks#task".
                - 'id' (str, optional): Task identifier.
                - 'etag' (str, optional): ETag of the resource.
                - 'title' (str): Title of the task.
                - 'updated' (str, optional): Last modification time of the task (RFC 3339 timestamp).
                - 'selfLink' (str, optional): URL pointing to this task.
                - 'parent' (str, optional): Parent task identifier. This field is only set for subtasks.
                - 'position' (str, optional): String indicating the position of the task among its sibling tasks.
                - 'notes' (str, optional): Notes describing the task.
                - 'status' (str, optional): Status of the task. Can be "needsAction" or "completed".
                - 'due' (str, optional): Due date of the task (RFC 3339 timestamp).
                - 'completed' (str, optional): Completion date of the task (RFC 3339 timestamp).
                - 'deleted' (bool, optional): Flag indicating whether the task has been deleted.
                - 'hidden' (bool, optional): Flag indicating whether the task is hidden.
                - 'links' (List[dict], optional): Collection of links, where each link is a dictionary with 'type', 'description', and 'link' keys.

        Returns:
            Task: A Task object populated with the provided data.
        """
        links_data = data.get("links", [])
        links = [Link(type=link.get("type"), description=link.get("description"), link=link.get("link")) for link in links_data]

        return Task(
            kind=data.get("kind", "tasks#task"),
            id=data.get("id"),
            etag=data.get("etag"),
            title=data["title"],
            updated=data.get("updated"),
            selfLink=data.get("selfLink"),
            parent=data.get("parent"),
            position=data.get("position"),
            notes=data.get("notes"),
            status=data.get("status"),
            due=data.get("due"),
            completed=data.get("completed"),
            deleted=data.get("deleted"),
            hidden=data.get("hidden"),
            links=links,
        )
    
    def to_dict(self) -> dict:
        """
        Converts the Task object to a dictionary.

        Returns:
            dict: A dictionary representation of the Task object.
        """
        return asdict(self)

    def __repr__(self):
        return f"Task(id={self.id}, title={self.title})"
