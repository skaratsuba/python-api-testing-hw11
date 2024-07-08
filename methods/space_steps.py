import json
import random
import string
import time

def method_space(method, session, space_path, space_body):
    headers = {
        'Content-Type': 'application/json',
    }
    response = session.request(method, space_path, headers=headers, data=json.dumps(space_body))
    response_json = json.loads(response.text)
    print(response_json)
    time.sleep(2)
    return response, response_json


def create_space_body(manage_flag='false', empty_json='false'):
    random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
    with open('TestData/create_update_space.json', 'r') as file:
        body = json.load(file)
        body['name'] = random_string
    if manage_flag == 'true':
        body['admin_can_manage'] = 'true'
    if empty_json == 'true':
        body = {}
    return body
