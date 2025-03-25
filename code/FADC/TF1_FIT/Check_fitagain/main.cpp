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
#include "RootfileManager.h"
#include "HistogramProcessor.h"
#include "DataManager.h"
#include "GaussFitter.h"
#include "Chi2perNDF.h"
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
void setupCanvas(TCanvas*& canvas, TString& canvasName) {
    canvas = new TCanvas("canvas", "canvas", 800, 600);
    canvas->Print("./" + canvasName + "[");  // Open PDF
}

// Function to update the canvas
void updateCanvas(TCanvas* canvas, const TString& canvasName) {
    canvas->SetLogy(true);
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
    // ROOT::Math::MinimizerOptions::SetDefaultMinimizer("Minuit2", "Migrad");
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
    int HV = stoi(HV_default);
    int WALL = stoi(wall_default);

    // Construct file paths based on arguments
    string file_led = Form("../../../../result/CB%d/data/FADC/%s/%s", CB, type_default.c_str(), file_led_default.c_str());
    string file_ped = Form("../../../../result/CB%d/data/FADC/%s/%s", CB, type_default.c_str(), file_ped_default.c_str());
    string path = Form("../../../../result/CB%d/WALL%d/ROB%d/FADC/%s/HV%d", CB, WALL, ROB, type_default.c_str(), HV);

    // Apply custom style
    MyStyle style;
    style.Apply();

    // Canvas setup
    TCanvas* canvas = nullptr;
    TString canvasName = Form("%s/CB%d_WALL%d_ROB%d_FADC_Final_result.pdf", path.c_str(), CB,WALL,  ROB);
    setupCanvas(canvas, canvasName);

    // Read lines from the input file
    std::string infile = Form("%s/CB%d_WALL%d_ROB%d_FADC_Second_result.txt", path.c_str(), CB, WALL,  ROB);
    DataManager result_in(infile);
    vector<vector<double>> lines = result_in.readLines();

    // Prepare output file and ensure it doesn't exist before writing
    std::string outfile = Form("%s/CB%d_WALL%d_ROB%d_FADC_Final_result.txt", path.c_str(), CB,  WALL,ROB);
    DataManager result_out(outfile);
    result_out.checkAndDeleteFile();

    // Read the ROOT file for histograms
    RootfileManager reader(file_led);
    string newrootfile = Form("%s/CB%d_WALL%d_ROB%d_FADC_Final_result.root", path.c_str(), CB, WALL, ROB);
    cout << "Output ROOT file: " << newrootfile << endl;

    // Histogram processing
    HistogramProcessor processor;
    for (const auto& line : lines) {
        string formatted_rob = result_out.formatNumber(ROB);
        string formatted_cn = result_out.formatNumber(line[0]);
        string histName = Form("h_charge_ROB%s_ch%s", formatted_rob.data(), formatted_cn.data());
        cout << "Processing histogram: " << histName << endl;
        
        TH1F* hist = reader.GetHistogram(histName);
        if (!hist) {
            cout << "Histogram not found for " << histName << endl;
            continue;
        }

        double numEntries = hist->GetEntries();
        double integral = hist->Integral();
        hist->Scale(numEntries / integral);

        // Fit the histogram and save the results
        TF1* fittedFunc = processor.FitHistogram(hist, line, newrootfile, histName);

        if (fittedFunc) {
        std::cout << "Fitting succeeded! Fitted function: " << fittedFunc->GetName() << std::endl;
        } else {
            std::cerr << "Fitting failed!" << std::endl;
        }

        // Extract and save fit details
        // int fitStatus = processor.GetFitStatus();
        double chi2ndf = processor.GetChi2PerNDF();
        const auto &fitResults = processor.GetFitResults();
        const auto& fitErrors = processor.GetFitErrors();

          // Compute and print Chi2/NDF using Chi2perNDF class
        Chi2perNDF CHI2NDF(hist, fittedFunc);
        vector<double> chi2_peak_pede;
        CHI2NDF.Calculate_chi2perNDF(chi2_peak_pede);
        // cout << chi2_peak_pede[0] << "===========" << chi2_peak_pede[1] << endl;

        // Save fit results to the output file
        result_out.saveToText(outfile, to_string(static_cast<int>(line[0])), fitResults, fitErrors, chi2ndf, chi2_peak_pede);


        // Update canvas with the fitted histogram
        updateCanvas(canvas, canvasName);
    }

    // Save and close the canvas
    saveCanvas(canvas, canvasName);
    return 0;
}
