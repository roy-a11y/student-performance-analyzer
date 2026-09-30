import logging
from pathlib import Path
from typing import Optional, Sequence

import pandas as pd

logger = logging.getLogger(__name__)

MAX_FILE_BYTES = 500 * 1024 * 1024  # 500 MB cap; adjust to your needs


def load_student_data(
    file_path: str,
    base_dir: Optional[str] = None,
    chunksize: Optional[int] = None,
    non_negative_cols: Optional[Sequence[str]] = None,
    max_bytes: int = MAX_FILE_BYTES,
) -> pd.DataFrame:
    """Load a student CSV with validation.

    base_dir: if set, the file must resolve inside this directory.
    non_negative_cols: columns where negatives are invalid; they are set
        to NaN (not 0) and counted in the log, never silently altered.
    """
    path = Path(file_path).resolve(strict=False)

    if base_dir is not None:
        try:
            path.relative_to(Path(base_dir).resolve())
        except ValueError:
            raise PermissionError("File path is outside the allowed directory")

    if not path.is_file():
        raise FileNotFoundError(f"Dataset not found: {path.name}")
    if path.suffix.lower() != ".csv":
        raise ValueError("Only .csv files are supported")
    if path.stat().st_size > max_bytes:
        raise ValueError(f"File exceeds {max_bytes:,} byte limit")
    if chunksize is not None and (not isinstance(chunksize, int) or chunksize <= 0):
        raise ValueError("chunksize must be a positive integer")

    read_kwargs = dict(encoding="utf-8", on_bad_lines="error")

    try:
        if chunksize:
            parts = []
            with pd.read_csv(path, chunksize=chunksize, **read_kwargs) as reader:
                for chunk in reader:
                    chunk.columns = chunk.columns.str.strip()
                    parts.append(chunk)  # process/reduce here to actually save memory
            if not parts:
                raise ValueError("CSV contains no data")
            df = pd.concat(parts, ignore_index=True)
        else:
            df = pd.read_csv(path, **read_kwargs)
            df.columns = df.columns.str.strip()
    except pd.errors.EmptyDataError:
        raise ValueError("CSV file is empty")
    except (pd.errors.ParserError, UnicodeDecodeError) as e:
        raise ValueError(f"Malformed CSV: {type(e).__name__}") from e

    if df.empty:
        raise ValueError("CSV contains no rows")
    if df.columns.duplicated().any():
        dupes = df.columns[df.columns.duplicated()].tolist()
        raise ValueError(f"Duplicate column names: {dupes}")

    if non_negative_cols:
        missing = set(non_negative_cols) - set(df.columns)
        if missing:
            raise ValueError(f"Columns not found: {sorted(missing)}")
        for col in non_negative_cols:
            if not pd.api.types.is_numeric_dtype(df[col]):
                raise TypeError(f"Column '{col}' is not numeric")
            bad = df[col] < 0
            if bad.any():
                logger.warning("Column '%s': %d negative values set to NaN", col, int(bad.sum()))
                df.loc[bad, col] = float("nan")

    logger.info("Loaded %s rows, %s columns from %s", f"{len(df):,}", len(df.columns), path.name)
    return df