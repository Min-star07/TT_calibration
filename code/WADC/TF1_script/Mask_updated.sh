#!/bin/bash
# Save the current directory
original_dir=$(pwd)

# Define constants
type1=correction_before
type2=correction_after
mode=WADC

# Read file and skip the first line
while IFS=$'\t' read -r current_WALL current_CB current_ROB current_FEB current_PMT current_HV current_MAX_OPERA current_MAX_JUNO _ || [[ -n "$current_WALL" ]]; do
    current_HV=6

    echo "Processing file: $file with MODE=$mode, CB=$current_CB, WALL=$current_WALL, ROB=$current_ROB, FEB=$current_FEB, PMT=$current_PMT, HV=$current_HV, max channel in opera=$current_MAX_OPERA, max channel in JUNO=$current_MAX_JUNO"

 

    # Analyze result
    cd "$original_dir" || { echo "Failed to return to original directory"; exit 1; }
    cd ../TF1_FIT/Ana || { echo "Directory not found"; exit 1; }
    python mask_correction.py --CB $current_CB --WALL $current_WALL --ROB $current_ROB --mode $mode --PMT $current_PMT --HV $current_HV  --TYPE1 $type1 --TYPE2 $type2 --max_channel "$current_MAX_JUNO"



done < <(sed '1d' configuration.txt)