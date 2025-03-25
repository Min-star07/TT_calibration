#!/bin/bash


HV=800
type=correction_after

python read_data.py --CB 22 --ROB 15 --mode WADC  --HV $HV  --TYPE $type --WALL 1  --FEB 61 