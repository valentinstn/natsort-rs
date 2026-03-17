use natord::compare;
use pyo3::prelude::*;
use pyo3::types::{PyList, PyString, PyTuple};

/// Compare two rows (slices of strings) element-by-element using natural sort order.
/// Implements Python-style tuple comparison semantics: compare element by element,
/// and if all compared elements are equal, the shorter row is considered smaller.
fn compare_vec_nat(a: &[String], b: &[String]) -> std::cmp::Ordering {
    let len = a.len().min(b.len());

    for i in 0..len {
        let ord = compare(&a[i], &b[i]);
        if ord != std::cmp::Ordering::Equal {
            return ord;
        }
    }

    a.len().cmp(&b.len())
}

/// Convert a single Python item (str, list, or tuple) into a Vec<String> row.
/// A bare string becomes a single-element row, while a list or tuple becomes a
/// multi-element row — enabling unified handling of both flat and tuple inputs.
fn extract_row(item: &Bound<'_, PyAny>, ignore_case: bool) -> PyResult<Vec<String>> {
    // Try tuple first, then list, then fall back to bare string
    if let Ok(py_tuple) = item.cast::<PyTuple>() {
        let mut row = Vec::with_capacity(py_tuple.len());
        for elem in py_tuple.iter() {
            let s = elem.cast::<PyString>()?.str()?.to_string();
            row.push(if ignore_case { s.to_lowercase() } else { s });
        }
        return Ok(row);
    }

    if let Ok(py_list) = item.cast::<PyList>() {
        let mut row = Vec::with_capacity(py_list.len());
        for elem in py_list.iter() {
            let s = elem.cast::<PyString>()?.str()?.to_string();
            row.push(if ignore_case { s.to_lowercase() } else { s });
        }
        return Ok(row);
    }

    // Bare string — wrap in a single-element row
    let s = item.cast::<PyString>()?.str()?.to_string();
    Ok(vec![if ignore_case { s.to_lowercase() } else { s }])
}

/// Return the indices that would sort `rows` in natural order.
///
/// Each element of `rows` may be:
/// - a plain `str`  → sorted as a single key (original behaviour)
/// - a `tuple[str, ...]` or `list[str]` → sorted lexicographically across all
///   keys using natural comparison (new tuple-support behaviour)
///
/// `ignore_case` applies to every string element regardless of the row shape.
#[pyfunction]
fn get_sorted_indices(
    _py: Python,
    rows: &Bound<PyList>,
    ignore_case: bool,
) -> PyResult<Vec<usize>> {
    let mut data: Vec<Vec<String>> = Vec::with_capacity(rows.len());

    for item in rows.iter() {
        data.push(extract_row(&item, ignore_case)?);
    }

    let mut idx: Vec<usize> = (0..data.len()).collect();
    idx.sort_by(|&i, &j| compare_vec_nat(&data[i], &data[j]));
    Ok(idx)
}

/// The Python module definition
#[pymodule]
#[pyo3(gil_used = false)]
fn natsort_rs(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(get_sorted_indices, m)?)?;
    Ok(())
}
