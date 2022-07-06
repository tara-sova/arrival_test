import allure
import pytest

from signal_states import AccPedalState
from contants import ErrorMsg


class TestAccPedalPosState:
    @pytest.mark.parametrize('acc_pedal_state', [AccPedalState.ERROR,
                                                 AccPedalState.PERCENT_0,
                                                 AccPedalState.PERCENT_30,
                                                 AccPedalState.PERCENT_50,
                                                 AccPedalState.PERCENT_100])
    @allure.title('Switch AccPedalPos state')
    def test_acc_pedal_pos(self, client,
                           acc_pedal_pin, acc_pedal_sig, acc_pedal_state):
        with allure.step(f'Switch AccPedalPos state to {acc_pedal_state}'):
            voltage = acc_pedal_pin.get_voltage_by_state(acc_pedal_state)
            acc_pedal_pos_state_res = client.update_pin_by_id(pin_id=acc_pedal_pin.pin_id,
                                                              voltage=voltage)
            assert acc_pedal_pos_state_res.voltage == voltage, \
                ErrorMsg.RES_VOLTAGE_ERR.format(res_volt=acc_pedal_pos_state_res.voltage,
                                                exp_volt=acc_pedal_pos_state_res)
            signal_value = client.get_signal_by_id(acc_pedal_sig.sig_id).value
            assert signal_value == acc_pedal_state, \
                ErrorMsg.SWITCH_STATE_ERR.format(act_state=signal_value, exp_state=acc_pedal_state)
