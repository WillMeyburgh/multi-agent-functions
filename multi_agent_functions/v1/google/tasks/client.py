
import os
from pathlib import Path
import pickle
from typing import List
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from time import sleep # Added for potential delays

from multi_agent_functions.v1.google.tasks.model.task import Task
from multi_agent_functions.v1.google.tasks.model.tasklist import TaskList

class GoogleTasksClient:
    def __init__(self):
        """
        Initializes the GoogleTasksClient by setting up credentials and the Google Tasks API service.
        """
        self.credentials = self.__get_credentials()
        self.service = build('tasks', 'v1', credentials=self.credentials)
        self._call_count = 0
        self._rebuild_threshold = 50 # Rebuild service after this many API calls

    def _rebuild_service(self):
        """
        Rebuilds the Google Tasks API service to refresh connections and release resources.
        """
        self.service = build('tasks', 'v1', credentials=self.credentials)
        print("GoogleTasksClient: Service rebuilt due to call threshold.")

    def _execute_and_manage_service(self, api_request_object):
        """
        Executes an API request, increments call count, and rebuilds service if threshold is met.
        """
        self._call_count += 1
        if self._call_count >= self._rebuild_threshold:
            self._rebuild_service()
            self._call_count = 0 # Reset count after rebuild
        # Add a small delay to prevent overwhelming the API or for resource cleanup
        sleep(0.05)
        return api_request_object.execute()

    def __get_credentials(self):
        """
        Retrieves user credentials for Google Tasks API.
        It first tries to load credentials from a pickle file. If not found or expired,
        it initiates the OAuth 2.0 flow to get new credentials and saves them.

        Returns:
            google.oauth2.credentials.Credentials: The user's Google API credentials.
        """
        Path('tmp').mkdir(exist_ok=True)
        SCOPES = ['https://www.googleapis.com/auth/tasks'] # Changed scope to allow read/write access
        creds = None
        if os.path.exists('tmp/google-tasks-token.pickle'):
            with open('tmp/google-tasks-token.pickle', 'rb') as token:
                creds = pickle.load(token)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            with open('tmp/google-tasks-token.pickle', 'wb') as token:
                pickle.dump(creds, token)
        return creds

    def __paging_collect(self, func, args, kwargs):
        """
        Helper function to collect all items from a paginated API response.

        Args:
            func (callable): The API function to call (e.g., self.service.tasklists().list).
            args (list): Positional arguments to pass to the API function.
            kwargs (dict): Keyword arguments to pass to the API function.

        Returns:
            list: A list of all collected items from the API.
        """
        items = []
        page_token = None
        while True:
            results = func(*args, **kwargs, pageToken=page_token).execute()
            items.extend(results.get('items', []))
            page_token = results.get('nextPageToken')
            if not page_token:
                break
        return items
    
    def tasklists_list(self) -> List[TaskList]:
        """
        Lists all task lists for the authenticated user.

        Returns:
            List[TaskList]: A list of TaskList objects.
        """
        tasklists = self.__paging_collect(
            self.service.tasklists().list,
            args=[],
            kwargs={}
        )
        return [TaskList.from_dict(tasklist) for tasklist in tasklists]

    def tasklists_delete(self, tasklist_id: str) -> None:
        """
        Deletes a specific task list.

        Args:
            tasklist_id (str): The ID of the TaskList to be deleted.
        """
        self._execute_and_manage_service(self.service.tasklists().delete(tasklist=tasklist_id))

    def tasklists_get(self, tasklist_id: str) -> TaskList:
        """
        Retrieves a specific task list by its ID.

        Args:
            tasklist_id (str): The ID of the task list to retrieve.

        Returns:
            TaskList: The retrieved TaskList object.
        """
        tasklist = self._execute_and_manage_service(self.service.tasklists().get(tasklist=tasklist_id))
        return TaskList.from_dict(tasklist)

    def tasklists_insert(self, title: str) -> TaskList:
        """
        Inserts a new task list.

        Args:
            title (str): The title for the new task list.

        Returns:
            TaskList: The newly created TaskList object.
        """
        tasklist_data = {"title": title}
        tasklist = self._execute_and_manage_service(self.service.tasklists().insert(body=tasklist_data))
        return TaskList.from_dict(tasklist)

    def tasklists_patch(self, tasklist_id: str, title: str) -> TaskList:
        """
        Partially updates a task list. This method supports patch semantics.

        Args:
            tasklist_id (str): The ID of the TaskList to update.
            title (str): The new title for the task list.

        Returns:
            TaskList: The updated TaskList object.
        """
        tasklist_data = {"title": title}
        tasklist = self._execute_and_manage_service(self.service.tasklists().patch(tasklist=tasklist_id, body=tasklist_data))
        return TaskList.from_dict(tasklist)

    def tasklists_update(self, tasklist_id: str, title: str) -> TaskList:
        """
        Updates a task list. This method replaces the entire task list resource.

        Args:
            tasklist_id (str): The ID of the TaskList to update.
            title (str): The new title for the task list.

        Returns:
            TaskList: The updated TaskList object.
        """
        tasklist_data = {"title": title}
        tasklist = self._execute_and_manage_service(self.service.tasklists().update(tasklist=tasklist_id, body=tasklist_data))
        return TaskList.from_dict(tasklist)

    def tasks_clear(self, tasklist_id: str) -> None:
        """
        Clears all completed tasks from a specified task list.

        Args:
            tasklist_id (str): The ID of the TaskList from which to clear completed tasks.
        """
        self._execute_and_manage_service(self.service.tasks().clear(tasklist=tasklist_id))

    def tasks_delete(self, tasklist_id: str, task_id: str) -> None:
        """
        Deletes a specific task from a task list.

        Args:
            tasklist_id (str): The ID of the TaskList containing the task.
            task_id (str): The ID of the Task to be deleted.
        """
        self._execute_and_manage_service(self.service.tasks().delete(tasklist=tasklist_id, task=task_id))

    def tasks_get(self, tasklist_id: str, task_id: str) -> Task:
        """
        Retrieves a specific task from a task list.

        Args:
            tasklist_id (str): The ID of the TaskList containing the task.
            task_id (str): The ID of the task to retrieve.

        Returns:
            Task: The retrieved Task object.
        """
        task = self._execute_and_manage_service(self.service.tasks().get(tasklist=tasklist_id, task=task_id))
        return task

    def tasks_insert(self, tasklist_id: str, title: str, notes: str = None, due: str = None) -> Task:
        """
        Inserts a new task into a specified task list.

        Args:
            tasklist_id (str): The ID of the TaskList where the task will be inserted.
            title (str): The title of the new task.
            notes (str, optional): The notes for the new task. Defaults to None.
            due (str, optional): The due date for the new task. Defaults to None.

        Returns:
            Task: The newly created Task object.
        """
        body = {'title': title, 'notes': notes, 'due': due}
        task = self._execute_and_manage_service(self.service.tasks().insert(tasklist=tasklist_id, body=body))
        return task

    def tasks_list(self, tasklist_id: str) -> List[Task]:
        """
        Lists all tasks in a specified task list.

        Args:
            tasklist_id (str): The ID of the TaskList from which to list tasks.

        Returns:
            List[Task]: A list of Task objects.
        """
        tasks = self.__paging_collect(
            self.service.tasks().list,
            args=[],
            kwargs={'tasklist': tasklist_id}
        )
        return tasks

    def tasks_patch(self, tasklist_id: str, task_id: str, title: str = None, notes: str = None, due: str = None) -> Task:
        """
        Partially updates a task in a specified task list. This method supports patch semantics.

        Args:
            tasklist_id (str): The ID of the TaskList containing the task.
            task_id (str): The ID of the Task to update.
            title (str, optional): The new title for the task. Defaults to None.
            notes (str, optional): The new notes for the task. Defaults to None.
            due (str, optional): The new due date for the task. Defaults to None.

        Returns:
            Task: The updated Task object.
        """
        body = {'title': title, 'notes': notes, 'due': due}
        task = self._execute_and_manage_service(self.service.tasks().patch(tasklist=tasklist_id, task=task_id, body=body))
        return task

    def tasks_update(self, tasklist_id: str, task_id: str, title: str = None, notes: str = None, due: str = None) -> Task:
        """
        Updates a task in a specified task list. This method replaces the entire task resource.

        Args:
            tasklist_id (str): The ID of the TaskList containing the task.
            task_id (str): The ID of the Task to update.
            title (str, optional): The new title for the task. Defaults to None.
            notes (str, optional): The new notes for the task. Defaults to None.
            due (str, optional): The new due date for the task. Defaults to None.

        Returns:
            Task: The updated Task object.
        """
        body = {'title': title, 'notes': notes, 'due': due}
        task = self._execute_and_manage_service(self.service.tasks().update(tasklist=tasklist_id, task=task_id, body=body))
        return task
