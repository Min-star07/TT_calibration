#include <iostream>
#include <omp.h>
#include <cstdlib>
#include <string>

int main() {
    const int ROB_num[2] = {5, 15};
    const int CB_num[2] = {22, 23};
    const int HV_num[1] = {800};
    const int wall[1] = {1};

    std::string fl = "WADC_LED_800_after_cCB-22_2024-10-02_17_56_000000_hist.root";
    std::string type = "correction_after";

    // Outer loop for OpenMP parallelization
    #pragma omp parallel for
  
        for (int ROB = 0; ROB < 2; ROB++) {
            // Build the command with the full file name and type
            std::string command = "/home/lim/Desktop/TT_code/TT_calibration_analysis_final_version2/code/WADC/TF1_FIT/Init/Run_Fit -ROB " + std::to_string(ROB_num[ROB]) + " -CB " + std::to_string(CB_num[0]) + " -fl " + fl + " -type " + type + " -HV " + std::to_string(HV_num[0]);

            // Print the command and the thread number
            std::cout << "\n Run command: " << command 
                      << " in thread " << omp_get_thread_num() << std::endl;

            // Execute the command
            system(command.c_str());
        }

    
    return 0;
}
