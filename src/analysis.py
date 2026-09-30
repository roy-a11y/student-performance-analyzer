import pandas as pd
import numpy as np

def get_subject_columns(df: pd.DataFrame) -> list:
    """
    Dynamically identifies academic subject columns.
    Excludes identifiers, demographics, and computed behavioral metrics.
    """
    excluded = {
        "student_id", "name", "gender", "grade_level", "parent_education",
        "attendance_rate", "study_hours_weekly", "previous_gpa", "internet_access",
        "extracurricular", "average_score", "average", "at_risk", "grade"
    }
    return [col for col in df.columns if col.lower() not in excluded and np.issubdtype(df[col].dtype, np.number)]

def calculate_comprehensive_statistics(df: pd.DataFrame) -> dict:
    """
    Calculates statistical distributions, cohort breakdowns,
    correlation matrix, and flags at-risk students.
    """
    subject_cols = get_subject_columns(df)
    if not subject_cols:
        raise ValueError("No subject score columns found in dataset.")

    # Calculate overall average if not present
    if "average_score" not in df.columns and "Average" not in df.columns:
        df["average_score"] = df[subject_cols].mean(axis=1).round(2)
    score_col = "average_score" if "average_score" in df.columns else "Average"

    # 1. Subject-wise detailed distribution
    subject_stats = pd.DataFrame({
        "Mean": df[subject_cols].mean().round(2),
        "Median": df[subject_cols].median().round(2),
        "Std_Dev": df[subject_cols].std().round(2),
        "P25": df[subject_cols].quantile(0.25).round(2),
        "P75": df[subject_cols].quantile(0.75).round(2),
        "Pass_Rate_%": ((df[subject_cols] >= 50).mean() * 100).round(1)
    })

    # 2. Toppers & Weakest
    topper = df.loc[df[score_col].idxmax()]
    weakest = df.loc[df[score_col].idxmin()]

    # 3. Early Warning: At-Risk Students
    name_col = "name" if "name" in df.columns else "Name"
    id_col = "student_id" if "student_id" in df.columns else name_col

    if "at_risk" in df.columns:
        at_risk_df = df[df["at_risk"] == 1]
    else:
        at_risk_df = df[df[score_col] < 50]

    # 4. Cohort Performance (e.g. by Grade Level if available)
    cohort_stats = {}
    if "grade_level" in df.columns:
        cohort_stats["by_grade"] = df.groupby("grade_level")[score_col].agg(["mean", "median", "count"]).round(2)
    if "parent_education" in df.columns:
        cohort_stats["by_parent_education"] = df.groupby("parent_education")[score_col].mean().round(2)

    # 5. Correlation with Behavioral Metrics
    correlations = {}
    for metric in ["attendance_rate", "study_hours_weekly", "previous_gpa"]:
        if metric in df.columns:
            correlations[metric] = round(df[metric].corr(df[score_col]), 3)

    return {
        "subject_stats": subject_stats,
        "topper": topper,
        "weakest": weakest,
        "total_students": len(df),
        "at_risk_count": len(at_risk_df),
        "at_risk_percentage": round((len(at_risk_df) / len(df)) * 100, 2),
        "cohort_stats": cohort_stats,
        "correlations": correlations,
        "data": df
    }
