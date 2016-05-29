#!/bin/env python
import os,sys,string
from math import *
from array import array


#this program computes the number of showers needed to populate a spill
K=float(sys.argv[1]) #flux constant
lowE=float(sys.argv[2]) #low energy
highE=float(sys.argv[3]) #high energy
a=float(sys.argv[4]) #area over which showers are to be distributed in m^2
totalTimeWindow=float(sys.argv[5]) #duration of spill in s, e.g. 6.4e-3 s

eslope=-2.7
EiToOneMinusGamma=pow(lowE,1+eslope)
EfToOneMinusGamma=pow(highE,1+eslope)
#a=6621.449405
#totalTimeWindow=6.4e-3


NumShowers=totalTimeWindow*(pi*a*K*(EfToOneMinusGamma - EiToOneMinusGamma)/(1+eslope))

print int(ceil(NumShowers))

