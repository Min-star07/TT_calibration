import argparse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from read_figure import figure_cropping, figure_trans

from split import read_data
from app import num_dis
import os

# Use the custom plotting style (ensure that 'mystyle.txt' exists)
plt.style.use("mystyle.txt")


def main():
    """
    Main function to handle command-line arguments and run the analysis.

    This function parses command-line arguments, constructs input and output file
    paths based on those arguments, processes images using figure_cropping and
    figure_trans, splits and crops the data, and then applies classification
    to the resulting data using num_dis.
    """

    # Argument parser to get command-line arguments
    parser = argparse.ArgumentParser(description="Analysis fit result")
    parser.add_argument("--CB", type=int, help="CB number", required=True)
    parser.add_argument("--ROB", type=int, help="ROB number", required=True)
    parser.add_argument("--mode", type=str, help="Mode number", required=True)
    parser.add_argument("--FEB", type=int, help="FEB number", required=True)
    parser.add_argument("--WALL", type=int, help="WALL number", required=True)
    parser.add_argument("--HV", type=int, help="HV number", required=True)
    parser.add_argument("--TYPE", type=str, help="Type number", required=True)
    parser.add_argument("--max_channel", type=int, help="Max channel", required=True)
    parser.add_argument("--PMT", type=int, help="PMT number", required=True)

    # Parse the arguments
    args = parser.parse_args()

    # Construct file paths based on input arguments
    base_path = f"../../../../result/CB{args.CB}/WALL{args.WALL}/ROB{args.ROB}/{args.mode}/{args.TYPE}/HV{args.HV}"
    infile_suffix = (
        f"CB{args.CB}_WALL{args.WALL}_ROB{args.ROB}_{args.mode}_Q1_hist2D.png"
    )
    outfile_suffix = (
        f"CB{args.CB}_WALL{args.WALL}_ROB{args.ROB}_{args.mode}_trans_Q1_hist2D.png"
    )

    infile = os.path.join(base_path, infile_suffix)
    outfile = os.path.join(base_path, outfile_suffix)
    print(infile)
    # Ensure input file exists before processing
    if not os.path.exists(infile):
        print(f"Error: The input file {infile} does not exist.")
        return

    try:
        # Crop the figure and save the output
        figure_cropping(infile, outfile)
    except Exception as e:
        print(f"Error during figure cropping: {e}")
        return

    # Process the image and get the list of figures
    figure_list = figure_trans(outfile)
    if not figure_list:
        print(f"Warning: No figures returned from {outfile}.")
        return

    # Read and process the data from the split figures
    try:
        result = read_data(figure_list)
    except Exception as e:
        print(f"Error during figure data reading: {e}")
        return

    # Process the results and classify the data
    for key, value in result.items():
        try:
            # Get predictions for both split parts (gain_left and gain_right)
            gain_left = num_dis(value[0])
            gain_right = num_dis(value[1])

            # Display results in a formatted manner
            print(f"{key}:")
            print(
                f"  Left prediction = {gain_left[0]}, Right prediction = {gain_right[0]}"
            )
            print(f"  Left index = {gain_left[1]}, Right index = {gain_right[1]}")
        except Exception as e:
            print(f"Error processing {key}: {e}")


if __name__ == "__main__":
    main()
