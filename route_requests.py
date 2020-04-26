import requests
import datetime
import json


def create_datetime_object(time, date):
    str_date_and_time = f'{time} {date}'
    date_and_time = datetime.datetime.strptime(str_date_and_time, '%H.%M %d.%m.%Y')
    return date_and_time


def create_points(**kwargs):
    start_point = {
        "latitude": kwargs['start_latitude'],
        "longitude": kwargs['start_longitude']
    }
    finish_point = {
        "latitude": kwargs['finish_latitude'],
        "longitude": kwargs['finish_longitude']
    }
    return start_point, finish_point


def create_one_time_route_request(telegram_id, date_and_time, start_point, finish_point):
    response = requests.post('https://medic-bot-site.herokuapp.com/routes/', json={
        'user': telegram_id,
        'date_and_time': date_and_time,
        'start_point': start_point,
        'finish_point': finish_point
    })
    return response


def create_regular_ride(telegram_id, start_point, finish_point):
    response = requests.post('https://medic-bot-site.herokuapp.com/routes/', json={
        'user': telegram_id,
        'start_point': start_point,
        'finish_point': finish_point
    })
    return response


def create_route_request(**kwargs):

    start_point, finish_point = create_points(start_latitude=kwargs['start_latitude'],
                                              start_longitude=kwargs['start_longitude'],
                                              finish_latitude=kwargs['finish_latitude'],
                                              finish_longitude=kwargs['finish_longitude'])

    if kwargs.get('time_of_departure'):
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


def get_similar_routes_request(**kwargs):

    start_point, finish_point = create_points(start_latitude=kwargs['start_latitude'],
                                              start_longitude=kwargs['start_longitude'],
                                              finish_latitude=kwargs['finish_latitude'],
                                              finish_longitude=kwargs['finish_longitude'])

    if kwargs.get('time_of_departure'):
        date_and_time = create_datetime_object(time=kwargs['time_of_departure'],
                                               date=kwargs['date_of_departure'])

        response = requests.get('https://medic-bot-site.herokuapp.com/get_similar/', json={
            'telegram_id': kwargs['telegram_id'],
            'date_and_time': date_and_time,
            'start_point': start_point})
    else:
        response = requests.get('https://medic-bot-site.herokuapp.com/get_similar/', json={
            'telegram_id': kwargs['telegram_id'],
            'start_point': start_point})

    data = response.content.decode('utf-8')
    response = json.loads(data)
    return response










