from .natsort_rs import get_sorted_indices

def natsort(
    vals: list,
    key = None,
    ignore_case: bool = True,
    return_indices: bool = False,
    none_last: bool = True,
) -> list:
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
