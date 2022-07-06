import allure
import pytest

from signal_states import GearState, BatteryState, BrakePedalState, AccPedalState
from contants import ErrorMsg


class TestBatteryState:
    @pytest.mark.parametrize('battery_voltage', [100, 400, 0.01])
    @pytest.mark.parametrize('gear_shifter_state', [GearState.PARK])
    @allure.title('Switch BatteryState to Ready')
    def test_battery_state_ready(self, client,
                                 battery_voltage,  battery_voltage_pin,
                                 gear_1_pin, gear_2_pin,
                                 gear_position_sig,
                                 switch_gear_shifter_to_state, gear_shifter_state):
        with allure.step(f'Set BatteryState to {BatteryState.NOT_READY}'):
            battery_state_res = client.update_pin_by_id(pin_id=battery_voltage_pin.pin_id,
                                                        voltage=battery_voltage)
            assert battery_state_res.voltage == battery_voltage, \
                ErrorMsg.RES_VOLTAGE_ERR.format(res_volt=battery_state_res.voltage, exp_volt=battery_voltage)

        with allure.step(f'GearPosition state should be equal to {GearState.NEUTRAL}'):
            gear_pos_signal = client.get_signal_by_id(gear_position_sig.sig_id)
            assert gear_pos_signal.value == GearState.NEUTRAL, \
                ErrorMsg.SWITCH_STATE_ERR.format(act_state=gear_pos_signal.value,
                                                 exp_state=GearState.NEUTRAL)

        with allure.step(f'Can not switch GearPosition state to {GearState.DRIVE}'):
            client.update_pin_by_id(gear_1_pin.pin_id, gear_1_pin.get_voltage_by_state(GearState.DRIVE))
            client.update_pin_by_id(gear_2_pin.pin_id, gear_2_pin.get_voltage_by_state(GearState.DRIVE))
            act_state = client.get_signal_by_id(gear_position_sig.sig_id).value
            assert act_state == GearState.NEUTRAL, ErrorMsg.SWITCH_STATE_ERR.format(act_state=act_state,
                                                                                    exp_state=GearState.NEUTRAL)
