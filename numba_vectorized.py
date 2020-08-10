# TODO:
#   A. Placeholder

# Library Imports
import math
from numba import vectorize

# Local Imports


@vectorize(['f8(f8)','f4(f4)'])
def sin(x):
    return math.sin(x)

@vectorize(['f8(f8)','f4(f4)'])
def cos(x):
    return math.cos(x)

@vectorize(['int8(int8,int8)',
            'int16(int16,int16)',
            'int32(int32,int32)',
            'int64(int64,int64)',
            'f4(f4,f4)',
            'f8(f8,f8)'])
def add(x,y):
    return x + y