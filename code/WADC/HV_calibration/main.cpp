#include <iostream>
#include <string>
#include <vector>
#include <TChain.h>
#include <TTree.h>
#include <TFile.h>
#include <TH1.h>
#include <TF1.h>
#include <TGraphErrors.h>
#include <TCanvas.h>
#include <TLegend.h>
#include <TPaveStats.h>
#include <TLine.h>
#include <TLatex.h>
#include "DataAnalysis.h"
#include "Mystyle.h"

using namespace std;

// Function to fit a linear model
double FitLinear(double *x, double *par) {
    return par[0] + par[1] * x[0];
}

int main(int argc, char **argv) {
    // Default parameters
    string file_default = "../../../../../";
    string CB_default = "22";
    string ROB_default = "15";
    string FEB_default = "61";
    string wall_default = "1";

    // Parse command-line arguments
    for (int i = 1; i < argc; i++) {
        if (strcmp(argv[i], "-CB") == 0) {
            CB_default = argv[i + 1];
        } else if (strcmp(argv[i], "-ROB") == 0) {
            ROB_default = argv[i + 1];
        } else if (strcmp(argv[i], "-f") == 0) {
            file_default = argv[i + 1];
        } else if (strcmp(argv[i], "-w") == 0) {
            wall_default = argv[i + 1];
        }
    }

    int CB = atoi(CB_default.c_str());
    int ROB = atoi(ROB_default.c_str());
    int WALL = atoi(wall_default.c_str());

    // Construct the path and filename
    string path = Form("../../../result/CB%d/WALL%d/ROB%d/WADC/HV_cal/", CB,WALL,  ROB);
    string filename = path + Form("CB%d_WALL%d_ROB%d_gain_calibration_result.txt",  CB,WALL, ROB);
    string outfile = path + Form("CB%d_WALL%d_ROB%d_HV_calibration_result.txt",  CB,WALL, ROB);
    cout << filename << endl;

    // Read data from the file
    DataAnalysis reader(filename);
    vector<string> lines = reader.readLines();

    // Extract relevant columns
    vector<int> columnIndices_HV = {0};
    vector<int> columnIndices_Q1 = {1};
    vector<int> columnIndices_Q1_error = {2};
    vector<int> columnIndices_gain = {4};
    vector<int> columnIndices_gain_after = {22};

    vector<string> HV_set = reader.getRandomColumns(lines, columnIndices_HV);
    vector<string> Q1_set = reader.getRandomColumns(lines, columnIndices_Q1);
    vector<string> Q1_error_set = reader.getRandomColumns(lines, columnIndices_Q1_error);
    vector<string> Gain_set = reader.getRandomColumns(lines, columnIndices_gain);
    vector<string> gain_set_after = reader.getRandomColumns(lines, columnIndices_gain_after);

    vector<double_t> doubleVec_HV_set = reader.stringVectorToDoubleVector(HV_set);
    vector<double_t> doubleVec_Q1_set = reader.stringVectorToDoubleVector(Q1_set);
    vector<double_t> doubleVec_Q1_error_set = reader.stringVectorToDoubleVector(Q1_error_set);
    vector<double_t> doubleVec_Gain_set = reader.stringVectorToDoubleVector(Gain_set);
    vector<double_t> doubleVec_gain_set_after = reader.stringVectorToDoubleVector(gain_set_after);

    // Set custom style
    SetMystyle();

    // Create and configure the canvas
    TCanvas *c = new TCanvas("c", "c", 800, 600);

    // Define errors for HV points (if applicable)
    vector<double> x_error(doubleVec_HV_set.size(), 0);

    // Create graph with error bars
    TGraphErrors *graph = new TGraphErrors(doubleVec_HV_set.size(), &doubleVec_HV_set[0], &doubleVec_Q1_set[0], &x_error[0], &doubleVec_Q1_error_set[0]);
    graph->GetXaxis()->SetTitle("HV");
    graph->GetYaxis()->SetTitle("Gain [ADC]");
    graph->SetTitle("");
    graph->SetMarkerColor(kRed);
    graph->SetMarkerStyle(52);
    graph->SetMarkerSize(2);

    // Fit the graph with a linear function
    TF1 *fit = new TF1("fit", FitLinear, 790, 820, 2);
    fit->SetParNames("Intercept", "Slope");
    graph->Fit("fit");

    // Configure and draw the graph
    graph->GetXaxis()->CenterTitle();
    graph->GetYaxis()->CenterTitle();
    graph->Draw("AP");
    c->Update();

    // Save the graph and fit to a file
    TFile *outFile = new TFile("fitResults.root", "RECREATE");
    graph->Write();
    outFile->Close();

    // Adjust and position the stats box
    TPaveStats *ps = (TPaveStats *)c->GetPrimitive("stats");
    if (ps) {
        ps->SetName("mystats");
        ps->SetX1NDC(0.2);
        ps->SetX2NDC(0.5);
        ps->SetY1NDC(0.6);
        ps->SetY2NDC(0.9);
    }

    // Calculate HV from gain
    cout << "--------------------------------" << endl;
    cout << "GAIN = " << doubleVec_Gain_set[0] << endl;
    Double_t HV_Cal = (doubleVec_Gain_set[0] - fit->GetParameter(0)) / fit->GetParameter(1);
    cout << "HV = " << HV_Cal << endl;
    cout << "--------------------------------" << endl;

     std::ofstream outFile_HV(outfile);

    if (outFile_HV.is_open()) {
        outFile_HV << HV_Cal<< std::endl;
        outFile_HV.close();
    } else {
        std::cerr << "Error: Unable to open file." << std::endl;
    }

    // Draw lines to indicate the calculated HV
    TLine *lineVerticalExp = new TLine(HV_Cal, c->GetUymin(), HV_Cal, doubleVec_Gain_set[0]);
    lineVerticalExp->SetLineColor(kBlue);
    lineVerticalExp->SetLineStyle(2);
    lineVerticalExp->Draw();

    TLine *lineHorizontalExp = new TLine(c->GetUxmin(), doubleVec_Gain_set[0], HV_Cal, doubleVec_Gain_set[0]);
    lineHorizontalExp->SetLineColor(kBlue);
    lineHorizontalExp->SetLineStyle(2);
    lineHorizontalExp->Draw();

    // Add a marker for the calculated HV and gain
    Int_t pointIndex = graph->GetN();
    graph->SetPoint(pointIndex, HV_Cal, doubleVec_Gain_set[0]);
    // graph->SetPointColor(kGreen);

    // Annotate the graph with HV and gain values
    TString HV_Value = Form("(%d , %.1f)", int(HV_Cal), doubleVec_Gain_set[0]);
    TLatex *text = new TLatex(HV_Cal - 0.5, doubleVec_Gain_set[0] - 0.3, HV_Value);
    text->SetTextSize(0.03);
    text->SetTextColor(kBlack);
    text->Draw("same");

    // Save the canvas as a PDF
    TString figurepath = path + Form("WALL%d_CB%d_ROB%d_GainvsADC.pdf", WALL, CB, ROB);
    c->Print(figurepath);

    return 0;
}
