from nancy_python import Curve, Sequence, Rational, Point, Segment

if __name__ == '__main__':
    curve = Curve.fromUppParameters(
        Sequence(elements = [
            Point(time=0, value=0),
            Segment(startTime=0, endTime=1, rightLimitAtStartTime=4, slope=Rational(num=3, den=4)),
            Point(time=1, value=Rational(num=19, den=4)),
            Segment(startTime=1, endTime=2, rightLimitAtStartTime=Rational(num=19, den=4), slope=Rational(num=3, den=4))
        ]),
        1,
        1,
        Rational(num=3, den=4)
    )
    print(curve.getCurve().model_dump_json())

    curve.submit()
    json = curve.retrieveJsonAsDict()
    print(json)

    convolution = Curve.convolution(curve, curve)
    convolution.retrieve()
    print(convolution.getCurve().model_dump_json())

    closure = Curve.subAdditiveClosure(convolution)
    sample = Curve.rightLimitAt(closure, 10)

    print(sample)



