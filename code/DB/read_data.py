import argparse
import pandas as pd
import python_mysql_upload

if __name__ == "__main__":

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
    args = parser.parse_args()

    # Construct file paths based on input arguments
    base_path = f"../../result/WALL{args.WALL}/CB{args.CB}/ROB{args.ROB}/{args.mode}/{args.TYPE}/HV{args.HV}"
    infile_suffix = (
        f"/WALL{args.WALL}_CB{args.CB}_ROB{args.ROB}_{args.mode}_Final_result.txt"
    )
    outfile_suffix = (
        f"./WALL{args.WALL}_CB{args.CB}_ROB{args.ROB}_{args.mode}_Final_result.txt"
    )

    infile = f"{base_path}{infile_suffix}"
    outfile = f"{outfile_suffix}"  # Include base path for the output file

    # Load the data from the input file
    try:
        # df = pd.read_csv(infile, sep="\t", header=None)
        # print("Input DataFrame:")
        # print(df)

        # # Insert additional columns
        # df.insert(0, "FEB", [args.FEB] * len(df))
        # df.insert(0, "ROB", [args.ROB] * len(df))
        # df.insert(0, "CB", [args.CB] * len(df))
        # df.insert(0, "WALL", [args.WALL] * len(df))
        # df.insert(len(df.columns), "mode", [args.mode] * len(df))
        # df.insert(len(df.columns), "HV", [args.HV] * len(df))

        # print("Modified DataFrame:")
        # print(df)
        python_mysql_upload.databaseupolad(args, infile,outfile)

        # Save the modified DataFrame to the output file
        # df.to_csv(outfile, sep="\t", header=None, index=False)

    except FileNotFoundError:
        print(f"Error: File '{infile}' not found.")
    except pd.errors.EmptyDataError:
        print(f"Error: The file '{infile}' is empty.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
