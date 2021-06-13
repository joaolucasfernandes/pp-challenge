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
        This can be replaced by a request to an auth endpoint that returns a token given a user/password.
        For security reasons, this user and password should be obtained from environment variables also.
        """
        return 'Bearer 4036e8a535449c1e91050813efe1a72e0d10150c410e152295b82b36e362f310'

    def get_default_headers(self, token):

        headers = {
            'Authorization': token,
            'Content-Type': 'application/json',
            'Host': self.RAW_HOST
        }
        return headers
