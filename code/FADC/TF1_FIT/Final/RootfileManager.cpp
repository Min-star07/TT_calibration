#include <fstream>
#include <string>
#include <vector>
#include "RootfileManager.h"
#include <iostream>
#include <iomanip>
#include "TFile.h"
#include "TTree.h"
#include "TH1F.h"
#include "TCanvas.h"
#include "TStyle.h"
#include "TF1.h"
using namespace std;

RootfileManager::RootfileManager(const std::string& filename) {
    // open the file
    file = TFile::Open(filename.c_str(), "READ");
    if(!file || file->IsZombie()) {
       std::cerr << "Error: Could not open file " << filename << std::endl;
}
}

// Destructor implementation
RootfileManager::~RootfileManager() {
    if(file) {
        file->Close();
        delete file;
    }
}


// Method to get the a histogram from the root file
TH1F*RootfileManager::GetHistogram(const std::string& histName) {
    if(!file){
        std::cerr << "Error: File not open" << std::endl;
        return nullptr;
    }
    return static_cast<TH1F *>(file->Get(histName.c_str()));
}
