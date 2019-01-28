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


CONST_LINESTYLES=['-', '-.', ':', '-', '-.', ':', '-', '-.', ':']
CONST_DEFAULT_MEASUREMENTS = (
    '/home/lorenzo/tmp/openloop/100k_60/n1m1w4zerocopy.log||tot w 4||0,'
    '/home/lorenzo/tmp/openloop/100k_60/n1m1w8zerocopy.log||tot w 8||0,'
    '/home/lorenzo/tmp/openloop/100k_60/n1m1w16zerocopy.log||tot w 16||0,'
    '/home/lorenzo/tmp/openloop/100k_60/n2m1w2.log||n2m1w2||1,'
    '/home/lorenzo/tmp/openloop/100k_60/n2m1w4.log||n2m1w4||1,'
    '/home/lorenzo/tmp/openloop/100k_60/n2m1w8.log||n2m1w8||1,'
    '/home/lorenzo/tmp/openloop/100k_60/n2m2w2.log||n2m2w2||2,'
    '/home/lorenzo/tmp/openloop/100k_60/n2m2w4.log||n2m2w4||2,'
    '/home/lorenzo/tmp/openloop/100k_60/n2m2w8.log||n2m2w8||2'
)
CONST_TITLES = ['n1m1', 'n2m1', 'n2m2']

CONST_DEFAULT_PROGRAM = 'rust-tcp-latency'


# Plot given measurments samples
def plot_cdf(measurements, plot, label, plot_id, i=-1):
    x_axis = []
    y_axis = []
    for sample in measurements:
        x_axis.append(sample.value)
        y_axis.append(sample.percentage)

    plot.plot(x_axis, y_axis, linestyle=CONST_LINESTYLES[i], label=label if plot_id == 0 else None, linewidth=2)
    plot.grid(True, which="both", ls="--")
    plot.loglog()
    #plot.set_title(CONST_TITLES[plot_id])


# Measurements file names should be in the format: <<file>||<label>>,<<file>||<label>> etc
def plot_measurements(measurement_files, program):
    i = 0
    fig, axs = plt.subplots(3, 1, sharex=True)
    # Remove horizontal space between axes

    for measurement_file in measurement_files.split(','):
        file_name = measurement_file.split('||')[0]
        label = measurement_file.split('||')[1]
        plot_id = int(measurement_file.split('||')[2])
        with open(file_name, 'r') as ifile:
            measurments = create_measurements_list(ifile.readlines())
            plot_cdf(measurments, axs[plot_id], label, plot_id, i)
        i += 1

    for x in range(0, 3):
        axs[x].text(0.5, 0.01, CONST_TITLES[x],
                verticalalignment='bottom', horizontalalignment='right',
                transform=axs[x].transAxes, fontsize=10)

    # fig.title('Openloop latency, fdr, 100 Khz, 100s, pinning 0-1')
    fig.legend(loc='lower left', bbox_to_anchor=(0.12,0.1))

    plt.xlabel('ns')
    #plt.ylim(bottom=0.0001)
    plt.xlim([7000, 1600000])
    #fig.subplots_adjust(hspace=0)

    fig.subplots_adjust(hspace=0)
    fig.suptitle("YOLO")
    plt.show()


def main():
    measurement_files = sys.argv[1] if len(sys.argv) > 1 else CONST_DEFAULT_MEASUREMENTS
    program = sys.argv[2] if len(sys.argv) > 2 else CONST_DEFAULT_PROGRAM
    plot_measurements(measurement_files, program)


if __name__ == "__main__":
    main()
