from typing import Optional, Tuple, TypeVar, Union

from typing_extensions import Protocol, overload, runtime_checkable

from .iterable import Iterable, Iterator

__all__ = [
    "Mapping",
]


K = TypeVar("K")
V = TypeVar("V")
T = TypeVar("T")


@runtime_checkable
class Mapping(Protocol[K, V]):
    def __contains__(self, item: V) -> bool:
        ...

    def __getitem__(self, index: K) -> V:
        ...

    def __iter__(self) -> Iterator[K]:
        ...

    def __len__(self) -> int:
        ...

    def __eq__(self, other: object) -> bool:
        ...

    def __ne__(self, other: object) -> bool:
        ...

    @overload
    def get(self, key: K) -> Optional[V]:
        ...

    @overload
    def get(self, key: K, default: Union[V, T]) -> Union[V, T]:
        ...

    def items(self) -> Iterable[Tuple[K, V]]:
        ...

    def keys(self) -> Iterable[K]:
        ...

    def values(self) -> Iterable[V]:
        ...
