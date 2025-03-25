#ifndef HISTOGRAMPROCESSOR_H
#define HISTOGRAMPROCESSOR_H

#include <vector>
#include <string>
#include "TH1F.h"
#include "TF1.h"

class HistogramProcessor {
public:
    // Constructor
    HistogramProcessor();

    // Destructor
    ~HistogramProcessor();

    // Method to fit a histogram with a Gaussian function or similar based on the input data
    void FitHistogram(TH1F* hist, const std::vector<double>& line,  const std::string& histName);

    // Method to determine the range of the histogram
    void GetRange(TH1F* hist, std::vector<double>& xrange);

private:
    // Helper method to get initial parameters for the fit based on the histogram data
    std::vector<double> GetInitialParameters(const std::vector<double>& line, double numEntries);

};

#endif // HISTOGRAMPROCESSOR_H
