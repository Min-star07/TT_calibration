import argparse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from analysis_fitparameters import Plotter
from Getdatafromdatabase import DataAnalyzer
from check_channel_fit_result import CHECK
from generate_config import Generate_JUNO_json

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
    parser.add_argument("--max_channel", type=int, help="max channel", required=True)
    parser.add_argument("--PMT", type=int, help="max channel", required=True)

    args = parser.parse_args()

    # Construct file paths based on input arguments
    base_path_in = f"../../../../result/CB{args.CB}/WALL{args.WALL}/ROB{args.ROB}/{args.mode}/{args.TYPE}/HV{args.HV}"
    base_path_out = f"../../../../result/CB{args.CB}"
    infile_suffix = (
        f"/CB{args.CB}_WALL{args.WALL}_ROB{args.ROB}_{args.mode}_Final_result.txt"
    )
    infile = f"{base_path_in}{infile_suffix}"
    # Load the data from the input file
    try:
        df = pd.read_csv(infile, sep="\t", header=None)
        print(df)
    except FileNotFoundError:
        print(f"Error: File '{infile}' not found.")
        return

    ##################################################
    # Gain calculation and other data processing
    ##################################################

    # # Input and output file for gain analysis
    mask_output_suffix = (
        f"/CB{args.CB}_WALL{args.WALL}_ROB{args.ROB}_{args.mode}_mask_result.txt"
    )
    mask_output_file = f"{base_path_out}{mask_output_suffix}"

    # # Gain calculation steps
    DataAnalyzer.get_max_channel(infile)
    DataAnalyzer.get_amplification_factor(infile, mask_output_file, args)

    # Optional: Uncomment if gain calibration and distribution are needed
    DataAnalyzer.gain_calibration_result(args, infile)
    DataAnalyzer.gain_distribution_histogram(args, base_path_out, infile)


if __name__ == "__main__":
    main()
