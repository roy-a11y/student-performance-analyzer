import matplotlib.pyplot as plt

def plot_subject_averages(subject_average):
    plt.figure()
    subject_average.plot(kind="bar")
    plt.title("Average Marks per Subject")
    plt.xlabel("Subject")
    plt.ylabel("Average Marks")
    plt.tight_layout()

    plt.savefig("../output/subject_averages.png")
    plt.show()
