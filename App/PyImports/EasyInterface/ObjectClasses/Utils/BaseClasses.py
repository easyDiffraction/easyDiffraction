from typing import Union, Optional, Any, NoReturn

from ..units import Unit
from .DictTools import PathDict


class Data(PathDict):
    """
    
    """
    def __init__(self, value: Optional[Any] = None, unit: Optional[Union[str, Unit]] = ''):
        if not isinstance(unit, Unit):
            unit = Unit(unit)
        super().__init__(value=value, unit=unit, error=0, constraint=None, hide=True, refine=False)

    def __repr__(self) -> str:
        return '{}'.format(self['value'])

    @property
    def min(self) -> float:
        value = self['value']
        ret = None
        if value is not None:
            if isinstance(value, (int, float, complex)) and not isinstance(value, bool):
                ret = 0.8*self['value']
        return ret

    @property
    def max(self) -> float:
        value = self['value']
        ret = None
        if value is not None:
            if isinstance(value, (int, float, complex)) and not isinstance(value, bool):
                ret = 1.2*self['value']
        return ret


class Base(PathDict):
    def __init__(self, value: object = None, unit: object = '') -> object:
        super().__init__(header='Undefined', tooltip='', url='', store=Data(value, unit))

    def __repr__(self) -> str:
        return '{} {}'.format(self.value, self.getItemByPath(['store', 'unit']))

    @property
    def value(self) -> Any:
        return self.getItemByPath(['store', 'value'])

    @value.setter
    def value(self, value: Any) -> NoReturn:
        self.setItemByPath(['store', 'value'], value)

    def get(self, item: str) -> Any:
        return self.getItemByPath(['store', item])

    def set(self, item: str, value: Any) -> NoReturn:
        self.setItemByPath(['store', item], value)

    def unitConversionFactor(self, newUnit: str) -> float:
        if self.getItemByPath(['store', 'unit']) is None:
            return 1
        return self.getItemByPath(['store', 'unit']).get_conversion_factor(newUnit)

    def convertUnits(self, newUnit: str) -> NoReturn:
        cf = self.unitConversionFactor(newUnit)
        self.setItemByPath(['store', 'value'], cf * self['value'])
        self.setItemByPath(['store', 'unit'], Unit(newUnit))

    def valueInUnit(self, newUnit: str) -> float:
        cf = self.unitConversionFactor(newUnit)
        return cf * self['value']
