import requests
import os
import json
from ..utils.base_api import BaseApi
from ..utils.user_utils import *

class UserClient(BaseApi):

    def post_user(self, payload, token):
        headers = self.get_default_headers(token)
        response = requests.post('{}/users'.format(self.BASE_URL), headers=headers, json=payload)
        return response

    def get_users(self, last_page=False):
        page = '?page={}'.format(json.loads(requests.get('{}/users'.format(self.BASE_URL)).content)['meta']['pagination']['pages']) if last_page else ''
        response = requests.get('{}/users{}'.format(self.BASE_URL, page))
        return response

    def get_user(self, id):
        response = requests.get('{}/users/{}'.format(self.BASE_URL, id))
        return response

    def delete_user(self, id, token):
        headers = self.get_default_headers(token)
        response = requests.delete('{}/users/{}'.format(self.BASE_URL, id), headers=headers)
        return response

    def put_user(self, payload, token, id):        
        headers = self.get_default_headers(token)
        response = requests.put(url='{}/users/{}'.format(self.BASE_URL, id), headers=headers, json=payload)
        return response
    
    def create_a_valid_user(self):
       payload = get_valid_user_payload()
       response = self.post_user(token=self.get_auth_token(), payload=payload)
       return response