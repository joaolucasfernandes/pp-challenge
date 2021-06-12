from requests.models import parse_header_links
from resources.clients.user_client import UserClient
from resources.utils.user_utils import *
import json

def test_successful_post_user():

    user = UserClient()
    create_user_request = user.create_a_valid_user()
    create_user_response_data = json.loads(create_user_request.content)

    user_id = create_user_response_data['data']['id']
    user_list = json.loads(user.get_users(last_page=True).content)['data']
    matches = search_values_in_a_json(user_list, 'id', user_id)

    assert create_user_request.status_code == 200
    assert create_user_response_data['code'] == 201
    assert len(matches) == 1
    assert user_id in matches

def test_successful_put_user():
    
    user = UserClient()
    create_user_request = user.create_a_valid_user()
    create_user_response_data = json.loads(create_user_request.content)

    user_data = create_user_response_data['data']
    user_id = user_data['id']
    original_name = user_data['name']
    original_email = user_data['email']

    put_payload = get_valid_user_payload()

    new_name = put_payload['name']
    new_email = put_payload['email']

    modified_user_request = user.put_user(payload=put_payload, token=user.get_auth_token(), id=user_id)
    modified_user_response_data = json.loads(modified_user_request.content)

    modified_user_data = json.loads(user.get_user(user_id).content)['data']

    assert modified_user_request.status_code == 200
    assert modified_user_response_data['code'] == 200
    assert modified_user_data['name'] == new_name
    assert modified_user_data['email'] == new_email

def test_successful_delete_user():
    pass

def test_unauthorized_post_user():
    pass

def test_unauthorized_put_user():
    pass

def test_unauthorized_delete_user():
    pass

def test_user_not_found_on_delete():
    pass

def test_user_not_found_on_put():
    pass

def test_post_with_empty_fields():
    pass














    

