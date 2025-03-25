import os
import shutil
from datetime import datetime
import argparse


def create_or_rename_path(args):
    # Check if the directory exists
    if os.path.exists(args.path):
        # Get the current time as a string in the format YYYYMMDD_HHMMSS
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        # Create the new directory name with the timestamp
        new_path = f"{args.path}_{timestamp}"
        # Rename the existing directory
        shutil.move(args.path, new_path)
        print(f"Renamed existing directory to {new_path}")
    # Create the directory
    os.makedirs(args.path, exist_ok=True)
    print(f"Created directory {args.path}")

    if os.path.exists(args.path):
        # HV_cal path
        HV_cal_path = args.path + "/HV_cal"
        os.makedirs(HV_cal_path, exist_ok=True)
        print(f"Created directory {HV_cal_path}")
        # correction before
        correction_before_path = args.path + "/correction_before"
        os.makedirs(correction_before_path, exist_ok=True)
        print(f"Created directory {correction_before_path}")
        # correction after
        correction_after_path = args.path + "/correction_after"
        os.makedirs(correction_after_path, exist_ok=True)
        print(f"Created directory {correction_after_path}")
        # data
        data_HV_path = args.path_data + "/data/" + args.mode + "/HV_cal"
        os.makedirs(data_HV_path, exist_ok=True)
        print(f"Created directory {data_HV_path}")
        data_before_path = args.path_data + "/data/" + args.mode + "/correction_before"
        os.makedirs(data_before_path, exist_ok=True)
        print(f"Created directory {data_before_path}")
        data_after_path = args.path_data + "/data/" + args.mode + "/correction_after"
        os.makedirs(data_after_path, exist_ok=True)
        print(f"Created directory {data_after_path}")


# Example usage
# path = "example_directory"


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Analysis fit result")
    parser.add_argument("--WALL", type=int, help="WALL number", required=True)
    parser.add_argument("--CB", type=int, help="CB number", required=True)
    parser.add_argument("--ROB", type=int, help="ROB number", required=True)
    parser.add_argument("--mode", type=str, help="str number", required=True)

    args = parser.parse_args()
    filepath = (
        "../result/"
        + "/CB"
        + str(args.CB)
        + "/WALL"
        + str(args.WALL)
        + "/ROB"
        + str(args.ROB)
        + "/"
        + str(args.mode)
    )
    filepath_data = "../result" + "/CB" + str(args.CB)
    parser.add_argument(
        "--path", type=str, default=filepath, help="in and out file path"
    )
    parser.add_argument(
        "--path_data", type=str, default=filepath_data, help="in and out file path"
    )
    args = parser.parse_args()

    create_or_rename_path(args)
