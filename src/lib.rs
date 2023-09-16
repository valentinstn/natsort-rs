// src/lib.rs

use pyo3::prelude::*;
use pyo3::types::PyList; // Import PyList from pyo3::types
use human_sort::sort;

/// Sort a list of strings naturally (Python-facing function).
#[pyfunction]
fn natsort(list: &PyList) -> PyResult<Vec<String>> {
    let vec: Vec<String> = list.extract()?;
    
    // Convert Vec<String> to Vec<&str>
    let mut vec_str_ref: Vec<&str> = vec.iter().map(|s| s.as_str()).collect();

    // Sort the Vec<&str>
    sort(&mut vec_str_ref);

    // Convert Vec<&str> back to Vec<String>
    let vec_sorted: Vec<String> = vec_str_ref.iter().map(|s| s.to_string()).collect();

    Ok(vec_sorted)
}

/// A Python module implemented in Rust.
#[pymodule]
fn natsort_rs(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(natsort, m)?)?;
    Ok(())
}
