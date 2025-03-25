#ifndef MYSTYLE_H
#define MYSTYLE_H

#include <TStyle.h>

class MyStyle {
public:
    MyStyle(); // Constructor to set the style
    void Apply(); // Method to apply the style settings

private:
    void SetStyle(); // Private method to define the style settings
};

#endif // MYSTYLE_H
