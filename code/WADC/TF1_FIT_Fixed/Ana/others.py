import argparse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

plt.style.use("mystyle.txt")


def read_data(base_path, infile_suffix):
    """
    Function to read data from a given file.

    Parameters:
    base_path (str): The base path of the file.
    infile_suffix (str): The suffix of the file name.

    Returns:
    pd.DataFrame: The data read from the file.
    """
    infile = f"{base_path}{infile_suffix}"
    try:
        df = pd.read_csv(infile, sep="\t", header=None)
        return df
    except FileNotFoundError:
        print(f"Error: File '{infile}' not found.")
        return None


def calculate_ratio(df1, df2, column_index):
    """
    Function to calculate the ratio between two columns of different DataFrames.

    Parameters:
    df1 (pd.DataFrame): First DataFrame.
    df2 (pd.DataFrame): Second DataFrame.
    column_index (int): The index of the column to calculate the ratio.

    Returns:
    pd.Series: The ratio of the two columns.
    """
    Q1_1 = df1[column_index]
    Q1_2 = df2[column_index]

    if len(Q1_1) != len(Q1_2):
        raise ValueError(
            "Error: The number of channels (rows) in the two files does not match."
        )

    return Q1_1 / Q1_2


def plot_data(df, outfile, label, yerr_col=None):
    """
    Function to plot the data with optional error bars.

    Parameters:
    df (pd.DataFrame): The DataFrame containing the data to plot.
    outfile (str): The output file path to save the plot.
    label (str): The label for the plot.
    yerr_col (int): The column index for the y-error bars.
    """

    plt.errorbar(
        df[0],
        df[6],
        yerr=df[yerr_col] if yerr_col is not None else None,
        fmt=".",
        capsize=7,
        label=label,
    )


def main():
    """
    Main function to handle command-line arguments and run analysis.
    """

    # Argument parser
    parser = argparse.ArgumentParser(description="Analysis fit result")
    parser.add_argument("--CB", type=int, help="CB number", required=True)
    parser.add_argument("--ROB", type=int, help="ROB number", required=True)
    parser.add_argument("--mode", type=str, help="mode number", required=True)
    parser.add_argument("--WALL", type=int, help="WALL number", required=True)
    parser.add_argument("--TYPE", type=str, help="type number", required=True)
    args = parser.parse_args()

    # Construct file paths based on input arguments
    infile_suffix = (
        f"/WALL{args.WALL}_CB{args.CB}_ROB{args.ROB}_{args.mode}_Final_result.txt"
    )
    outfile_suffix = (
        f"/WALL{args.WALL}_CB{args.CB}_ROB{args.ROB}_{args.mode}_Q1_compare.pdf"
    )

    # HV values and labels for the two fits
    HV = [800, 801]
    labels = ["second fit", "third fit"]
    plt.figure(figsize=(8, 6))
    # Load and plot data from both input files
    for i, hv in enumerate(HV):
        base_path = f"../../../../result/WALL{args.WALL}/CB{args.CB}/ROB{args.ROB}/{args.mode}/{args.TYPE}/HV{hv}"
        infile = f"{base_path}{infile_suffix}"
        outfile = f"{base_path}{outfile_suffix}"

        # Read the data
        df = read_data(base_path, infile_suffix)
        if df is None:
            return  # Skip if the file is not found

        # Plot the data
        plot_data(df, outfile, label=labels[i], yerr_col=7)
    plt.xlabel("Channel")
    plt.ylabel("Q1")
    plt.ylim(5, 11)
    plt.title("Q1 Across Channels")
    plt.legend()

    plt.savefig(outfile)
    plt.show()

    # Now, load both datasets again to calculate and plot the ratio
    base_path1 = f"../../../../result/WALL{args.WALL}/CB{args.CB}/ROB{args.ROB}/{args.mode}/{args.TYPE}/HV{HV[0]}"
    base_path2 = f"../../../../result/WALL{args.WALL}/CB{args.CB}/ROB{args.ROB}/{args.mode}/{args.TYPE}/HV{HV[1]}"

    df1 = read_data(base_path1, infile_suffix)
    df2 = read_data(base_path2, infile_suffix)

    if df1 is not None and df2 is not None:
        try:
            # Calculate the ratio between Q1 (column 6) from both datasets
            ratio = calculate_ratio(df1, df2, 6)

            # Plot the ratio
            plt.figure(figsize=(8, 6))
            plt.plot(
                df1[0],
                ratio,
                marker="o",
                label="Q1 Ratio (Fit second / Fit third)",
                color="blue",
            )
            plt.axhline(y=1, color="red", linestyle="--", label="Ratio = 1")
            plt.xlabel("Channel")
            plt.ylabel("Q1 Ratio")
            plt.title("Q1 Ratio Across Channels")
            plt.ylim(0.8, 1.2)
            plt.legend()

            # Save the ratio plot
            outfile_ratio = (
                f"{base_path2}{outfile_suffix.replace('Q1_compare', 'Q1_ratio_plot')}"
            )
            plt.savefig(outfile_ratio)

            # Show the ratio plot
            plt.show()

        except ValueError as e:
            print(e)


if __name__ == "__main__":
    main()
