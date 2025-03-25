import argparse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

# Use the custom plotting style
plt.style.use("mystyle.txt")


def parse_arguments():
    """
    Parse command-line arguments.
    Ensure all required arguments are provided.
    """
    parser = argparse.ArgumentParser(description="Analysis fit result")
    parser.add_argument("--CB", type=int, help="CB number", required=True)
    parser.add_argument("--ROB", type=int, help="ROB number", required=True)
    parser.add_argument("--mode", type=str, help="Mode number", required=True)
    parser.add_argument("--WALL", type=int, help="WALL number", required=True)
    parser.add_argument("--TYPE", type=str, help="Type", required=True)

    # Parse the arguments
    args = parser.parse_args()

    # Ensure all arguments are valid
    if args.CB < 0 or args.ROB < 0 or args.WALL < 0:
        raise ValueError("CB, ROB, and WALL values must be positive integers.")

    return args


def load_data(args, Event_num):
    """
    Load Q1 and error data from files based on input arguments.
    If files are not found, return None.
    """
    infile_suffix = (
        f"/WALL{args.WALL}_CB{args.CB}_ROB{args.ROB}_{args.mode}_Final_result.txt"
    )
    Q1_list = []
    Q1_error_list = []

    for item in Event_num:
        base_path = f"../../../../result/WALL{args.WALL}/CB{args.CB}/ROB{args.ROB}/{args.mode}/{args.TYPE}/HV{item}"
        infile = f"{base_path}{infile_suffix}"
        print(f"Loading data from: {infile}")

        try:
            # Load file with tab separator
            df = pd.read_csv(infile, sep="\t", header=None)
            Q1_list.append(df[6])  # Assuming Q1 is in the 6th column
            Q1_error_list.append(df[7])  # Assuming error is in the 7th column
        except FileNotFoundError:
            print(f"Error: File '{infile}' not found.")
            return None, None
        except pd.errors.EmptyDataError:
            print(f"Error: File '{infile}' is empty or corrupted.")
            return None, None

    # Convert to DataFrames
    df_Q1 = pd.DataFrame(Q1_list).reset_index(drop=True)
    df_Q1_error = pd.DataFrame(Q1_error_list).reset_index(drop=True)

    return df_Q1, df_Q1_error


def plot_data(df_Q1, df_Q1_error, Event_num, outfile):
    """
    Plot Q1 values with error bars and save to a PDF.
    """
    with PdfPages(outfile) as pdf_pages:
        for i in range(64):  # Iterate through each channel
            plt.errorbar(
                Event_num,
                df_Q1[i],
                yerr=df_Q1_error[i],
                fmt="o",
                color="blue",
                capsize=5,
            )

            plt.xlabel(r"Gain Factor")
            plt.ylabel("Q1 Value")
            plt.title(f"Channel {i}")  # Start from 1 for user-friendliness

            pdf_pages.savefig()
            plt.close()


def calculate_differences(df_Q1, df_Q1_error):
    """
    Calculate the differences between the last row and all previous rows.
    Also adjust error values.
    """
    last_row = df_Q1.iloc[-1]  # Get the last row of Q1 values
    row_squares = df_Q1_error.apply(np.square, axis=1)
    last_row_error = row_squares.iloc[-1]  # Get the last row of error values

    # Calculate the new error values (sum of squares)
    df_Q1_error_trans = row_squares.add(last_row_error, axis=1).apply(np.sqrt, axis=1)
    df_Q1_diff = df_Q1.subtract(last_row, axis=1)  # Subtract last row from each row

    return df_Q1_diff, df_Q1_error_trans


def plot_differences(df_Q1_diff, df_Q1_error_trans, Event_num, outfile_diff):
    """
    Plot differences with error bars and save to a PDF.
    """
    with PdfPages(outfile_diff) as pdf_pages:
        for i in range(64):  # Iterate through each channel
            plt.errorbar(
                Event_num,
                df_Q1_diff[i],
                yerr=df_Q1_error_trans[i],
                fmt="o",
                color="blue",
                capsize=5,
            )

            plt.xlabel("Gain Factor")
            plt.ylabel("Q1 Difference Value")
            plt.title(f"Channel {i}")  # Start from 1 for user-friendliness

            pdf_pages.savefig()
            plt.close()


