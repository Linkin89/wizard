import requests


class MailhogApi:

    def __init__(self, host, headers=None):
        self.host = host
        self.headers = headers

    
    def get_api_v2_messages(self, limit=10):
        """Получение писем"""
        # Получение писем
        params = {
            'limit': limit,
        }
        response = requests.get(url = f'{self.host}/api/v2/messages', params=params, verify=False)
        assert response.status_code == 200, "Не получили письма!"
        return response