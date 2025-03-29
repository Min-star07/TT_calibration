#!/bin/bash

# Define constants

mode=WADC

# Check if the configuration file exists
config_file="./WADC/TF1_script/configure/cb76.txt"
if [[ ! -f $config_file ]]; then
    echo "Configuration file not found!"
    exit 1
fi

# Read file and skip the first line
while IFS=$'\t' read -r current_WALL current_CB current_PMT current_FEB current_ROB_ID current_ROB _ || [[ -n "$current_WALL" ]]; do
    echo "Processing file: with TYPE=$type, MODE=$mode, WALL=$current_WALL, CB=$current_CB, ROB=$current_ROB, FEB=$current_FEB, PMT=$current_PMT, HV=$current_HV"

    # Uncomment to create necessary paths if not already created
    python3 create_path.py --WALL $current_WALL --CB $current_CB --ROB $current_ROB --mode $mode      #to create necessary path, if you have created, comment this line

done < <(sed '1d' "$config_file")
