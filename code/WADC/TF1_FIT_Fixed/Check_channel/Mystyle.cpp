#include "Mystyle.h"

MyStyle::MyStyle() {
    SetStyle();
}

void MyStyle::SetStyle() {
    // Show the fit statistics box
    gStyle->SetOptFit(1111);
    gStyle->SetOptStat(11);

    // Set pad margins
    gStyle->SetPadLeftMargin(0.15);
    gStyle->SetPadBottomMargin(0.15);
    gStyle->SetPadTopMargin(0.05);
    gStyle->SetPadRightMargin(0.05);

    // Set grid lines for X and Y axes
    gStyle->SetPadGridX(1);
    gStyle->SetPadGridY(1);

    // Set line width
    gStyle->SetLineWidth(2);

    // Customize axes labels
    gStyle->SetLabelSize(0.05, "XYZ");
    gStyle->SetLabelFont(132, "XYZ");
    gStyle->SetLabelOffset(0.01, "XYZ");
    gStyle->SetNdivisions(105, "XYZ");

    // Set legend properties
    gStyle->SetLegendBorderSize(0);
    gStyle->SetLegendFont(132);

    // Customize histogram line width
    gStyle->SetHistLineWidth(5);
}

void MyStyle::Apply() {
    // Apply the style settings
    SetStyle();
}
