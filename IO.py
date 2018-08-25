#-*- coding: utf-8 -*-
import sys

import numpy as np


def LoadMatrix(matrix_file):
    '''
    Load Matrix file.
    Matrix file must be a text file. The format can be:
    ```
    0.0000 0.0000 0.0281 0.0268 0.0227 0.0189 0.0143 ... 0.0126
    0.0000 0.0000 0.0000 0.0305 0.0272 0.0235 0.0184 ... 0.0166
    0.0281 0.0000 0.0000 0.0000 0.0326 0.0259 0.0197 ... 0.0174
    0.0268 0.0305 0.0000 0.0000 0.0000 0.0328 0.0234 ... 0.0199
    0.0227 0.0272 0.0326 0.0000 0.0000 0.0000 0.0185 ... 0.0204
    0.0189 0.0235 0.0259 0.0328 0.0000 0.0000 0.0000 ... 0.0180
    0.0143 0.0184 0.0197 0.0234 0.0185 0.0000 0.0000 ... 0.0000
    ...    ...    ...    ...    ...    ...    ...    ... ...
    0.0126 0.0166 0.0174 0.0199 0.0204 0.0180 0.0000 ... 0.0000
    ```
    or be:
    ```
    0   1   0.0281
    0   2   0.0197
    0   3   0.0259
    0   4   0.0143
    ...
    256 255 0.0185
    ```
    '''
    f_o = open(matrix_file, "r")
    file_matrix = []
    for line in f_o.readlines():

        line = line.strip()
        if line:
            pass
        else:
            continue
        l_s = line.split()
        file_matrix.append(l_s)

    f_o.close()

    file_matrix = np.array(file_matrix, dtype = np.float32)
    matrix_shape = file_matrix.shape
    if matrix_shape[0] == matrix_shape[1]:
        matrix = file_matrix
    else:
        bin_num = int(max(np.max(file_matrix[:, 0]), np.max(file_matrix[:, 1])))
        matrix = np.zeros((bin_num, bin_num), dtype = np.float32)
        for e in file_matrix:
            i = int(e[0] - 1)
            j = int(e[1] - 1)
            v = e[2]
            matrix[i, j] = v
            matrix[j, i] = v

    return matrix

def ReadPDB(pdb_file):
    '''Read PDB file.'''
    f_o = open(pdb_file)
    f_r = f_o.read().split("\n")
    f_o.close()

    x = []
    y = []
    z = []

    c_r = {}

    for e in f_r:
        if "ATOM" in e:
            x_p = float(e[30:38])
            y_p = float(e[38:46])
            z_p = float(e[46:54])

            x.append(x_p)
            y.append(y_p)
            z.append(z_p)

        if "CONECT" in e:
            c1 = int(e[6:11]) - 1
            c2 = int(e[11:16]) - 1

            c_r[c1] = c2

    return x, y, z, c_r

def LoadCL(CL_File):
    '''Load .cl file. This is the file where the OpenCL kernel function is located.'''
    f_o = open(CL_File)
    f_r = f_o.read()
    f_o.close()

    return f_r


def WritePDB(positions, pdb_file, ctype = "0"):
    '''Save the result as a .pdb file'''
    o_file = open(pdb_file, "w")
    o_file.write("\n")

    col1 = "ATOM"
    col3 = "CA MET"
    col8 = "0.20 10.00"

    bin_num = len(positions)

    for i in range(1, bin_num+1):
        col2 = str(i)
        col4 = "B"+col2
        col5 = "%.3f" % positions[i-1][0]
        col6 = "%.3f" % positions[i-1][1]
        col7 = "%.3f" % positions[i-1][2]
        col2 = " "*(5 - len(col2)) + col2
        col4 = col4 + " " * (6 - len(col4))
        col5 = " " * (8 - len(col5)) + col5
        col6 = " " * (8 - len(col6)) + col6
        col7 = " " * (8 - len(col7)) + col7

        col = (col1, col2, col3, col4, col5, col6, col7,col8)
        line = "%s  %s   %s %s   %s%s%s  %s\n" % col
        o_file.write(line)
    col1 = "CONECT"
    for i in range(1, bin_num+1):
        col2 = str(i)
        j = i + 1
        if j > bin_num:
            if ctype == "1":
                continue
            j = 1
        col3 = str(j)

        col2 = " " * (5 - len(col2)) + col2
        col3 = " " * (5 - len(col3)) + col3

        line = "%s%s%s\n" % (col1, col2, col3)
        o_file.write(line)

    o_file.write("END")
    o_file.close()
