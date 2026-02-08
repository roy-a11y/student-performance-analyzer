import pandas as pd

def load_student_data(file_path):
    """
    Loads student data from a CSV file.
    """
    return pd.read_csv(file_path)
