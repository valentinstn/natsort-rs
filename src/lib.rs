// src/lib.rs

use pyo3::prelude::*;
use pyo3::types::PyList; // Import PyList from pyo3::types
use human_sort::compare;

/// Sort a list of strings naturally (Python-facing function).
#[pyfunction]
fn natsort_strings(list: &PyList, ignore_case: bool) -> PyResult<Vec<usize>> {
    let vec: Vec<String> = list.extract()?;
    let mut indexed_strings: Vec<(usize, String)>;
    if ignore_case {
        indexed_strings = vec.iter().map(|val| val.to_lowercase()).enumerate().collect();
    } else {
        indexed_strings = vec.iter().map(|val| val.clone()).enumerate().collect();
    }
    indexed_strings.sort_by(|(_, a), (_, b)| compare(a, b));
    Ok(indexed_strings.iter().map(|(index, _)| *index).collect())
}

/// A Python module implemented in Rust.
#[pymodule]
fn natsort_rs(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(natsort_strings, m)?)?;
    Ok(())
}
