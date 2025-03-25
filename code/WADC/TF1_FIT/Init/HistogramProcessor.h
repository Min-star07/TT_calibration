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

    // Method to fit histogram
    void FitHistogram(TH1F* hist,  std::vector<double>& line, const std::string& newFilename, const std::string& histName);

    // Method to get histogram range
    void GetRange(TH1F *hist, std::vector<double>& xrange);
    // std::tuple<int, std::vector<double>, std::vector<double>> GetFitDetails(TF1 *func);

    // Accessor methods to get fit details
    int GetFitStatus() const;
    const std::vector<double>& GetFitResults() const;
    const std::vector<double>& GetFitErrors() const;

private:
    // Helper methods
    std::vector<double> GetInitialParameters(const std::vector<double>& line, double numEntries);
    std::vector<std::pair<double, double>> GetParameterLimits(const std::vector<double>& line, double numEntries);
    void SaveHistogramToRootFile(TH1F *hist, TF1 *func, const std::string &newFilename, const std::string &histName);

    // Method to retrieve fit details from the fit function
    void GetFitDetails(TF1* func);

    // Member variables to store fit details
    int fitStatus;
    std::vector<double> fitResults;
    std::vector<double> fitErrors;
};

#endif // HISTOGRAMPROCESSOR_H
