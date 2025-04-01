#!/bin/bash

########################################################################
# Calculate HV vs Gain
########################################################################

# Save the current directory
original_dir=$(pwd)

# Check if the configuration file exists
config_file="./configure/cb76.txt"
# # Define an array of filenames
filename_list=(
"LED_Wilkinson_cCB-76_correction_before_hist.root"
)
# Define constants
type=correction_before
mode=WADC


for file in "${filename_list[@]}"; do
    # First-time fit
    cd "$original_dir" || { echo "Failed to return to original directory"; exit 1; }
    # cd ../TF1_FIT/Init || { echo "Directory not found"; exit 1; }
    ./OpenMP_FIT -path ../TF1_FIT/Init -fl $filename_list -v 1 -m -type $type

done
