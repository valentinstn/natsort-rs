use natord::compare;
use pyo3::prelude::*;
use pyo3::exceptions::PyTypeError;
use pyo3::types::{PyList, PyNone, PyString, PyTuple};

/// Compare two optional strings using natural sort order.
/// `None` sorts after (or before) all `Some` values depending on `none_last`.
#[inline]
fn compare_opt_str(a: &Option<String>, b: &Option<String>, none_last: bool) -> std::cmp::Ordering {
    match (a, b) {
        (Some(sa), Some(sb)) => compare(sa, sb),
        (None, None) => std::cmp::Ordering::Equal,
        (None, Some(_)) => {
            if none_last {
                std::cmp::Ordering::Greater
            } else {
                std::cmp::Ordering::Less
            }
        }
        (Some(_), None) => {
            if none_last {
                std::cmp::Ordering::Less
            } else {
                std::cmp::Ordering::Greater
            }
        }
    }
}

/// Compare two rows element-by-element using natural sort order.
/// Implements Python-style tuple comparison: compare element by element,
/// and if all compared elements are equal, the shorter row is considered smaller.
/// `None` elements within a row sort after (or before) strings per `none_last`.
fn compare_vec_nat(
    a: &[Option<String>],
    b: &[Option<String>],
    none_last: bool,
) -> std::cmp::Ordering {
    for (x, y) in a.iter().zip(b.iter()) {
        let ord = compare_opt_str(x, y, none_last);
        if ord != std::cmp::Ordering::Equal {
            return ord;
        }
    }
    a.len().cmp(&b.len())
}

/// Compare two optional rows. A `None` row sorts after (or before) all
/// `Some` rows depending on `none_last`. Two `None` rows are equal.
fn compare_opt_rows(
    a: &Option<Vec<Option<String>>>,
    b: &Option<Vec<Option<String>>>,
    none_last: bool,
) -> std::cmp::Ordering {
    match (a, b) {
        (Some(ra), Some(rb)) => compare_vec_nat(ra, rb, none_last),
        (None, None) => std::cmp::Ordering::Equal,
        (None, Some(_)) => {
            if none_last {
                std::cmp::Ordering::Greater
            } else {
                std::cmp::Ordering::Less
            }
        }
        (Some(_), None) => {
            if none_last {
                std::cmp::Ordering::Less
            } else {
                std::cmp::Ordering::Greater
            }
        }
    }
}

/// Extract a single element as an optional string.
/// Returns `Ok(None)` for Python `None`, `Ok(Some(s))` for strings.
#[derive(Debug)]
enum ExtractRes {
    Value(Option<String>),
    Unsupported,
}

#[inline]
fn extract_opt_str(item: &Bound<'_, PyAny>, ignore_case: bool) -> PyResult<ExtractRes> {
    if item.is_none() {
        return Ok(ExtractRes::Value(None));
    }
    // Fast case: native Python string
    if item.is_instance_of::<PyString>() {
        let s = item.cast::<PyString>()?.str()?.to_string();
        return Ok(ExtractRes::Value(Some(if ignore_case { s.to_lowercase() } else { s })));
    }
    // Try extracting as integer without producing Python exceptions to the caller
    if let Ok(i) = item.extract::<i64>() {
        let s = i.to_string();
        return Ok(ExtractRes::Value(Some(if ignore_case { s.to_lowercase() } else { s })));
    }
    // Try extracting as float
    if let Ok(f) = item.extract::<f64>() {
        let s = f.to_string();
        return Ok(ExtractRes::Value(Some(if ignore_case { s.to_lowercase() } else { s })));
    }
    // Signal that this element's type is unsupported; caller will decide whether to
    // turn this into a Python exception (only once, avoiding per-element PyErr allocs).
    Ok(ExtractRes::Unsupported)
}

