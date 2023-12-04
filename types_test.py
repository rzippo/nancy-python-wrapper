from typing import List, Union

from nancy_python import Rational, Element, Point, Segment, Sequence, UppCurve, Curve

if __name__ == '__main__':
    print("Rationals:")

    r1 = Rational(num=1, den=2)
    print(r1.model_dump_json())

    j2 = "{\"num\":1,\"den\":2}"
    r2 = Rational.model_validate_json(j2)
    j2s = r2.model_dump_json()
    print(j2)
    print(j2s)
    print(j2 == j2s)

    j3 = "2"
    r3 = Rational.model_validate_json(j3)
    print(f'{r3.numerator}/{r3.denominator}')
    print(r3.model_dump_json())

    r4o = Rational(num=3, den=2)
    j4o = r4o.model_dump_json()
    print(j4o)
    r4d = Rational.model_validate_json(j4o)
    print(r4d.model_dump_json())

    print()
    print("Elements, serialization")

    p1 = Point(time=1, value=2)
    jp1 = p1.model_dump_json()
    print(jp1)

    s1 = Segment(startTime=1, endTime=2, rightLimitAtStartTime=2, slope=Rational(num=2, den=3))
    js1 = s1.model_dump_json()
    print(js1)

    e1: ElementTypes = p1
    print(e1.model_dump_json())

    e2: ElementTypes = s1
    print(e2.model_dump_json())

    print()
    print("Elements, deserialization")

    p1d = Point.model_validate_json(jp1)
    print(p1d.model_dump_json())

    s1d = Segment.model_validate_json(js1)
    print(s1d.model_dump_json())

    p1ed = Element.model_validate_json(jp1)
    print(p1ed.model_dump_json())

    s1ed = Element.model_validate_json(js1)
    print(s1ed.model_dump_json())

    print()
    print("Sequences")

    seq1 = Sequence(elements=[Point(time=1, value=2),
                              Segment(startTime=2, endTime=3, rightLimitAtStartTime=2, slope=Rational(num=2, den=3))])
    jseq1 = seq1.model_dump_json()
    print(jseq1)

    seq1d = Sequence.model_validate_json(jseq1)
    print(seq1d.model_dump_json())

    print()
    print("Curves")

    c1 = UppCurve(
        baseSequence = Sequence(elements = [
            Point(time=0, value=0),
            Segment(startTime=0, endTime=2, rightLimitAtStartTime=0, slope=1)
        ]),
        pseudoPeriodStart = 1,
        pseudoPeriodLength = 1,
        pseudoPeriodHeight = 1
    )
    jc1 = c1.model_dump_json()
    print(jc1)
    c1d = Curve.model_validate_json(jc1)
    print(c1d.model_dump_json())
