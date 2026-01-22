from __future__ import annotations

from dataclasses import dataclass

import pytest

import interface_classes as m


@dataclass(frozen=True)
class Item:
    value: int
    tag: str


ALGORITHMS = [
    m.bubble_sort,
    m.selection_sort,
    m.insertion_sort,
    m.merge_sort,
    m.quick_sort,
]


@pytest.mark.parametrize(
    "data",
    [
        [],
        [1],
        [2, 1],
        [3, 2, 1],
        [5, 1, 4, 2, 8, 0, 2],
        [1, 1, 1, 1],
        [-1, 3, 0, -5, 2],
    ],
)
@pytest.mark.parametrize("algo", ALGORITHMS)
def test_algorithms_match_sorted_and_do_not_mutate(algo, data):
    original = list(data)
    out = algo(data)

    assert out == sorted(data)
    assert list(data) == original  # not mutated


@pytest.mark.parametrize("algo", ALGORITHMS)
def test_key_and_reverse(algo):
    items = [Item(2, "b"), Item(1, "x"), Item(2, "a"), Item(3, "z")]

    out = algo(items, key=lambda it: it.value)
    assert [it.value for it in out] == sorted([it.value for it in items])

    out_rev = algo(items, key=lambda it: it.value, reverse=True)
    assert [it.value for it in out_rev] == sorted([it.value for it in items], reverse=True)


def test_abc_strategy_context():
    data = [3, 1, 2]
    sorter = m.SorterABC(m.MergeSortABC())
    assert sorter.sort(data) == [1, 2, 3]


def test_protocol_strategy_context():
    data = [3, 1, 2]
    sorter = m.SorterProto(m.FunctionSortStrategy(m.quick_sort))
    assert sorter.sort(data) == [1, 2, 3]


def test_callable_strategy_context():
    data = [3, 1, 2]
    sorter = m.SorterCallable(m.insertion_sort)
    assert sorter.sort(data) == [1, 2, 3]
