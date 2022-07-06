import pytest
from clients import VehicleApiClient
from models import SignalModel, GearPin1, GearPin2, BatteryVoltagePin, BrakePedalPin, AccPedalPin
from signal_states import BatteryState, BrakePedalState, AccPedalState, GearState
from contants import ErrorMsg


@pytest.fixture(scope='session')
def client() -> VehicleApiClient:
    return VehicleApiClient()


@pytest.fixture(scope='function', autouse=True)
def prepare_stand(client: VehicleApiClient, battery_voltage_pin):
    client.update_pin_by_id(battery_voltage_pin.pin_id,
                            battery_voltage_pin.get_voltage_by_state(BatteryState.READY))
    yield
    client.update_pin_by_id(battery_voltage_pin.pin_id,
                            battery_voltage_pin.get_voltage_by_state(BatteryState.ERROR))


@pytest.fixture(scope='function')
def switch_gear_shifter_to_state(client: VehicleApiClient, prepare_stand,
                                 gear_shifter_state: GearState,
                                 battery_voltage_pin, brake_pedal_pin, acc_pedal_pin,
                                 gear_1_pin, gear_2_pin, gear_position_sig):
    ready_voltage = battery_voltage_pin.get_voltage_by_state(BatteryState.READY)
    client.update_pin_by_id(pin_id=battery_voltage_pin.pin_id, voltage=ready_voltage)

    pressed_voltage = brake_pedal_pin.get_voltage_by_state(BrakePedalState.PRESSED)
    client.update_pin_by_id(pin_id=brake_pedal_pin.pin_id, voltage=pressed_voltage)

    perc0_voltage = acc_pedal_pin.get_voltage_by_state(AccPedalState.PERCENT_0)
    client.update_pin_by_id(pin_id=acc_pedal_pin.pin_id, voltage=perc0_voltage)

    client.update_pin_by_id(gear_1_pin.pin_id, gear_1_pin.get_voltage_by_state(gear_shifter_state))
    client.update_pin_by_id(gear_2_pin.pin_id, gear_2_pin.get_voltage_by_state(gear_shifter_state))
    act_state = client.get_signal_by_id(gear_position_sig.sig_id).value
    assert act_state == gear_shifter_state, ErrorMsg.SWITCH_STATE_ERR.format(act_state=act_state,
                                                                             exp_state=gear_shifter_state)


@pytest.fixture(scope='session')
def gear_1_pin():
    yield GearPin1()


@pytest.fixture(scope='session')
def gear_2_pin():
    yield GearPin2()


@pytest.fixture(scope='session')
def acc_pedal_pin():
    yield AccPedalPin()


@pytest.fixture(scope='session')
def brake_pedal_pin():
    yield BrakePedalPin()


@pytest.fixture(scope='session')
def battery_voltage_pin():
    yield BatteryVoltagePin()


@pytest.fixture(scope='session')
def gear_position_sig():
    yield SignalModel(name='GearPosition', sig_id=1)


@pytest.fixture(scope='session')
def acc_pedal_sig():
    yield SignalModel(name='AccPedalPos', sig_id=2)


@pytest.fixture(scope='session')
def brake_pedal_sig():
    yield SignalModel(name='BrakePedalState', sig_id=3)


@pytest.fixture(scope='session')
def req_torque_sig():
    yield SignalModel(name='ReqTorque', sig_id=4)


@pytest.fixture(scope='session')
def battery_state_sig():
    yield SignalModel(name='BatteryState', sig_id=5)
