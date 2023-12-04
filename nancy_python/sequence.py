from typing import Union, List

from pydantic import BaseModel

from .elements import Element, Point, Segment, ElementTypes


class Sequence(BaseModel):
    elements: List[Element]

    @staticmethod
    def fromElements(elements: List[ElementTypes]):
        s = Sequence(elements=elements)
        return s
