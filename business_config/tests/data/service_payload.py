from core import datetime

today = datetime.date.today()
yesterday = today - datetime.datetimedelta(days=1)
tomorrow = today + datetime.datetimedelta(days=1)

service_create_payload = {
    'key': 'key1',
    'value': 'value1',
    'date_valid_from': str(yesterday),
    'date_valid_to': str(tomorrow),
}

service_update_payload = {
    'key': 'key1',
    'value': 'value2',
    'date_valid_from': str(yesterday),
    'date_valid_to': str(tomorrow),
}
