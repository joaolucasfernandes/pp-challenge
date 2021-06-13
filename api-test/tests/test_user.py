from resources.clients.user_client import UserClient
from resources.utils.user_utils import *
import json
import pytest

@pytest.fixture
def create_new_user_and_return_data():
    user_client = UserClient()
    create_user_request = user_client.create_a_valid_user()
    user_data = json.loads(create_user_request.content)['data']
    return user_data

def test_successful_post_user():

    user_client = UserClient()
    create_user_request = user_client.create_a_valid_user()
    create_user_response_data = json.loads(create_user_request.content)

    user_id = create_user_response_data['data']['id']
    user_list = json.loads(user_client.get_users(last_page=True).content)['data']
    matched_users_with_user_id = search_and_return_values_from_a_field_in_a_json(user_list, 'id', user_id)

    assert create_user_request.status_code == 200
    assert create_user_response_data['code'] == 201
    assert len(matched_users_with_user_id) == 1
    assert user_id in matched_users_with_user_id

def test_successful_put_user(create_new_user_and_return_data):
    
    user_id = create_new_user_and_return_data['id']
    original_name = create_new_user_and_return_data['name']
    put_payload = get_valid_user_payload()
    new_name = put_payload['name']

    user_client = UserClient()

    modified_user_request = user_client.put_user(payload=put_payload, token=user_client.get_auth_token(), id=user_id)
    modified_user_response_data = json.loads(modified_user_request.content)

    modified_user_data = json.loads(user_client.get_user(user_id).content)['data']

    assert modified_user_request.status_code == 200
    assert modified_user_response_data['code'] == 200
    assert modified_user_data['name'] == new_name

def test_successful_delete_user(create_new_user_and_return_data):
    
    user_id = create_new_user_and_return_data['id']

    user_client = UserClient()

    delete_user_request = user_client.delete_user(token=user_client.get_auth_token(), id=user_id)
    delete_user_response_data = json.loads(delete_user_request.content)

    user_list = json.loads(user_client.get_users(last_page=True).content)['data']
    matched_users_with_user_id = search_and_return_values_from_a_field_in_a_json(user_list, 'id', user_id)

    get_user_after_removing_request = user_client.get_user(user_id)
    get_user_after_removing_response_data = json.loads(get_user_after_removing_request.content)

    assert delete_user_request.status_code == 200
    assert delete_user_response_data['code'] == 204
    assert get_user_after_removing_request.status_code == 200
    assert get_user_after_removing_response_data['code'] == 404 
    assert get_user_after_removing_response_data['data']['message'] == 'Resource not found'
    assert len(matched_users_with_user_id) == 0
    assert user_id not in matched_users_with_user_id

def test_unauthorized_post_user():

    """
    The creation of the user before the request with wrong credentials is necessary to test this scenario because 
    the HTTP Not Found errors are having precedence on Authentication errors in the app.
    If the authentication is verified before checking if the resource exists, this will not be necessary.
    In my opinion, this is a bug, and should be fixed on the application.
    """
    user_client = UserClient()
    payload = get_valid_user_payload()
    post_user_request_with_invalid_token = user_client.post_user(payload, 'DummyToken')
    post_user_response_with_invalid_token_data = json.loads(post_user_request_with_invalid_token.content)

    assert post_user_request_with_invalid_token.status_code == 200
    assert post_user_response_with_invalid_token_data['code'] == 401
    assert post_user_response_with_invalid_token_data['data']['message'] == 'Authentication failed'

def test_unauthorized_put_user(create_new_user_and_return_data):

    """
    The creation of the user before the request is necessary to test this scenario because 
    the HTTP Not Found erros are having precedence on Authentication errors in the app.
    If the authentication is verified before checking if the resource exists, this will not be necessary.
    In my opinion, this is a bug, and should be fixed on the application.
    """
    user_id = create_new_user_and_return_data['id']
    original_name = create_new_user_and_return_data['name']

    put_payload = get_valid_user_payload()
    
    user_client = UserClient()
    put_user_request_with_invalid_token = user_client.put_user(payload=put_payload, token='DummyToken', id=user_id)
    put_user_with_invalid_token_response_data = json.loads(put_user_request_with_invalid_token.content)

    assert put_user_request_with_invalid_token.status_code == 200
    assert put_user_with_invalid_token_response_data['code'] == 401
    assert put_user_with_invalid_token_response_data['data']['message'] == 'Authentication failed'

