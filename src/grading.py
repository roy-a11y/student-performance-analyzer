def assign_grade(average_marks):
    """
    Assigns grade based on average marks.
    """
    if average_marks >= 85:
        return "A"
    elif average_marks >= 70:
        return "B"
    elif average_marks >= 55:
        return "C"
    else:
        return "Fail"
