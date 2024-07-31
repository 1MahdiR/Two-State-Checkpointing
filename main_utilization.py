import matplotlib.pyplot as plt

from bench_utilization import BENCH

BENCH_LENGTH = len(BENCH)

PLOT_ALL = True

if __name__ == "__main__":
    et_data = {'TsCp':0, "TsCp-DVS":0, "Non-Uniform":0, "Uniform":0, "R_target":0}
    e_data = {'TsCp':0, "TsCp-DVS":0, "Non-Uniform":0, "Uniform":0, "R_target":0}
    r_data = {'TsCp':0, "TsCp-DVS":0, "Non-Uniform":0, "Uniform":0, "R_target":0}
    k_data = {'TsCp':0, "TsCp-DVS":0, "Non-Uniform":0, "Uniform":0, "R_target":0}
    schemes_labels = ["TsCp", "TsCp-DVS", "Non-Uniform", "Uniform", "R_target(0.99999)"]
    for bench in BENCH:
        data = bench.run_bench()
        et_ls = []
        e_ls = []
        r_ls = []
        k_ls = []
        d = bench.d
        
        for i in data:
            et, e, r, k = i
            et_ls.append(et)
            e_ls.append(e)
            r_ls.append(r)
            k_ls.append(k)

        et_data["TsCp"] += et_ls[0]
        et_data["TsCp-DVS"] += et_ls[1]
        et_data["Non-Uniform"] += et_ls[2]
        et_data["Uniform"] += et_ls[3]
        et_data["R_target"] += et_ls[4]

        e_data["TsCp"] += e_ls[0]
        e_data["TsCp-DVS"] += e_ls[1]
        e_data["Non-Uniform"] += e_ls[2]
        e_data["Uniform"] += e_ls[3]
        e_data["R_target"] += e_ls[4]

        r_data["TsCp"] += r_ls[0]
        r_data["TsCp-DVS"] += r_ls[1]
        r_data["Non-Uniform"] += r_ls[2]
        r_data["Uniform"] += r_ls[3]
        r_data["R_target"] += r_ls[4]

        k_data["TsCp"] += k_ls[0]
        k_data["TsCp-DVS"] += k_ls[1]
        k_data["Non-Uniform"] += k_ls[2]
        k_data["Uniform"] += k_ls[3]
        k_data["R_target"] += k_ls[4]
            
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
            ax.set_ylim(min(r_ls) - 0.01, 1.001)
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

    plt.figure() 
    ax = plt.subplot(1, 1, 1)
    bar_width = 0.35
    et_data_ls = [ round(x/BENCH_LENGTH, 2) for x in list(et_data.values()) ]
    ax.bar(schemes_labels, et_data_ls, bar_width, label="et_data_ls", color="green")
    ax.set_ylim(min(et_data_ls) - 100, max(et_data_ls) + 100)
    for i, v in enumerate(et_data_ls):
        ax.text(i, v + 0.5, str(v), ha='center', va='bottom')
    plt.title("Execution Time by Different Schemes")
    plt.ylabel("execution time")
    plt.tight_layout()
    plt.show()

    plt.figure() 
    ax = plt.subplot(1, 1, 1)
    bar_width = 0.35
    e_data_ls = [ round(x/BENCH_LENGTH, 2) for x in list(e_data.values()) ]
    ax.bar(schemes_labels, e_data_ls, bar_width, label="e_data_ls", color="orange")
    ax.set_ylim(min(e_data_ls) - 1000, max(e_data_ls) + 1000)
    for i, v in enumerate(e_data_ls):
        ax.text(i, v + 0.5, str(round(v, 2)), ha='center', va='bottom')  
    plt.title("Energy Consumption by Different Schemes")
    plt.ylabel("energy consumption")
    plt.tight_layout()
    plt.show()

    plt.figure() 
    ax = plt.subplot(1, 1, 1)
    bar_width = 0.35
    r_data_ls = [ round(x/BENCH_LENGTH, 6) for x in list(r_data.values()) ]
    ax.bar(schemes_labels, r_data_ls, bar_width, label="r_ls", color="blue")
    ax.set_ylim(min(r_data_ls) - 0.01, 1.001)
    for i, v in enumerate(r_data_ls):
        ax.text(i, v, str(v), ha='center', va='bottom')  
    plt.title("Reliability by Different Schemes")
    plt.ylabel("reliability")
    plt.tight_layout()
    plt.show()

    plt.figure() 
    ax = plt.subplot(1, 1, 1)
    bar_width = 0.35
    k_data_ls = [ round(x/BENCH_LENGTH) for x in list(k_data.values()) ]
    ax.bar(schemes_labels, k_data_ls, bar_width, label="k_ls", color="green")
    ax.set_ylim(min(k_data_ls) - 1, max(k_data_ls) + 1)
    for i, v in enumerate(k_data_ls):
        ax.text(i, v, str(v), ha='center', va='bottom')  
    plt.title("Number of Checkpoints by Different Schemes")
    plt.ylabel("number of checkpoints")
    plt.tight_layout()
    plt.show()