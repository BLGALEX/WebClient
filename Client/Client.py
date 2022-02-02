from collections import namedtuple
import json
from os import path
import requests
from urllib.parse import urljoin
import shutil

TodoElement = namedtuple('TodoElement', ['task_id', 'name', 'done'])


class ClientClass:
    USER_REGISTER = '/user/register/'
    USER_LOGIN = '/user/login/'
    TODO_ROUTE = '/todo/'
    FILES_STORAGE = '/files/'
    default_json = {
        "username": '',
        "password": ''
    }

    def __init__(self, url, username, password):
        self.url = url
        self.default_json['username'] = username
        self.default_json['password'] = password

    def register(self):
        data = self.default_json.copy()
        response = requests.post(urljoin(self.url, self.USER_REGISTER), data)
        return response.status_code

    def login(self):
        data = self.default_json.copy()
        response = requests.post(urljoin(self.url, self.USER_LOGIN), data)
        response.raise_for_status()
        return response.status_code

    def add_task(self, task_title):
        data = self.default_json.copy()
        data["title"] = task_title
        response = requests.post(urljoin(self.url, self.TODO_ROUTE), data=data)
        content = json.loads(response.content)
        response.raise_for_status()

        if response.status_code not in [200, 201]:
            return 'Something goes wrong!'

        return f'Created task with id {content["id"]}'

    def rename_task(self, task_id, task_title):
        data = self.default_json.copy()
        data['title'] = task_title
        response = requests.put(urljoin(self.url, path.join(self.TODO_ROUTE, str(task_id))), data=data)
        response.raise_for_status()

        if response.status_code not in [200, 201]:
            return 'Something goes wrong!'

        return f'Task with id {task_id} renamed to "{task_title}"'

    def complet_task(self, task_id):
        data = self.default_json.copy()
        data['complete'] = True
        response = requests.put(urljoin(self.url, path.join(self.TODO_ROUTE, str(task_id))), data=data)
        response.raise_for_status()

        if response.status_code not in [200, 201]:
            return 'Something goes wrong!'

        return f'Task completed!'

    def remove_task(self, task_id):
        data = self.default_json.copy()
        response = requests.delete(urljoin(self.url, path.join(self.TODO_ROUTE, str(task_id))), data=data)
        response.raise_for_status()
        if response.status_code not in [200, 201]:
            return 'Something goes wrong!'

        return f'Deleted task with id {task_id}'

    def get_todo(self):
        data = self.default_json.copy()
        response = requests.get(urljoin(self.url, self.TODO_ROUTE), data=data)
        response.raise_for_status()

        if response.status_code not in [200, 201]:
            return 'Something goes wrong!'

        content = json.loads(response.content)
        result = ''
        for task in content["tasks"]:
            completed = "completed" if task["complete"] else "not completed"
            result += f'Task with id {task["id"]} and title {task["title"]} is {completed}!\n'
        return result

    def upload_file(self, filepath):
        data = self.default_json.copy()
        files = {'file': open(filepath, 'rb')}
        response = requests.post(urljoin(self.url, self.FILES_STORAGE), data=data, files=files)

        if response.status_code not in [200, 201]:
            return 'Something goes wrong!'
        content = json.loads(response.content)
        return f'File with id {content["id"]} was uploaded\nFile name {content["file"]} \nFile size {content["size"]}'

    def download_file(self, filename, filepath):
        data = self.default_json.copy()
        response = requests.get(urljoin(self.url, path.join(self.FILES_STORAGE, filename)), data=data, stream=True)
        response.raise_for_status()

        with open(filepath, 'wb') as f:
            response.raw.decode_content = True
            shutil.copyfileobj(response.raw, f)

        if response.status_code not in [200, 201]:
            return 'Something goes wrong!'

        return f'File was downloaded to {filepath}'

    def get_files(self):
        data = self.default_json.copy()
        response = requests.get(urljoin(self.url, self.FILES_STORAGE), data=data)

        if response.status_code not in [200, 201]:
            return 'Something goes wrong!'
        content = json.loads(response.content)
        res = ''
        for file in content:
            res += f'File id {file["id"]}\nFile name {file["file"]} \nFile size {file["size"]}'
            res += '\n_______________________________________\n'
        return res

    def remove_file(self, filename):
        data = self.default_json.copy()
        response = requests.delete(urljoin(self.url, path.join(self.FILES_STORAGE, filename)), data=data)
        response.raise_for_status()

        if response.status_code not in [200, 201]:
            return 'Something goes wrong!'

        return f'File {filename} was removed'