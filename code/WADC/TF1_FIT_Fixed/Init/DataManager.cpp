#include "DataManager.h"
#include <iostream>
#include <fstream>
#include <string>
#include <filesystem>

namespace fs = std::filesystem;


DataManager::DataManager(const std::string &filename) : filename(filename){}
DataManager::~DataManager() {}

std::vector<std::vector<double>>DataManager::readLines(){
    std::ifstream file(filename);
     // 检查文件是否成功打开
    if (!file.is_open()) {
        std::cerr << "无法打开文件================:" << filename << std::endl;
        std::exit(1);
    }
     // 定义一个向量来存储每一行拆分后的字段
    std::vector<std::vector<double>> lines;
    // 从文件中逐行读取数据
    std::string line;
    while (std::getline(file, line)) {
        // 创建一个字符串流，用于拆分行
        std::istringstream lineStream(line);
        std::vector<std::string> fields;
        std::string field;

        // 使用制表符（\t）作为分隔符拆分行
        while (std::getline(lineStream, field, '\t')) {
            fields.push_back(field); // 将每个字段添加到向量中
        }
     

        // transform string int odouble
        std::vector<double> doubleVec;
         for (const std::string& str : fields) {
            std::istringstream iss(str);
            double value;
            if (iss >> value) {
                doubleVec.push_back(value);
            } else {
            // Handle invalid input
            std::cerr << "Failed to convert string to double: " << str << std::endl;
        }
         }
        // 将拆分后的字段向量添加到 lines 向量中
        lines.push_back(doubleVec);
        
    }
    // 关闭文件输入流
    file.close();

//    for (const auto& line : lines) {
//         for (const auto& field : line) {
//             std::cout << field << " ";
//         }
//         std::cout << std::endl;
//     }


    return lines;

}


std::string DataManager::formatNumber(const int &channel) {
    // Format the number with leading zeros
    std::stringstream ss;
    ss << std::setw(2) << std::setfill('0') << channel;

    // Copy the formatted result to a new variable
    std::string formattedNum;
    ss >> formattedNum;

    return formattedNum;
}

// Function to replace 'LED' with 'PED' in a string
std::string DataManager::ReplaceLEDwithPED(const std::string& input) {
    std::string modifiedString = input;
    std::string toReplace = "LED";
    std::string replacement = "PED";

    size_t pos = 0;
    while ((pos = modifiedString.find(toReplace, pos)) != std::string::npos) {
        modifiedString.replace(pos, toReplace.length(), replacement);
        pos += replacement.length();
    }

    return modifiedString;
}


// 从文件中读取数据
void DataManager::saveToText(const std::string &outfile, const std::string & channel, const std::vector<double> parameters, const std::vector<double> paraerror, const int status ){
        for (size_t i = 0; i < parameters.size(); ++i) {
            std::cout <<"parameter "<< i << "\t" << parameters[i] << " ± " << paraerror[i] << std::endl;
        }

    std::ofstream out(outfile, std::ios::app);
    out << channel << "\t";
    for (int i = 0; i < parameters.size(); i++) {
        if (i != parameters.size()-1){
            out << parameters[i] << "\t" << paraerror[i]<<"\t";
        }
        else{
            out << parameters[i] << "\t" << paraerror[i] << std::endl;
        }
    }
    // out << std::endl;
    out.close();
 }

void DataManager::checkAndDeleteFile() {
    // Check if the file exists
    if (fs::exists(filename)) {
        // Print a message indicating the file is being deleted
        std::cout << "File " << filename << " exists. Deleting it..." << std::endl;

        // Attempt to delete the file
        try {
            fs::remove(filename);
            std::cout << "File deleted successfully." << std::endl;
        } catch (const fs::filesystem_error& e) {
            // Catch and print any filesystem-related errors
            std::cerr << "Error deleting file: " << e.what() << std::endl;
        }
    } else {
        // Print a message indicating the file does not exist
        std::cout << "File " << filename << " does not exist. No action needed." << std::endl;
    }
}