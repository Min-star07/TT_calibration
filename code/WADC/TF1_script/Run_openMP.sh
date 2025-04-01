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
    path=../TF1_FIT/Init
    ./OpenMP_FIT -path $path -fl $filename_list -v 1 -m $mode -type $type
    # First-time fit
    cd "$original_dir" || { echo "Failed to return to original directory"; exit 1; }
    path=../TF1_FIT/Final
    ./OpenMP_FIT -path $path -fl $filename_list -v 1 -m $mode -type $type

    # First-time fit
    cd "$original_dir" || { echo "Failed to return to original directory"; exit 1; }
    path=../TF1_FIT/Check_fitagain
    ./OpenMP_FIT -path $path -fl $filename_list -v 1 -m $mode -type $type

done
