# natsort-rs

*A blazing fast natural sorting library for Python written in Rust 🚀*

Warning: **This is a pre-alpha library. It should not yet be used for production code.**

## Installation

Find package files on [PyPI](https://pypi.org/project/natsort-rs/).

## Examples

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

## Benchmark

| No. of items | natsort [s] | natsort-rs [s] | speedup [-] |
|-----|-----|-----|-----|
| 10 | 0.00006 | 0.00000 | 17.0 |
| 100 | 0.00071 | 0.00003 | 24.6 |
| 1000 | 0.00285 | 0.00036 | 7.9 |
| 10000 | 0.02892 | 0.00462 | 6.3 |
| 100000 | 0.29960 | 0.06098 | 4.9 |
| 1000000 | 3.33878 | 0.80086 | 4.2 |

Execute `benchmark.py` to reproduce the results.

## Credits

This Python module is build on top of the [`human-sort`](https://crates.io/crates/human-sort) crate and inspired by [`natsort`](https://pypi.org/project/natsort/).


## License

MIT License