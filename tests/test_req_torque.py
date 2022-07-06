import allure
import pytest

from signal_states import GearState, BrakePedalState, AccPedalState
from contants import ErrorMsg


class TestReqTorqueState:
    @pytest.mark.parametrize('acc_pedal_state', [AccPedalState.PERCENT_30,
                                                 AccPedalState.PERCENT_50])
    @pytest.mark.parametrize('gear_shifter_state', [GearState.DRIVE, GearState.REVERSE])
    @allure.title('Switch ReqTorque state')
    def test_req_torque_state(self, client,
                              switch_gear_shifter_to_state, gear_shifter_state,
                              brake_pedal_pin,
                              acc_pedal_pin, acc_pedal_sig, acc_pedal_state, req_torque_sig):
        with allure.step(f'Set AccPedalPos to {acc_pedal_state}'):
            voltage = acc_pedal_pin.get_voltage_by_state(acc_pedal_state)
            acc_pedal_res = client.update_pin_by_id(pin_id=acc_pedal_pin.pin_id, voltage=voltage)
            assert acc_pedal_res.voltage == voltage, \
                ErrorMsg.RES_VOLTAGE_ERR.format(res_volt=acc_pedal_res.voltage, exp_volt=voltage)

        with allure.step(f'Set BrakePedalState to {BrakePedalState.RELEASED}'):
            released_voltage = brake_pedal_pin.get_voltage_by_state(BrakePedalState.RELEASED)
            brake_pedal_res = client.update_pin_by_id(pin_id=brake_pedal_pin.pin_id, voltage=released_voltage)
            assert brake_pedal_res.voltage == released_voltage, \
                ErrorMsg.RES_VOLTAGE_ERR.format(res_volt=brake_pedal_res.voltage, exp_volt=released_voltage)

        exp_state = acc_pedal_pin.get_reqtorque_by_state(acc_pedal_state)
        with allure.step(f'ReqTorque state should be equal to {exp_state}'):
            signal_value = client.get_signal_by_id(req_torque_sig.sig_id).value
            assert signal_value == exp_state, \
                ErrorMsg.SWITCH_STATE_ERR.format(act_state=signal_value, exp_state=exp_state)
