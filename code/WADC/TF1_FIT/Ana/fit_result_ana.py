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
    # parser.add_argument("--max_channel", type=int, help="max channel", required=True)
    parser.add_argument("--PMT", type=int, help="max channel", required=True)

    args = parser.parse_args()

    # Construct file paths based on input arguments
    base_path_in = f"../../../../result/CB{args.CB}/WALL{args.WALL}/ROB{args.ROB}/{args.mode}/{args.TYPE}/HV{args.HV}"
    base_path_out = f"../../../../result/CB{args.CB}"
    infile_suffix = (
        f"/CB{args.CB}_WALL{args.WALL}_ROB{args.ROB}_{args.mode}_Final_result.txt"
    )

    outfile_suffix = f"/CB{args.CB}_WALL{args.WALL}_ROB{args.ROB}_{args.mode}_fitparameters_result.pdf"

    infile = f"{base_path_in}{infile_suffix}"
    outfile = f"{base_path_out}{outfile_suffix}"

    # Load the data from the input file
    try:
        df = pd.read_csv(infile, sep="\t", header=None)
        print(df)
    except FileNotFoundError:
        print(f"Error: File '{infile}' not found.")
        return

    # Define parameter names for plotting
    parameters_name = [
        r"$N_{0}$",
        r"Q$_{0}$",
        r"Q$_{1}$",
        r"$\sigma_{0}$",
        r"$\sigma_{1}$",
        r"$w$",
        r"$\alpha$",
        r"$\mu$",
    ]

    # Open a PDF to save the plots
    with PdfPages(outfile) as pdf_pages:
        for i, param_name in enumerate(parameters_name):
            title_item = f"CB{args.CB}_ROB{args.ROB}_{param_name}"
            print(f"Plotting {title_item}")
            plotter = Plotter(title=title_item, xlabel="Channel", ylabel=param_name)

            # Draw scatter plot (with error bars) and save to the PDF
            plotter.draw_scatter(
                df[0], df[19], df[2 * (i + 1)], df[2 * i + 3], pdf_pages
            )

    # Plot Q1 distribution
    plotter = Plotter(
        title=f"CB{args.CB}_WALL{args.WALL}_ROB{args.ROB}_{args.mode}_Q1",
        xlabel="Q1",
        ylabel="Counts",
    )

    # Save Q1 distribution as both 1D and 2D histograms
    plotter.Q1_distri_hist1d(base_path_out, df[0], df[6])
    plotter.Q1_distri_hist2d(base_path_out, df[0], df[6])

    print(f"Plots saved to {outfile}")

    


if __name__ == "__main__":
    main()
