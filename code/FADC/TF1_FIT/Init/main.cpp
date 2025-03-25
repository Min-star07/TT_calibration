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
#include "FileManager.h"

using namespace std;

// Function to parse command line arguments
void parseArguments(int argc, char** argv, string& CB_default, string& ROB_default, string& FEB_default, 
                    string& file_led_default, string& file_ped_default, string& times_default, string& xmin_default, string& xmax_default, 
                    string& HV_default, string& wall_default, string& type_default) {
    for (int i = 1; i < argc; i++) {
        if (strcmp(argv[i], "-CB") == 0) {
            CB_default = argv[i + 1];
        } else if (strcmp(argv[i], "-ROB") == 0) {
            ROB_default = argv[i + 1];
        } else if (strcmp(argv[i], "-FEB") == 0) {
            FEB_default = argv[i + 1];
        } else if (strcmp(argv[i], "-fl") == 0) {
            file_led_default = argv[i + 1];
        } else if (strcmp(argv[i], "-fd") == 0) {
            file_ped_default = argv[i + 1];
        }else if (strcmp(argv[i], "-t") == 0) {
            times_default = argv[i + 1];
        } else if (strcmp(argv[i], "-left") == 0) {
            xmin_default = argv[i + 1];
        } else if (strcmp(argv[i], "-right") == 0) {
            xmax_default = argv[i + 1];
        } else if (strcmp(argv[i], "-v") == 0) {
            HV_default = argv[i + 1];
        } else if (strcmp(argv[i], "-w") == 0) {
            wall_default = argv[i + 1];
        } else if (strcmp(argv[i], "-type") == 0) {
            type_default = argv[i + 1];
        }
    }
}

// Function to print parsed arguments
void printArguments(const string& CB, const string& ROB, const string& FEB, const string& file_led,  const string& file_ped, const string& times) {
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
     // Set logarithmic scale on the Y-axis
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
    parseArguments(argc, argv, CB_default, ROB_default, FEB_default, file_led_default, file_ped_default, times_default, xmin_default, xmax_default, HV_default, wall_default, type_default);
    printArguments(CB_default, ROB_default, FEB_default, file_led_default, file_ped_default, times_default);

    // Convert strings to integers for use in file paths
    int times = atoi(times_default.c_str());
    int CB = atoi(CB_default.c_str());
    int ROB = atoi(ROB_default.c_str());
    int HV = atoi(HV_default.c_str());
    int WALL = atoi(wall_default.c_str());
    string file_led = Form("../../../../result/CB%d/data/FADC/%s/%s",CB, type_default.c_str(), file_led_default.c_str());
    string file_ped = Form("../../../../result/CB%d/data/FADC/%s/%s",CB, type_default.c_str(), file_ped_default.c_str());
    string path = Form("../../../../result/CB%d/WALL%d/ROB%d/FADC/%s/HV%d", CB, WALL,ROB, type_default.c_str(), HV);

    FileManager filemanager;
    filemanager.Createpath(path);
    // Apply custom style
    MyStyle style;
    style.Apply();

    TCanvas* canvas = nullptr;
    TString canvasName = Form("%s/CB%d_WALL%d_ROB%d_FADC_Init_result.pdf", path.c_str(),  CB,  WALL, ROB);
    setupCanvas(canvas, canvasName);

    std::string outfile = Form("%s/CB%d_WALL%d_ROB%d_FADC_Init_result.txt", path.c_str(),  CB, WALL, ROB);
    DataManager result(outfile);
    result.checkAndDeleteFile();
    // DataManager result(Form("%s/WALL%d_CB%d_ROB%d_WADC_Final_result.txt", path.c_str(), WALL, CB, ROB));

    std::vector<std::string> setParamsName = {"N_{0}", "Q_{0}", "Q_{1}", "#sigma_{0}", "#sigma_{1}", "w", "#alpha", "#mu"};

    // vector<vector<double>> lines_final = result.readLines();
    RootfileManager reader(file_led);
    RootfileManager reader_pede(file_led);
   
    string newrootfile = Form("%s/CB%d_WALL%d_ROB%d_FADC_Init_result.root", path.c_str(),  CB, WALL,ROB);
    cout << newrootfile << endl;

    string newrootfile_ped = Form("%s/CB%d_WALL%d_ROB%d_FADC_PED.root", path.c_str(),  CB, WALL, ROB);
    cout << newrootfile_ped << endl;

    HistogramProcessor processor;

    GaussFitter PedeFit;

    // Initialize a line counter
    int lineCount = 0;
    // Process histograms
    for (int channel = 0; channel< 64; channel++)
    {
        // Output the current line count
        cout << "channel " << channel << endl;

        // Format the channel and ROB numbers for histogram naming
        string formatted_cn = result.formatNumber(channel);
        string formatted_rob = result.formatNumber(ROB);
        string histName = Form("h_charge_ROB%s_ch%s", formatted_rob.data(), formatted_cn.data());
        cout << "histName : " << histName << endl;
        TH1F *hist = reader.GetHistogram(histName);
        if (!hist) {
            cout << "Histogram not found for " << histName << endl;
            continue;
        }
        double numEntries = hist->GetEntries();
        double integral = hist->Integral();
        hist->Scale(numEntries / integral);
        TH1F *hist_ped = reader_pede.GetHistogram(histName);
        numEntries = hist_ped->GetEntries();
        integral = hist_ped->Integral();
        hist_ped->Scale(numEntries / integral);


        vector<double> PedInfo = PedeFit.FitPedestal(hist_ped);
        // Retrieve the fit function
        TF1* fitFunc = PedeFit.GetFitFunction();
        // You can now use fitFunc for further processing or visualization
        if (fitFunc) {
            std::cout << "Fit function retrieved successfully." << std::endl;
            // Save the histogram and the fit function to a new ROOT file
            PedeFit.SaveHistogramToRootFile(hist_ped, fitFunc, newrootfile_ped, histName);
        }
        processor.FitHistogram(hist, PedInfo, newrootfile, histName); // Fit histogram and save results

        // Print fit details using the accessor methods
        int fitStatus =  processor.GetFitStatus();
        // Print fit results in "value ± error" format
        const auto& fitResults = processor.GetFitResults();
        const auto& fitErrors = processor.GetFitErrors();

        result.saveToText(outfile, formatted_cn, fitResults, fitErrors, fitStatus);
        // reader.DrawHistogram(hist, histName);
        updateCanvas(canvas, canvasName); // Update canvas after each histogram
    }

    saveCanvas(canvas, canvasName);  // Save and close the canvas
    return 0;
}
