#!/bin/bash

########################################################################
# Calculate HV vs Gain
########################################################################

# Save the current directory
original_dir=$(pwd)

# # Define an array of filenames
filename_list=(
# "LED_Wilkinson_6_after_cCB-42_2024-12-12_21_29_000000_hist.root"
'LED_Wilkinson_6_after_cCB-42_2024-12-12_23_42_000000_hist.root'
)
# Define constants
type=correction_after
mode=WADC

# Read file and skip the first line
while IFS=$'\t' read -r current_WALL current_CB current_ROB current_FEB current_PMT current_HV current_MAX_OPERA current_MAX_JUNO _ || [[ -n "$current_WALL" ]]; do
    current_HV=6

    echo "Processing file: $file with TYPE=$type, MODE=$mode, CB=$current_CB, WALL=$current_WALL, ROB=$current_ROB, FEB=$current_FEB, PMT=$current_PMT, HV=$current_HV, max channel in opera=$current_MAX_OPERA, max channel in JUNO=$current_MAX_JUNO"

    for file in "${filename_list[@]}"; do
        # Analyze result
        cd "$original_dir" || { echo "Failed to return to original directory"; exit 1; }
        cd ../TF1_FIT/CNN || { echo "Directory not found"; exit 1; }
        python main.py --TYPE "$type" --mode "$mode" --CB "$current_CB" --WALL "$current_WALL" --ROB "$current_ROB" --FEB "$current_FEB" --PMT "$current_PMT" --HV "$current_HV" --max_channel "$current_MAX_JUNO"
    done

done < <(sed '1d' configuration.txt)
