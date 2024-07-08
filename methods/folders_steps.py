import json

def create_folder(session, folder_path, create_folder_data):
    headers = {
        'Content-Type': 'application/json',
    }
    response = session.request('post', folder_path, headers=headers, data=json.dumps(create_folder_data))
    response_json = json.loads(response.text)
    print(response_json)
    return  response