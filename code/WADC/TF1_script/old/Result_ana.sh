# #!/bin/bash

# Save the current directory
original_dir=$(pwd)

# Check if the configuration file exists
config_file="./configure/cb76.txt"
if [[ ! -f "$config_file" ]]; then
    echo "Configuration file not found: $config_file"
    exit 1
fi

# Define an array of filenames
filename_list=(
    "LED_Wilkinson_cCB-76_correction_before_hist.root"
)

# Define constants
type="correction_before"
mode="WADC"

# Read file and skip the first line
sed '1d' "$config_file" | while IFS=$'\t' read -r current_WALL current_CB current_PMT current_FEB current_ROB_ID current_ROB _; do
    current_HV=1
    current_MAX_JUNO=0

    for file in "${filename_list[@]}"; do
        echo "Processing file: $file with TYPE=$type, MODE=$mode, CB=$current_CB, WALL=$current_WALL, ROB=$current_ROB, FEB=$current_FEB, PMT=$current_PMT, HV=$current_HV, max channel in JUNO=$current_MAX_JUNO"

        # Navigate to analysis directory
        cd "$original_dir" || { echo "Failed to return to original directory"; exit 1; }
        cd ../TF1_FIT/Ana || { echo "Directory not found: ../TF1_FIT/Ana"; exit 1; }
        
        # Execute analysis scripts
        python fit_result_ana.py --TYPE "$type" --mode "$mode" --CB "$current_CB" --WALL "$current_WALL" --ROB "$current_ROB" --FEB "$current_FEB" --PMT "$current_PMT" --HV "$current_HV" 
        python fit_result_check.py --TYPE "$type" --mode "$mode" --CB "$current_CB" --WALL "$current_WALL" --ROB "$current_ROB" --FEB "$current_FEB" --PMT "$current_PMT" --HV "$current_HV"
        python gain_confige_result.py --TYPE "$type" --mode "$mode" --CB "$current_CB" --WALL "$current_WALL" --ROB "$current_ROB" --FEB "$current_FEB" --PMT "$current_PMT" --HV "$current_HV" 
        python gain_result_ana.py --TYPE "$type" --mode "$mode" --CB "$current_CB" --WALL "$current_WALL" --ROB "$current_ROB" --FEB "$current_FEB" --PMT "$current_PMT" --HV "$current_HV" --max_channel "$current_MAX_JUNO"

    done

done
