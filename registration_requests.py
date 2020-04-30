import requests


def get_user(telegram_id):
    response = requests.get('https://medic-bot-site.herokuapp.com/users/', data={
        'telegram_id': telegram_id
    })
    return response


def send_registration_request(telegram_id, user_type, first_name, last_name, phone_number):
    response = requests.post('https://medic-bot-site.herokuapp.com/users/', data={
        'telegram_id': telegram_id,
        'type': user_type,
        'first_name': first_name,
        'last_name': last_name,
        'phone_number': phone_number
    })
    return response


def send_user_deletion_request(telegram_id):
    response = requests.delete(f'https://medic-bot-site.herokuapp.com/delete-user/{telegram_id}/')
    return response
