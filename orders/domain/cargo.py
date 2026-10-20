# заявки нет без клиента

from pydantic import ConfigDict, field_validator, BaseModel
from dataclasses import dataclass, fields
from pint import UnitRegistry, Unit
from enum import StrEnum, Enum, auto
from uuid import UUID


class CargoTimeType(StrEnum):
    STANDARD = auto()
    EXPRESS = auto()
    URGENT = auto()


ureg = UnitRegistry()
Q_ = ureg.Quantity # type: ignore

    
ALLOWED = {
    "length": ureg.meter,
    "weight": ureg.kilogram,
    "volume": ureg.meter ** 3
}


class CargoUnit(BaseModel):  # доменнная модель "Товар"
    model_config = ConfigDict(arbitrary_types_allowed=True)

    length: Q_     
    width: Q_ 
    height: Q_ 
    weight: Q_  

    @field_validator("length", "width", "height")
    @classmethod
    def check_length_units(cls, v: Q_):
        if not v.units == ALLOWED["length"]:
            raise ValueError(f"{v.units}:{ALLOWED['length']}") # TODO: Переделать вывод

        return v


    @field_validator("weight")
    @classmethod
    def check_weight_units(cls, v: Q_):
        if not v.units == ALLOWED["weight"]:
            raise ValueError(f"{v.units}:{ALLOWED['length']}") # TODO: Переделать вывод
        return v

    @property
    def volume(self) -> Q_:
        return self.length * self.width * self.height 
   
 

@dataclass
class Cargo: # доменная модель "Загрузка"
    time_type: CargoTimeType
    units: list[CargoUnit]

    @property
    def sum(self) -> int:
        return len(self.units)

    @property
    def weight(self) -> Q_:
        return sum((u.weight for u in self.units), Q_(0, "kg"))

    @property
    def volume(self) -> Q_:
        return sum((u.volume for u in self.units), Q_(0, "m**3"))

    
    def dimensional_weight(self, coefficient: int = 200) -> Q_:
        if self.volume.units == "m**3":
            dw = (self.volume * coefficient).magnitude
        # sum((u.dimensional_weight().magnitude for u in self.units), Q_(0, "kg"))
        return Q_(dw, self.weight.units)

    def chargeable_weight(self) -> Q_:
        return max(self.weight, self.dimensional_weight())




