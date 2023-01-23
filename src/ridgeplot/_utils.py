import sys
from typing import (
    Callable,
    Iterable,
    Iterator,
    List,
    Mapping,
    Optional,
    Sequence,
    Tuple,
    TypeVar,
)

if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol


class _Comparable(Protocol):
    def __lt__(self, __other: "_Comparable") -> bool:
        ...

    def __gt__(self, __other: "_Comparable") -> bool:
        ...


_ComparableT = TypeVar("_ComparableT", bound=_Comparable)


def get_xy_extrema(
    arrays: Iterable[Sequence[Sequence[_ComparableT]]],
) -> Tuple[_ComparableT, _ComparableT, _ComparableT, _ComparableT]:
    """Returns the global x-y extrema (x_min, x_max, y_min, y_max) of a
    sequence of 2D array-like objects.

    Args:
        arrays:
            A sequence of 2D array-like objects.

    Returns:
        A tuple of the form (x_min, x_max, y_min, y_max).
    """
    x: List[_ComparableT] = []
    y: List[_ComparableT] = []
    for array in arrays:
        if len(array) != 2:
            raise ValueError(f"Expected 2D array, got {len(array)}D array instead.")
        if 0 in (len(array[0]), len(array[1])):
            raise ValueError("Cannot get extrema of an empty array.")
        x.extend(array[0])
        y.extend(array[1])
    if 0 in (len(x), len(y)):
        raise ValueError("Cannot get extrema of empty array sequence.")
    return min(x), max(x), min(y), max(y)


def normalise_min_max(val: float, min_: float, max_: float) -> float:
    if max_ <= min_:
        raise ValueError(
            f"max_ should be greater than min_. Got max_={max_} and min_={min_} instead."
        )
    if not (min_ <= val <= max_):
        raise ValueError(f"val ({val}) is out of bounds ({min_}, {max_}).")
    return (val - min_) / (max_ - min_)


KT = TypeVar("KT")  # Mapping key type
VT = TypeVar("VT")  # Mapping value type


class LazyMapping(Mapping[KT, VT]):
    __slots__ = ("_loader", "_inner_mapping")

    def __init__(self, loader: Callable[[], Mapping[KT, VT]]):
        self._loader = loader
        self._inner_mapping: Optional[Mapping[KT, VT]] = None

    @property
    def _mapping(self) -> Mapping[KT, VT]:
        if self._inner_mapping is None:
            self._inner_mapping = self._loader()
        return self._inner_mapping

    def __getitem__(self, item: KT) -> VT:
        return self._mapping.__getitem__(item)

    def __iter__(self) -> Iterator[KT]:
        return self._mapping.__iter__()

    def __len__(self) -> int:
        return self._mapping.__len__()

    def __str__(self) -> str:
        return self._mapping.__str__()

    def __repr__(self) -> str:
        return self._mapping.__repr__()
