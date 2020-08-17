#!/usr/bin/env python3
import pytest

import wing_utils as wu


def test_sumPts():
    assert wu.sumPts((0, 0), (0, 0)) == (0, 0)
    assert wu.sumPts((-1, -1), (1, 1)) == (0, 0)
    assert wu.sumPts((-1, -1), (0, 0)) == (-1, -1)
    assert wu.sumPts((0, -1), (-2, 0)) == (-2, -1)
    assert wu.sumPts((-1, 0), (0, -2)) == (-1, -2)
    assert wu.sumPts((1, -1), (-2, 2)) == (-1, 1)
    assert wu.sumPts((-1, 1), (2, -2)) == (1, -1)
    assert wu.sumPts((1, 2), (3, 4)) == (4, 6)


def test_diffPts():
    assert wu.diffPts((0, 0), (0, 0)) == (0, 0)
    assert wu.diffPts((-1, -1), (1, 1)) == (-2, -2)
    assert wu.diffPts((-1, -1), (0, 0)) == (-1, -1)
    assert wu.diffPts((0, -1), (-2, 0)) == (2, -1)
    assert wu.diffPts((-1, 0), (0, -2)) == (-1, 2)
    assert wu.diffPts((1, -1), (-2, 2)) == (3, -3)
    assert wu.diffPts((-1, 1), (2, -2)) == (-3, 3)
    assert wu.diffPts((1, 2), (3, 4)) == (-2, -2)


def test_prodPts():
    assert wu.prodPts((0, 0), (0, 0)) == (0, 0)
    assert wu.prodPts((-1, -1), (1, 1)) == (-1, -1)
    assert wu.prodPts((-1, -1), (0, 0)) == (0, 0)
    assert wu.prodPts((0, -1), (-2, 0)) == (0, 0)
    assert wu.prodPts((-1, 0), (0, -2)) == (0, 0)
    assert wu.prodPts((1, -1), (-2, 2)) == (-2, -2)
    assert wu.prodPts((-1, 1), (2, -2)) == (-2, -2)
    assert wu.prodPts((1, 2), (3, 4)) == (3, 8)


def test_crossProdPts():
    assert wu.crossProdPts((0, 0), (0, 0)) == 0
    assert wu.crossProdPts((-1, -1), (1, 1)) == 0
    assert wu.crossProdPts((-1, -1), (0, 0)) == 0
    assert wu.crossProdPts((0, -1), (-2, 0)) == -2
    assert wu.crossProdPts((-1, 0), (0, -2)) == 2
    assert wu.crossProdPts((1, -1), (-2, 2)) == 0
    assert wu.crossProdPts((-1, 1), (2, -2)) == 0
    assert wu.crossProdPts((1, 2), (3, 4)) == -2

    # from: https://www.geeksforgeeks.org/direction-point-line-segment/
    assert wu.crossProdPts((29, -15), (15, 28)) == 1037
    assert wu.crossProdPts((59, -25), (45, 18)) == 2187


def test_intersectionLines_2d():
    assert wu.intersectionLines_2d((2, 0), (3, 0), (1, 0.01), (1, -0.01)) == (1, 0)

    # https://www.geeksforgeeks.org/program-for-point-of-intersection-of-two-lines/
    assert wu.intersectionLines_2d((1, 1), (4, 4), (1, 8), (2, 4)) == (2.4, 2.4)


def test_split_2d():
    lst = [(1, 0.01), (0.4, 0.2), (0, 0), (0.4, -0.2), (1, -0.01)]
    linePt1 = (2, 0)
    linePt2 = (3, 0)
    # print(f"lst={lst} linePt1={linePt1} linePt2={linePt2}")
    listAbove = wu.split_2d(linePt1=linePt1, linePt2=linePt2, lst=lst, retAbove=True)
    # print(f"listAbove={listAbove}")
    assert all(
        [a == b for a, b in zip(listAbove, [(1, 0), (1, 0.01), (0.4, 0.2), (0, 0)])]
    )

    listBelow = wu.split_2d(linePt1=linePt1, linePt2=linePt2, lst=lst, retAbove=False)
    # print(f"listBelow={listBelow}")
    assert all(
        [a == b for a, b in zip(listBelow, [(1, 0), (0, 0), (0.4, -0.2), (1, -0.01)])]
    )


def main():
    # For debugging, use `make t` or `pytest` to actually run the tests
    test_sumPts()
    test_diffPts()
    test_prodPts()
    test_crossProdPts()
    test_intersectionLines_2d()
    test_split_2d()


if __name__ == "__main__":
    main()
