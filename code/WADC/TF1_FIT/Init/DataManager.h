#ifndef DATAMANAGER_H
#define DATAMANAGER_H
#include <fstream>
#include <string>
#include <vector>
#include <map>
#include <set>
#include <sstream>

class DataManager{
    public:
        DataManager(const std::string&filename);
        ~DataManager();
        // 定义一个函数，检查文件是否存在，如果存在则删除
        void checkAndDeleteFile();
        std::vector<std::vector<double>> readLines();
        std::string formatNumber(const int &channel);
        std::string ReplaceLEDwithPED(const std::string &input);
        void saveToText(const std::string &outfile, const std::string &channel, const std::vector<double> parameters, const std::vector<double> paraerror, const int status);
      

    private:
        std::string filename;
};

#endif