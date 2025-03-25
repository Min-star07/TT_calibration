#include <iostream>
#include <string>
#include <vector>
#include <TChain.h>
#include <TTree.h>
#include <TFile.h>
#include <TH1.h>
#include <TF1.h>
#include <TCanvas.h>
#include <TLegend.h>
#include <TPaveStats.h>
#include <TMinuit.h>
#include <TLatex.h>
#include "Mystyle.h"
#include "Bellamy.h"
#include "DataManager.h"
#include "RootfileManager.h"
#include "HistogramProcessor.h"
using namespace std;

// Function to parse command line arguments
void parseArguments(int argc, char** argv, string& CB_default, string& ROB_default, string& FEB_default, 
                    string& file_led_default, string& file_ped_default, string& times_default, string& xmin_default, 
                    string& xmax_default, string& HV_default, string& wall_default, string& type_default) {
    for (int i = 1; i < argc; i++) {
        if (strcmp(argv[i], "-CB") == 0) CB_default = argv[i + 1];
        else if (strcmp(argv[i], "-ROB") == 0) ROB_default = argv[i + 1];
        else if (strcmp(argv[i], "-FEB") == 0) FEB_default = argv[i + 1];
        else if (strcmp(argv[i], "-fl") == 0) file_led_default = argv[i + 1];
        else if (strcmp(argv[i], "-fd") == 0) file_ped_default = argv[i + 1];
        else if (strcmp(argv[i], "-t") == 0) times_default = argv[i + 1];
        else if (strcmp(argv[i], "-left") == 0) xmin_default = argv[i + 1];
        else if (strcmp(argv[i], "-right") == 0) xmax_default = argv[i + 1];
        else if (strcmp(argv[i], "-v") == 0) HV_default = argv[i + 1];
        else if (strcmp(argv[i], "-w") == 0) wall_default = argv[i + 1];
        else if (strcmp(argv[i], "-type") == 0) type_default = argv[i + 1];
    }
}

// Function to print parsed arguments
void printArguments(const string& CB, const string& ROB, const string& FEB, const string& file_led,  
                    const string& file_ped, const string& times) {
    cout << "CB: " << CB << endl;
    cout << "ROB: " << ROB << endl;
    cout << "FEB: " << FEB << endl;
    cout << "file_led: " << file_led << endl;
    cout << "file_ped: " << file_ped << endl;
    cout << "times: " << times << endl;
}

// Function to set up the canvas
void setupCanvas(TCanvas*& canvas, const TString& canvasName) {
    canvas = new TCanvas("canvas", "canvas", 800, 600);
    canvas->Print("./" + canvasName + "[");  // Open PDF
}

// Function to update the canvas
void updateCanvas(TCanvas* canvas, const TString& canvasName) {
    canvas->SetLogy(true); // Log scale for better visibility of histogram
    canvas->Modified();
    canvas->Update();
    canvas->Print("./" + canvasName);  // Save current canvas state
}

// Function to save and close the canvas
void saveCanvas(TCanvas* canvas, const TString& canvasName) {
    canvas->Print("./" + canvasName + "]");  // Close PDF
    delete canvas;  // Properly delete the canvas to avoid memory leaks
}

int main(int argc, char **argv) {
    // Default argument values
    string file_led_default = "led_cCB-22_2024-01-16_20_37_hist.root";
    string file_ped_default = "ped_cCB-22_2024-01-16_20_37_hist.root";
    string CB_default = "22";
    string ROB_default = "15";
    string FEB_default = "61";
    string times_default = "1";
    string xmin_default = "1";
    string xmax_default = "1";
    string HV_default = "1";
    string wall_default = "1";
    string type_default = "HV_cal";

    // Parse command-line arguments
    parseArguments(argc, argv, CB_default, ROB_default, FEB_default, file_led_default, file_ped_default, 
                   times_default, xmin_default, xmax_default, HV_default, wall_default, type_default);
    printArguments(CB_default, ROB_default, FEB_default, file_led_default, file_ped_default, times_default);

    // Convert strings to integers for use in file paths
    int times = stoi(times_default);
    int CB = stoi(CB_default);
    int ROB = stoi(ROB_default);
    // int HV = stoi(HV_default);
    int WALL = stoi(wall_default);

    

    // Apply custom style
    MyStyle style;
    style.Apply();

    // Canvas setup
    TCanvas* canvas = nullptr;
    TString canvasName = Form("./WALL%d_CB%d_ROB%d_WADC_data_result.pdf",  WALL, CB, ROB);
    setupCanvas(canvas, canvasName);


    int HV[2] = {800, 801};
    for (int i = 0; i < 2; i++)
    {
        HistogramProcessor processor;
        string path = Form("../../../../../result/WALL%d/CB%d/ROB%d/WADC/%s/HV%d", WALL, CB, ROB, type_default.c_str(), HV[i]);
        
        std::string infile = Form("%s/WALL%d_CB%d_ROB%d_WADC_Final_result.txt", path.c_str(), WALL, CB, ROB);
        // Construct file paths based on arguments
        string file_led = Form("../../../../../result/WALL%d/CB%d/data/WADC/%s/%s", WALL, CB, type_default.c_str(), file_led_default.c_str());
        cout << infile << endl;

        DataManager result_in(infile);
        vector<vector<double>> lines = result_in.readLines();
        for(const auto& line :lines){
            string formatted_rob = result_in.formatNumber(ROB);
            string formatted_cn = result_in.formatNumber(line[0]);
            string histName = Form("h_charge_ROB%s_ch%s", formatted_rob.data(), formatted_cn.data());
            // cout << "Processing histogram: " << histName << endl;
            // Read the ROOT file for histograms
            RootfileManager reader(file_led);
            TH1F* hist = reader.GetHistogram(histName);
            if (!hist) {
                cout << "Histogram not found for " << histName << endl;
                continue;
            }
            if(line[0] == 56)
            processor.FitHistogram(hist, line, histName);


        }

    }
    // Save and close the canvas
    saveCanvas(canvas, canvasName);
        return 0;
}