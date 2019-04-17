import sys


def solver_p(chromosome, matrix, min_dis, max_dis, iter_num = "auto", ctype = "0"):
    '''
    Use pure python code to optimize the structure.
    Single-thread solution.
    '''
    from CORE import evr_cyc, evr_lin

    if ctype == "0":
        kernel = evr_cyc
    else:
        kernel = evr_lin

    i = 0
    f0 = 0
    while True:
        trans, f = kernel(chromosome.coor, matrix.dis_matrix, min_dis, max_dis)

        chromosome.Translate(trans)
        i += 1
        print(i, f)

        if iter_num != "auto":
            if i > int(iter_num):
                break
        else:
            if abs(f - f0) < 0.00001:
                break
            f0 = f

def CalF(trans_matrix):
    '''Calculate F value using coordinate transformation matrix.'''
    import math
    f_value = 0.0
    trans = trans_matrix.reshape((-1, 3))
    for vec in trans:
        f_value += math.sqrt(vec[0] ** 2 + vec[1] ** 2 + vec[2] ** 2)
    return f_value


def solver_opencl(chromosome, matrix, min_dis, max_dis, iter_num = "auto", ctype = "0"):
    '''
    Optimize the structure with PyOpenCL.
    This function will automatically detect the OpenCL platform installed in the system, 
    create a context on the corresponding platform and a device according to the user's choice, 
    compile the kernel function, and execute for structure optimization.
    '''
    try:
        import pyopencl as cl
    except:
        print("PyopenCL library not found!")
        print("Using pure python engine to solve it.")

        solver_p(chromosome, matrix, min_dis, max_dis, iter_num, ctype)
        return

    import numpy as np 
    from IO import LoadCL

    coor = chromosome.coor.ravel()
    dis_matrix = matrix.dis_matrix.ravel()

    trans = np.empty_like(coor)

    context = cl.create_some_context()
    queue = cl.CommandQueue(context)
    mf = cl.mem_flags

    coor_buf = cl.Buffer(context, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf = coor)

    matrix_buf = cl.Buffer(context, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf = dis_matrix)

    trans_buf = cl.Buffer(context, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf = trans)

    src = LoadCL("CORE.cl")

    program = cl.Program(context, src).build()
    if ctype == "0":
        kernel = program.evr_cyc
    else:
        kernel = program.evr_lin

    kernel.set_scalar_arg_dtypes([None, None, np.float32, np.float32, np.int32, None])

    i = 0
    f0 = 0
    while True:
        i += 1
        kernel(queue, [chromosome.bin_num, 1], None, coor_buf, matrix_buf, min_dis, max_dis, chromosome.bin_num, trans_buf)

        cl.enqueue_copy(queue, trans, trans_buf)
        f = CalF(trans)
        coor += trans
        
        print(i, f)
        if iter_num == "auto":
            if abs(f - f0) < 0.00001:
                break
            f0 = f
        else:
            if i > int(iter_num): 
                break

        coor_buf.release()
        coor_buf = cl.Buffer(context, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf = coor)

        trans_buf.release()
        trans_buf = cl.Buffer(context, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf = trans)
    
    coor_buf.release()
    matrix_buf.release()
    trans_buf.release()
    chromosome.coor = coor.reshape((-1, 3))

def solver_c(chromosome, matrix, min_dis, max_dis, ncpu = "auto", iter_num = "auto", ctype = "0"):
    '''
    Optimize the structure with Cython and openmp.
    This function can only run on CPUs.
    This function requires the .pyx file to be compiled in advance.
    '''
    try:
        from COREC import evr_cyc, evr_lin
    except:
        print("Dynamic Library EVRC not found. Run the command 'python setup.py build_ext --inplace' to create it.")
        print("Using pure python engine to solve it.")

        solver_p(chromosome, matrix, min_dis, max_dis, iter_num, ctype)
        return
    
    if ncpu == "auto":
        ncpu = 0

    if ctype == "0":
        kernel = evr_cyc
    else:
        kernel = evr_lin
    
    i = 0
    f0 = 0
    while True:
        coor, f = kernel(chromosome.coor, matrix.dis_matrix, min_dis, max_dis, ncpu)

        chromosome.SetCoor(coor)
        i += 1
        print(i, f)

        if iter_num != "auto":
            if i > int(iter_num):
                break
        else:
            if abs(f - f0) < 0.00001:
                break
            f0 = f
