// GaussFitter.h
#ifndef GAUSSFITTER_H
#define GAUSSFITTER_H

#include <vector>
#include <string>
#include <TF1.h>
#include <TH1F.h>

class GaussFitter {
public:
    GaussFitter();
    ~GaussFitter();

    std::vector<double> FitPedestal(TH1F* hist);
    TF1* GetFitFunction(); // New method to get the fit function

    void SaveHistogramToRootFile(TH1F* hist, TF1* func, const std::string& newFilename, const std::string& histName);

private:
    TF1* CreateGaussianFitFunction(double x_left, double x_right);
    TF1* fitFunction;  // Store the fit function

};

#endif
