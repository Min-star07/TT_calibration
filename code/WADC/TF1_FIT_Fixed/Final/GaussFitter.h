#ifndef GAUSSFITTER_H
#define GAUSSFITTER_H

#include <vector>
#include <string>
#include "TH1F.h"
#include "TF1.h"

class GaussFitter {
public:
    // Constructor and Destructor
    GaussFitter();
    ~GaussFitter();

    // Method to perform Gaussian fit on the histogram and get mean and sigma
   std::vector<double> FitPedestal(TH1F* hist);

private:
    // Internal method to set up the Gaussian function for fitting
    TF1* CreateGaussianFitFunction(double x_left, double x_right);
};

#endif // GAUSSFITTER_H
