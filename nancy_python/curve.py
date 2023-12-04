from typing import Literal, Union, NewType, List

import requests
from pydantic import BaseModel, RootModel, Field

from .rational import Rational, RationalUnion
from .elements import Element, Point, Segment
from .sequence import Sequence
from .nancy_http_server import NancyHttpServer

class UppCurve(BaseModel):
    type: Literal['curve'] = 'curve'
    baseSequence: Sequence
    pseudoPeriodStart: Rational
    pseudoPeriodLength: Rational
    pseudoPeriodHeight: Rational

CurveTypes = NewType('CurveTypes', Union[UppCurve])

class RetrievedCurve(RootModel):
    root: CurveTypes = Field(discriminator="type")

class Curve:
    def __init__(self):
        self._curve: CurveTypes = None
        self._curveId: str = None

    # Properties

    def isRetrieved(self) -> bool:
        if self._curve is not None:
            return True
        else:
            return False

    def isSubmitted(self) -> bool:
        if self._curveId is not None:
            return True
        else:
            return False

    def getCurve(self) -> CurveTypes:
        if self.isRetrieved():
            return self._curve
        else:
            self.retrieve()
            return self._curve

    def getCurveId(self) -> str:
        if self.isSubmitted():
            return self._curveId
        else:
            self.submit()
            return self._curveId

    # Constructors

    @staticmethod
    def fromJsonOb(curve: CurveTypes):
        c = Curve()
        c._curve = curve
        return c

    @staticmethod
    def fromCurveId(curveId: str):
        c = Curve()
        c._curveId = curveId
        return c

    @staticmethod
    def fromUppParameters(
            baseSequence: Sequence,
            pseudoPeriodStart: RationalUnion,
            pseudoPeriodLength: RationalUnion,
            pseudoPeriodHeight: RationalUnion ):
        c = Curve()
        c._curve = UppCurve(
            baseSequence = baseSequence,
            pseudoPeriodStart = Rational.fromUnion(pseudoPeriodStart),
            pseudoPeriodLength = Rational.fromUnion(pseudoPeriodLength),
            pseudoPeriodHeight = Rational.fromUnion(pseudoPeriodHeight)
        )
        return c

    # HTTP methods

    def retrieveJsonAsDict(self):
        if not self.isSubmitted():
            raise Exception("Cannot retrieve a curve that is not submitted")
        else:
            r = requests.get(
                f"{NancyHttpServer.getCurveApiUrl()}/{self.getCurveId()}"
            )
            return r.json()["curve"]

    def retrieve(self):
        jsonDict = self.retrieveJsonAsDict()
        self._curve = RetrievedCurve.model_validate(jsonDict)

    def submit(self):
        if not self.isRetrieved():
            raise Exception("Cannot submit a curve that is not retrieved")
        else:
            json = self._curve.model_dump()
            r = requests.post(
                NancyHttpServer.getCurveApiUrl(),
                json=json
            )
            print(r.text)
            self._curveId = r.json()["id"]

    # HTTP operations

    @staticmethod
    def callCurveOperation(curve: 'Curve', operation: str):
        operand = curve.getCurveId()
        r = requests.post(
            NancyHttpServer.getOperationUrl(operation),
            json=operand
        )
        id = r.json()
        return Curve.fromCurveId(id)

    def callCurveSamplingOperation(curve: 'Curve', time: RationalUnion, operation: str):
        operand = curve.getCurveId()
        body = Rational.fromUnion(time).model_dump()
        r = requests.post(
            NancyHttpServer.getCurveOperationUrl(operand, operation),
            json=body
        )
        value = r.json()
        return Rational.model_validate(value)

    def callCurvesOperation(curves: List['Curve'], operation: str):
        operands = list(map(lambda c: c.getCurveId(), curves))
        r = requests.post(
            NancyHttpServer.getOperationUrl(operation),
            json=operands
        )
        id = r.json()
        return Curve.fromCurveId(id)

    @staticmethod
    def valueAt(f: 'Curve', time: RationalUnion):
        return Curve.callCurveSamplingOperation(f, time, 'valueAt')

    @staticmethod
    def rightLimitAt(f: 'Curve', time: RationalUnion):
        return Curve.callCurveSamplingOperation(f, time, 'rightLimitAt')

    @staticmethod
    def leftLimitAt(f: 'Curve', time: RationalUnion):
        return Curve.callCurveSamplingOperation(f, time, 'leftLimitAt')

    @staticmethod
    def horizontalDeviation(f: 'Curve', g:'Curve'):
        return Curve.callCurvesOperation([f, g], 'horizontalDeviation')

    @staticmethod
    def verticalDeviation(f: 'Curve', g:'Curve'):
        return Curve.callCurvesOperation([f, g], 'verticalDeviation')

    @staticmethod
    def addition(f: 'Curve', g:'Curve'):
        return Curve.callCurvesOperation([f, g], 'addition')

    @staticmethod
    def additionList(curves: List['Curve']):
        return Curve.callCurvesOperation(curves, 'addition')

    @staticmethod
    def subtraction(f: 'Curve', g:'Curve'):
        return Curve.callCurvesOperation([f, g], 'subtraction')

    @staticmethod
    def minimum(f: 'Curve', g: 'Curve'):
        return Curve.callCurvesOperation([f, g], 'minimum')

    @staticmethod
    def minimumList(curves: List['Curve']):
        return Curve.callCurvesOperation(curves, 'minimum')

    @staticmethod
    def maximum(f: 'Curve', g: 'Curve'):
        return Curve.callCurvesOperation([f, g], 'maximum')

    @staticmethod
    def maximumList(curves: List['Curve']):
        return Curve.callCurvesOperation(curves, 'maximum')

    @staticmethod
    def convolution(f: 'Curve', g: 'Curve'):
        return Curve.callCurvesOperation([f, g], 'convolution')

    @staticmethod
    def convolutionList(curves: List['Curve']):
        return Curve.callCurvesOperation(curves, 'convolution')

    @staticmethod
    def maxPlusConvolution(f: 'Curve', g: 'Curve'):
        return Curve.callCurvesOperation([f, g], 'maxPlusConvolution')

    @staticmethod
    def maxPlusConvolutionList(curves: List['Curve']):
        return Curve.callCurvesOperation(curves, 'maxPlusConvolution')

    @staticmethod
    def deconvolution(f: 'Curve', g:'Curve'):
        return Curve.callCurvesOperation([f, g], 'deconvolution')

    @staticmethod
    def maxPlusDeconvolution(f: 'Curve', g:'Curve'):
        return Curve.callCurvesOperation([f, g], 'maxPlusDeconvolution')

    @staticmethod
    def subAdditiveClosure(f: 'Curve'):
        return Curve.callCurveOperation(f, 'subAdditiveClosure')

    @staticmethod
    def superAdditiveClosure(f: 'Curve'):
        return Curve.callCurveOperation(f, 'superAdditiveClosure')
