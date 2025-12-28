use pyo3::prelude::*;
use pyo3::types::PyList;
use natord::compare;

/// Sort a list of strings naturally (Python-facing function) and return their sorted indices
#[pyfunction]
fn get_sorted_indices(list: &Bound<'_, PyList>, ignore_case: bool) -> PyResult<Vec<usize>> {
    let vec: Vec<String> = list.extract()?;
    let mut indexed_strings: Vec<(usize, String)>;
    if ignore_case {
        indexed_strings = vec.iter().map(|val| val.to_lowercase()).enumerate().collect();
    } else {
        indexed_strings = vec.iter().cloned().enumerate().collect();
    }

    indexed_strings.sort_by(|(_, a), (_, b)| compare(a, b));
    Ok(indexed_strings.iter().map(|(index, _)| *index).collect())
}

/// The Python module definition
#[pymodule]
#[pyo3(gil_used = false)]
fn natsort_rs(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(get_sorted_indices, m)?)?;
    Ok(())
}
