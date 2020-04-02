GET_USER_STATUS, GET_START_POINT, GET_FINISH_POINT, GET_DEPARTURE_DATE, GET_DEPARTURE_TIME, \
 GET_RIDE_STATUS = map(chr, range(6))
DRIVER, DOCTOR = map(chr, range(6, 8))
ONE_TIME, REGULAR = map(chr, range(8, 10))
GET_DETAILS = chr(10)

# состояния для работы с совпадениями
GET_RESULT_LIST = chr(11)
