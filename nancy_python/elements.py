from typing import Any, Literal, Union, NewType

from pydantic import BaseModel, RootModel, Field, model_serializer, model_validator

from nancy_python import Rational


class Point(BaseModel):
    type: Literal['point'] = 'point'
    time: Rational
    value: Rational


class Segment(BaseModel):
    type: Literal['segment'] = 'segment'
    startTime: Rational = Field()
    endTime: Rational = Field()
    rightLimitAtStartTime: Rational = Field()
    slope: Rational = Field()

ElementTypes = NewType('ElementType', Union[Point, Segment])

class Element(RootModel):
    root: ElementTypes = Field(discriminator='type')
