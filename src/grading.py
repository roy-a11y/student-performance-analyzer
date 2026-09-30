import numbers
import numpy as np
import pandas as pd

MIN_SCORE, MAX_SCORE = 0.0, 100.0

# Single source of truth: (inclusive lower bound, label), ascending.
_CUTOFFS = [(55, "C"), (70, "B"), (85, "A")]
_FAIL = "Fail"
_BINS = [-np.inf] + [c for c, _ in _CUTOFFS] + [np.inf]
_LABELS = [_FAIL] + [g for _, g in _CUTOFFS]


def assign_grades_vectorized(scores, strict: bool = True) -> pd.Series:
    """
    Grade a series of scores. Bands: [0,55) Fail, [55,70) C, [70,85) B, [85,100] A.
    strict=True: raise on NaN / non-numeric / out-of-range values.
    strict=False: return NaN for those rows instead.
    """
    s = pd.to_numeric(pd.Series(scores), errors="coerce")
    valid = s.between(MIN_SCORE, MAX_SCORE)  # False for NaN and +/-inf

    if strict and not valid.all():
        bad = s.index[~valid]
        raise ValueError(
            f"{len(bad)} invalid score(s) (missing, non-numeric, or outside "
            f"[{MIN_SCORE}, {MAX_SCORE}]); first indices: {list(bad[:5])}"
        )

    return pd.cut(s.where(valid), bins=_BINS, labels=_LABELS, right=False)


def assign_grade(average_marks: float) -> str:
    """Scalar version; same thresholds and validation as the vectorized one."""
    if isinstance(average_marks, (bool, np.bool_)) or not isinstance(
        average_marks, numbers.Real
    ):
        raise TypeError(f"Expected a real number, got {type(average_marks).__name__}")
    x = float(average_marks)
    if not (MIN_SCORE <= x <= MAX_SCORE):  # also rejects NaN and inf
        raise ValueError(f"Score must be in [{MIN_SCORE}, {MAX_SCORE}], got {x}")

    for cutoff, grade in reversed(_CUTOFFS):
        if x >= cutoff:
            return grade
    return _FAIL