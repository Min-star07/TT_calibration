import uproot
import pandas as pd
import numpy as np


def read_root_to_csv(root_file_path, tree_name, output_csv_path):
    # Open the ROOT file
    events = uproot.open(root_file_path)

    data = events.arrays(
        [
            "FEB_ID",
            "cat_ID",
            "data_UID",
            "CH",
            "a0",
            "a00_err",
            "a1",
            "a1_err",
            "a2",
            "a3",
            "a4",
            "a5",
            "a5_err",
            "b",
            "ChiSq",
            "status",
        ],
        library="pd",
    )
    print(data)
    # Save the DataFrame to a CSV file
    data.to_csv(output_csv_path, index=False)
    print(f"Data saved to {output_csv_path}")


# Example usage
if __name__ == "__main__":
    root_file_path = "test_b2.root:TB_lin_par"  # Specify your ROOT file path
    tree_name = "TB_lin_par"  # Specify the name of the tree you want to read
    output_csv_path = "tt_elec_calibration.csv"  # Specify the output CSV file path

    read_root_to_csv(root_file_path, tree_name, output_csv_path)
