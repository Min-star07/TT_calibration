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

TF1* HistogramProcessor::FitHistogram(TH1F* hist, const std::vector<double>& line, const std::string& newFilename, const std::string& histName) {
    if (!hist) {
        std::cerr << "Histogram not found!" << std::endl;
        return nullptr;
    }

    double numEntries = hist->GetEntries();
    // std::cout << "Histogram entries: " << numEntries << std::endl;

    // Get initial parameters and limits for the fit
    std::vector<double> initParams = GetInitialParameters(line, numEntries);
    std::vector<std::pair<double, double>> paramLimits = GetParameterLimits(line, numEntries);

    // Define parameter names
    std::vector<std::string> setParamsName = {"N_{0}", "Q_{0}", "Q_{1}", "#sigma_{0}", "#sigma_{1}", "w", "#alpha", "#mu"};

    // Get the range of the histogram for fitting
    std::vector<double> xrange;
    GetRange(hist, xrange);
    // std::cout << "Fit range: x_min = " << xrange[0] << ", x_max = " << xrange[1] << std::endl;

    // Define the function to fit
    TF1* func = new TF1("func", Bellamy, xrange[0], xrange[1], 8);

    // Set initial parameters and limits
    for (size_t i = 0; i < initParams.size(); ++i) {
        func->SetParameter(i, initParams[i]);
        func->SetParLimits(i, paramLimits[i].first, paramLimits[i].second);
        func->SetParName(i, setParamsName[i].c_str());
        
    }

    func->SetNpx(10000);
    // Fit histogram and store the status
    fitStatus = hist->Fit(func, "RBW");

    // Store fit details
    GetFitDetails(hist, func);

    // Save histogram and function to ROOT file
    SaveHistogramToRootFile(hist, func, newFilename, histName);

    // Return the fitted function
    return func;
}

std::vector<double> HistogramProcessor::GetInitialParameters(const std::vector<double>& line, double numEntries) {
    // Set initial parameters for the fit
    return {numEntries, line[4], line[6], line[8], line[10], line[12], line[14], line[16]};
}

std::vector<std::pair<double, double>> HistogramProcessor::GetParameterLimits(const std::vector<double>& line, double numEntries) {
    // Define parameter limits
    return {
        {0.95 * numEntries, 1.05 * numEntries},
        {0.95 * line[4], 1.05 * line[4]},
        {0.95 * line[6], 1.05 * line[6]},
        {0.95 * line[8], 1.05 * line[8]},
        {0.95 * line[10], 1.05 * line[10]},
        {0.95 * line[12], 1.05 * line[12]},
        {0.95 * line[14], 1.05 * line[14]},
        {0.95 * line[16], 1.05 * line[16]},
    };
}

void HistogramProcessor::GetRange(TH1F* hist, std::vector<double>& xrange) {
    if (!hist) {
        std::cerr << "Histogram is null!" << std::endl;
        return;
    }

    int nBins = hist->GetNbinsX();
    int maxBin = hist->GetMaximumBin();
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
    double x_max = maxBin;
    
    // Find the right range
    for (int i = maxBin; i <=nBins; ++i) {
         if (hist->GetBinContent(i) > 0 && hist->GetBinContent(i + 1) > 0) {
        // if (hist->GetBinContent(i) > 0) {
            x_max = hist->GetXaxis()->GetBinCenter(i);
        } else {
            break;
        }
    }
    //  for (int i = nBins; i >maxBin; --i) {
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
    // Open a new ROOT file in "UPDATE" mode
    TFile* outFile = TFile::Open(newFilename.c_str(), "UPDATE");

    if (!outFile || outFile->IsZombie()) {
        std::cerr << "Error: Could not open or create file " << newFilename << std::endl;
        return;
    }

    // Set X-axis limits and write the histogram to the file
    hist->GetXaxis()->SetRangeUser(0, 150);
    hist->Write(histName.c_str(), TObject::kOverwrite);

    // Close the file
    outFile->Close();
    delete outFile;
}

void HistogramProcessor::GetFitDetails(TH1F *hist,  TF1* func) {
    if (!func) {
        std::cerr << "Function is null!" << std::endl;
        fitStatus = -1;
        chi2ndf = 0;
        fitResults.clear();
        fitErrors.clear();
        return;
    }

    // Resize vectors to store fit results and errors
    fitResults.resize(func->GetNpar());
    fitErrors.resize(func->GetNpar());

    for (int i = 0; i < func->GetNpar(); ++i) {
        fitResults[i] = func->GetParameter(i);
        fitErrors[i] = func->GetParError(i);
    }


     // Obtain fit parameters
    auto par = GetFitResults();  // Assuming this returns std::vector<double>

    // Number of fit parameters
    int Npars = func->GetNpar(); 

    // Get the fitting range from the histogram
    std::vector<double> xrange;
    GetRange(hist, xrange);  // Assuming this fills xrange with two values: xmin and xmax

    // Ensure the range vector contains at least two values
    if (xrange.size() < 2) {
        std::cerr << "Error: Invalid range provided." << std::endl;
        return;
    }

    double x_min = xrange[0];
    double x_max = xrange[1];
    double chi2 = 0;
    std::cout << hist->FindBin(x_min) + 1 << "\t" << hist->FindBin(x_max) -1 << std::endl;
    // Loop through the bins in the specified range
    int maxBin = hist->GetMaximumBin();
    // for (int i = hist->FindBin(x_min) + 1; i <= hist->FindBin(x_max) -1 ; ++i) {
    for (int i = maxBin; i <= 60 ; ++i) {
        
        double x = hist->GetBinCenter(i);
        double y_obs = hist->GetBinContent(i);
        double error = hist->GetBinError(i);
        if (error == 0) continue;  // Skip bins with no error to avoid division by zero

        // Calculate the expected value from the Bellamy function
        double y_exp = Bellamy(&x, par.data());

        // Calculate the residual and add it to chi2
        double residual = (y_obs - y_exp) / error;
        chi2 += residual * residual;
    }

    // Calculate chi2 per degree of freedom
    // int Nbins = (hist->FindBin(x_max) -1) - (hist->FindBin(x_min)+1) + 1;
    int Nbins = 60 - maxBin + 1;
    if (Nbins > Npars) {
        chi2ndf = chi2 / (Nbins - Npars);  // Number of degrees of freedom = Nbins - Npars
    } else {
        std::cerr << "Error: Not enough bins for degrees of freedom." << std::endl;
        chi2ndf = 0;
    }

    // Output the result for debugging purposes
    std::cout << "Chi2/NDF: " << chi2ndf << std::endl;
    // return chi2ndf;
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

double HistogramProcessor::GetChi2PerNDF() const {
    return chi2ndf;
}
