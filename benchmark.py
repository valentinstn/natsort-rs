import time
import random
import string

from natsort import natsorted as natsort_py
from natsort_rs import natsort as natsort_rs
from tomark import Tomark


def generate_random_strings(seed, num, length=10, prefix=''):
    random.seed(seed)
    
    characters = string.ascii_letters + string.digits
    
    random_strings = []
    for _ in range(num):
        random_string = ''.join(random.choice(characters) for _ in range(length))
        random_strings.append(prefix + random_string)
    
    return random_strings


def measure_execution_time(fn_name, func, *args, **kwargs):
    num_runs = 10
    total_execution_time = 0
    for _ in range(num_runs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        execution_time = end_time - start_time
        total_execution_time += execution_time
    average_execution_time = total_execution_time / num_runs
    print(f"{fn_name} took an average of {average_execution_time:.6f} seconds "
          f"to execute ({len(args[0])} items).")
    return average_execution_time, result


if __name__ == '__main__':
    random_seed = 1
    string_length = 15
    example_datas = [
        generate_random_strings(random_seed, rep, string_length) for rep in [
            10, 
            100, 
            1_000, 
            10_000, 
            100_000, 
            1_000_000
        ]
    ]

    benchmark_results = []
    for example_data in example_datas:
        dur_py, _ = measure_execution_time('natsort_py', natsort_py, example_data)
        dur_rs, _ = measure_execution_time('natsort_rs', natsort_rs, example_data, None, False, False)
        dur_rs_par, _ = measure_execution_time('natsort_rs_par', natsort_rs, example_data, None, False, True)
        ratio = dur_py / dur_rs_par

        print(f'Speed improvement: {ratio:.1f} times')
        benchmark_results.append({
            'No. of items': len(example_data),
            'Duration natsort [s]': f'{dur_py:.5f}',
            'Duration natsort-rs [s]': f'{dur_rs:.5f}',
            'Duration natsort-rs parallel [s]': f'{dur_rs_par:.5f}',
            'Relative speedup': f'{ratio:.1f}'
        })
    
    print(Tomark.table(benchmark_results))