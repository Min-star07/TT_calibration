#include <iostream>
#include <vector>
#include "Chi2perNDF.h"
#include "TFile.h"
#include "TTree.h"
#include "TH1F.h"
#include "TCanvas.h"
#include "TStyle.h"
#include "TF1.h"
#include "Bellamy.h"
// #include <TSpectrum.h>
#include <algorithm> // for std::max_element

// Constructor
Chi2perNDF::Chi2perNDF(TH1F *hist, TF1 *fittedFunc) : hist(hist), fittedFunc(fittedFunc) {}

// Destructor
Chi2perNDF::~Chi2perNDF() {}

// Function to calculate Chi2/NDF
void Chi2perNDF::Calculate_chi2perNDF(std::vector<double>& chi2Results) {
    // Ensure chi2Results has at least 2 elements
    chi2Results.resize(2);
    
    for (int i = 0; i < 2; i++) {
        std::vector<int> xrange;
        if (i == 0) {
            xrange = GetPedestalRange();
        } else {
            xrange = GetPeakRange();
        }

        double chi2 = Getchi2perNDF(xrange);
        chi2Results[i] = chi2;
    }
}

// Function to get the pedestal range around the maximum bin
std::vector<int> Chi2perNDF::GetPedestalRange() {
    int maxBin = hist->GetMaximumBin();
    int nBins = hist->GetNbinsX();
    int x_valley = maxBin;

    for (int i = maxBin; i < nBins; i++) {
        if ((hist->GetBinContent(i) <= hist->GetBinContent(i - 1)) && 
            (hist->GetBinContent(i) <= hist->GetBinContent(i + 1))) {
            x_valley = i;
            break;
        }
    }
    // x_valley = maxBin + 2;
    int left_bin_pedestal = std::max(1, maxBin - 20);                // Ensure bin index does not go below 1
    int right_bin_pedestal = std::min(hist->GetNbinsX(), x_valley); // Ensure bin index does not exceed max
    std::cout << "left_bin_pedestal : " << left_bin_pedestal << "\t" << "right_bin_pedestal : " << right_bin_pedestal << std::endl;
    return {left_bin_pedestal, right_bin_pedestal};
}

// Function to get the peak range around the maximum bin
std::vector<int> Chi2perNDF::GetPeakRange() {
    int maxBin = hist->GetMaximumBin();
    int nBins = hist->GetNbinsX();
    // int x_peak = maxBin + 2;
    int x_valley = maxBin;

    for (int i = maxBin; i < nBins; i++) {
        if ((hist->GetBinContent(i) <= hist->GetBinContent(i - 1)) && 
            (hist->GetBinContent(i) <= hist->GetBinContent(i + 1))) {
            x_valley = i;
            break;
        }
    }
    std::vector<int> max_numbers_x;
    std::vector<int> max_numbers_y;
    for (int i = x_valley; i < nBins; i++)
    {
        if ((hist->GetBinContent(i) > hist->GetBinContent(i - 1))) {
            // x_peak = i;
            max_numbers_x.push_back(i);
            max_numbers_y.push_back(hist->GetBinContent(i));
        }
    }
    int left_bin_peak;
    int right_bin_peak;
    // Ensure `max_numbers` is not empty before finding maximum element
    if (!max_numbers_y.empty()) {
        auto x_peak_iter = std::max_element(max_numbers_y.begin(), max_numbers_y.end());
        // Get the index and the value of the maximum element
        int x_peak_index = std::distance(max_numbers_y.begin(), x_peak_iter);

        int x_peak = max_numbers_x[x_peak_index];
        // / Print max_numbers contents
        // std::cout << "max_numbers: ";
        // for (int num : max_numbers) {
        //     std::cout << num << " ";
        // }
        // std::cout << std::endl;


        // Setting bounds for `left_bin_peak` and `right_bin_peak`
        left_bin_peak = std::max(maxBin, x_valley); 
        right_bin_peak = std::min(nBins, x_peak + 40); 

        std::cout << "left_bin_peak : " << left_bin_peak << "\t" 
                  << "right_bin_peak : " << right_bin_peak << std::endl;
    } else {
        std::cout << "No peak found in max_numbers vector." << std::endl;
    }

    return {left_bin_peak, right_bin_peak};
}

double Chi2perNDF::Getchi2perNDF(const std::vector<int> binRange) {
    if (!fittedFunc) {
        std::cerr << "No fitted function provided!" << std::endl;
        return 0;
    }

    double chi2 = 0;
    int ndf = 0;

    for (int i = binRange[0]; i <= binRange[1]; i++) { // Use <= to include right bin
        double x = hist->GetBinCenter(i);
        double y_obs = hist->GetBinContent(i);
        double error = hist->GetBinError(i);

        if (error == 0) continue; // Skip bins with no error

        double y_exp = fittedFunc->Eval(x);
        chi2 += std::pow((y_obs - y_exp) / error, 2);
        ++ndf; // Increment degrees of freedom
    }

    // Calculate Chi2/NDF
    if (ndf > fittedFunc->GetNpar()) {
        return (chi2 / (ndf - fittedFunc->GetNpar()));
    } else {
        // std::cerr << "Insufficient degrees of freedom!" << std::endl;
        return chi2;
    }
}



