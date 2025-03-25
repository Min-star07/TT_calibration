#include "GaussFitter.h"
#include <TFile.h>
#include <iostream>

GaussFitter::GaussFitter() : fitFunction(nullptr) {}

GaussFitter::~GaussFitter() {
    if (fitFunction) delete fitFunction;
}

std::vector<double> GaussFitter::FitPedestal(TH1F* hist) {
    if (!hist) {
        std::cerr << "Error: Histogram is null!" << std::endl;
        return {};
    }

    // Find the bin with the maximum content (peak)
    int maxBin = hist->GetMaximumBin();
    double x_left = hist->GetXaxis()->GetBinCenter(maxBin) - 20.0; // Define a range around the peak
    double x_right = hist->GetXaxis()->GetBinCenter(maxBin) + 20.0;

    // Create Gaussian function for fitting
    fitFunction = CreateGaussianFitFunction(x_left, x_right);
    // Perform the fit within the specified range
    hist->Fit(fitFunction, "RQL"); // "R" to restrict the range, "Q" for quiet mode to suppress printouts

    // Get the mean and sigma from the fit
    double mean = fitFunction->GetParameter(1);  // Mean of the Gaussian
    double sigma = fitFunction->GetParameter(2); // Sigma (standard deviation) of the Gaussian

    std::cout << "Pedestal Mean: " << mean << ", Sigma: " << sigma << std::endl;

    // Return the mean and sigma as a vector
    return {mean, sigma};
}

// Internal method to create a Gaussian function for fitting
TF1* GaussFitter::CreateGaussianFitFunction(double x_left, double x_right) {
    // Define a Gaussian function within the specified range
    TF1* gaussFunc = new TF1("gaussFunc", "gaus", x_left, x_right);
    return gaussFunc;
}

// Method to retrieve the fit function after fitting
TF1* GaussFitter::GetFitFunction() {
    return fitFunction;
}

void GaussFitter::SaveHistogramToRootFile(TH1F* hist, TF1* func, const std::string& newFilename, const std::string& histName) {
    TFile* outFile = TFile::Open(newFilename.c_str(), "UPDATE");

    if (!outFile || outFile->IsZombie()) {
        std::cerr << "Error: Could not open or create file " << newFilename << std::endl;
        return;
    }

    // Write the histogram to the new ROOT file
    outFile->cd();
    hist->GetXaxis()->SetRangeUser(260, 340);
    hist->Write(histName.c_str(), TObject::kOverwrite);  // Save with the given name, overwriting if it exists

    // Write the function to the new ROOT file if available
    // if (func) {
    //     func->Write((histName + "_fit").c_str(), TObject::kOverwrite);
    // }

    outFile->Close();
    delete outFile;
}
