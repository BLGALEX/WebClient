import os
import sys
from Client.Client import ClientClass

URL = 'http://159.65.207.158:5000'
USERNAME = "leha"
PASSWORD = "leha"
DATA_DIR = "data/"


def main():
    client = ClientClass(url=URL, username=USERNAME, password=PASSWORD)
    if not os.path.isdir(DATA_DIR):
        os.mkdir(DATA_DIR)
    print(f'Trying to register user {USERNAME}...')
    register_code = client.register()

    if register_code != 201:
        print('Ops, user already exist, trying to login...')
        register_code = client.login()
    if register_code == 201 or register_code == 200:
        print('Success!')
    while True:
        print('~#', end=' ')
        command = input().strip().split()
        try:
            if command[0] == 'exit':
                assert(len(command) == 1)
                break

            elif command[0] == 'addtask':
                assert (len(command) >= 2)
                task_title = ' '.join(command[1:])
                print(client.add_task(task_title))

            elif command[0] == 'renametask':
                assert (len(command) >= 3)
                task_title = ' '.join(command[2:])
                task_id = int(command[1])
                print(client.rename_task(task_id, task_title))

            elif command[0] == 'completetask':
                assert (len(command) == 2)
                task_id = int(command[1])
                print(client.complet_task(task_id))

            elif command[0] == 'removetask':
                assert (len(command) == 2)
                task_id = int(command[1])
                print(client.remove_task(task_id))

            elif command[0] == 'todo':
                assert (len(command) == 1)
                print(client.get_todo())

            elif command[0] == 'uploadfile':
                assert(len(command) == 2)
                path = command[1]
                print(client.upload_file(path))

            elif command[0] == 'downloadfile':
                assert(len(command) == 3)
                filename = command[1]
                downloadfilename = command[2]
                print(client.download_file(filename, os.path.join(DATA_DIR, downloadfilename)))

            elif command[0] == 'removefile':
                assert(len(command) == 2)
                filename = command[1]
                print(client.remove_file(filename))

            elif command[0] == 'files':
                assert(len(command) == 1)
                print(client.get_files())

            else:
                raise Exception()
        except Exception:
            print('Fail, wrong command!')


if __name__ == '__main__':
    main()

