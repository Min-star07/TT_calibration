#!/bin/bash

type=correction_after


# ########################################################################
# # Get the before results such as max channel
# #####################################################################
# Define the other parameters
CB=22
ROB=(5 15)
FEB=(985 61)

type=correction_after
mode="WADC"
wall=1
HV=800

cd "$original_dir" || { echo "Failed to return to original directory"; exit 1; }
cd ../WADC/TF1_FIT/Ana || { echo "Directory not found"; exit 1; }
pwd  # Print the current directory

# Loop over the indices of the ROB and FEB arrays
for i in "${!ROB[@]}"; do
    current_CB=$CB
    current_ROB=${ROB[$i]}
    current_FEB=${FEB[$i]}

    echo "Processing with CB=$current_CB, ROB=$current_ROB, FEB=$current_FEB"

    # python Q1_compare.py --CB $current_CB --ROB $current_ROB --mode $mode   --TYPE $type --WALL $wall 
    python chi2perndf.py --CB $current_CB --ROB $current_ROB --mode $mode   --TYPE $type --WALL $wall  --HV $HV
    # python others.py --CB $current_CB --ROB $current_ROB --mode $mode   --TYPE $type --WALL $wall
    done