# Two-State Checkpointing (TsCp)
This is an implementation of the proposed method in the paper ["Two-State Checkpointing for Energy-Efficient Fault Tolerance in Hard Real-Time Systems"](https://doi.org/10.1109/TVLSI.2015.2512839).

> **Abstract:**
> Checkpointing with rollback recovery is a well-established technique to tolerate transient faults. However, it incurs significant time and energy overheads, which go wasted in fault-free execution states and may not even be feasible in hard real-time systems. This paper presents a low-overhead two-state checkpointing (TsCp) scheme for fault-tolerant hard real-time systems. It differentiates between the fault-free and faulty execution states and leverages two types of checkpoint intervals for these two different states. The first type is nonuniform intervals that are used while no fault has occurred. These intervals are determined based on postponing checkpoint insertions in fault-free states, with the aim of decreasing the number of checkpoint insertions. The second type is uniform intervals that are used from the time when the first fault occurs. They are determined so as to minimize execution time for faulty states, leaving more time available for energy management in fault-free states. Experimental evaluation on an embedded processor (LEON3) and an emerging nonvolatile memory technology (ReRAM) illustrates that TsCp significantly reduces the number of checkpoints (62% on average) compared with previous works, while preserving fault tolerance. This results in 14% and 13% reduced execution time and energy consumption, respectively. Furthermore, we combine TsCp with dynamic voltage scaling (DVS) and achieve up to 26% (21% on average) energy saving compared with the state-of-the-art techniques.

## About TsCp

"Two-State Checkpointing" is a [checkpointing technique](https://en.wikipedia.org/wiki/Application_checkpointing) that uses two different kind of checkpoint intervals; Nonuniform checkpoints and uniform checkpoints. This technique uses nonuniform checkpoints to reduce the energy and time overhead of the application. Then, when the application enters the faulty state it will use uniform checkpoints to tolerate upcoming faults. This way the system will be able to tolerate potential faults while reducing energy and time overheads.

## About the implementation

This implementation is just a simulation and comparison of the TsCp (and TsCp-DVS) vs some other similar approaches like using only nonuniform or only uniform checkpoints which are mentioned in the paper. So basically there are 5 different checkpointing techniques that are implemented in 'Task.py':
- TsCp (`run()`): normal TsCp
- TsCp-DVS (`run_dvs()`): TsCp with applying ['Dynamic Voltage Scaling' (DVS)](https://en.wikipedia.org/wiki/Dynamic_voltage_scaling) technique.
- Nonuniform (`run_non_uniform()`): Only nonuniform checkpoints
- Uniform (`run_uniform()`): Only uniform checkpoints
- Reliability-Aware (`run_reliability_target(R_target)`): Runs in a way that meets a certain level of reliability

**note:** You'll probably need the `matplotlib==3.5.1` python package for the graphs and plots.

## About the 'Reliability-Aware' checkpointing technique
As I said before this method runs in a way that meets a certain level of reliability while other methods only takes the number of tolerable faults and set the checkpointing scheme based on that number. 'Reliability-Aware' approach takes a reliability target as input and based on the parameters (like task execution time, etc.) it calculates how many faults the checkpointing scheme should be able to tolerate to meet the reliability target. After calculating, it will set the checkpointing scheme like a normal TsCp and execute it. 

## Running the simulation

There are 3 kind of simulation available in this project.

#### Synthetic benchmarks
This simulation runs the synthetic benchmarks that are written in 'bench.py' file in the form of python classes. You can edit or add the benchmarks if you want. But remember to add the benchmarks (class names) to the `BENCH` constant at the end of the file.

If you want to run this simulation just run the 'main.py' file.

``` $ python3 main.py ```

#### MiBench benchmarks
This is another simulation which is similar to the previous one but it uses the benchmark from the [MiBench testsuite](https://github.com/embecosm/mibench).

If you want to run this simulation run the 'run_mibench.py' file.

``` $ python3 run_mibench.py ```

#### Utilization simulation
This is a simulation on only one benchmark but it is based on the cpu utilization level.

If you want to run this simulation run the 'main_utilization.py' file.

``` $ python3 main_utilization.py ```

## Configuration

Like I said you can change the configuration of the benchmarks. These benchmarks are at these addresses in the project:
- synthetic: 'bench.py' file
- MiBench: 'mibench/' directory
- utilization-based: 'bench_utilization.py' file

## Last but not least...
I hope you'll find this project useful.

Any comments or contribution to this project would be appreciated.

---

Happy Hacking... :)