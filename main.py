import matplotlib.pyplot as plt

from bench import bench_1

PLOT_ALL = True

if __name__ == "__main__":
    data = bench_1.run_bench()
    et_ls = []
    e_ls = []
    r_ls = []
    k_ls = []
    d = bench_1.d
    schemes_labels = ["TsCp", "TsCp-DVS", "Non-Uniform", "Uniform", "R_target(0.99999)"]
    for i in data:
        et, e, r, k = i
        et_ls.append(et)
        e_ls.append(e)
        r_ls.append(r)
        k_ls.append(k)
        
    if PLOT_ALL:
        plt.figure() 
        ax = plt.subplot(1, 1, 1)
        bar_width = 0.35
        ax.bar(schemes_labels, et_ls, bar_width, label="et_ls", color="green")
        ax.set_ylim(min(et_ls) - 100, max(et_ls) + 100)
        for i, v in enumerate(et_ls):
            ax.text(i, v + 0.5, str(v), ha='center', va='bottom')
        ax.axhline(y=d, color='red', linestyle='-', label=f'Deadline ({d})')  
        plt.title("Execution Time by Different Schemes")
        plt.ylabel("execution time")
        plt.tight_layout()
        plt.show()

        plt.figure() 
        ax = plt.subplot(1, 1, 1)
        bar_width = 0.35
        ax.bar(schemes_labels, e_ls, bar_width, label="e_ls", color="orange")
        ax.set_ylim(min(e_ls) - 1000, max(e_ls) + 1000)
        for i, v in enumerate(e_ls):
            ax.text(i, v + 0.5, str(round(v, 2)), ha='center', va='bottom')  
        plt.title("Energy Consumption by Different Schemes")
        plt.ylabel("energy consumption")
        plt.tight_layout()
        plt.show()

        plt.figure() 
        ax = plt.subplot(1, 1, 1)
        bar_width = 0.35
        ax.bar(schemes_labels, r_ls, bar_width, label="r_ls", color="blue")
        ax.set_ylim(min(r_ls) - 0.01, 1.01)
        for i, v in enumerate(r_ls):
            ax.text(i, v, str(round(v, 6)), ha='center', va='bottom')  
        plt.title("Reliability by Different Schemes")
        plt.ylabel("reliability")
        plt.tight_layout()
        plt.show()

        plt.figure() 
        ax = plt.subplot(1, 1, 1)
        bar_width = 0.35
        ax.bar(schemes_labels, k_ls, bar_width, label="k_ls", color="green")
        ax.set_ylim(min(k_ls) - 1, max(k_ls) + 1)
        for i, v in enumerate(k_ls):
            ax.text(i, v, str(round(v, 2)), ha='center', va='bottom')  
        plt.title("Number of Checkpoints by Different Schemes")
        plt.ylabel("number of checkpoints")
        plt.tight_layout()
        plt.show()