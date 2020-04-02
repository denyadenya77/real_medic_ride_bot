GET_USER_STATUS, GET_USER_CONTACT, GET_START_POINT, GET_FINISH_POINT, GET_DEPARTURE_DATE, GET_DEPARTURE_TIME, \
 GET_RIDE_STATUS = map(chr, range(7))
DRIVER, DOCTOR = map(chr, range(7, 9))
ONE_TIME, REGULAR = map(chr, range(9, 11))
GET_DETAILS = chr(11)

# состояния для работы с совпадениями
GET_RESULT_LIST = chr(12)

# кнопки сброса данных регистрации и отмены
DELETE_DATA, STOP_ACTION = map(chr, range(12, 14))
CHOSE_DELETE_USER_DATA = chr(14)

