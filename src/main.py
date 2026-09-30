import argparse
import logging
import os

from load_data import load_student_data
from analysis import calculate_comprehensive_statistics
from grading import assign_grades_vectorized
from visualize import generate_analytics_dashboard

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_INPUT = os.path.join(BASE_DIR, "data", "students_large.csv")
if not os.path.exists(DEFAULT_INPUT):
    DEFAULT_INPUT = os.path.join(BASE_DIR, "data", "students.csv")
DEFAULT_OUTPUT_DIR = os.path.join(BASE_DIR, "output")


def main():
    parser = argparse.ArgumentParser(description="Scalable Student Academic Performance Analyzer")
    parser.add_argument("--input", type=str, default=DEFAULT_INPUT, help="Path to students CSV file")
    parser.add_argument("--output-dir", type=str, default=DEFAULT_OUTPUT_DIR, help="Directory to save output files")
    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)

    # 1. Load Data
    df = load_student_data(args.input, base_dir=BASE_DIR)

    # 2. Comprehensive Analytics
    results = calculate_comprehensive_statistics(df)
    df = results["data"]

    # 3. Vectorized Grade Assignment
    score_col = "average_score" if "average_score" in df.columns else "Average"
    df["Grade"] = assign_grades_vectorized(df[score_col])

    # 4. Console Output
    print("\n" + "=" * 50)
    print("      STUDENT PERFORMANCE ANALYTICS REPORT      ")
    print("=" * 50)
    print(f"Total Students Processed: {results['total_students']:,}")
    print(f"Identified At-Risk Students: {results['at_risk_count']:,} ({results['at_risk_percentage']}%)")
    
    print("\n--- Subject-Wise Performance ---")
    print(results["subject_stats"].to_string())

    name_col = "name" if "name" in df.columns else "Name"
    print("\n--- Academic Standings ---")
    print(f"Top Performer : {results['topper'][name_col]} (Score: {results['topper'][score_col]})")
    print(f"Lowest Score  : {results['weakest'][name_col]} (Score: {results['weakest'][score_col]})")

    if results["correlations"]:
        print("\n--- Key Behavioral Correlations with Scores ---")
        for metric, corr in results["correlations"].items():
            print(f"  • {metric.replace('_', ' ').title()}: {corr:+.3f}")

    # 5. Export Output Artifacts
    output_csv = os.path.join(args.output_dir, "final_result.csv")
    cols_to_export = [col for col in ["student_id", name_col, "grade_level", score_col, "Grade", "at_risk"] if col in df.columns]
    df[cols_to_export].to_csv(output_csv, index=False)
    print(f"\nSaved processed records to: {output_csv}")

    # 6. Save Text Summary Report
    summary_path = os.path.join(args.output_dir, "summary.txt")
    with open(summary_path, "w", encoding="utf-8") as f:
        f.write("STUDENT PERFORMANCE SUMMARY REPORT\n")
        f.write("===================================\n\n")
        f.write(f"Total Cohort Size: {results['total_students']:,}\n")
        f.write(f"At-Risk Students : {results['at_risk_count']:,} ({results['at_risk_percentage']}%)\n\n")
        f.write("Subject Statistics:\n")
        f.write(results["subject_stats"].to_string())
        f.write("\n\n")
        f.write(f"Top Performer: {results['topper'][name_col]} - {results['topper'][score_col]}\n")
        f.write(f"Lowest Score : {results['weakest'][name_col]} - {results['weakest'][score_col]}\n")
    print(f"Saved text report to: {summary_path}")

    # 7. Visualization
    dashboard_img = os.path.join(args.output_dir, "analytics_dashboard.png")
    generate_analytics_dashboard(df, results["subject_stats"], dashboard_img)

    print("=" * 50)
    print("Analysis pipeline completed successfully!")


if __name__ == "__main__":
    main()
