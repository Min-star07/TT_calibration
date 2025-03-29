import argparse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
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
    parser.add_argument("--PMT", type=int, help="max channel", required=True)

    args = parser.parse_args()

    # Construct file paths based on input arguments
    base_path_in_mask = f"../../../../result/CB{args.CB}/WALL{args.WALL}/ROB{args.ROB}/{args.mode}/{args.TYPE}/HV{args.HV}"
    mask_output_suffix = (
        f"/CB{args.CB}_WALL{args.WALL}_ROB{args.ROB}_{args.mode}_mask_result.txt"
    )
    mask_output_file = f"{base_path_in_mask}{mask_output_suffix}"

    ##################################################
    # Generate json config
    ##################################################
    # base_path_in_HV = f"../../../../result/CB{args.CB}/WALL{args.WALL}/ROB{args.ROB}/{args.mode}/HV_cal"
    base_path_in_HV = f"../../../../result/CB{args.CB}"
    hv_input_suffix = f"/Test_HV_calibration_result.txt"
    hv_infile = f"{base_path_in_HV}{hv_input_suffix}"
    print(hv_infile)
    base_path_out = f"../../../../result/CB{args.CB}"
    hv_output_suffix = f"/CB{args.CB}_WALL{args.WALL}_ROB{args.ROB}_{args.mode}_PM{args.PMT}_result.json"
    outfile = f"{base_path_out}{hv_output_suffix}"
    Generate_JUNO_json.JUNO_TT_config(args, hv_infile, mask_output_file, outfile)


if __name__ == "__main__":
    main()
