class BaseApi:
    """
    This url's can be replaced to an environment variable, when running on CI or other remote environments.
    """
    RAW_HOST = 'gorest.co.in'
    BASE_URL = 'https://{}/public-api'.format(RAW_HOST)

    def get_auth_token(self):
        """
        I changed the token passed on postman collection and use my own personal token from Go Rest Api... 
        I do this for avoid authentication failures due to token reset by the api creator.
        The token value that are hardcoded here can be replaced by a request to an auth endpoint that returns a token given a user/password(I did not find it for this api).
        For security reasons, this user and password should be obtained from environment variables or secrets(when talking about docker/kubernetes environment) also.
        """
        return 'Bearer a46a3a7240068a78f563b5dfe533c51a3b7ef4a695387212637b37aa983f402a'

    def get_default_headers(self, token):

        headers = {
            'Authorization': token,
            'Content-Type': 'application/json',
            'Host': self.RAW_HOST
        }
        return headers
