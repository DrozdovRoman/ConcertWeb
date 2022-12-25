from http.client import OK
import requests
import fake_useragent

# Входные данные:
# Словарь данных Qtickets Аккаунтов формата
# QticketsAccountInfo = {
    # "admin11" : # Данные от аккаунта Руслана
    #     {
    #     'login' : 'Логин',
    #     'password' : 'Пароль',
    #     '_session_key' : 'Ключ Сессии',
    #     '_token' : 'Токен',
    #     'postback' : '1'
    #     }, ...
# }

# Выходные Данные:
#   Словарь где,
#       key: название аккаунта
#       value: переменная сессии аккаунта

def CreateSession(accountData):
    accountSessionDict = dict()
    user = fake_useragent.UserAgent().random
    for key, data in accountData.items():
        session = requests.Session()
        linkAuth = "https://qtickets.app/auth/signin"
        header = { "user-agent" : user }
        responce = session.post(linkAuth, data=data, headers=header).text
        accountSessionDict.update({key:session})

    return accountSessionDict