import json
import requests


def get_stiket(ID):
    try:
        if int(ID) > 0:
            gets = requests.get('https://paladinbot.pythonanywhere.com/dbu/?method=get_stiker&id={}'.format(ID)).json()
            return gets
        else:
            'DBU_EROR: user_id должен быть больше 0'
    except Exception as e:
        print(e)
        return 'DBU_EROR: user_id должен быть числом.'
