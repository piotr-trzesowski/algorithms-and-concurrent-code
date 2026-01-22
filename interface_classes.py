"""Strategy Pattern examples: 5 sorting algorithms in 3 interface styles.

This module is intentionally self-contained (educational / interview-style).

Contract (shared by all implementations)
--------------------------------------
- Input: any sequence of comparable items `Sequence[T]`.
- Output: a *new* `list[T]` (the input is never mutated).
- Options:
  - `key`: custom key function (like `sorted()`)
  - `reverse`: descending order

Algorithms implemented (common textbook set):
- Bubble sort
- Selection sort
- Insertion sort
- Merge sort
- Quick sort

Three strategy styles demonstrated:
1) Explicit interface with `abc.ABC`
2) Implicit interface with `typing.Protocol`
3) Plain `Callable`

Run this file directly to see a small demo.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Callable, Generic, Optional, Protocol, Sequence, TypeVar


T = TypeVar("T")
K = TypeVar("K")


def _identity(x: T) -> T:
    return x


def _normalize_key(key: Optional[Callable[[T], Any]]) -> Callable[[T], Any]:
    return _identity if key is None else key


def _should_swap(a_key: Any, b_key: Any, *, reverse: bool) -> bool:
    """Return True when items in (a,b) order violate desired ordering."""
    return a_key < b_key if reverse else a_key > b_key


# ---------------------------------------------------------------------------
# Sorting algorithms (pure functions)
# ---------------------------------------------------------------------------

def bubble_sort(data: Sequence[T], *, key: Callable[[T], Any] | None = None, reverse: bool = False) -> list[T]:
    items = list(data)
    k = _normalize_key(key)

    n = len(items)
    for end in range(n - 1, 0, -1):
        swapped = False
        for i in range(end):
            if _should_swap(k(items[i]), k(items[i + 1]), reverse=reverse):
                items[i], items[i + 1] = items[i + 1], items[i]
                swapped = True
        if not swapped:
            break

    return items


def selection_sort(data: Sequence[T], *, key: Callable[[T], Any] | None = None, reverse: bool = False) -> list[T]:
    items = list(data)
    k = _normalize_key(key)

    n = len(items)
    for i in range(n):
        best_idx = i
        for j in range(i + 1, n):
            if _should_swap(k(items[best_idx]), k(items[j]), reverse=reverse):
                best_idx = j
        if best_idx != i:
            items[i], items[best_idx] = items[best_idx], items[i]

    return items


def insertion_sort(data: Sequence[T], *, key: Callable[[T], Any] | None = None, reverse: bool = False) -> list[T]:
    items = list(data)
    k = _normalize_key(key)

    for i in range(1, len(items)):
        current = items[i]
        current_key = k(current)

        j = i - 1
        while j >= 0 and _should_swap(k(items[j]), current_key, reverse=reverse):
            items[j + 1] = items[j]
            j -= 1
        items[j + 1] = current

    return items


def merge_sort(data: Sequence[T], *, key: Callable[[T], Any] | None = None, reverse: bool = False) -> list[T]:
    items = list(data)
    k = _normalize_key(key)

    def merge(left: list[T], right: list[T]) -> list[T]:
        result: list[T] = []
        i = j = 0
        while i < len(left) and j < len(right):
            # append the "next" item based on ordering
            if _should_swap(k(left[i]), k(right[j]), reverse=reverse):
                result.append(right[j])
                j += 1
            else:
                result.append(left[i])
                i += 1
        result.extend(left[i:])
        result.extend(right[j:])
        return result

    def sort(seq: list[T]) -> list[T]:
        if len(seq) <= 1:
            return seq
        mid = len(seq) // 2
        return merge(sort(seq[:mid]), sort(seq[mid:]))

    return sort(items)


def quick_sort(data: Sequence[T], *, key: Callable[[T], Any] | None = None, reverse: bool = False) -> list[T]:
    items = list(data)
    k = _normalize_key(key)

    def sort(seq: list[T]) -> list[T]:
        if len(seq) <= 1:
            return seq
        pivot = seq[len(seq) // 2]
        pivot_key = k(pivot)

        left: list[T] = []
        middle: list[T] = []
        right: list[T] = []

        for item in seq:
            item_key = k(item)
            if item_key == pivot_key:
                middle.append(item)
            elif _should_swap(item_key, pivot_key, reverse=reverse):
                # item should appear after pivot in desired ordering
                right.append(item)
            else:
                left.append(item)

        return sort(left) + middle + sort(right)

    return sort(items)


# ---------------------------------------------------------------------------
# 1) Strategy Pattern with ABC (explicit interface)
# ---------------------------------------------------------------------------


class SortingStrategyABC(ABC, Generic[T]):
    @abstractmethod
    def sort(
        self,
        data: Sequence[T],
        *,
        key: Callable[[T], Any] | None = None,
        reverse: bool = False,
    ) -> list[T]:
        raise NotImplementedError


@dataclass(frozen=True, slots=True)
class BubbleSortABC(SortingStrategyABC[T]):
    def sort(self, data: Sequence[T], *, key: Callable[[T], Any] | None = None, reverse: bool = False) -> list[T]:
        return bubble_sort(data, key=key, reverse=reverse)


@dataclass(frozen=True, slots=True)
class SelectionSortABC(SortingStrategyABC[T]):
    def sort(self, data: Sequence[T], *, key: Callable[[T], Any] | None = None, reverse: bool = False) -> list[T]:
        return selection_sort(data, key=key, reverse=reverse)


@dataclass(frozen=True, slots=True)
class InsertionSortABC(SortingStrategyABC[T]):
    def sort(self, data: Sequence[T], *, key: Callable[[T], Any] | None = None, reverse: bool = False) -> list[T]:
        return insertion_sort(data, key=key, reverse=reverse)


@dataclass(frozen=True, slots=True)
class MergeSortABC(SortingStrategyABC[T]):
    def sort(self, data: Sequence[T], *, key: Callable[[T], Any] | None = None, reverse: bool = False) -> list[T]:
        return merge_sort(data, key=key, reverse=reverse)


@dataclass(frozen=True, slots=True)
class QuickSortABC(SortingStrategyABC[T]):
    def sort(self, data: Sequence[T], *, key: Callable[[T], Any] | None = None, reverse: bool = False) -> list[T]:
        return quick_sort(data, key=key, reverse=reverse)


@dataclass(slots=True)
class SorterABC(Generic[T]):
    """The Context in Strategy Pattern terms."""

    strategy: SortingStrategyABC[T]

    def sort(self, data: Sequence[T], *, key: Callable[[T], Any] | None = None, reverse: bool = False) -> list[T]:
        return self.strategy.sort(data, key=key, reverse=reverse)


# ---------------------------------------------------------------------------
# 2) Strategy Pattern with Protocol (implicit interface)
# ---------------------------------------------------------------------------


class SortingStrategyProto(Protocol[T]):
    def sort(
        self,
        data: Sequence[T],
        *,
        key: Callable[[T], Any] | None = None,
        reverse: bool = False,
    ) -> list[T]:
        ...


# A callable strategy with the same signature as our algorithms.
SortCallable = Callable[[Sequence[T]], list[T]]


@dataclass(frozen=True, slots=True)
class FunctionSortStrategy(Generic[T]):
    """Adapter: wrap a sort function so it can be used as a Strategy object."""

    fn: Callable[[Sequence[T]], list[T]]

    def sort(self, data: Sequence[T], *, key: Callable[[T], Any] | None = None, reverse: bool = False) -> list[T]:
        return self.fn(data, key=key, reverse=reverse)  # type: ignore[misc]


@dataclass(slots=True)
class SorterProto(Generic[T]):
    strategy: SortingStrategyProto[T]

    def sort(self, data: Sequence[T], *, key: Callable[[T], Any] | None = None, reverse: bool = False) -> list[T]:
        return self.strategy.sort(data, key=key, reverse=reverse)


# ---------------------------------------------------------------------------
# 3) Strategy Pattern with Callable
# ---------------------------------------------------------------------------


SortFn = Callable[[Sequence[T]], list[T]]


@dataclass(slots=True)
class SorterCallable(Generic[T]):
    strategy: Callable[[Sequence[T]], list[T]]

    def sort(self, data: Sequence[T], *, key: Callable[[T], Any] | None = None, reverse: bool = False) -> list[T]:
        return (self.strategy)(data, key=key, reverse=reverse)  # type: ignore[misc]


# ---------------------------------------------------------------------------
# Small demo
# ---------------------------------------------------------------------------


def _demo() -> None:
    data = [5, 1, 4, 2, 8, 0, 2]

    abc_sorter = SorterABC(BubbleSortABC())
    proto_strategy: SortingStrategyProto[int] = FunctionSortStrategy(merge_sort)
    proto_sorter = SorterProto(proto_strategy)
    callable_sorter = SorterCallable(quick_sort)

    print("input      :", data)
    print("abc/bubble :", abc_sorter.sort(data))
    print("proto/merge:", proto_sorter.sort(data))
    print("call/quick :", callable_sorter.sort(data))
    print("reverse    :", callable_sorter.sort(data, reverse=True))

    words = ["pear", "banana", "fig", "apple"]
    print("key=len    :", proto_sorter.sort(words, key=len))


if __name__ == "__main__":
    _demo()
