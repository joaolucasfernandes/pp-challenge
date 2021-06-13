class BaseApi:
    """
    This url's can be replaced to an environment variable, when running on CI or other remote environments.
    """
    RAW_HOST = 'gorest.co.in'
    BASE_URL = 'https://{}/public-api'.format(RAW_HOST)

    def get_auth_token(self):
        """
        This can be replaced by a request to an auth endpoint that returns a token given a user/password.
        For security reasons, this user and password should be obtained from environment variables also.
        """
        return 'Bearer 2275e2cbbf8dc1d113b25fb018cdb2e07e088b35bb5f7b7c13ca160ed96a82ba'

    def get_default_headers(self, token):

        headers = {
            'Authorization': token,
            'Content-Type': 'application/json',
            'Host': self.RAW_HOST
        }
        return headers
