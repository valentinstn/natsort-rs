from .natsort_rs import get_sorted_indices

from typing import Callable, Literal, overload

@overload
def natsort[T](
    vals: list[T],
    key: Callable | None = None,
    ignore_case: bool = True,
    return_indices: Literal[False] = False,
    none_last: bool = True,
) -> list[T]: ...

@overload
def natsort[T](
    vals: list[T],
    key: Callable | None = None,
    ignore_case: bool = True,
    return_indices: Literal[True] = True,
    none_last: bool = True,
) -> list[int]: ...

def natsort[T](
    vals: list[T],
    key: Callable | None = None,
    ignore_case: bool = True,
    return_indices: bool = False,
    none_last: bool = True,
) -> list[T] | list[int]:
    if key is None:
        strs_for_sorting = vals
    else:
        strs_for_sorting = [key(item) for item in vals]

    # Performance-critical part is implemented in Rust
    sorted_indices = get_sorted_indices(strs_for_sorting, ignore_case, none_last)

    if return_indices:
        return sorted_indices
    else:
        return [vals[idx] for idx in sorted_indices]
