#include "HistogramProcessor.h"
#include "Bellamy.h"
#include <iostream>
#include <TCanvas.h>
#include <TFile.h>
#include <TF1.h>
#include <TH1F.h>

// Constructor
HistogramProcessor::HistogramProcessor() {}

// Destructor
HistogramProcessor::~HistogramProcessor() {}

void HistogramProcessor::FitHistogram(TH1F* hist, const std::vector<double>& line, const std::string& histName) {
    if (!hist) {
        std::cerr << "Histogram not found!" << std::endl;
    }

    double numEntries = hist->GetEntries();
    // std::cout << "Histogram entries: " << numEntries << std::endl;

    // Get initial parameters and limits for the fit
    // std::vector<Double_t> initParams = GetInitialParameters(line, numEntries);
    auto initParams = GetInitialParameters(line, numEntries);
   
    // Define parameter names
    std::vector<std::string> setParamsName = {"N_{0}", "Q_{0}", "Q_{1}", "#sigma_{0}", "#sigma_{1}", "w", "#alpha", "#mu"};

    // Get the range of the histogram for fitting
    std::vector<double> xrange;
    GetRange(hist, xrange);
    double x_min_bin = xrange[0];
    double x_max_bin = xrange[1];
     // Find the right range
    for (int i = x_min_bin; i <=x_max_bin; ++i) {
        double x = hist->GetBinCenter(i);
        double y_obs = hist->GetBinContent(i);
        double error = hist->GetBinError(i);
        if (error == 0) continue;  // Skip bins with no error to avoid division by zero

        // Calculate the expected value from the Bellamy function
        double y_exp = Bellamy(&x, initParams.data());
        
        double diff = y_exp - y_obs;
        std::cout << x << "\t" <<y_obs << "\t" << "\t"<< y_exp << "\t"<< diff << "\t" << error <<  "\t" << initParams[0] << std::endl;
    }
}
std::vector<double> HistogramProcessor::GetInitialParameters(const std::vector<double>& line, double numEntries) {
    // Set initial parameters for the fit
    return {line[2], line[4], line[6], line[8], line[10], line[12], line[14], line[16]};
}

void HistogramProcessor::GetRange(TH1F* hist, std::vector<double>& xrange) {
    if (!hist) {
        std::cerr << "Histogram is null!" << std::endl;
        return;
    }

    int nBins = hist->GetNbinsX();
    int maxBin = hist->GetMaximumBin();
    double x_min = maxBin -2;
    
    // Find the right range
    double x_max = maxBin;
    
    // Find the right range
    for (int i = maxBin; i <=nBins; ++i) {
         if (hist->GetBinContent(i) > 0 && hist->GetBinContent(i + 1) > 0) {
        // if (hist->GetBinContent(i) > 0) {
            x_max = i;
        } else {
            break;
        }
    }

    xrange.push_back(x_min);
    xrange.push_back(x_max);
}

