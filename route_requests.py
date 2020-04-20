import requests
import datetime


def create_datetime_object(time, date):
    str_date_and_time = f'{time} {date}'
    date_and_time = datetime.datetime.strptime(str_date_and_time, '%H.%M %d.%m.%Y')
    return date_and_time


def create_one_time_route_request(telegram_id, date_and_time, start_point, finish_point):
    response = requests.post('http://127.0.0.1:8000/routes/', json={
        'user': telegram_id,
        'date_and_time': date_and_time,
        'start_point': start_point,
        'finish_point': finish_point
    })
    return response


def create_regular_ride(telegram_id, start_point, finish_point):
    response = requests.post('http://127.0.0.1:8000/routes/', json={
        'user': telegram_id,
        'start_point': start_point,
        'finish_point': finish_point
    })
    return response


def create_route_request(**kwargs):
    start_point = {
        "latitude": kwargs['start_latitude'],
        "longitude": kwargs['start_longitude']
    }
    finish_point = {
        "latitude": kwargs['finish_latitude'],
        "longitude": kwargs['finish_longitude']
    }

    if kwargs['time_of_departure']:
        date_and_time = create_datetime_object(time=kwargs['time_of_departure'],
                                               date=kwargs['date_of_departure'])
        response = create_one_time_route_request(telegram_id=kwargs['telegram_id'],
                                                 date_and_time=date_and_time,
                                                 start_point=start_point,
                                                 finish_point=finish_point)
    else:
        response = create_regular_ride(telegram_id=kwargs['telegram_id'],
                                       start_point=start_point,
                                       finish_point=finish_point)

    return response

