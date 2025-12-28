<h1 align="center">natsort-rs</h1>
<p align="center">
    <em>🚀 A blazing fast natural sorting library for Python written in Rust 🦀</em>
</p>

## Installation

```
pip install natsort-rs
```

## Usage

```py
from natsort_rs import natsort
```

### Sort a list of strings

```py
items = ['item 1', 'item 10', 'item 3']
print(natsort(items))  
# ['item 1', 'item 3', 'item 10']
```

### Sort case insensitively

```py
items = ['Item 1', 'Item 3', 'item 2']
print(natsort(items, ignore_case=True))
# ['Item 1', 'item 2', 'Item 3']
```

### Sort complex objects based on property

```py
items = [
    {'name': 'item 1', 'id': 1},
    {'name': 'item 3', 'id': 3},
    {'name': 'item 2', 'id': 2}
]
print(natsort(items, key=lambda d: d['name']))
# [{'name': 'item 1', 'id': 1}, {'name': 'item 2', 'id': 2}, {'name': 'item 3', 'id': 3}]
```

### Return the sorting indices

This can be helpful if you only want to get the sorted indices returned, that makes the performance-critical part
useful for custom sorting use cases:

```py
items = ['item 1', 'item 10', 'item 3']
print(natsort(items, return_indices=True))  
# [0, 2, 1]
```

## Benchmark

| No. of items | Duration natsort [s] | Duration natsort-rs [s] | Relative speedup |
|-----|-----|-----|-----|
| 10 | 0.00006 | 0.00000 | 16.8 |
| 100 | 0.00094 | 0.00002 | 44.3 |
| 1000 | 0.00281 | 0.00022 | 12.7 |
| 10000 | 0.02835 | 0.00262 | 10.8 |
| 100000 | 0.29712 | 0.03334 | 8.9 |
| 1000000 | 3.31207 | 0.45333 | 7.3 |

Execute `benchmark.py` to reproduce the results.

## Development

### Local build

To build and test the package locally using `uv`:

```bash
uv run maturin develop --release
```

### Running benchmarks

To run benchmarks:

```bash
uv run benchmark.py
```

This will compare the performance of `natsort-rs` against the pure Python `natsort` library and display results in a table format.

## Credits

This Python module is build on top of the [`natord`](https://docs.rs/natord/latest/natord/) crate and inspired by [`natsort`](https://pypi.org/project/natsort/).


## License

MIT License