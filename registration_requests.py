import requests


def send_registration_request(telegram_id, user_type, first_name, last_name, phone_number):
    response = requests.post('http://127.0.0.1:8000/users/', data={
        'telegram_id': telegram_id,
        'type': user_type,
        'first_name': first_name,
        'last_name': last_name,
        'phone_number': phone_number
    })
    return response


def send_user_deletion_request(telegram_id):
    response = requests.delete(f'http://127.0.0.1:8000/delete-user/{telegram_id}/')
    return response