def test_unauthorized_delete_user(create_new_user_and_return_data):

    """
    The creation of the user before the request is necessary to test this scenario because 
    the HTTP Not Found errors are having precedence on Authentication errors in the app.
    If the authentication is verified before checking if the resource exists, this will not be necessary.
    In my opinion, this is a bug, and should be fixed on the application.
    """
    user_id = create_new_user_and_return_data['id']

    user_client = UserClient()
    delete_user_request_with_invalid_token = user_client.delete_user(token='Dummy Token', id=user_id)
    delete_user_with_invalid_token_response_data = json.loads(delete_user_request_with_invalid_token.content)
    
    assert delete_user_request_with_invalid_token.status_code == 200
    assert delete_user_with_invalid_token_response_data['code'] == 401
    assert delete_user_with_invalid_token_response_data['data']['message'] == 'Authentication failed'

def test_user_not_found_on_delete():

    user_client = UserClient()

    delete_user_request = user_client.delete_user(token=user_client.get_auth_token(), id='XXXXX')
    delete_user_response_data = json.loads(delete_user_request.content)

    assert delete_user_request.status_code == 200
    assert delete_user_response_data['code'] == 404
    assert delete_user_response_data['data']['message'] == 'Resource not found'
    
def test_user_not_found_on_put():

    user_client = UserClient()

    put_user_request = user_client.put_user(payload=user_client.get_auth_token(), token='DummyToken', id='XXXXX')
    put_user_response_data = json.loads(put_user_request.content)

    assert put_user_request.status_code == 200
    assert put_user_response_data['code'] == 404
    assert put_user_response_data['data']['message'] == 'Resource not found'

@pytest.mark.parametrize("field, expected_message", 
                            [("name", "can't be blank"),
                             ("email", "can't be blank"),
                             ("gender", "can't be blank"),
                             ("status", "can't be blank")]
                        )
def test_post_user_with_empty_fields(field, expected_message):

    user_client = UserClient()
    request_payload = get_valid_user_payload()
    request_payload[field] = None

    expected_error_message_payload = {'field': field, 'message': expected_message}

    post_user_request_with_empty_fields = user_client.post_user(request_payload, user_client.get_auth_token())
    post_user_response_with_empty_fields_data = json.loads(post_user_request_with_empty_fields.content)

    matched_error_responses = search_and_return_objects_from_matched_field_in_a_json(post_user_response_with_empty_fields_data['data'], 'field', field)

    assert post_user_request_with_empty_fields.status_code == 200
    assert post_user_response_with_empty_fields_data['code'] == 422
    assert len(matched_error_responses) == 1
    assert matched_error_responses[0] == expected_error_message_payload

@pytest.mark.parametrize("field, invalid_value, expected_message", 
                            [("email", "x", "is invalid"),
                             ("gender", "y", "can be Male or Female" ),
                             ("status", "z", "can be Active or Inactive")]
                        )
def test_post_user_with_invalid_fields(field, invalid_value, expected_message):

    user_client = UserClient()
    request_payload = get_valid_user_payload()
    request_payload[field] = invalid_value

    expected_error_message_payload = {'field': field, 'message': expected_message}

    post_user_request_with_invalid_fields = user_client.post_user(request_payload, user_client.get_auth_token())
    post_user_response_with_invalid_fields_data = json.loads(post_user_request_with_invalid_fields.content)

    matched_error_responses = search_and_return_objects_from_matched_field_in_a_json(post_user_response_with_invalid_fields_data['data'], 'field', field)

    assert post_user_request_with_invalid_fields.status_code == 200
    assert post_user_response_with_invalid_fields_data['code'] == 422
    assert len(matched_error_responses) == 1
    assert matched_error_responses[0] == expected_error_message_payload