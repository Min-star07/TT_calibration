#include "FileManager.h"

// 检查文件是否存在，如果存在则删除
void FileManager::checkAndDeleteFile(const std::string& filename) {
    std::ifstream file(filename);
    if (file.good()) {
        file.close();
        if (std::remove(filename.c_str()) != 0) {
            std::cerr << "Error deleting file: " << filename << std::endl;
        } else {
            std::cout << "File deleted successfully: " << filename << std::endl;
        }
    } else {
        std::cout << "File does not exist: " << filename << std::endl;
    }
}

// 将文件从一个文件夹移动到另一个文件夹
void FileManager::moveFilesToNewFolder(const std::string& sourceFolderPath, const std::string& destinationFolderPath) {
    try {
        if (!fs::exists(destinationFolderPath)) {
            fs::create_directories(destinationFolderPath);
        }

        for (const auto& entry : fs::directory_iterator(sourceFolderPath)) {
            if (entry.is_regular_file()) {
                fs::path sourcePath = entry.path();
                fs::path destinationPath = destinationFolderPath + "/" + sourcePath.filename().string();
                fs::rename(sourcePath, destinationPath);
                std::cout << "Moved file: " << sourcePath << " to: " << destinationPath << std::endl;
            }
        }
    } catch (const std::exception& e) {
        std::cerr << "Error: " << e.what() << std::endl;
    }
}

// 检查文件夹是否存在
bool FileManager::directoryExists(const std::string& path) {
    return fs::exists(path) && fs::is_directory(path);
}

// 创建新的文件夹
bool FileManager::createDirectory(const std::string& path) {
    return fs::create_directories(path);
}

// 获取当前时间
std::string FileManager::getCurrentTime() {
    std::time_t t = std::time(nullptr);
    char buffer[20];
    std::strftime(buffer, sizeof(buffer), "%Y%m%d%H%M%S", std::localtime(&t));
    return std::string(buffer);
}

// 检查目录路径并根据情况创建或重命名目录
int FileManager::Createpath(const std::string& folderName) {
    if (!fs::exists(folderName)) {
        if (!fs::create_directories(folderName)) {
            std::cerr << "Failed to create directory: " << folderName << std::endl;
            return EXIT_FAILURE;
        }
        std::cout << "Directory created successfully: " << folderName << std::endl;
    } else {
        std::cout << "Directory already exists: " << folderName << std::endl;
        std::string newFolderName = folderName +"_" + getCurrentTime();
        if (fs::create_directories(newFolderName)) {
            moveFilesToNewFolder(folderName, newFolderName);
            std::cout << "Directory renamed successfully." << std::endl;
        } else {
            std::cerr << "Failed to create new directory: " << newFolderName << std::endl;
            return EXIT_FAILURE;
        }
    }
    return EXIT_SUCCESS;
}


// 将特定文件移动到另一个路径
void FileManager::copyFileToPath(const std::string& sourceFilePath, const std::string& destinationPath) {
    try {
        if (fs::exists(sourceFilePath)) {
            fs::path sourcePath = sourceFilePath;
            fs::path destPath = destinationPath;

            // 确保目标文件夹存在，如果不存在则创建
            if (!fs::exists(destPath.parent_path())) {
                fs::create_directories(destPath.parent_path());
            }

            // 将文件移动到目标路径
            fs::copy(sourcePath, destPath);
            std::cout << "Moved file: " << sourceFilePath << " to: " << destinationPath << std::endl;
        } else {
            std::cout << "File does not exist: " << sourceFilePath << std::endl;
        }
    } catch (const std::exception& e) {
        std::cerr << "Error moving file: " << sourceFilePath << " to: " << destinationPath << std::endl;
        std::cerr << "Exception: " << e.what() << std::endl;
    }
}


// Rename a folder to a specific name
bool FileManager::renameFolder(const std::string& oldName, const std::string& newName) {
    
    if (!fs::exists(oldName)) {
        if (!fs::create_directories(oldName)) {
            std::cerr << "Failed to create directory: " << oldName << std::endl;
            return EXIT_FAILURE;
        }
        std::cout << "Directory created successfully: " << oldName << std::endl;
     }
        else {
        std::cout << "Directory already exists: " << oldName << std::endl;
        std::string newFolderName = newName;
        if (fs::create_directories(newFolderName)) {
            moveFilesToNewFolder(oldName, newFolderName);
            std::cout << "Directory renamed successfully." << std::endl;
        } else {
            std::cerr << "Failed to create new directory: " << newFolderName << std::endl;
            return false;
        }
    } 
    return true;
}