import getopt
import os
import sys


def ShowHelp():
    '''
    Print help information to the terminal.
    '''
    message = "\
Usage:\n\
    python %s -i InputFile -o OutputFile [options]\n\n\
    Required Parameters:\n\
    \
    -i          Input File.\n\
    \
    -o          Output File.\n\n\
    Optional Parameters:\n\
    \
    -h          Print help messages.\n\
    \
    --se        Smoothing Factor. \n\
                        Default: 2.\n\
    \
    --alpha     Alpha, Factor in transforming interaction matrix into distance matrix. \n\
                        Default: 0.5.\n\
    \
    --scale     Chromosome size. \n\
                        Default: 20.0.\n\
    \
    --min_dis   Minimum distance between two bins.\n\
                        Default: 0.001.\n\
    \
    --max_dis   Maximum distance between two adjacent bins.\n\
                        Default: 0.2.\n\
    \
    --iter_num  The number of iterations needed to run. If equal to 'auto', the program will terminate when f value is less than 0.001.\n\
                        Default: 2000. \n\
    \
    -t          Number of threads. If equal to 'auto', all the cores will be used.\n\
                        Default: 'auto'.\n\
    \
    --seed      Seed for generating random initial structure.\n\
                        Default: 'auto'. \n\
    \
    --ChrType   Chromosome type. \n\
                        0 -> Circular\n\
                        1 -> Linear\n\
                        Default: 0\n\
    \
    --OpenCL    Using OpenCL solver.\n        " % (sys.argv[0])
    
    print(message)
    os._exit(0)

def GetArg():
    '''
    Get command line parameters.
    '''
    matrix_file = None
    output_file = None
    se = 2
    alpha = 0.5
    scale = 20.0
    min_dis = 0.001
    max_dis = 0.2
    iter_num = 2000
    thread = "auto"
    using_cl = False
    seed = "auto"
    chr_type = "0"
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hi:o:t:", ["alpha=", "scale=", "min_dis=", "max_dis=", "iter_num=", "OpenCL", "seed=", "ChrType="])

        for opt, value in opts:
            if opt == "-i":
                matrix_file = value
            elif opt == "-o":
                output_file = value
            elif opt == "--se":
                try:
                    se = float(value)
                except:
                    print("Error: the parameter --se must be a numeric type!")
            elif opt == "--alpha":
                try:
                    alpha = float(value)
                except:
                    print("Error: the parameter --alpha must be a numeric type!")
            elif opt == "--scale":
                try:
                    scale = float(value)
                except:
                    print("Error: the parameter --scale must be a numeric type!")
            elif opt == "--min_dis":
                try:
                    min_dis = float(value)
                except:
                    print("Error: the parameter --min_dis must be a numeric type!")
            elif opt == "--max_dis":
                try:
                    max_dis = float(value)
                except:
                    print("Error: the parameter --max_dis must be a numeric type!")
            elif opt == "-h":
                ShowHelp()
            elif opt == "--iter_num":
                if value != "auto":
                    try:
                        iter_num = int(value)
                    except:
                        print("Error: the parameter --iter_num must be a numeric type!")
            elif opt == "-t":
                if value != "auto":
                    try:
                        thread = int(value)
                    except:
                        print("Error: the parameter --auto must be a numeric type!")
            elif opt == "--OpenCL":
                using_cl = True
            elif opt == "--seed":
                if value != "auto":
                    try:
                        seed = int(value)
                    except:
                        print("Error: the parameter --seed must be a numeric type!")
            elif opt == "--ChrType":
                if value not in ["0", "1"]:
                    print("error: ChrType value must be 0 or 1.")
                    ShowHelp()
                else:
                    chr_type = value
            else:
                print("error: missing argument to '%s'" % (value))
                ShowHelp()
        if not matrix_file:
            print("fatal error: no input file.")
            ShowHelp()
        if not output_file:
            print("fatal error: no output file.")
            ShowHelp()
    except getopt.GetoptError as err:
        print(str(err))
        ShowHelp()
    return matrix_file, output_file, se, alpha, scale, min_dis, max_dis, iter_num, thread, using_cl, seed, chr_type
