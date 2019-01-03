'''
This section contains the basic data structure of the program.
Chrmosome Class: Defines the coordinates of chromosomes and some basic transformations.
Matrix Class: Defining the interaction matrix and the distance matrix and some basic processing functions.
'''

import numpy as np
from scipy.ndimage import gaussian_filter

from IO import LoadMatrix

class Chromosome:
    '''The chromosome object contains the coordinates of each bin of the chromosome structure.'''
    def __init__(self, bin_num, seed, s = 20):
        self.bin_num = bin_num
        self.seed = seed

        self.CoordinateInit(s)

    def CoordinateInit(self, s):
        '''Randomly generates the coordinates of each bin using a random or specified seed.'''
        if self.seed != "auto":
            np.random.seed(seed = self.seed)
        #self.coor = s * (np.random.rand(self.bin_num, 3) - 1)
        self.coor = np.random.rand(self.bin_num, 3) - 1
        self.coor = self.coor.astype(np.float32)
        self.GetCenter()
        self.Center2Origin()

    def SetCoor(self, coor):
        self.coor = coor

    def GetCenter(self):
        '''Get the coordinates of the chromosome structure center.'''
        self.center = np.array([0.0, 0.0, 0.0])
        for i in range(self.bin_num):
            self.center += self.coor[i]

        self.center /= self.bin_num

    def Center2Origin(self):
        '''Transform coordinates so that the chromosome center is at the origin of coordinate system.'''
        for i in range(self.bin_num):
            self.coor[i] -= self.center

    def Translate(self, trans_matrix):
        self.coor += trans_matrix

class Matrix:
    '''The matrix object involves IF matrix processing and transforming into the expected distance matrix.'''
    def __init__(self, if_matrix_file = None):
        self.SetMatrixFromFile(if_matrix_file)
        self.bin_num = self.if_matrix.shape[0]

    def SetMatrixFromFile(self, if_matrix_file):
        '''Read the IF matrix from a file.'''
        self.if_matrix = LoadMatrix(if_matrix_file)

    def GuassianFilter(self, smooth_coef):
        '''Gaussian smoothing.'''
        self.if_matrix = gaussian_filter(self.if_matrix, smooth_coef)

    def IFThreshFilt(self, prop):
        '''IF matrix filtering.'''
        thresh = self.FindThresh(prop)
        is_low = self.if_matrix < thresh
        self.if_matrix[is_low] = 0

    def FindThresh(self, prop):
        matrix_1d = self.if_matrix.copy().reshape((1, -1))
        matrix_1d.sort()
        index = int(prop * self.bin_num * 2)

        thresh = matrix_1d[0][index]

        return thresh

    def IF2Dis(self, alpha, scale):
        '''Convert the IF matrix to the expected distance matrix.'''
        self.dis_matrix = np.zeros(self.if_matrix.shape, np.float32)

        is_zero = self.if_matrix != 0
        self.dis_matrix[is_zero] = (1 / self.if_matrix[is_zero]) ** alpha
        self.SizeChange(scale)

    def SizeChange(self, scale = 20):
        prop = scale / np.max(self.dis_matrix)
        self.dis_matrix *= prop

    def DisThreshFilt(self, min_dis):
        is_low = self.dis_matrix < min_dis
        self.dis_matrix[is_low] = 0
