#!/usr/bin/env python3
'''
MIT License

Copyright (c) 2021 Autograders

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''
import os
import sys
import json
import zipfile
import argparse
import requests
from getpass import getpass
from tabulate import tabulate


# CLI title
__TITLE__ = '''

   ___       __                        __
  / _ |__ __/ /____  ___ ________ ____/ /__ _______
 / __ / // / __/ _ \/ _ `/ __/ _ `/ _  / -_) __(_-<
/_/ |_\_,_/\__/\___/\_, /_/  \_,_/\_,_/\__/_/ /___/
                   /___/

            Command Line Interface
               Autograders.org
'''

# Test flag
TEST = False
# API URL
API_URL = 'http://localhost:8080' if TEST else 'https://api.autograders.org'
# Sign Up URL
SIGN_UP_URL = f'{API_URL}/auth/signup'
# Sign In URL
SIGN_IN_URL = f'{API_URL}/auth/signin'
# Upload task URL
UPLOAD_TASK_URL = f'{API_URL}/task/upload'
# Get Task URL
GET_TASK_URL = f'{API_URL}/task/%s'
# Task stats URL
TASK_STATS_URL = f'{API_URL}/task/stats/%s'
# Autograder directory
AUTOGRADER_DIR = '.autograder'
# Autograder config file
AUTOGRADER_CFG = 'autograder.json'


def write_file(name, text):
    if not os.path.exists(AUTOGRADER_DIR):
        os.mkdir(AUTOGRADER_DIR)
    with open(os.path.join(AUTOGRADER_DIR, name), 'w') as f:
        f.write(text)
        f.close()


def read_file(name):
    with open(os.path.join(AUTOGRADER_DIR, name), 'r') as f:
        return f.read().strip()


def file_exists(name):
    return os.path.exists(os.path.join(AUTOGRADER_DIR, name))


def read_config():
    if not os.path.exists(AUTOGRADER_CFG):
        print(f'Autograder configuration file "{AUTOGRADER_CFG}" not found')
        sys.exit(1)
    try:
        with open(AUTOGRADER_CFG, 'r') as f:
            return json.loads(f.read().strip())
    except Exception:
        print(f'Could not parse autograder configuration file "{AUTOGRADER_CFG}"')
        sys.exit(1)


def register():
    try:
        print(__TITLE__)
        print('User Registration')
        print('')
        # set payload
        payload = {
            'fullName': input(' - Full Name: ').strip(),
            'email': input(' - Email: ').strip(),
            'password': getpass(' - Password: ').strip()
        }
        print('')
        r = requests.post(SIGN_UP_URL, json=payload)
        data = r.json()
        if r.status_code != 200:
            print(' [*] Error: ' + data['message'])
            sys.exit(1)
        else:
            print(' [*] Success: ' + data['message'])
            sys.exit(0)
    except:
        print(' [*] Fatal: Could not register user')
        sys.exit(1)


def login(force=False):
    try:
        if force:
            print('Enter credentials:')
            print('')
        # get cached token
        if not force and file_exists('auth'):
            return read_file('auth').split('|')
        # set payload
        payload = {
            'email': input(' - Email: ').strip(),
            'password': getpass(' - Password: ').strip()
        }
        print('')
        r = requests.post(SIGN_IN_URL, json=payload)
        data = r.json()
        if r.status_code != 200:
            print(' [*] Error: ' + data['message'])
            sys.exit(1)
        else:
            user_id = data['id']
            token = data['access_token']
            write_file('auth', f'{user_id}|{token}')
            return user_id, token
    except Exception:
        print(' [*] Fatal: Could not login')
        sys.exit(1)


def stats(force=False):
    try:
        print(__TITLE__)
        print('Get Task Stats')
        print('')
        config = read_config()
        task_id = config.get('id')
        user_id, token = login(force=force)
        headers = { 'Authorization': token }
        r = requests.get(TASK_STATS_URL % task_id, headers=headers)
        data = r.json()
        if r.status_code == 200:
            grade = data['grade']
            print(' - Queued: %s' % grade['queued'])
            print(' - Grade: %.2f/100' % grade['grade'] )
            print(' - Created At: ' + grade['createdAt'])
            print(' - Updated At: ' + grade['updatedAt'])
            details = grade['details']
            t = []
            for d in details:
                t.append([d['name'], d['grade'], d['message']])
            if len(t) > 0:
                print('')
                print('Details:')
                print('')
                print(tabulate(t, headers=['Name', 'Grade', 'Message'], tablefmt="fancy_grid"))
            stdout = grade['stdout'].strip()
            if stdout != '':
                print('')
                print('stdout:')
                print(grade['stdout'])
            stderr = grade['stderr'].strip()
            if stderr != '':
                print('')
                print('stderr:')
            print('')
            print(' [*] Success')
            sys.exit(1)
        elif not force and (r.status_code == 401 or r.status_code == 403):
            stats(force=True)
        else:
            print(' [*] Error: ' + data['message'])
            sys.exit(1)
    except Exception as e:
        print(e)
        print(' [*] Fatal: Could not get task stats')
        sys.exit(1)


def get_task_files(config, force=False):
    try:
        task_id = config.get('id')
        user_id, token = login(force=force)
        headers = { 'Authorization': token }
        r = requests.get(GET_TASK_URL % task_id, headers=headers)
        data = r.json()
        if r.status_code == 200:
            return data['task']['files']
        elif not force and (r.status_code == 401 or r.status_code == 403):
            return get_task_files(config, force=True)
        else:
            print(' [*] Error: ' + data['message'])
            sys.exit(1)
    except Exception:
        print(' [*] Fatal: Could not get task files')
        sys.exit(1)


def zip_files(files, task_id, user_id):
    try:
        filename = os.path.join(AUTOGRADER_DIR, f'{task_id}-{user_id}.zip')
        # create zip file
        with zipfile.ZipFile(filename, 'w', zipfile.ZIP_DEFLATED) as zip:
            # get all files to zip
            for f in files:
                zip.write(f)
            zip.close()
        return open(filename, 'rb'), filename
    except Exception:
        print(' [*] Fatal: Could not generate zip file')
        sys.exit(1)


def upload(force=False):
    try:
        print(__TITLE__)
        print('Upload Task')
        print('')
        config = read_config()
        task_id = config.get('id')
        files = get_task_files(config)
        user_id, token = login(force=force)
        headers = { 'Authorization': token }
        f, filename = zip_files(files, task_id, user_id)
        files = { 'task': f }
        r = requests.post(UPLOAD_TASK_URL, files=files, headers=headers)
        data = r.json()
        if r.status_code == 200:
            print(' [*] Success: ' + data['message'])
        elif not force and (r.status_code == 401 or r.status_code == 403):
            upload(force=True)
        else:
            print(' [*] Error: ' + data['message'])
            sys.exit(1)
    except Exception:
        print(' [*] Fatal: Could not upload task')
        sys.exit(1)


def autograder(args):
    '''Autograder CLI'''
    try:
        if args.upload:
            upload()
        elif args.stats:
            stats()
        elif args.register:
            register()
    except KeyboardInterrupt:
        pass


def main():
    parser = argparse.ArgumentParser(description='Autograders Command Line Interface')
    parser.add_argument('--upload', action='store_true', help='Upload files to autograder')
    parser.add_argument('--stats', action='store_true', help='Get task stats')
    parser.add_argument('--register', action='store_true', help='Register user')
    args = parser.parse_args()
    autograder(args)


if __name__ == '__main__':
    main()
