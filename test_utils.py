#!/usr/bin/env python3
import pytest  # type: ignore

from wing_utils import split_2d


def test_split_2d():
    lst = [(1, 0), (0.4, 0.2), (0, 0), (0.4, -0.2), (1, 0)]
    line = [(2, 0), (3, 0)]
    print(f"lst={lst} line={line}")
    listAbove = split_2d(lst=lst, line=line, retAbove=True)
    print(f"listAbove={listAbove}")
    assert all(
        [a == b for a, b in zip(listAbove, [(1, 0), (0.4, 0.2), (0, 0), (1, 0)])]
    )
    listBelow = split_2d(lst=lst, line=line, retAbove=False)
    print(f"listBelow={listBelow}")
    assert all(
        [a == b for a, b in zip(listBelow, [(1, 0), (0, 0), (0.4, -0.2), (1, 0)])]
    )


def main():
    test_split_2d()


if __name__ == "__main__":
    main()
