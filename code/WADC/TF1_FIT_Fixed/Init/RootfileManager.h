#ifndef ROOTFILEMANAGER_H
#define ROOTFILEMANAGER_H
#include "TH1.h"
#include "TFile.h"
#include "TTree.h"
#include "TList.h"
#include "TCanvas.h"
#include "TStyle.h"
#include "TMath.h"
#include <vector>
#include <string>
#include <iostream>
#include <fstream>
#include <string>
class RootfileManager {
   public:
        // Constructor that takes a file name
        RootfileManager(const std::string& filename);
        // Destructor to close the ROOT file
        ~RootfileManager();
        TH1F* GetHistogram(const std::string& histName);
        void SaveHistogramToRootFile(TH1F *hist, const std::string &newFilename, const std::string &histName);

    private:
        // Pointer to the ROOT file
        TFile* file;
};

#endif