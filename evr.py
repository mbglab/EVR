#!/usr/bin/python2
#-*- coding: utf-8 -*-
'''
Author: Kang-Jian Hua
E-mail: huakangjian1995@gmail.com
Usage:
python evr.py -i INPUT-FILE -o OUTPUT-FILE [...]
'''
import sys

from CELL import Chromosome, Matrix
from IO import WritePDB
from OPT import GetArg

#Get command line parameters
matrix_file, output_file, se, alpha, scale, min_dis, max_dis, iter_num, thread, use_cl, seed, chr_type = GetArg()

if not matrix_file:
    print("fatal error: no input file.")
    sys.exit()

if not output_file:
    print("fatal error: no output file.")
    sys.exit()

#Get matrix, process matrix and convert IF matrix to distance matrix
matrix = Matrix(matrix_file)
matrix.GuassianFilter(se)
#matrix.IFThreshFilt(0.0)
matrix.IF2Dis(alpha, scale)
matrix.DisThreshFilt(min_dis)

#Initialize the chromosome structure object
chromosome = Chromosome(matrix.bin_num, seed, s = scale)

#Optimize chromosome structure using Cython or OpenCL scheme
if use_cl:
    from SOLVER import solver_opencl
    solver_opencl(chromosome, matrix, min_dis, max_dis, iter_num, chr_type)
else:
    from SOLVER import solver_c
    solver_c(chromosome, matrix, min_dis, max_dis, thread, iter_num, chr_type)

#chromosome.GetCenter()
#chromosome.Center2Origin()
#Export structure as .pdb file
WritePDB(chromosome.coor, output_file, ctype = chr_type)
print("Solving Done!")
