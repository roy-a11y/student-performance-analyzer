def calculate_statistics(df):
    """
    Calculates subject-wise statistics and identifies
    topper and weakest student.
    """

    # Drop the Name column to work only with numeric data
    marks_df = df.drop(columns=["Name"])

    # Subject-wise statistics
    subject_average = marks_df.mean()
    subject_median = marks_df.median()

    # Student-wise average
    df["Average"] = marks_df.mean(axis=1)

    # Identify topper and weakest student
    topper = df.loc[df["Average"].idxmax()]
    weakest = df.loc[df["Average"].idxmin()]

    return {
        "subject_average": subject_average,
        "subject_median": subject_median,
        "topper": topper,
        "weakest": weakest,
        "data": df
    }
