#include "GaussFitter.h"
#include <iostream>

GaussFitter::GaussFitter() {}

GaussFitter::~GaussFitter() {}

// Method to perform Gaussian fit on the pedestal and get mean and sigma
std::vector<double> GaussFitter::FitPedestal(TH1F* hist) {
    if (!hist) {
        std::cerr << "Error: Histogram is null!" << std::endl;
        return {};
    }

   // Find the bin with the maximum content (peak)
    int maxBin = hist->GetMaximumBin();
    double x_left = hist->GetXaxis()->GetBinCenter(maxBin) - 20.0;  // Define a range around the peak
    double x_right = hist->GetXaxis()->GetBinCenter(maxBin) + 20.0;


    // Create Gaussian function for fitting
    TF1* gaussFunc = CreateGaussianFitFunction(x_left, x_right);

     // Perform the fit within the specified range
    hist->Fit(gaussFunc, "RQL"); // "R" to restrict the range, "Q" for quiet mode to suppress printouts

    // Get the mean and sigma from the fit
    double mean = gaussFunc->GetParameter(1);  // Mean of the Gaussian
    double sigma = gaussFunc->GetParameter(2); // Sigma (standard deviation) of the Gaussian

    std::cout << "Pedestal Mean: " << mean << ", Sigma: " << sigma << std::endl;

    // Clean up
    delete gaussFunc;

    // PedeInfo.push_back(mean);
    // PedeInfo.push_back(sigma);
    // Return the mean and sigma as a vector
    return {mean, sigma};
}

// Internal method to create a Gaussian function for fitting
TF1* GaussFitter::CreateGaussianFitFunction(double x_left, double x_right) {
    // Define a Gaussian function within the specified range
    TF1* gaussFunc = new TF1("gaussFunc", "gaus", x_left, x_right);
    return gaussFunc;
}
