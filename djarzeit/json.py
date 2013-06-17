from copy import deepcopy
from datetime import datetime


JSON_TEMPLATE_TO_CLIENT = {
    'error': False,
    'error_msg': '',
    'server_time': None,
    'data': {},
}

JSON_TEMPLATE_TO_SERVER = {
    'client_time': None,
    'data': {},
}


TIME_FORMAT = '%Y-%m-%d %H:%M:%S'

def get_new_json_response():
    response = deepcopy(JSON_TEMPLATE_TO_CLIENT)
    response['server_time'] = datetime.now().strftime(TIME_FORMAT)
    return response
