#ifndef CHI2PERNDF_H
#define CHI2PERNDF_H

#include <vector>
#include "TH1F.h"
#include <TSpectrum.h>

class Chi2perNDF {
public:
    // Constructor and Destructor
    Chi2perNDF(TH1F *hist, TF1 *fittedFunc);
    ~Chi2perNDF();
    
    // Method to calculate chi2 per NDF based on fit results
    void Calculate_chi2perNDF(std::vector<double>& chi2Results);

    void findSecondPeak();

    // Methods to get ranges for pedestal and peak
    std::vector<int> GetPedestalRange();
    std::vector<int> GetPeakRange();

    double Getchi2perNDF(const std::vector<int> binRange);

private:
    TH1F *hist; // Histogram pointer for analysis
    TF1 *fittedFunc;
};

#endif // CHI2PERNDF_H
