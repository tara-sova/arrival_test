import allure
from datetime import datetime


def __log_response(response, start: datetime, end: datetime):
    request = response.request
    allure_rest_attachment = 'REQUEST:\n' \
                             f'Headers: {request.headers}\n' \
                             f'Url: {request.url}\n' \
                             f'Method: {request.method}\n' \
                             f'{f"Body: {request.body}" if request.body else ""}\n\n' \
                             'RESPONSE:\n' \
                             f'Body: {response.content.decode()}\n' \
                             f'Status code: {response.status_code} {response.reason}\n' \
                             f'Start / End / Elapsed\t {start.time()} / {end.time()} / {end - start}'
    allure.attach(allure_rest_attachment, 'REST', allure.attachment_type.TEXT)


def log_rest_request(func):
    def wrapper(request_func, **kwargs):
        start = datetime.now()
        response = func(request_func, **kwargs)
        end = datetime.now()
        __log_response(response, start, end)
        return response

    return wrapper
