#include "DataAnalysis.h"
#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <vector>
#include "Mystyle.h"
#include <TChain.h>
#include <TTree.h>
#include <TFile.h>
#include <TTree.h>
#include <TH1.h>
#include <TF1.h>
#include "TGraphErrors.h"
#include "DataAnalysis.h"
#include "Mystyle.h"
#include <TChain.h>
#include <TTree.h>
#include <TFile.h>
#include <TTree.h>
#include <TH1.h>
#include <TF1.h>
#include "TGraphErrors.h"
#include "TPaveStats.h"
#include <TGraph.h>
#include <TCanvas.h>
#include <TLegend.h>
#include "TLine.h"
using namespace std;


DataAnalysis::DataAnalysis(const std::string& filename) : filename(filename) {}

DataAnalysis::~DataAnalysis() {
    // Destructor is a good place to release resources
    // If there are dynmaically allocated resources, release them here
    std::cout << "Destructor called here" << std::endl;
}

std::vector<std::string> DataAnalysis::readLines() {
    std::ifstream file(filename);
    std::vector<std::string> lines;

    if (file.is_open()) {
        std::string line;
        while (std::getline(file, line)) {
            lines.push_back(line);
        }
        file.close();
    } else {
        std::cerr << "Unable to open file: " << filename << std::endl;
    }

    return lines;
}

std::vector<std::string> DataAnalysis::getRandomColumns(const std::vector<std::string>& lines, const std::vector<int>& columnIndices) {
    std::vector<std::string> randomColumns;
    for (const auto& line : lines) {
        std::istringstream iss(line);
        std::string token;
        int currentIndex = 0;
        while (std::getline(iss, token, '\t')) {
            if (std::find(columnIndices.begin(), columnIndices.end(), currentIndex) != columnIndices.end()) {
                randomColumns.push_back(token);
            }
            currentIndex++;
        }
    }
    return randomColumns;
}

std::vector<double> DataAnalysis::stringVectorToDoubleVector(const std::vector<std::string>& stringVec) {
    std::vector<double> doubleVec;
    for (const std::string& str : stringVec) {
        std::istringstream iss(str);
        double value;
        if (iss >> value) {
            doubleVec.push_back(value);
        } else {
            // Handle invalid input
            std::cerr << "Failed to convert string to double: " << str << std::endl;
        }
    }
    return doubleVec;
}

