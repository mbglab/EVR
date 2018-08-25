#cython: boundscheck=False
from cython.parallel import prange
from libc.math cimport sqrt

import numpy
cimport openmp


def evr_cyc(float[:, :] positions, float[:, :] matrix, float min_dis, float max_dis, int ncpu):
    cdef:
        int bin_num = positions.shape[0]
        float[:, :] trans_matrix = numpy.zeros((bin_num, 3), numpy.float32)
        float f_value = 0.0

        float pos_ix, pos_iy, pos_iz
        float pos_jx, pos_jy, pos_jz

        float divec_x, divec_y, divec_z
        float ervec_x, ervec_y, ervec_z

        float mod, dis, err
    
        int i, j

    if ncpu == 0:
        ncpu = openmp.omp_get_num_procs()
    
    for i in prange(bin_num, nogil = True, num_threads = ncpu):
        pos_ix, pos_iy, pos_iz = positions[i, 0], positions[i, 1], positions[i, 2]

        divec_x, divec_y, divec_z = 0.0, 0.0, 0.0
        ervec_x, ervec_y, ervec_z = 0.0, 0.0, 0.0

        for j in xrange(bin_num):
            if i == j:
                continue
            pos_jx, pos_jy, pos_jz = positions[j, 0], positions[j, 1], positions[j, 2]

            divec_x = pos_jx - pos_ix
            divec_y = pos_jy - pos_iy
            divec_z = pos_jz - pos_iz

            mod = sqrt(divec_x ** 2 + divec_y ** 2 + divec_z ** 2)
            dis = matrix[i, j]

            if dis == 0.0 or mod == 0.0:
                continue
            
            divec_x = divec_x / mod
            divec_y = divec_y / mod
            divec_z = divec_z / mod
            
            if i == (j + 1) % bin_num or i == (j - 1) % bin_num:
                if mod > max_dis:
                    err = mod - max_dis
                elif mod < min_dis:
                    err = mod - min_dis
                else:
                    err = mod - dis
            else:
                err = mod - dis
            
            divec_x = divec_x * err
            divec_y = divec_y * err
            divec_z = divec_z * err

            ervec_x = ervec_x + divec_x
            ervec_y = ervec_y + divec_y
            ervec_z = ervec_z + divec_z
            
        ervec_x = ervec_x / bin_num
        ervec_y = ervec_y / bin_num
        ervec_z = ervec_z / bin_num
        
        trans_matrix[i, 0] += ervec_x
        trans_matrix[i, 1] += ervec_y
        trans_matrix[i, 2] += ervec_z
        
    for i in prange(bin_num, nogil = True, num_threads = ncpu):
        f_value += sqrt(trans_matrix[i, 0] ** 2 + trans_matrix[i, 1] ** 2 + trans_matrix[i, 2] ** 2)

    for i in prange(bin_num, nogil = True, num_threads = ncpu):
        positions[i, 0] += trans_matrix[i, 0]
        positions[i, 1] += trans_matrix[i, 1]
        positions[i, 2] += trans_matrix[i, 2]

    return positions, f_value

def evr_lin(float[:, :] positions, float[:, :] matrix, float min_dis, float max_dis, int ncpu):
    cdef:
        int bin_num = positions.shape[0]
        float[:, :] trans_matrix = numpy.zeros((bin_num, 3), numpy.float32)
        float f_value = 0.0

        float pos_ix, pos_iy, pos_iz
        float pos_jx, pos_jy, pos_jz

        float divec_x, divec_y, divec_z
        float ervec_x, ervec_y, ervec_z

        float mod, dis, err
    
        int i, j

    if ncpu == 0:
        ncpu = openmp.omp_get_num_procs()
    
    for i in prange(bin_num, nogil = True, num_threads = ncpu):
        pos_ix, pos_iy, pos_iz = positions[i, 0], positions[i, 1], positions[i, 2]

        divec_x, divec_y, divec_z = 0.0, 0.0, 0.0
        ervec_x, ervec_y, ervec_z = 0.0, 0.0, 0.0

        for j in xrange(bin_num):
            if i == j:
                continue
            pos_jx, pos_jy, pos_jz = positions[j, 0], positions[j, 1], positions[j, 2]

            divec_x = pos_jx - pos_ix
            divec_y = pos_jy - pos_iy
            divec_z = pos_jz - pos_iz

            mod = sqrt(divec_x ** 2 + divec_y ** 2 + divec_z ** 2)
            dis = matrix[i, j]

            if dis == 0.0 or mod == 0.0:
                continue
            
            divec_x = divec_x / mod
            divec_y = divec_y / mod
            divec_z = divec_z / mod

            if i == j + 1 or i == j - 1:
                if mod > max_dis:
                    err = mod - max_dis
                elif mod < min_dis:
                    err = mod - min_dis
                else:
                    err = mod - dis
            else:
                err = mod - dis
            
            divec_x = divec_x * err
            divec_y = divec_y * err
            divec_z = divec_z * err

            ervec_x = ervec_x + divec_x
            ervec_y = ervec_y + divec_y
            ervec_z = ervec_z + divec_z
            
        ervec_x = ervec_x / bin_num
        ervec_y = ervec_y / bin_num
        ervec_z = ervec_z / bin_num
        
        trans_matrix[i, 0] += ervec_x
        trans_matrix[i, 1] += ervec_y
        trans_matrix[i, 2] += ervec_z
        
    for i in prange(bin_num, nogil = True, num_threads = ncpu):
        f_value += sqrt(trans_matrix[i, 0] ** 2 + trans_matrix[i, 1] ** 2 + trans_matrix[i, 2] ** 2)

    for i in prange(bin_num, nogil = True, num_threads = ncpu):
        positions[i, 0] += trans_matrix[i, 0]
        positions[i, 1] += trans_matrix[i, 1]
        positions[i, 2] += trans_matrix[i, 2]

    return trans_matrix, f_value