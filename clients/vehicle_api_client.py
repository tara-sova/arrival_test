import os
import requests
from requests import Response
from http import HTTPStatus
from models import PinModel, SignalModel
from typing import List, Callable
from singleton_decorator import singleton
from clients.logger import log_rest_request


@singleton
class VehicleApiClient:
    FORM_HEADERS = {'Accept': 'application/json', 'Content-Type': 'application/x-www-form-urlencoded'}
    JSON_HEADERS = {'Accept': 'application/json', 'Content-Type': 'application/json'}

    def __init__(self):
        self.url = os.getenv('API_URL', 'http://localhost:8099') + '/api'
        self.pins_url = f'{self.url}/pins'
        self.sigs_url = f'{self.url}/signals'

    def get_pins(self) -> List[PinModel]:
        resp = self._request(requests.get, url=self.pins_url, headers=self.JSON_HEADERS)
        return [PinModel.from_dict(pin_json) for pin_json in resp.json()]

    def get_pin_by_id(self, pin_id: int) -> PinModel:
        resp = self._request(requests.get, url=f'{self.pins_url}/{pin_id}', headers=self.JSON_HEADERS)
        return PinModel.from_dict(resp.json())

    def update_pin_by_id(self, pin_id: int, voltage: float) -> PinModel:
        data = {'Voltage': voltage}
        resp = self._request(requests.post,
                             url=f'{self.pins_url}/{pin_id}/update_pin', headers=self.FORM_HEADERS, data=data)
        return PinModel.from_dict(resp.json())

    def update_pins(self, pin_list: List[PinModel]):
        data = {'Pins': [pin.to_dict() for pin in pin_list]}
        resp = self._request(requests.post, url=f'{self.pins_url}/update_pins', headers=self.JSON_HEADERS, json=data)
        return [PinModel.from_dict(pin_json) for pin_json in resp.json()]

    def get_signals(self) -> List[SignalModel]:
        resp = self._request(requests.get, url=self.sigs_url, headers=self.JSON_HEADERS)
        return [SignalModel.from_dict(signal_json) for signal_json in resp.json()]

    def get_signal_by_id(self, sig_id: int) -> SignalModel:
        resp = self._request(requests.get, url=f'{self.sigs_url}/{sig_id}', headers=self.JSON_HEADERS)
        return SignalModel.from_dict(resp.json())

    def _request(self,
                 request_func: Callable,
                 expected_status_code: HTTPStatus = HTTPStatus.OK,
                 **kwargs) -> Response:
        resp = self.__request(request_func, **kwargs)
        assert resp.status_code == expected_status_code, \
            f'Unexpected value: {resp.status_code} instead of {expected_status_code}\n{resp.content}'
        return resp

    @staticmethod
    @log_rest_request
    def __request(request_func: Callable, **kwargs) -> Response:
        return request_func(**kwargs)
