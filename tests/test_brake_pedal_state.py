import allure
import pytest

from signal_states import GearState, AccPedalState
from contants import ErrorMsg
from signal_states import BrakePedalState, ReqTorqueState


class TestBrakePedalState:
    @pytest.mark.parametrize('brake_pedal_voltage', [2, 2.5, 2.99])
    @pytest.mark.parametrize('acc_pedal_value', [AccPedalState.PERCENT_0,
                                                 AccPedalState.PERCENT_30,
                                                 AccPedalState.PERCENT_50])
    @pytest.mark.parametrize('gear_shifter_state', [GearState.REVERSE])
    @allure.title('Switch BrakePedalState to Released')
    def test_brake_pedal_state_to_released(self, client,
                                           brake_pedal_voltage, acc_pedal_value,
                                           brake_pedal_pin, acc_pedal_pin, req_torque_sig,
                                           switch_gear_shifter_to_state, gear_shifter_state):
        with allure.step(f'Set BrakePedalState to {BrakePedalState.RELEASED}'):
            brake_pedal_res = client.update_pin_by_id(pin_id=brake_pedal_pin.pin_id, voltage=brake_pedal_voltage)
            assert brake_pedal_res.voltage == brake_pedal_voltage, \
                ErrorMsg.RES_VOLTAGE_ERR.format(res_volt=brake_pedal_res.voltage, exp_volt=brake_pedal_voltage)

        with allure.step(f'ReqTorque should be equal to {ReqTorqueState.NM_0}'):
            gear_pos_signal = client.get_signal_by_id(req_torque_sig.sig_id)
            assert gear_pos_signal.value == ReqTorqueState.NM_0

        exp_reqtorque_value = acc_pedal_pin.get_reqtorque_by_state(acc_pedal_value)
        with allure.step(f'ReqTorqueValue should be equal to {exp_reqtorque_value}'
                         f'after AccPedalPos was switched to {acc_pedal_value}'):
            client.update_pin_by_id(acc_pedal_pin.pin_id,
                                    acc_pedal_pin.get_voltage_by_state(acc_pedal_value))
            req_torque_state = client.get_signal_by_id(req_torque_sig.sig_id).value
            assert req_torque_state == exp_reqtorque_value, \
                ErrorMsg.SWITCH_STATE_ERR.format(act_state=req_torque_state, exp_state=exp_reqtorque_value)
