import os
from load_data import load_student_data
from analysis import calculate_statistics
from grading import assign_grade
from visualize import plot_subject_averages


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "students.csv")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)


def main():
    # Load data
    df = load_student_data(DATA_PATH)

    # Analyze data
    results = calculate_statistics(df)

    # Assign grades
    df["Grade"] = df["Average"].apply(assign_grade)

    # Print results
    print("\nSubject-wise Average Marks:")
    print(results["subject_average"])

    print("\nSubject-wise Median Marks:")
    print(results["subject_median"])

    print("\nTopper:")
    print(results["topper"]["Name"], "-", results["topper"]["Average"])

    print("\nWeakest Student:")
    print(results["weakest"]["Name"], "-", results["weakest"]["Average"])

    print("\nFinal Result Table:")
    print(df[["Name", "Average", "Grade"]])

    # Save final results to CSV
    output_csv_path = os.path.join(OUTPUT_DIR, "final_result.csv")
    df[["Name", "Average", "Grade"]].to_csv(output_csv_path, index=False)

    # Save summary report to TXT
    summary_path = os.path.join(OUTPUT_DIR, "summary.txt")
    with open(summary_path, "w") as f:
        f.write("Student Performance Summary\n")
        f.write("===========================\n\n")

        f.write("Subject-wise Average Marks:\n")
        f.write(str(results["subject_average"]))
        f.write("\n\n")

        f.write("Subject-wise Median Marks:\n")
        f.write(str(results["subject_median"]))
        f.write("\n\n")

        f.write(
            f"Topper: {results['topper']['Name']} - {results['topper']['Average']}\n"
        )
        f.write(
            f"Weakest Student: {results['weakest']['Name']} - {results['weakest']['Average']}\n"
        )

    # Visualization
    plot_subject_averages(results["subject_average"], os.path.join(OUTPUT_DIR, "subject_averages.png"))


if __name__ == "__main__":
    main()
