from typing import Any, NewType, Union

from pydantic import BaseModel, Field, model_serializer, model_validator


RationalUnion = NewType('RationalUnion', Union['Rational', int])

class Rational(BaseModel):
    numerator: int = Field(serialization_alias="num", validation_alias="num")
    denominator: int = Field(serialization_alias="den", validation_alias="den")

    def __str__(self):
        if self.denominator == 1:
            return f"{self.numerator}"
        else:
            return f"{self.numerator}/{self.denominator}"

    @staticmethod
    def fromInt(n: int):
        return Rational(num=n, den=1)

    @staticmethod
    def fromUnion(ru: RationalUnion) -> 'Rational':
        if isinstance(ru, int):
            return Rational.fromInt(ru)
        else:
            return ru

    @model_serializer
    def customRationalSerializer(self):
        if self.denominator == 1:
            return self.numerator
        else:
            return {
                "num": self.numerator,
                "den": self.denominator
            }

    @model_validator(mode='before')
    def customRationalValidator(cls, data: Any) -> Any:
        if isinstance(data, int):
            return {
                "num": data,
                "den": 1
            }
        else:
            return data
