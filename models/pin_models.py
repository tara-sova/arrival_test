from dataclasses import dataclass
from dataclasses_json import dataclass_json, LetterCase
from signal_states import GearState, AccPedalState, BrakePedalState, BatteryState, ReqTorqueState


@dataclass_json(letter_case=LetterCase.PASCAL)
@dataclass
class PinModel:
    pin_id: int
    voltage: float = None
    name: str = None

    @staticmethod
    def get_voltage_by_state(status):
        pass


@dataclass_json(letter_case=LetterCase.PASCAL)
@dataclass
class GearPin1(PinModel):
    pin_id: int = 1
    name: str = 'Gear_1'

    @staticmethod
    def get_voltage_by_state(status: GearState):
        if status == GearState.PARK:
            return 0.67
        elif status == GearState.NEUTRAL:
            return 1.48
        elif status == GearState.REVERSE:
            return 2.28
        elif status == GearState.DRIVE:
            return 3.12
        else:
            ValueError('Unknown status')


@dataclass_json(letter_case=LetterCase.PASCAL)
@dataclass
class GearPin2(PinModel):
    pin_id: int = 2
    name: str = 'Gear_2'

    @staticmethod
    def get_voltage_by_state(status: GearState):
        if status == GearState.PARK:
            return 3.12
        elif status == GearState.NEUTRAL:
            return 2.28
        elif status == GearState.REVERSE:
            return 1.48
        elif status == GearState.DRIVE:
            return 0.67
        else:
            ValueError('Unknown status')


@dataclass_json(letter_case=LetterCase.PASCAL)
@dataclass
class AccPedalPin(PinModel):
    pin_id: int = 3
    name: str = 'AccPedal'

    @staticmethod
    def get_voltage_by_state(status: AccPedalState):
        if status == AccPedalState.ERROR:
            return 0
        elif status == AccPedalState.PERCENT_0:
            return 1.5
        elif status == AccPedalState.PERCENT_30:
            return 2.2
        elif status == AccPedalState.PERCENT_50:
            return 2.7
        elif status == AccPedalState.PERCENT_100:
            return 3.2
        else:
            ValueError('Unknown status')

    @staticmethod
    def get_reqtorque_by_state(status: AccPedalState):
        if status == AccPedalState.ERROR:
            return ReqTorqueState.NM_0
        elif status == AccPedalState.PERCENT_0:
            return ReqTorqueState.NM_0
        elif status == AccPedalState.PERCENT_30:
            return ReqTorqueState.NM_3000
        elif status == AccPedalState.PERCENT_50:
            return ReqTorqueState.NM_5000
        elif status == AccPedalState.PERCENT_100:
            return ReqTorqueState.NM_10000
        else:
            ValueError('Unknown status')


@dataclass_json(letter_case=LetterCase.PASCAL)
@dataclass
class BrakePedalPin(PinModel):
    pin_id: int = 4
    name: str = 'BrakePedal'

    @staticmethod
    def get_voltage_by_state(status: BrakePedalState):
        if status == BrakePedalState.ERROR:
            return 0
        elif status == BrakePedalState.PRESSED:
            return 1.5
        elif status == BrakePedalState.RELEASED:
            return 2.2
        else:
            ValueError('Unknown status')


@dataclass_json(letter_case=LetterCase.PASCAL)
@dataclass
class BatteryVoltagePin(PinModel):
    pin_id: int = 5
    name: str = 'BatteryVoltage'

    @staticmethod
    def get_voltage_by_state(status: BatteryState):
        if status == BatteryState.ERROR:
            return 0
        elif status == BatteryState.NOT_READY:
            return 200
        elif status == BatteryState.READY:
            return 600
        else:
            ValueError('Unknown status')
