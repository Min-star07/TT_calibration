#include <iostream>
#include <string>
#include <vector>
#include <fstream>
#include <sstream>
#include <omp.h>
#include <cstdlib>

using namespace std;

// Structure to hold ROB configuration
struct ROBConfig {
    int wall;
    int cb;
    int pmt;
    int feb;
    int rob_id;
    int rob;
};

// Structure to hold all configuration parameters
struct Config {
    string file_led = "led_cCB-22_2024-01-16_20_37_hist.root";
    string file_ped = "ped_cCB-22_2024-01-16_20_37_hist.root";
    string HV = "1";
    string type = "HV_cal";
    string path = "./";
    vector<ROBConfig> rob_configs;
};

// Function to load ROB configurations from file
void loadROBConfigurations(const string& filename, Config& config) {
    ifstream file(filename);
    if (!file.is_open()) {
        cerr << "Error: Could not open file " << filename << endl;
        return;
    }

    string line;
    // Skip header line
    getline(file, line);
    
    while (getline(file, line)) {
        ROBConfig cfg;
        stringstream ss(line);
        string token;
        
        getline(ss, token, '\t');
        cfg.wall = stoi(token);
        getline(ss, token, '\t');
        cfg.cb = stoi(token);
        getline(ss, token, '\t');
        cfg.pmt = stoi(token);
        getline(ss, token, '\t');
        cfg.feb = stoi(token);
        getline(ss, token, '\t');
        cfg.rob_id = stoi(token);
        getline(ss, token, '\t');
        cfg.rob = stoi(token);
        
        config.rob_configs.push_back(cfg);
    }
}

// Function to parse command line arguments
void parseArguments(int argc, char** argv, Config& config) {
    for (int i = 1; i < argc; i++) {
        string arg = argv[i];
        if (i + 1 >= argc) continue;  // Skip if no value following the option
        
        if (arg == "-fl") {
            config.file_led = argv[i + 1];
        } else if (arg == "-fd") {
            config.file_ped = argv[i + 1];
        }else if (arg == "-v") {
            config.HV = argv[i + 1];
        } else if (arg == "-type") {
            config.type = argv[i + 1];
        }else if (arg == "-path") {
            config.path = argv[i + 1];
        }
    }
}

// Function to print configuration
void printConfig(const Config& config) {
    cout << "Configuration Parameters:\n";
    cout << "LED file: " << config.file_led << endl;
    cout << "PED file: " << config.file_ped << endl;
    cout << "HV: " << config.HV << endl;
    cout << "Type: " << config.type << endl;
    cout << "path: " << config.path<< endl;
    cout << "ROB configurations loaded: " << config.rob_configs.size() << endl;
}

int main(int argc, char **argv) {
    Config config;
    
    // Load ROB configurations from file
    loadROBConfigurations("../TF1_script/configure/cb76.txt", config);
    
    // Parse command-line arguments
    parseArguments(argc, argv, config);
    printConfig(config);

    // Convert strings to integers for processing
    int HV = atoi(config.HV.c_str());

    // Process each ROB configuration in parallel
    #pragma omp parallel for
    for (size_t i = 0; i < config.rob_configs.size(); i++) {
        const ROBConfig& cfg = config.rob_configs[i];
        
        // Build the command
        string command = config.path + "/Run_Fit -ROB " + to_string(cfg.rob) 
                        + " -CB " + to_string(cfg.cb) 
                        + " -FEB " + to_string(cfg.feb)
                        + " -fl " + config.file_led
                        + " -type " + config.type
                        + " -v " + config.HV
                        + " -w " + to_string(cfg.wall);

        // Print thread information and command
        #pragma omp critical
        {
            cout << "Thread " << omp_get_thread_num() 
                 << " processing ROB " << cfg.rob 
                 << " (WALL " << cfg.wall << ")" << endl;
            cout << "Command: " << command << endl;
        }

        // Execute the command
        int result = system(command.c_str());
        if (result != 0) {
            cerr << "Error: Command failed for ROB " << cfg.rob 
                 << " with exit code: " << result << endl;
        }
    }
    
    return 0;
}

// g++ -fopenmp OpenMP_FIT.cpp -o OpenMP_FIT