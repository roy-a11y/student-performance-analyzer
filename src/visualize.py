import os
import matplotlib.pyplot as plt
import pandas as pd

def generate_analytics_dashboard(df: pd.DataFrame, subject_stats: pd.DataFrame, output_path: str):
    """
    Generates a 4-panel comprehensive analytics dashboard figure.
    """
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle("Academic Performance & Cohort Analytics Dashboard", fontsize=16, fontweight="bold")
    plt.subplots_adjust(hspace=0.35, wspace=0.3)

    # 1. Subject-wise Mean & Median
    ax1 = axes[0, 0]
    x_indices = range(len(subject_stats.index))
    width = 0.35
    ax1.bar([i - width/2 for i in x_indices], subject_stats["Mean"], width=width, label="Mean", color="#2563eb")
    ax1.bar([i + width/2 for i in x_indices], subject_stats["Median"], width=width, label="Median", color="#059669")
    ax1.set_xticks(list(x_indices))
    ax1.set_xticklabels(subject_stats.index, rotation=15)
    ax1.set_ylabel("Marks (0-100)")
    ax1.set_title("Subject Average vs Median")
    ax1.legend()
    ax1.grid(axis="y", linestyle="--", alpha=0.5)

    # 2. Grade Distribution
    ax2 = axes[0, 1]
    if "Grade" in df.columns:
        grade_counts = df["Grade"].value_counts().reindex(["A", "B", "C", "Fail"]).fillna(0)
        colors = ["#16a34a", "#2563eb", "#eab308", "#dc2626"]
        bars = ax2.bar(grade_counts.index, grade_counts.values, color=colors)
        ax2.set_title("Overall Grade Distribution")
        ax2.set_ylabel("Number of Students")
        ax2.grid(axis="y", linestyle="--", alpha=0.5)
        for bar in bars:
            height = bar.get_height()
            ax2.annotate(f"{int(height):,}",
                         xy=(bar.get_x() + bar.get_width() / 2, height),
                         xytext=(0, 3), textcoords="offset points",
                         ha="center", va="bottom", fontsize=9)

    # 3. Attendance vs Average Score (Risk Scatter)
    ax3 = axes[1, 0]
    score_col = "average_score" if "average_score" in df.columns else "Average"
    if "attendance_rate" in df.columns:
        if "at_risk" in df.columns:
            normal = df[df["at_risk"] == 0]
            risk = df[df["at_risk"] == 1]
            ax3.scatter(normal["attendance_rate"], normal[score_col], alpha=0.3, s=15, color="#2563eb", label="Good Standing")
            ax3.scatter(risk["attendance_rate"], risk[score_col], alpha=0.6, s=25, color="#dc2626", label="At-Risk")
        else:
            ax3.scatter(df["attendance_rate"], df[score_col], alpha=0.3, s=15, color="#2563eb")
        ax3.set_xlabel("Attendance Rate (%)")
        ax3.set_ylabel("Average Score")
        ax3.set_title("Attendance vs Academic Performance")
        ax3.legend()
        ax3.grid(True, linestyle="--", alpha=0.5)

    # 4. Cohort / Grade Level Performance
    ax4 = axes[1, 1]
    if "grade_level" in df.columns:
        cohort = df.groupby("grade_level")[score_col].mean()
        ax4.plot([f"Grade {g}" for g in cohort.index], cohort.values, marker="o", linewidth=2.5, color="#7c3aed")
        ax4.set_title("Performance across Grade Levels")
        ax4.set_ylabel("Mean Score")
        ax4.grid(True, linestyle="--", alpha=0.5)
    else:
        ax4.text(0.5, 0.5, "Cohort breakdown not available\n(no grade_level column)",
                 ha="center", va="center", color="gray")

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, dpi=200, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved analytics dashboard plot to {output_path}")
