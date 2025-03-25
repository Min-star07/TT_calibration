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
    TF1* FitHistogram(TH1F* hist, const std::vector<double>& line, const std::string& newFilename, const std::string& histName);

    // Method to determine the range of the histogram
    void GetRange(TH1F* hist, std::vector<double>& xrange);

    // Accessor methods to get fit status, results, and errors
    int GetFitStatus() const;                           // Returns the fit status
    const std::vector<double>& GetFitResults() const;   // Returns fit parameters (values)
    const std::vector<double>& GetFitErrors() const;    // Returns fit parameter errors
    double GetChi2PerNDF() const;

     // Getter method to access the fit function
    // TF1* GetFitFunction() const;

private:
    // Helper method to get initial parameters for the fit based on the histogram data
    std::vector<double> GetInitialParameters(const std::vector<double>& line, double numEntries);

    // Helper method to set parameter limits for the fit based on input data
    std::vector<std::pair<double, double>> GetParameterLimits(const std::vector<double>& line, double numEntries);

    // Saves the histogram and the fitted function to a ROOT file
    void SaveHistogramToRootFile(TH1F* hist, TF1* func, const std::string& newFilename, const std::string& histName);

    // Extracts and stores fit details from the fitted function (e.g., status, results, errors)
    void GetFitDetails(TH1F *hist, TF1* func);

    // Member variables to store fit details
    int fitStatus;                      // Stores the status of the fit (e.g., success, error code)
    std::vector<double> fitResults;     // Stores the results of the fit (parameters)
    std::vector<double> fitErrors;      // Stores the errors associated with the fit parameters
    double chi2ndf;
    // TF1 *func;
};

#endif // HISTOGRAMPROCESSOR_H
