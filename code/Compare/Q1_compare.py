import argparse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from scipy.optimize import curve_fit

# Use the custom plotting style
plt.style.use("mystyle.txt")


# Define the double Gaussian function
def gaussian(x, a1, b1, c1):
    """Gaussian function."""
    return a1 * np.exp(-((x - b1) ** 2) / (2 * c1**2))


def parse_arguments():
    """
    Parse command-line arguments.
    Ensure all required arguments are provided.
    """
    parser = argparse.ArgumentParser(description="Analysis fit result")
    parser.add_argument("--CB", type=int, help="CB number", required=True)
    parser.add_argument("--ROB", type=int, help="ROB number", required=True)
    parser.add_argument("--HV", type=int, help="HV value", required=True)
    parser.add_argument(
        "--mode",
        nargs=2,
        type=str,
        help="Mode numbers (e.g., FADC and WADC)",
        required=True,
    )
    parser.add_argument("--WALL", type=int, help="WALL number", required=True)
    parser.add_argument("--TYPE", type=str, help="Type", required=True)

    # Parse the arguments
    args = parser.parse_args()

    # Ensure all arguments are valid
    if args.CB < 0 or args.ROB < 0 or args.WALL < 0:
        raise ValueError("CB, ROB, and WALL values must be positive integers.")

    return args


def compare_Q1(args):
    """
    Load Q1 and error data from files based on input arguments.
    If files are not found, return None.
    """
    Q1_list = []
    for i, item in enumerate(args.mode):
        infile_suffix = f"/WALL{args.WALL}_CB{args.CB}_ROB{args.ROB}_{args.mode[i]}_Final_result.txt"
        base_path = f"../../result/WALL{args.WALL}/CB{args.CB}/ROB{args.ROB}/{args.mode[i]}/{args.TYPE}/HV{args.HV}"
        infile = f"{base_path}{infile_suffix}"
        print(f"Loading data from: {infile}")

        try:
            # Load file with tab separator
            df = pd.read_csv(infile, sep="\t", header=None)
            Q1_list.append(df[6])
        except FileNotFoundError:
            print(f"Error: File '{infile}' not found.")
            return None, None
        except pd.errors.EmptyDataError:
            print(f"Error: File '{infile}' is empty or corrupted.")
            return None, None
    return Q1_list


def Q1_distri_hist2d(args, ratio):
    """Create a 2D histogram plot."""
    numbers = np.array(ratio)
    # Reshape the data into a square array (8x8)
    data = numbers.reshape(8, 8)

    # Create the 2D heatmap
    plt.figure(figsize=(10, 10))
    plt.imshow(data, cmap="viridis", interpolation="nearest")

    # Annotate each cell with its value
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            plt.text(j, i, f"{data[i, j]:.1f}", ha="center", va="center", color="white")

    plt.xlabel("Channel")
    plt.ylabel("Channel")
    plt.title(f"Q1_Ratio_FADC/WADC_ROB{args.ROB}")

    figname = f"WALL{args.WALL}_CB{args.CB}_ROB{args.ROB}_Q1_compare_hist2D.pdf"
    plt.savefig(figname)
    plt.show()


def Q1_distri_hist1d(args, ratio):
    """Create a 1D histogram and fit a Gaussian."""
    y_min, y_max = np.min(ratio), np.max(ratio)
    y_mean, y_std = np.mean(ratio), np.std(ratio)
    lower = y_min - (y_max - y_min)
    upper = y_max + (y_max - y_min)

    print("Y-axis range:", lower, upper)

    # Create a histogram
    bins = 30
    hist, bin_edges = np.histogram(
        ratio, range=[lower, upper], bins=bins, density=False
    )
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2

    # Fit the histogram data to the Gaussian function
    popt, pcov = curve_fit(
        gaussian, bin_centers, hist, p0=[40, y_mean, y_std], maxfev=1000
    )
    print("Fitted parameters:", popt)

    # Calculate chi-squared
    chi_squared = np.sum((hist - gaussian(bin_centers, *popt)) ** 2)
    ndf = len(hist) - 3  # Degrees of freedom (bins - parameters)
    chi_squared_ndf = chi_squared / ndf if ndf > 0 else np.inf

    print(f"Chi-squared: {chi_squared}")
    print(f"Degrees of freedom: {ndf}")
    print(f"Chi-squared per degree of freedom: {chi_squared_ndf}")

    # Plot the histogram and the fitted Gaussian
    plt.hist(
        ratio,
        range=[lower, upper],
        bins=bins,
        label=f"Q$_{{1}}$: mean = {y_mean:.1f}, std = {y_std:.1f}",
    )
    plt.plot(
        bin_centers,
        gaussian(bin_centers, *popt),
        "r-",
        linewidth=2,
        label=r"fit: $\mu$ = %.1f, $\sigma$ = %.1f" % (popt[1], popt[2]),
    )

    plt.title(f"Q1_Ratio_FADC/WADC_ROB{args.ROB}")

    plt.xlabel("Q1 Ratio")
    plt.ylabel("# of events")
    plt.legend()

    figname = f"WALL{args.WALL}_CB{args.CB}_ROB{args.ROB}_Q1_compare_hist1D.pdf"
    plt.savefig(figname)
    plt.show()


def main():
    # Parse command-line arguments
    args = parse_arguments()
    print(args.mode[0])
    Q1 = compare_Q1(args)
    print(Q1)
    ratio = Q1[0] / Q1[1]
    Q1_distri_hist2d(args, ratio)
    Q1_distri_hist1d(args, ratio)


if __name__ == "__main__":
    main()
