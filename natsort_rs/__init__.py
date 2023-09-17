from .natsort_rs import natsort_strings


def natsort(
        vals: list, 
        key = None, 
        ignore_case = False
        ):
    if key is None:
        strs_for_sorting = vals
    else:
        strs_for_sorting = [key(item) for item in vals]
    
    sorted_indices = natsort_strings(strs_for_sorting, ignore_case)
    return [vals[idx] for idx in sorted_indices]