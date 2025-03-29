import argparse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from analysis_fitparameters import Plotter
from Getdatafromdatabase import DataAnalyzer
from check_channel_fit_result import CHECK

# Use the custom plotting style
plt.style.use("mystyle.txt")


def main():
    """
    Main function to handle command-line arguments and run analysis.
    """

    # Argument parser
    parser = argparse.ArgumentParser(description="Analysis fit result")
    parser.add_argument("--CB", type=int, help="CB number", required=True)
    parser.add_argument("--ROB", type=int, help="ROB number", required=True)
    parser.add_argument("--mode", type=str, help="mode number", required=True)
    parser.add_argument("--FEB", type=int, help="FEB number", required=True)
    parser.add_argument("--WALL", type=int, help="WALL number", required=True)
    parser.add_argument("--HV", type=int, help="HV number", required=True)
    parser.add_argument("--TYPE", type=str, help="type number", required=True)
    parser.add_argument("--PMT", type=int, help="max channel", required=True)

    args = parser.parse_args()

    # Construct file paths based on input arguments
    base_path = f"../../../../result/CB{args.CB}/WALL{args.WALL}/ROB{args.ROB}/{args.mode}/{args.TYPE}/HV{args.HV}"
    infile_suffix = (
        f"/CB{args.CB}_WALL{args.WALL}_ROB{args.ROB}_{args.mode}_Final_result.txt"
    )

    outfile_suffix = f"/CB{args.CB}_WALL{args.WALL}_ROB{args.ROB}_{args.mode}_fitparameters_result.pdf"

    infile = f"{base_path}{infile_suffix}"
    outfile = f"{base_path}{outfile_suffix}"

    # Load the data from the input file
    try:
        df = pd.read_csv(infile, sep="\t", header=None)
        print(df)
    except FileNotFoundError:
        print(f"Error: File '{infile}' not found.")
        return

    ##################################################
    # Check channel fit result
    ##################################################
    outfile_suffix = f"/CB{args.CB}_WALL{args.WALL}_ROB{args.ROB}_{args.mode}_channel_check_result.txt"
    outfile = f"{base_path}{outfile_suffix}"
    CHECK.channel_fit_result(infile, outfile)

    base_path = f"../../../../result/CB{args.CB}"
    outfile_suffix = f"/CB{args.CB}_channel_check_result.txt"
    outfile_check_result = f"{base_path}{outfile_suffix}"
    CHECK.merge(args, outfile, outfile_check_result)


if __name__ == "__main__":
    main()
