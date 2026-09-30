import argparse
import os
import numpy as np
import pandas as pd

def generate_students(n=10000, seed=42):
    np.random.seed(seed)
    
    first_names = ["Aarav", "Ananya", "Rohan", "Priya", "Rahul", "Neha", "Amit", "Sneha", 
                   "Vikram", "Pooja", "Arjun", "Aditi", "Karan", "Kavya", "Siddharth", "Riya"]
    last_names = ["Sharma", "Verma", "Patel", "Gupta", "Singh", "Kumar", "Iyer", "Reddy", 
                  "Roy", "Das", "Choudhury", "Nair", "Mehta", "Joshi", "Bose", "Ghosh"]

    student_ids = [f"STU-{10000 + i}" for i in range(n)]
    names = [f"{np.random.choice(first_names)} {np.random.choice(last_names)}" for _ in range(n)]
    genders = np.random.choice(["Male", "Female", "Other"], size=n, p=[0.48, 0.48, 0.04])
    grade_levels = np.random.choice([9, 10, 11, 12], size=n)
    
    # Behavioral features
    attendance = np.clip(np.random.beta(a=7, b=2, size=n) * 100, 35, 100).round(1)
    study_hours = np.clip(np.random.gamma(shape=3, scale=3, size=n), 1, 35).round(1)
    prev_gpa = np.clip(np.random.normal(loc=3.0, scale=0.5, size=n), 1.0, 4.0).round(2)
    extracurricular = np.random.choice(["Yes", "No"], size=n, p=[0.55, 0.45])
    internet_access = np.random.choice(["Yes", "No"], size=n, p=[0.90, 0.10])
    parent_education = np.random.choice(
        ["High School", "Some College", "Bachelor's", "Master's", "Doctorate"],
        size=n,
        p=[0.25, 0.20, 0.35, 0.15, 0.05]
    )

    # Base academic capability influenced by attendance, study hours, and previous GPA
    base_capability = (
        0.35 * (attendance / 100) * 100 +
        0.25 * np.clip(study_hours * 3.5, 0, 100) +
        0.40 * (prev_gpa / 4.0) * 100
    )

    # Subject scores with noise
    subjects = ["Math", "Physics", "Chemistry", "English", "Computer_Science"]
    scores = {}
    for sub in subjects:
        noise = np.random.normal(0, 8, size=n)
        scores[sub] = np.clip((base_capability + noise), 15, 100).round(1)

    df = pd.DataFrame({
        "student_id": student_ids,
        "name": names,
        "gender": genders,
        "grade_level": grade_levels,
        "parent_education": parent_education,
        "attendance_rate": attendance,
        "study_hours_weekly": study_hours,
        "previous_gpa": prev_gpa,
        "internet_access": internet_access,
        "extracurricular": extracurricular,
        **scores
    })

    # Overall average & At-Risk binary classification label
    subject_cols = subjects
    df["average_score"] = df[subject_cols].mean(axis=1).round(1)
    df["at_risk"] = ((df["average_score"] < 50) | (df["attendance_rate"] < 60)).astype(int)

    return df

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate synthetic student academic dataset")
    parser.add_argument("--count", type=int, default=10000, help="Number of student records to generate")
    parser.add_argument("--output", type=str, default="data/students_large.csv", help="Output file path")
    args = parser.parse_args()

    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    print(f"Generating {args.count} student records...")
    df = generate_students(n=args.count)
    df.to_csv(args.output, index=False)
    print(f"Successfully saved to {args.output} ({len(df)} rows, {len(df.columns)} columns)")
