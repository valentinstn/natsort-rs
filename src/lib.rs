use natord::compare;
use pyo3::prelude::*;
use pyo3::types::{PyList, PyString, PyTuple};

/// Compare two rows element-by-element using natural sort order.
/// Implements Python-style tuple comparison: compare element by element,
/// and if all compared elements are equal, the shorter row is considered smaller.
fn compare_vec_nat(a: &[String], b: &[String]) -> std::cmp::Ordering {
    for (x, y) in a.iter().zip(b.iter()) {
        let ord = compare(x, y);
        if ord != std::cmp::Ordering::Equal {
            return ord;
        }
    }
    a.len().cmp(&b.len())
}

#[inline]
fn extract_str(item: &Bound<'_, PyAny>, ignore_case: bool) -> PyResult<String> {
    let s = item.cast::<PyString>()?.str()?.to_string();
    Ok(if ignore_case { s.to_lowercase() } else { s })
}

/// Convert one item (str, tuple, or list) into a row of strings.
fn extract_row(item: &Bound<'_, PyAny>, ignore_case: bool) -> PyResult<Vec<String>> {
    if let Ok(t) = item.cast::<PyTuple>() {
        return t.iter().map(|e| extract_str(&e, ignore_case)).collect();
    }
    if let Ok(l) = item.cast::<PyList>() {
        return l.iter().map(|e| extract_str(&e, ignore_case)).collect();
    }
    Ok(vec![extract_str(item, ignore_case)?])
}

/// Return the indices that would sort `rows` in natural order.
///
/// Each element of `rows` may be a plain `str`, a `tuple[str, ...]`, or a
/// `list[str]`. For homogeneous string lists the fast bulk-extract path is
/// used; everything else is handled per-element.
#[pyfunction]
fn get_sorted_indices(
    _py: Python,
    rows: &Bound<PyList>,
    ignore_case: bool,
) -> PyResult<Vec<usize>> {
    let n = rows.len();

    // Fast path: homogeneous list of plain strings.
    if rows
        .get_item(0)
        .map(|f| f.is_instance_of::<PyString>())
        .unwrap_or(false)
    {
        if let Ok(vec) = rows.extract::<Vec<String>>() {
            let data: Vec<Vec<String>> = if ignore_case {
                vec.into_iter().map(|s| vec![s.to_lowercase()]).collect()
            } else {
                vec.into_iter().map(|s| vec![s]).collect()
            };
            let mut idx: Vec<usize> = (0..n).collect();
            idx.sort_by(|&i, &j| compare_vec_nat(&data[i], &data[j]));
            return Ok(idx);
        }
    }

    // General path: tuples, lists, or mixed input.
    let data: Vec<Vec<String>> = rows
        .iter()
        .map(|item| extract_row(&item, ignore_case))
        .collect::<PyResult<_>>()?;

    let mut idx: Vec<usize> = (0..n).collect();
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
