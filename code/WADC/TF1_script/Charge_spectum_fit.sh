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

# Read file and skip the first line
while IFS=$'\t' read -r current_WALL current_CB current_PMT current_FEB current_ROB_ID current_ROB _ || [[ -n "$current_WALL" ]]; do
    current_HV=1

    echo "Processing file: $file with TYPE=$type, MODE=$mode, CB=$current_CB, WALL=$current_WALL, ROB=$current_ROB, FEB=$current_FEB, PMT=$current_PMT, HV=$current_HV, max channel in opera=$current_MAX_OPERA, max channel in JUNO=$current_MAX_JUNO"

    for file in "${filename_list[@]}"; do
        # First-time fit
        cd "$original_dir" || { echo "Failed to return to original directory"; exit 1; }
        cd ../TF1_FIT/Init || { echo "Directory not found"; exit 1; }
        HV=$(echo "$file" | awk -F'_' '{print $3}')
        echo "Processing file: $file with HV=$current_HV, TYPE=$type, CB=$current_CB, wall=$current_WALL"
        pwd  # Print the current directory
        ./Run_Fit -CB "$current_CB" -ROB "$current_ROB" -fl "$file" -v "$current_HV" -type "$type" -w "$current_WALL"

        # Second-time fit
        cd "$original_dir" || { echo "Failed to return to original directory"; exit 1; }
        cd ../TF1_FIT/Final || { echo "Directory not found"; exit 1; }
        pwd  # Print the current directory
        echo "Processing file: $file with HV=$current_HV, TYPE=$type, CB=$current_CB, wall=$current_WALL, ROB="$current_ROB""
        ./Run_Fit -CB "$current_CB" -ROB "$current_ROB" -fl "$file" -v "$current_HV" -type "$type" -w "$current_WALL"

        # Final-time fit
        cd "$original_dir" || { echo "Failed to return to original directory"; exit 1; }
        cd ../TF1_FIT/Check_fitagain || { echo "Directory not found"; exit 1; }
        pwd  # Print the current directory
        ./Run_Fit -CB "$current_CB" -ROB "$current_ROB" -fl "$file" -v "$current_HV" -type "$type" -w "$current_WALL"
    done

done < <(sed '1d' "$config_file")
# --max_channel "$current_MAX_JUNO"