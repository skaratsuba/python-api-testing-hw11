import os

import pytest
from dotenv import load_dotenv
from pytest_steps import test_steps

from helpers.session import Session
from methods.space_steps import method_space, create_space_body

load_dotenv()
base_url = os.getenv('BASE_URL')

session = Session(base_url=os.getenv('BASE_URL'))

space_url = '/space/90152401675'
header_app_json = {
    'Content-Type': 'application/json',
}


@pytest.mark.parametrize('test_name, team_id, expected_status_code, archived',
                         [('Get list of active spaces for specific team_id', '9015704772', 200, None),
                          ('Get list of archived spaces for specific team_id', '9015704772', 200, True),
                          ('Get list of spaces for not existed team_id', '999999999999999999', 401, None),
                          ('Get list of spaces for not valid team_id', 'ttt', 400, None)])
def test_get_list_spaces(test_name, team_id, expected_status_code, archived):
    space_body = create_space_body('false', 'true')

    if archived is True:
        get_list_spaces_response, get_list_spaces_response_json = method_space('get', session,
                                                                               '/team/' + team_id + '/space?archived'
                                                                                                    '=true',
                                                                               space_body)
        assert get_list_spaces_response.status_code == expected_status_code
        assert get_list_spaces_response_json['spaces'][0]['id'] == '90152402010'

    else:
        get_list_spaces_response, get_list_spaces_response_json = method_space('get', session,
                                                                               '/team/' + team_id + '/space',
                                                                               space_body)

        assert get_list_spaces_response.status_code == expected_status_code

        if expected_status_code == 200:
            assert get_list_spaces_response_json['spaces'][0]['id'] == '90152681230'


@test_steps('Create space for specific team_id',
            'Create space with the same name for specific team_id', 'DELETE space', 'Create space for specific '
                                                                                    'team_id without the required '
                                                                                    'field "name"', 'Create space for '
                                                                                                    'specific team_id '
                                                                                                    'with invalid json')
def test_create_space():
    space_body = create_space_body()
    create_space_response, create_space_response_json = method_space('post', session, '/team/9015704772/space',
                                                                     space_body)
    assert create_space_response.status_code == 200
    space_id = create_space_response_json['id']
    get_space_response = session.request('get', '/space/' + space_id)
    assert get_space_response.status_code == 200
    yield

    create_space_same_name_response, create_space_same_name_response_json = method_space('post', session,
                                                                                         '/team/9015704772/space',
                                                                                         space_body)
    assert create_space_same_name_response.status_code == 400
    err_message_exist = 'Space with this name already exists'
    assert create_space_same_name_response_json.get('err') == err_message_exist
    yield

    delete_space_response, delete_space_response_json = method_space('delete', session, '/space/' + space_id,
                                                                     space_body)
    assert delete_space_response.status_code == 200
    yield

    space_body_no_name = create_space_body('false', 'true')
    create_space_no_name_response, create_space_no_name_response_json = method_space('post', session,
                                                                                     '/team/9015704772/space',
                                                                                     space_body_no_name)
    assert create_space_no_name_response.status_code == 400
    err_message_invalid = 'Space name invalid'
    assert create_space_no_name_response_json.get('err') == err_message_invalid
    yield

    space_body_bad_json = '{name:,'
    create_space_bad_json_response, create_space_bad_json_response_json = method_space('post', session,
                                                                                       '/team/9015704772/space',
                                                                                       space_body_bad_json)
    assert create_space_bad_json_response.status_code == 400
    err_message_bad_json = 'Unexpected token " in JSON at position 0'
    assert create_space_bad_json_response_json.get('err') == err_message_bad_json
    yield


@pytest.mark.parametrize('test_name, space_id, expected_status_code',
                         [('Get space details of specific space_id', '90152681230', 200),
                          ('Get details of not existed space_id', '999999999999999999', 401),
                          ('Get details of not valid space_id', 'SSS', 400)])
def test_get_space(test_name, space_id, expected_status_code):
    get_space_response = session.request('get', '/space/' + space_id)
    assert get_space_response.status_code == expected_status_code


@pytest.mark.parametrize('test_name, space_id, expected_status_code, manage_flag, make_json_empty',
                         [
                             ('Update space name by specific space_id', '90152681230', 200, 'false', 'false'),
                             ('Update space name by not existed space_id', '0', 401, 'false', 'false'),
                             ('Update space by specific space_id with empy json', '90152681230', 400, 'false', 'true'),
                             ('Update space by specific space_id with the parameter "admin_can_manage=true"',
                              '90152681230', 403, 'true', 'false')
                         ])
def test_update_space(test_name, space_id, expected_status_code, manage_flag, make_json_empty):
    space_body = create_space_body(manage_flag, make_json_empty)
    put_space_response, put_space_response_json = method_space('put', session, '/space/' + space_id, space_body)

    assert put_space_response.status_code == expected_status_code

    if expected_status_code == 200:
        assert put_space_response_json['name'] == space_body['name']

    if manage_flag == 'true':
        err_message = 'Allowing admins to manage Spaces is an Enterprise Plan feature'
        assert put_space_response_json.get('err') == err_message


@test_steps('Create space', 'DELETE space', 'Check if deleted')
def test_delete_by_space_id():
    print('Delete space by specific space_id')
    space_body = create_space_body()
    create_space_response, create_space_response_json = method_space('post', session, '/team/9015704772/space',
                                                                     space_body)
    assert create_space_response.status_code == 200
    space_id = create_space_response_json['id']
    yield

    delete_space_response, delete_space_response_json = method_space('delete', session, '/space/' + space_id,
                                                                     space_body)
    assert delete_space_response.status_code == 200
    yield

    get_space_response = session.request('get', '/space/' + space_id)
    assert get_space_response.status_code == 404
    yield


@pytest.mark.parametrize('test_name, space_id, expected_status_code',
                         [('Delete space by not existed space_id', '9999999999999999999', 401),
                          ('Delete space by not valid space_id', 'sss', 400),
                          ('Delete space by space_id=0', '0', 401)])
def test_delete_space(test_name, space_id, expected_status_code):
    space_body = create_space_body()
    delete_space_response, delete_space_response_json = method_space('delete', session, '/space/' + space_id,
                                                                     space_body)
    assert delete_space_response.status_code == expected_status_code
