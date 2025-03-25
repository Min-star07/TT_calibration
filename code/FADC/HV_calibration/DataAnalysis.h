#ifndef DATAANALYSIS_H
#define DATAANALYSIS_H

#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <vector>
#include "TGraph.h"
using namespace std;
class DataAnalysis {
public:
    DataAnalysis(const std::string& filename);
    //Destructor
    ~DataAnalysis();
    std::vector<std::string> readLines();
    std::vector<std::string> getRandomColumns(const std::vector<std::string>& lines, const std::vector<int>& columnIndices);
    std::vector<double> stringVectorToDoubleVector(const std::vector<std::string> &stringVec);


private:
    std::string filename;
};

#endif  // DATAANALYSIS_H