/// Convert one item (str, tuple, list, or None) into an optional row.
/// Returns `Ok(None)` for a top-level Python `None`.
/// Elements inside tuples/lists may themselves be `None`.
fn extract_row(
    item: &Bound<'_, PyAny>,
    ignore_case: bool,
) -> PyResult<Option<Vec<Option<String>>>> {
    if item.is_none() {
        return Ok(None);
    }
    if let Ok(t) = item.cast::<PyTuple>() {
        let mut out: Vec<Option<String>> = Vec::with_capacity(t.len());
        for e in t.iter() {
            match extract_opt_str(&e, ignore_case)? {
                ExtractRes::Value(v) => out.push(v),
                ExtractRes::Unsupported => {
                    return Err(PyTypeError::new_err("expected string, None, int, or float"))
                }
            }
        }
        return Ok(Some(out));
    }
    if let Ok(l) = item.cast::<PyList>() {
        let mut out: Vec<Option<String>> = Vec::with_capacity(l.len());
        for e in l.iter() {
            match extract_opt_str(&e, ignore_case)? {
                ExtractRes::Value(v) => out.push(v),
                ExtractRes::Unsupported => {
                    return Err(PyTypeError::new_err("expected string, None, int, or float"))
                }
            }
        }
        return Ok(Some(out));
    }
    match extract_opt_str(item, ignore_case)? {
        ExtractRes::Value(v) => Ok(Some(vec![v])),
        ExtractRes::Unsupported => Err(PyTypeError::new_err(
            "expected string, None, int, or float",
        )),
    }
}

/// Return the indices that would sort `rows` in natural order.
///
/// Each element of `rows` may be a plain `str`, a `tuple[str | None, ...]`, a
/// `list[str | None]`, or `None`. `None` values — whether top-level or inside
/// a tuple/list — are placed last when `none_last` is `True` (the default) or
/// first when it is `False`. For homogeneous non-`None` string lists the fast
/// bulk-extract path is used; everything else is handled per-element.
#[pyfunction]
#[pyo3(signature = (rows, ignore_case, none_last=true))]
fn get_sorted_indices(
    _py: Python,
    rows: &Bound<PyList>,
    ignore_case: bool,
    none_last: bool,
) -> PyResult<Vec<usize>> {
    let n = rows.len();

    // Fast path: homogeneous list of plain strings (no None values).
    // Uses Vec<Option<String>> with all-Some elements so the comparator is
    // compare_vec_nat; the None arms are never reached on this path.
    if rows
        .get_item(0)
        .map(|f| f.is_instance_of::<PyString>())
        .unwrap_or(false)
    {
        if let Ok(vec) = rows.extract::<Vec<String>>() {
            let data: Vec<Vec<Option<String>>> = if ignore_case {
                vec.into_iter()
                    .map(|s| vec![Some(s.to_lowercase())])
                    .collect()
            } else {
                vec.into_iter().map(|s| vec![Some(s)]).collect()
            };
            let mut idx: Vec<usize> = (0..n).collect();
            idx.sort_by(|&i, &j| compare_vec_nat(&data[i], &data[j], none_last));
            return Ok(idx);
        }
    }

    // All-None fast path: already sorted, return identity.
    if rows
        .get_item(0)
        .map(|f| f.is_instance_of::<PyNone>())
        .unwrap_or(false)
    {
        if rows.iter().all(|item| item.is_none()) {
            return Ok((0..n).collect());
        }
    }

    // General path: tuples, lists, mixed input, or any None values.
    let data: Vec<Option<Vec<Option<String>>>> = rows
        .iter()
        .map(|item| extract_row(&item, ignore_case))
        .collect::<PyResult<_>>()?;

    let mut idx: Vec<usize> = (0..n).collect();
    idx.sort_by(|&i, &j| compare_opt_rows(&data[i], &data[j], none_last));
    Ok(idx)
}

/// The Python module definition
#[pymodule]
#[pyo3(gil_used = false)]
fn natsort_rs(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(get_sorted_indices, m)?)?;
    Ok(())
}
