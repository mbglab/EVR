'''
Compile the CORE.pyx file into an executable file.
Compile command: python setup.py build_ext --inplace.
Before compiling, you need to install the cython library.
'''
import sys
from distutils.core import setup
from distutils.extension import Extension

from Cython.Build import cythonize

if "win" in sys.platform:
    ext_modules = [
        Extension(
            "COREC",
            ["CORE.pyx"],
            extra_compile_args=['/openmp'],
            extra_link_args=['/openmp']
        )
    ]
else:
    ext_modules = [
        Extension(
            "COREC",
            ["CORE.pyx"],
            extra_compile_args=['-fopenmp'],
            extra_link_args=['-fopenmp'],
            libraries=["m"]
        )
    ]


setup(
    name='COREC',
    ext_modules=cythonize(ext_modules),
)
