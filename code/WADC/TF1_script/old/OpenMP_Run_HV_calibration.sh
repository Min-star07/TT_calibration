#!/bin/bash


########################################################################
# Calculate HV vs Gain
########################################################################

# Save the current directory
original_dir=$(pwd)

# Define constants
type=HV_cal
mode=WADC

# Read file and skip the first line
while IFS=$'\t' read -r current_WALL current_CB current_ROB current_FEB current_PMT current_HV current_MAX current_MAX_JUNO _ || [[ -n "$current_WALL" ]]; do

    echo "Processing file: $file with TYPE=$type, MODE=$mode, CB=$current_CB, WALL=$current_WALL, ROB=$current_ROB, FEB=$current_FEB, PMT=$current_PMT, HV=$current_HV, max channel in opera=$current_MAX, max channel in JUNO=$current_MAX_JUNO"
    cd ../HV_calibration
    python main.py --CB $current_CB --ROB $current_ROB --FEB $current_FEB --mode $type  --WALL $current_WALL --max_channel $current_MAX_JUNO --HV $current_HV
    ./Run_Getfigure -CB $current_CB -ROB $current_ROB -w $current_WALL

done < <(sed '1d' configuration.txt)
