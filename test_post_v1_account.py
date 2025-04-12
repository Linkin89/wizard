import json
from pprint import pprint
import requests
import datetime


# Регистрация нового пользователя
def test_post_v1_aacount():
    """Регистрация нового пользователя"""

    login = f'vadimk{datetime.datetime.now().strftime("%d_%H_%M_%S")}'
    email = f'{login}@gmail.com'
    password = "ololo123"

    json_data = {
        'login': login,
        'email': email,
        'password': password,
    }

    response = requests.post('http://5.63.153.31:5051/v1/account', json=json_data)
    pprint(response.status_code)
    pprint(response.text)
    assert response.status_code == 201, f"Статус код дожен быть 201, а получили {response.status_code}"
    
    # Получение токена
    token = get_activation_token(email)

    # Активация пользователя
    response = requests.put(f'http://5.63.153.31:5051/v1/account/{token}')
    pprint(response.status_code)
    pprint(response.text)
    assert response.status_code == 200, "Не удалось активировать пользователя"

    # # Авторизация пользователя
    json_data = {
        'login': login,
        'password': password,
        'rememberMe': True,
    }

    response = requests.post('http://5.63.153.31:5051/v1/account/login', json=json_data)
    pprint(response.status_code)
    pprint(response.text)
    assert response.status_code == 200, "Не удалось авторизоваться"

def get_activation_token(email):
    # Получение писем
    params = {
        'limit': '5',
    }

    response = requests.get('http://5.63.153.31:5025/api/v2/messages', params=params, verify=False)
    assert response.status_code == 200, "Не получили письма!"

    # Получение токена
    token = None
    for item in response.json()["items"]:
        if item['Content']['Headers']['To'][0] == email:
            token = json.loads(item['Content']['Body']).get('ConfirmationLinkUrl').split('/')[-1]
    assert token is not None, "Не получили токен!"
    return token