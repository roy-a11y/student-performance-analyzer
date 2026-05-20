import matplotlib.pyplot as plt

def plot_subject_averages(subject_average, output_path):
    plt.figure()
    subject_average.plot(kind="bar")
    plt.title("Average Marks per Subject")
    plt.xlabel("Subject")
    plt.ylabel("Average Marks")
    plt.tight_layout()

    plt.savefig(output_path)
    plt.show()
