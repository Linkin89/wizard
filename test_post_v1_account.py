import json
from pprint import pprint
import datetime
from dm_api_account.apis.account_api import AccountApi
from dm_api_account.apis.login_api import LoginApi
from api_mailhog.apis.mailhog_api import MailhogApi


# Регистрация нового пользователя
def test_post_v1_aacount():
    """Регистрация нового пользователя"""

    account_api = AccountApi(host="http://5.63.153.31:5051")
    login_api = LoginApi(host="http://5.63.153.31:5051")
    mailhog_api = MailhogApi(host="http://5.63.153.31:5025")

    login = f'vadimk{datetime.datetime.now().strftime("%d_%H_%M_%S")}'
    email = f'{login}@gmail.com'
    password = "ololo123"

    json_data = {
        'login': login,
        'email': email,
        'password': password,
    }

    response = account_api.post_v1_account(json_data)
    pprint(response.status_code)
    pprint(response.text)
    assert response.status_code == 201, f"Статус код дожен быть 201, а получили {response.status_code}"

    # Получение писем
    response = mailhog_api.get_api_v2_messages()

    # Получение активационного токена
    token = get_activation_token(response, email)

    # Активация пользователя
    response = account_api.put_v1_account_token(token)
    pprint(response.status_code)
    pprint(response.text)
    assert response.status_code == 200, "Не удалось активировать пользователя"

    # # Авторизация пользователя
    json_data = {
        'login': login,
        'password': password,
        'rememberMe': True,
    }

    response = login_api.post_v1_account_login(json_data)
    pprint(response.status_code)
    pprint(response.text)
    assert response.status_code == 200, "Не удалось авторизоваться"


def get_activation_token(response, email):
    """Получение токена по email пользователя"""

    # Получение токена
    token = None
    for item in response.json()["items"]:
        if item['Content']['Headers']['To'][0] == email:
            token = json.loads(item['Content']['Body']).get(
                'ConfirmationLinkUrl').split('/')[-1]
    assert token is not None, "Не получили токен!"
    return token
