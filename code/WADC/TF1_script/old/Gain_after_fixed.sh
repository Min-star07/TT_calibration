#!/bin/bash

########################################################################
# Calculate HV vs Gain
########################################################################

# Save the current directory
original_dir=$(pwd)

# Define an array of filenames
filename_list=(
    'WADC_LED_800_after_cCB-22_2024-11-04_18_27_000000_hist.root'
)

ped=WADC_PED_800_after_cCB-22_2024-11-04_18_31_000000_hist.root
# Define the other parameters
CB=22
ROB=(5 15)
FEB=(985 61)
type="correction_after"
mode="WADC"
wall=1

########################################################################
# Initial FIT
########################################################################
# Change directory to the desired path for initial fitting
cd ../TF1_FIT_Fixed/Init || { echo "Directory not found"; exit 1; }

# Loop over the indices of the ROB and FEB arrays
for i in "${!ROB[@]}"; do
    current_CB=$CB
    current_ROB=${ROB[$i]}
    current_FEB=${FEB[$i]}

    echo "Processing with CB=$current_CB, ROB=$current_ROB, FEB=$current_FEB"

    # Process each file
    for file in "${filename_list[@]}"; do
        HV=$(echo "$file" | awk -F'_' '{print $3}')
        echo "Processing file: $file with HV=$HV, TYPE=$type, CB=$current_CB, ROB=$current_ROB, FEB=$current_FEB"
        
        # Run the fitting command
        ./Run_Fit -CB "$current_CB" -ROB "$current_ROB" -fl "$file" -fd "$ped" -v "$HV" -type "$type"
    done
done

# # ########################################################################
# # # Final FIT
# # ########################################################################
# # Return to the original directory
cd "$original_dir" || { echo "Failed to return to original directory"; exit 1; }
cd ../TF1_FIT_Fixed/Final || { echo "Directory not found"; exit 1; }
pwd  # Print the current directory

# Loop over the indices of the ROB and FEB arrays
for i in "${!ROB[@]}"; do
    current_CB=$CB
    current_ROB=${ROB[$i]}
    current_FEB=${FEB[$i]}


    echo "Processing with CB=$current_CB, ROB=$current_ROB, FEB=$current_FEB"

    # Process each file
    for file in "${filename_list[@]}"; do
        HV=$(echo "$file" | awk -F'_' '{print $3}')
        echo "Processing file: $file with HV=$HV, TYPE=$type, CB=$current_CB, ROB=$current_ROB, FEB=$current_FEB"
        
        # Run the fitting command
        ./Run_Fit -CB "$current_CB" -ROB "$current_ROB" -fl "$file" -v "$HV" -type "$type"
    done
done


cd "$original_dir" || { echo "Failed to return to original directory"; exit 1; }
cd ../TF1_FIT_Fixed/Check_fitagain || { echo "Directory not found"; exit 1; }
pwd  # Print the current directory

# Loop over the indices of the ROB and FEB arrays
for i in "${!ROB[@]}"; do
    current_CB=$CB
    current_ROB=${ROB[$i]}
    current_FEB=${FEB[$i]}

    echo "Processing with CB=$current_CB, ROB=$current_ROB, FEB=$current_FEB"

    # Process each file
    for file in "${filename_list[@]}"; do
        HV=$(echo "$file" | awk -F'_' '{print $3}')
        echo "Processing file: $file with HV=$HV, TYPE=$type, CB=$current_CB, ROB=$current_ROB, FEB=$current_FEB"
        
        # Run the fitting command
        ./Run_Fit -CB "$current_CB" -ROB "$current_ROB" -fl "$file" -v "$HV" -type "$type"
    done
done

#######################################################################
Get the before results such as max channel
#######################################################################

cd "$original_dir" || { echo "Failed to return to original directory"; exit 1; }
cd ../TF1_FIT_Fixed/Ana || { echo "Directory not found"; exit 1; }
pwd  # Print the current directory

# Loop over the indices of the ROB and FEB arrays
for i in "${!ROB[@]}"; do
    current_CB=$CB
    current_ROB=${ROB[$i]}
    current_FEB=${FEB[$i]}

    echo "Processing with CB=$current_CB, ROB=$current_ROB, FEB=$current_FEB"

    # Process each file
    for file in "${filename_list[@]}"; do
        HV=$(echo "$file" | awk -F'_' '{print $3}')
        echo "Processing file: $file with HV=$HV, TYPE=$type, CB=$current_CB, ROB=$current_ROB, FEB=$current_FEB"
        
        # Run the analysis script
        python main.py --CB "$current_CB" --ROB "$current_ROB" --mode "$mode" --HV "$HV" --TYPE "$type" --WALL "$wall" --FEB "$current_FEB"
    done
done
