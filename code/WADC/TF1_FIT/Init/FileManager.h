#ifndef FILEMANAGER_H
#define FILEMANAGER_H

#include <iostream>
#include <fstream>
#include <filesystem>
#include <ctime>
#include <string>

namespace fs = std::filesystem;

class FileManager {
public:
    // 检查文件是否存在，如果存在则删除
    void checkAndDeleteFile(const std::string& filename);

    // 将文件从一个文件夹移动到另一个文件夹
    void moveFilesToNewFolder(const std::string& sourceFolderPath, const std::string& destinationFolderPath);

    // 检查文件夹是否存在
    bool directoryExists(const std::string& path);

    // 创建新的文件夹
    bool createDirectory(const std::string& path);
    void copyFileToPath(const std::string &sourceFilePath, const std::string &destinationPath);

    // 获取当前时间
    std::string getCurrentTime();

    // 检查目录路径并根据情况创建或重命名目录
    int Createpath(const std::string& folderName);
      // Rename a folder to a specific name
    bool renameFolder(const std::string& oldName, const std::string& newName);
};

#endif // DIRECTORY_MANAGER_H