def select_max_abs_diff_columns(df_Q1_diff):
    """
    Select the columns with the maximum absolute differences in Q1_diff.
    Returns the indices and values of these columns.
    """
    abs_diff = df_Q1_diff.abs()  # Calculate the absolute differences
    max_abs_diff = abs_diff.max()  # Find the maximum absolute difference
    max_indices = abs_diff.idxmax()  # Get the indices of the max diffs
    return max_indices, max_abs_diff


class Plotter:
    def __init__(self, title="Plot", xlabel="X-axis", ylabel="Y-axis"):
        """Initialize the Plotter with title and axis labels."""
        self.title = title
        self.xlabel = xlabel
        self.ylabel = ylabel

    def draw_scatter(self, x, y, error, outfile):
        """Draw a scatter plot with error bars."""
        y_min, y_max = np.min(y), np.max(y)
        lower = y_min - 0.5 * (y_max - y_min)
        upper = y_max + 0.5 * (y_max - y_min)

        print("Y-axis range:", lower, upper)

        # Create a new figure and axis
        fig, ax = plt.subplots()

        # Plot with error bars
        plt.errorbar(
            x,
            y,
            yerr=error,
            fmt="o",
            color="blue",
            capsize=5,
        )

        # Set title and labels
        ax.set_title(self.title)
        ax.set_xlabel(self.xlabel)
        ax.set_ylabel(self.ylabel)
        ax.set_ylim(lower, upper)
        plt.savefig(outfile)
        plt.close()


def main():
    # Parse command-line arguments
    args = parse_arguments()

    # Define event numbers
    Event_num = [64, 84, 104, 124, 144, 164, 184]

    # Load data
    df_Q1, df_Q1_error = load_data(args, Event_num)
    if df_Q1 is None or df_Q1_error is None:
        return  # Exit if loading data fails

    # Define output file names
    outfile = (
        f"./WALL{args.WALL}_CB{args.CB}_ROB{args.ROB}_{args.mode}_Q1_compare_result.pdf"
    )
    outfile_diff = f"./WALL{args.WALL}_CB{args.CB}_ROB{args.ROB}_{args.mode}_Q1_compare_diff_result.pdf"

    # Plot original data
    plot_data(df_Q1, df_Q1_error, Event_num, outfile)

    # Calculate differences and errors
    df_Q1_diff, df_Q1_error_trans = calculate_differences(df_Q1, df_Q1_error)

    # Plot differences
    plot_differences(df_Q1_diff, df_Q1_error_trans, Event_num, outfile_diff)

    # Select columns with maximum absolute differences
    max_indices, max_abs_diff = select_max_abs_diff_columns(df_Q1_diff)

    # Collect errors for plotting
    # error_list = [df_Q1_error_trans[i] for i in max_indices]

    error_list = []
    for i, item in enumerate(max_indices):
        error_list.append(df_Q1_error_trans.iloc[item, i])
    print(error_list)

    # Print the results
    print(f"Columns with maximum absolute differences: Channel {max_indices}")
    print(f"Max Abs Diff = {max_abs_diff}")

    # Plot scatter for maximum differences
    max_diff_outfile = f"./WALL{args.WALL}_CB{args.CB}_ROB{args.ROB}_{args.mode}_Q1_max_diff_result.pdf"
    Plotter("Max Differences", "Channel", "Max Difference").draw_scatter(
        range(64), max_abs_diff, error_list, max_diff_outfile
    )
    max_diff_outfile = f"./WALL{args.WALL}_CB{args.CB}_ROB{args.ROB}_{args.mode}_Q1_max_diff_location_result.pdf"
    Plotter("Max Differences", "Channel", "Max Difference Location").draw_scatter(
        range(64), max_indices, error_list, max_diff_outfile
    )


if __name__ == "__main__":
    main()
