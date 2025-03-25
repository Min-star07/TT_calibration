import argparse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from Getdatafromdatabase import DataAnalyzer

# from analysis_checkresult import DataAnalyzer

plt.style.use("mystyle.txt")

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Analysis fit result")
    parser.add_argument("--CB", type=int, help="CB number", required=True)
    parser.add_argument("--ROB", type=int, help="ROB number", required=True)
    parser.add_argument("--mode", type=str, help="mode number", required=True)
    parser.add_argument("--FEB", type=str, help="FEB number", required=True)
    parser.add_argument("--WALL", type=int, help="int number", required=True)
    parser.add_argument("--max_channel", type=int, help="max channel", required=True)
    parser.add_argument("--HV", type=int, help="max channel", required=True)

    args = parser.parse_args()
    outfile = (
        "/CB"
        + str(args.CB)
        + "_WALL"
        + str(args.WALL)
        + "_ROB"
        + str(args.ROB)
        + "_merge_result.txt"
    )
    parser.add_argument(
        "--outfile", type=str, default=outfile, help="in and out file path"
    )
    outfilepath = (
        "../../../result"
        + "/CB"
        + str(args.CB)
        + "/WALL"
        + str(args.WALL)
        + "/ROB"
        + str(args.ROB)
        + "/WADC/"
        + args.mode
    )

    parser.add_argument(
        "--outfilepath", type=str, default=outfilepath, help="in and out file path"
    )

    args = parser.parse_args()
    DataAnalyzer.mergetxt(args)
    DataAnalyzer.Get_Calibration_result(args)
    # DataAnalyzer.Gain_result_a1(args)
