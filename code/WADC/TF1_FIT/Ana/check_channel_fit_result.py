import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


class CHECK:
    @staticmethod
    def channel_fit_result(infile, outfile):
        """
        Analyzes a channel data file and identifies channels
        with values exceeding the mean (excluding min and max).

        Parameters:
            infile (str): Path to the input file (tab-separated values).
            outfile (str): Path to the output file for saving results.
        """
        try:
            # Load the data from the input file
            df = pd.read_csv(infile, sep="\t", header=None)

            # Exclude the min and max values to calculate the mean
            data = df[19]
            # #######################Methods1 : use mean value###################################
            # mean_excluding_min_max = data[
            #     (data != data.min()) & (data != data.max())
            # ].mean()

            # print("Mean excluding min and max:", mean_excluding_min_max)

            # # Calculate the ratio of each value to the mean
            # ratio = data / mean_excluding_min_max

            # #######################Methods2 : use median value###################################
            median_value = data.median()

            print("Median value :", median_value)

            # Calculate the ratio of each value to the mean
            ratio = data / median_value

            # Identify problem channels where the ratio is greater than 1
            problem_channel_list = df[ratio > 4].copy()

            # Print the problematic channels for debugging
            print("Problem channels:")
            print(problem_channel_list)

            # Save the problematic channels to the output file
            problem_channel_list.to_csv(outfile, sep="\t", index=False, header=False)
            print(f"Problem channels saved to {outfile}")

        except Exception as e:
            print(f"An error occurred: {e}")

    # Example usage
    # CHECK.channel_fit_result("input_file.txt", "output_file.txt")
    @staticmethod
    def merge(args, infile, outfile):
        dict_res = {}
        try:
            df = pd.read_csv(infile, sep="\t", header=None)
            dict_res.update({"CB": args.CB})
            dict_res.update({"WALL": args.WALL})
            dict_res.update({"ROB": args.ROB})
            dict_res.update({"channel": df[0].tolist()})
            # df[0].to_csv(outfile, sep="\t", header=None, index=None, mode="a")
            df = pd.DataFrame([dict_res])
            df.to_csv(outfile, sep="\t", index=None, header=None, mode="a")
        except:
            print("All channels are ok!!!!!!!!!!!!!!!!!")
