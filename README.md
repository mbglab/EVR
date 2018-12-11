# EVR
EVR is a chromosome 3D structure reconstruction tool using an Error-Vector Resultant algorithm based on DNA interaction data. With normalized or unnormalized IF matrix as input, the program generate a chromosome 3D structure output in a .pdb file. 
Using Cython and OpenCL, the program can run on CPUs/GPUS/APUs and thus usually faster than similar tools. 

The executable files can be downloaded from https://github.com/HakimHua/EVR/releases.

## Installation
Requirement:
* python (2.7 or 3.x)
* numpy
* scipy

Optinal:
* matplotlib (For plotting)
* Cython (Accelerating by multi-core CPUs)
* PyOpenCL (Accelerating by multi-core CPUs or many-core Processors like GPUs/APUs. Need to install related drivers.)

## Usage
```bash
python evr.py -i [input file] -o [output file] [...]
```

### Parameters
|Parameter |Description | Default Value|
|:-:|:-|:-:|
|-i |Input file. |None |
|-o |Output file. |None |

Optional Parameters:

|Parameter |Description | Default Value|
|:-:|:-|:-:|
|-h |Printing help messages. |\ |
|--se |Smoothing Factor. |2 |
|--alpha |Factor in transforming interaction matrix into distance matrix.|0.5 |
|--scale |Chromosome size.|20.0 |
|--min_dis |Minimum distance between two bins.|0.001 |
|--max_dis |maximum distance between two adjacent bins.|0.2 |
|--iter_num |The number of iterations needed to run. If equal to 'auto', the program will terminate when f value is less than 0.00001. |'auto' |
|-t |Number of threads. |'auto' |
|--seed |Seed for generating random initial structure.|'auto' |
|--OpenCL |Using OpenCL solver.|\ |
|--ChrType |Chromosome type. "0": Circular chromosome; "1": Linear chromosome. |"0" |

## Input file format
1. Matrix format
```txt
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
2. Three columns format
The format of the input file can have three columns, separated by tabs:
```
>bin1   >bin2   >frequency
```
Example：
```
0   1   0.0281
0   2   0.0197
0   3   0.0259
0   4   0.0143
...
256 255 0.0185
```
## Output file format
The output file is a '.pdb' file that follows the standard PDB format. You can use the "plot.py" file to draw structure, or use any other PDB viewer program to do it.

## Other parameters.
With reference to Virginia S. Lioy et al, 2018, when the value of parameter alpha is 0.5, the expected distance matches the fluorescence data well. min_dis is the minimum distance between any two bins and max_dis is the maximum distance between two adjacent bins. 

The initial conformation of chromosome is generated randomly. Without a seed, the initial conformation will be totally random and the result may differ between different running times even with the same input data. But with a specified seed, the result will be the same.

### Speed up calculation
#### With Cython
The program uses Cython for acceleration by default. Iterative optimization code is written in Cython syntax (see CORE.pyx file). When running the program for the first time, you need to compile CORE.pyx into a dynamic link library by this command:
```bash
python setup.py build_ext --inplace
```
Before compiling, you need to install Cython by "pip install cython" and something alike. The build will produce a COREC.so file on a Linux system or a COREC.pyd file on a Windows system.

##### On windows (Only work with python 2.7)
1. Download and install [Microsoft Visual C++ Compiler for Python 2.7](https://www.microsoft.com/en-us/download/details.aspx?id=44266). The installation path is: C:\Users\Administrator\AppData\Local\Programs\Common\Microsoft\Visual C++ for Python\9.0
2. Modify the file: $PYTHON_PATH\Lib\distutils\msvc9compiler.py. 
If not compiled, the program will use pure python solver engine to optimize structure and that runs slow. If using Cython acceleration, you can specify the number of threads to use by -t parameter. All CPU cores will be used by default. 
The modification methods are as follows:
* Add a line between the 174 and 175 lines: "return 9"
* Add a line between the 174 and 175 lines: "return r'C:\Users\Administrator\AppData\Local\Programs\Common\Microsoft\Visual C++ for Python\9.0\vcvarsall.bat'"
3. Run the above command to compile.

##### On Linux
1. Install gcc, python-dev (for debain-based system), python-devel (for Red Hat based system).
2. Run the above command to compile.

#### With OpenCL
In addition to using Cython for acceleration, you can use OpenCL. With OpenCL, you can speed up computing on CPUs and other processors like APUs and GPUs. 

Firstly, you have to install the PyOpenCL library. On Linux, just type"pip install pyopencl" to install it. On Windows, you can download installation file on the [website](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyopencl), and use pip to install it(pip install file_name). In addition, you also need to install the relevant processor driver and OpenCL libraries. On Windows system, installation is easy. On Linux, you need to have administrator privileges and install the relevant OpenCL SDK.

To use OpenCL for acceleration, just add the "--OpenCL" parameter (no value):
```bash
python evr -i [Input file] -o [Output file] --OpenCL [...]
```
When using OpenCL to optimize the structure, the program will automatically detect the available OpenCL platforms. And then require the user to select the running platform and equipment (even if only one platform is detected). If you want to avoid user selection, you can add export PYOPENCL_CTX=id before the command. E.g:
```bash
export PYOPENCL_CTX='0'; python evr -i [Input file] -o [Output file] --OpenCL [...]
```
This command will make the program use the first platform detected.

Author: Kangjian-Hua
E-mail: huakangjian1995@gmail.com
