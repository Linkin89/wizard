import requests


class AccountApi:

    def __init__(self, host, headers=None):
        self.host = host
        self.headers = headers

    def post_v1_account(self, json_data):
        """Регистрация нового пользователя
        :param json_data:
        :return:"""

        response = requests.post(
            url=f'{self.host}/v1/account', json=json_data)
        return response

    def put_v1_account_token(self, token):
        """Активация пользователя
        :param token:
        :return:"""

        response = requests.put(url = f'{self.host}/v1/account/{token}')
        return response
