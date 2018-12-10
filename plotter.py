import matplotlib.pyplot as plt
import sys

# Run python plotter.py <results_file> where results file is the output of server.rs (bw) or client.rs (latency)
# Shows sampled values and computes bandwidth
# Helper to wrap utilities to parse measurments


# Represent a measurement line output by hdrist cdfthe server/client.
class Measurement:

    value = 0
    percentage = 0

    def __init__(self, oline):
        parsed_line = oline.rstrip('\n').replace('(', '').replace(')', '').split(', ')
        self.value = int(parsed_line[0])
        self.percentage = float(parsed_line[1])


# Returns list of measurements from program stdout
def create_measurements_list(output):
    measurements = []
    for line in output:
        # Debug output
        if len(line) > 1 and line[0] == '(':
            measurements.append(Measurement(line))
    return measurements


CONST_LINESTYLES=['-', '-.', '--', ':', ':']
CONST_DEFAULT_MEASUREMENTS = (
    '/home/lorenzo/thesis/experiments/20181203/latency_benchmark/latency_benchmark_fdr/latency_benchmark_fdr_m1/ds.txt||DS,'
    '/home/lorenzo/thesis/experiments/20181203/latency_benchmark/latency_benchmark_fdr/latency_benchmark_fdr_m1/tcp_loopback.txt||TCP lo'
)

CONST_DEFAULT_PROGRAM = 'rust-tcp-latency'


# Plot given measurments samples
def plot_cdf(measurements, label, i=-1):
    x_axis = []
    y_axis = []
    for sample in measurements:
        x_axis.append(sample.value)
        y_axis.append(sample.percentage)

    plt.plot(x_axis, y_axis, linestyle=CONST_LINESTYLES[i], label=label, linewidth=3)
    if i == -1:
        plt.grid(True)
        plt.loglog()
        plt.show()


# Measurements file names should be in the format: <<file>||<label>>,<<file>||<label>> etc
def plot_measurements(measurement_files, program):
    i = 0
    for measurement_file in measurement_files.split(','):
        file_name = measurement_file.split('||')[0]
        label = measurement_file.split('||')[1]
        with open(file_name, 'r') as ifile:
            measurments = create_measurements_list(ifile.readlines())
            plot_cdf(measurments, label, i)
        i += 1

    plt.grid(True)
    plt.title('Network effective bandwidth' if program == 'rust-tcp-bw' else 'Latency benchmark with m=1')
    plt.xlabel('MB/s' if program == 'rust-tcp-bw' else 'ns')
    plt.ylabel('%')
    plt.semilogy()
    plt.legend(loc='upper right')
    plt.show()


def main():
    measurement_files = sys.argv[1] if len(sys.argv) > 1 else CONST_DEFAULT_MEASUREMENTS
    program = sys.argv[2] if len(sys.argv) > 2 else CONST_DEFAULT_PROGRAM
    plot_measurements(measurement_files, program)


if __name__ == "__main__":
    main()
