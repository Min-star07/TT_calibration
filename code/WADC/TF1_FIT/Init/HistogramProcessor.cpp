#include "HistogramProcessor.h"
#include "Bellamy.h"
#include <iostream>
#include <TCanvas.h>
#include <TFile.h>
#include <TF1.h>
#include <TH1F.h>

HistogramProcessor::HistogramProcessor() {}

HistogramProcessor::~HistogramProcessor() {}

void HistogramProcessor::FitHistogram(TH1F* hist, std::vector<double>& line, const std::string& newFilename, const std::string& histName) {
    if (!hist) {
        std::cerr << "Histogram not found!" << std::endl;
        return;
    }

    double numEntries = hist->GetEntries();
    //  double integral = hist->Integral();
    //  // Normalize the histogram to have an integral of 1
    // hist->Scale(1.0 / integral);

    std::cout << "Histogram normalized. New integral: " << hist->Integral() << std::endl;



    std::vector<double> initParams = GetInitialParameters(line, numEntries);
    std::vector<std::pair<double, double>> paramLimits = GetParameterLimits(line, numEntries);
    std::vector<std::string> setParamsName = {"N_{0}", "Q_{0}", "Q_{1}", "#sigma_{0}", "#sigma_{1}", "w", "#alpha", "#mu"};
    std::vector<double> xrange;
    GetRange(hist, xrange);
    std::cout << "x_min = " << xrange[0] << "\t" << "x_max = " << xrange[1] << std::endl;

    TF1 *func = new TF1("func", Bellamy, xrange[0], xrange[1], 8);
    for (size_t i = 0; i < initParams.size(); ++i) {
        
        func->SetParameter(i, initParams[i]);
        func->SetParLimits(i, paramLimits[i].first, paramLimits[i].second);
        func->SetParName(i, setParamsName[i].c_str());
        //  if(i == 0)
        // {
        //     func->FixParameter(i, initParams[i]);
        // }
    }
     // Fit histogram and check status
    // fitStatus = hist->Fit(func, "RMBL"); // Fit and get status
    func->SetNpx(10000);
    
    fitStatus = hist->Fit(func, "RBML"); // Fit and get status
                                         // Store fit details after fitting
    GetFitDetails(func);
    // Save histogram and function to ROOT file
    SaveHistogramToRootFile(hist, func, newFilename, histName);

    delete func; // Clean up dynamically allocated function
}

std::vector<double> HistogramProcessor::GetInitialParameters(const std::vector<double>& line, double numEntries) {

    return {numEntries, line[0],  8, line[1], 4.0, 0.1, 0.1, 1.0};
}

std::vector<std::pair<double, double>> HistogramProcessor::GetParameterLimits(const std::vector<double>& line, double numEntries) {
    return {
        {0.95 * numEntries, 1.05 * numEntries},
        {0.95 * line[0], 1.05 * line[0]},
        {6,14},
        {0.95 * line[1], 1.05 * line[1]},
        {3.0,8.0},
        {0.0, 1.0},
        {0.0, 1.0},
        {0.0, 3.0}
    };
}

void HistogramProcessor::GetRange(TH1F *hist, std::vector<double>& xrange) {
    if (!hist) {
        std::cerr << "Histogram is null!" << std::endl;
        return;
    }

    int nBins = hist->GetNbinsX();
    int maxBin = hist->GetMaximumBin();
    // std::cout << maxBin << "===============" << std::endl;
    double x_min = hist->GetXaxis()->GetBinCenter(maxBin) - 2;

    // Find the left range
    // for (int i = maxBin; i >= 1; --i) {
    //     if (hist->GetBinContent(i) > 0 && hist->GetBinContent(i - 1) > 0) {
    //         x_min = hist->GetXaxis()->GetBinCenter(i);

    //     } else {
    //         break;
    //     }
    // }

    // Find the right range
    // Find the right range
    double x_max = maxBin;
 
    // // Find the right range
    for (int i = maxBin; i <=nBins; ++i) {
         if (hist->GetBinContent(i) > 0 && hist->GetBinContent(i + 1) > 0) {
        // if (hist->GetBinContent(i) > 0) {
            x_max = hist->GetXaxis()->GetBinCenter(i);
        } else {
            break;
        }
    }

        // Find the right range
    // for (int i = nBins; i >maxBin; --i) {
    //      if (hist->GetBinContent(i) > 0) {
    //     // if (hist->GetBinContent(i) > 0) {
    //         x_max = hist->GetXaxis()->GetBinCenter(i) - 10;
    //         break;
    //     }
        
    // }
    xrange.push_back(x_min);
    xrange.push_back(x_max);
}

void HistogramProcessor::SaveHistogramToRootFile(TH1F* hist, TF1* func, const std::string& newFilename, const std::string& histName) {
    // Open a new ROOT file in "UPDATE" mode, meaning we can add histograms to it
    TFile* outFile = TFile::Open(newFilename.c_str(), "UPDATE");
    
    if (!outFile || outFile->IsZombie()) {
        std::cerr << "Error: Could not open or create file " << newFilename << std::endl;
        return;
    }

    // Write the histogram to the new ROOT file
    outFile->cd();
    // Set X-axis limits
    hist->GetXaxis()->SetRangeUser(0,150);
    hist->Write(histName.c_str(), TObject::kOverwrite);  // Save with the given name, overwriting if it exists

    // Write the function to the new ROOT file
    // func->Write((histName + "_fit").c_str(), TObject::kOverwrite);  // Save the function with a modified name
    // func->Draw("same")
    // Close the output file
    // Set logarithmic scale on the Y-axis
    
    outFile->Close();
    delete outFile;
}


void HistogramProcessor::GetFitDetails(TF1* func) {
    if (!func) {
        std::cerr << "Function is null!" << std::endl;
        fitStatus = -1;  // Set an error status
        fitResults.clear();
        fitErrors.clear();
        return;
    }
    
    // Retrieve fit status, parameters, and errors
    fitResults.resize(func->GetNpar());
    fitErrors.resize(func->GetNpar());

    for (int i = 0; i < func->GetNpar(); ++i) {
        fitResults[i] = func->GetParameter(i);
        fitErrors[i] = func->GetParError(i);
    }
}

// Accessor methods
int HistogramProcessor::GetFitStatus() const {
    return fitStatus;
}

const std::vector<double>& HistogramProcessor::GetFitResults() const {
    return fitResults;
}

const std::vector<double>& HistogramProcessor::GetFitErrors() const {
    return fitErrors;
}

