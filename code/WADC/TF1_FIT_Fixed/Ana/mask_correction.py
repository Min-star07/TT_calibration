import argparse
import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from analysis_fitparameters import Plotter
from Getdatafromdatabase import DataAnalyzer
import math

# Use custom plot style
plt.style.use("mystyle.txt")


def build_file_path(wall, cb, rob, mode, hv, dtype):
    """Construct file path for result files based on input arguments."""
    return f"../../../../result/WALL{wall}/CB{cb}/ROB{rob}/{mode}/{dtype}/HV{hv}"


def build_input_file_path(wall, cb, rob, mode, dtype, hv, filename):
    """Construct input file path based on directory and filename."""
    return f"WALL{wall}_CB{cb}_ROB{rob}_{mode}_{filename}.txt"


def load_data(filepath, description, header="infer"):
    """
    Load data from a given file path with optional header handling.

    Parameters:
    - filepath: str, the path to the file to be loaded.
    - description: str, a label to describe the file for error messages.
    - header: str or int or None, default 'infer'. The header argument passed to pd.read_csv.

    Returns:
    - A pandas DataFrame containing the data from the file.
    """
    if not os.path.exists(filepath):
        print(f"Error: {description} file not found at {filepath}")
        exit(1)

    return pd.read_csv(filepath, sep="\t", header=header)


def calculate_gain_correction(df_mask, df_result):
    """Calculate new gain correction using result data."""
    last_column_mask = df_mask.iloc[:, -1]
    print(last_column_mask)
    ratio = (df_result[19] - 1e6) / 1e6
    print(ratio)
    # mask_new = df_mask["gain_correction"] / (1 + ratio)
    # Calculate the new values based on the last column of df_mask and ratio
    mask_new = last_column_mask / (1 + ratio)
    # Apply math.ceil element-wise
    mask_new = mask_new.apply(math.ceil)
    return mask_new


def save_updated_mask(df_mask, filepath):
    """Save the updated mask data back to the file."""
    df_mask.to_csv(filepath, sep="\t", index=False)
    print(f"Updated mask data saved to {filepath}")


def main():
    # Argument parsing
    parser = argparse.ArgumentParser(
        description="Analyze fit result and update mask data."
    )
    parser.add_argument("--CB", type=int, required=True, help="CB number")
    parser.add_argument("--ROB", type=int, required=True, help="ROB number")
    parser.add_argument("--mode", type=str, required=True, help="Mode number")
    parser.add_argument("--WALL", type=int, required=True, help="Wall number")
    parser.add_argument("--HV", type=int, required=True, help="HV number")
    parser.add_argument("--TYPE1", type=str, required=True, help="Data type 1")
    parser.add_argument("--TYPE2", type=str, required=True, help="Data type 2")
    args = parser.parse_args()

    # Build file paths
    path1 = build_file_path(
        args.WALL, args.CB, args.ROB, args.mode, args.HV, args.TYPE1
    )
    path2 = build_file_path(
        args.WALL, args.CB, args.ROB, args.mode, args.HV, args.TYPE2
    )

    # Build input filenames
    infile1 = os.path.join(
        path1,
        build_input_file_path(
            args.WALL, args.CB, args.ROB, args.mode, args.TYPE1, args.HV, "mask_result"
        ),
    )
    infile2 = os.path.join(
        path2,
        build_input_file_path(
            args.WALL, args.CB, args.ROB, args.mode, args.TYPE2, args.HV, "Final_result"
        ),
    )
    print(infile2)

    # # Load data
    df_mask = load_data(infile1, "Mask")
    df_result = load_data(infile2, "Final result", header=None)

    # Drop the first column from both DataFrames
    # df_mask = df_mask.drop(df_mask.columns[0], axis=1)
    # df_result = df_result.drop(df_result.columns[0], axis=1)

    # Ensure df_result has at least 20 columns
    if df_result.shape[1] <= 19:
        print("Error: df_result does not contain the required column (19).")
        exit(1)

    # Calculate the new gain correction
    # df_mask["gain_correction_new"] = calculate_gain_correction(df_mask, df_result)
    mask_new = calculate_gain_correction(df_mask, df_result)
    print(mask_new)
    # Transform the list into a DataFrame
    df_from_list = pd.DataFrame(mask_new)
    # print(df_from_list)

    # Merge with the original mask DataFrame
    # Assuming you want to add the new column to df_mask
    merged_df = pd.concat([df_mask, df_from_list], axis=1)

    # print("\nMerged DataFrame:")
    # print(merged_df)

    # # Save the updated mask data
    save_updated_mask(merged_df, infile1)


if __name__ == "__main__":
    main()
