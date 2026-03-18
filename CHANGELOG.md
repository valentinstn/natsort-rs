# Changelog

## 0.1.20

- Add support for `None` values: they sort last by default; pass `none_last=False` to sort them first instead
- New `none_last` parameter on `natsort()` and `get_sorted_indices()`

## 0.1.19

- Add support for tuple ordering
- Minimal Python version bumped to 3.11

## 0.1.18

- Add Python 3.15 support via pyo3 abi3 stable ABI (PEP 384)
- Upgrade pyo3 0.27.2 → 0.28.2

## 0.1.17

- Add PyPI-friendly metadata to pyproject.toml (homepage, repository, changelog, readme)

## 0.1.16

- Initial support for free-threaded Python (3.13t and 3.14t)
- Support for 32bit
