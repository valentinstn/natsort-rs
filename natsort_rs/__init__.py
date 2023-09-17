from .natsort_rs import get_sorted_indices


def natsort(
        vals: list, 
        key = None, 
        ignore_case = False
        ):
    if key is None:
        strs_for_sorting = vals
    else:
        strs_for_sorting = [key(item) for item in vals]
    
    sorted_indices = get_sorted_indices(strs_for_sorting, ignore_case)
    return [vals[idx] for idx in sorted_indices]