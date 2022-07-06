import allure
import pytest

from signal_states import GearState, BatteryState, BrakePedalState, AccPedalState
from contants import ErrorMsg


class TestGearPosition:
    @pytest.mark.parametrize('gear_state', [GearState.PARK,
                                            GearState.NEUTRAL,
                                            GearState.REVERSE,
                                            GearState.DRIVE])
    @allure.title('Switch GearPosition state')
    def test_gear_shifter(self, client, gear_state,
                          battery_voltage_pin, brake_pedal_pin, acc_pedal_pin,
                          gear_1_pin, gear_2_pin,
                          gear_position_sig):
        with allure.step(f'Set BatteryState to {BatteryState.READY}'):
            ready_voltage = battery_voltage_pin.get_voltage_by_state(BatteryState.READY)
            battery_state_res = client.update_pin_by_id(pin_id=battery_voltage_pin.pin_id,
                                                        voltage=ready_voltage)
            assert battery_state_res.voltage == ready_voltage, \
                ErrorMsg.RES_VOLTAGE_ERR.format(res_volt=battery_state_res.voltage, exp_volt=ready_voltage)

        with allure.step(f'Set BrakePedalState to {BrakePedalState.PRESSED}'):
            pressed_voltage = brake_pedal_pin.get_voltage_by_state(BrakePedalState.PRESSED)
            brake_pedal_res = client.update_pin_by_id(pin_id=brake_pedal_pin.pin_id, voltage=pressed_voltage)
            assert brake_pedal_res.voltage == pressed_voltage, \
                ErrorMsg.RES_VOLTAGE_ERR.format(res_volt=brake_pedal_res.voltage, exp_volt=pressed_voltage)

        with allure.step(f'Set AccPedalPos to {AccPedalState.PERCENT_0}'):
            perc0_voltage = acc_pedal_pin.get_voltage_by_state(AccPedalState.PERCENT_0)
            acc_pedal_res = client.update_pin_by_id(pin_id=acc_pedal_pin.pin_id, voltage=perc0_voltage)
            assert acc_pedal_res.voltage == perc0_voltage, \
                ErrorMsg.RES_VOLTAGE_ERR.format(res_volt=acc_pedal_res.voltage, exp_volt=perc0_voltage)

        with allure.step(f'Set GearPosition to {gear_state}'):
            client.update_pin_by_id(gear_1_pin.pin_id, gear_1_pin.get_voltage_by_state(gear_state))
            client.update_pin_by_id(gear_2_pin.pin_id, gear_2_pin.get_voltage_by_state(gear_state))
            act_state = client.get_signal_by_id(gear_position_sig.sig_id).value
            assert act_state == gear_state, ErrorMsg.SWITCH_STATE_ERR.format(act_state=act_state, exp_state=gear_state)
