#include <iostream>
#include <stdio.h>

int main(int argc, char** argv){

    int num = atoi(argv[1]);
    // std::cout << argv[1] << std::endl;
    printf("hello word %s times\n", argv[1]);
    return 0;
}