from faker import Faker
import json
        
def get_empty_user_payload():
    payload = {
        "name": None,
        "email": None,
        "gender": None,
        "status": None
    }
    return payload

def get_valid_user_payload():
    fake = Faker()
    payload = get_empty_user_payload()
    payload['name'] = fake.name()
    payload['email'] = fake.company_email()
    payload['gender'] = 'Female'
    payload['status'] = 'Active'
    return payload

def search_and_return_values_from_a_field_in_a_json(json, field, value):
    matches = []
    for data in json:
        if data[field] == value:
            matches.append(data[field])
    return matches

def search_and_return_objects_from_matched_field_in_a_json(json, field, value):
    matches = []
    for data in json:
        if data[field] == value:
            matches.append(data)
    return matches
