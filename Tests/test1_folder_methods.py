import json
import os
import random
import string

import pytest
from dotenv import load_dotenv
from pytest_steps import test_steps

from helpers.session import Session
from methods.folders_steps import create_folder

load_dotenv()
base_url = os.getenv('BASE_URL')

session = Session(base_url=os.getenv('BASE_URL'))

folder_url = '/space/90152401675/folder'
header_app_json = {
    'Content-Type': 'application/json',
}

@pytest.fixture
def create_folder_data():
    random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
    with open('../TestData/create_folder.json', 'r') as file:
        body = json.load(file)
        body['name'] = random_string
    return body


@test_steps('Get folder', 'POST foldr', 'Updte my folder')
@pytest.mark.parametrize('space_id, expected_status_code', [ ('90152401675',  200),('', 400), ('o87378127812', 400 )])
def test_get_folders(space_id, expected_status_code):
    get_folder_response =  session.request('get', '/space/'+ space_id + '/folder')
    assert (get_folder_response.status_code) == expected_status_code
    yield
    get_folder_response =  session.request('get', '/space/'+ space_id + '/folder')
    assert (get_folder_response.status_code) == expected_status_code
    yield
    get_folder_response =  session.request('get', '/space/'+ space_id + '/folder')
    assert (get_folder_response.status_code) == expected_status_code
    yield
#@
def test_post_folder(create_folder_data):

    post_folder_response =  session.request('post', folder_url,headers=header_app_json, data=json.dumps(create_folder_data))
    print(post_folder_response.text)
    assert (post_folder_response.status_code) == 200
#
#
@test_steps('Get folder', 'POST foldr')
def test_update_folder(create_folder_data):

    print("create folder")
    post_folder_response = create_folder(session, folder_url, create_folder_data)
    id = post_folder_response.json()['id']
    assert (id != 'undefined' )
    yield

    print("update folder")
    put_folder_response = session.request('put', '/folder/' + id ,headers=header_app_json, data=json.dumps(create_folder_data))
    assert put_folder_response.status_code == 200
    id = put_folder_response.json()['id']
    assert (id != 'undefined' )
    yield