#!/bin/bash



file_led=WADC_LED_805_after_cCB-22_2024-09-18_19_31_000000_hist.root
file_ped=WADC_PED_805_after_cCB-22_2024-09-18_19_35_000000_hist.root
HV=805
type=correction_after

./Run_Fit -CB 22 -ROB 5 -m WADC -fl $file_led -fd $file_ped -v $HV -type $type


