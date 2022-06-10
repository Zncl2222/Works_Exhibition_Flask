from ctypes import *


def quicksort_func(arr):
    dll = CDLL('./model/Library/qsort.dll')
    qsort = dll.quicksort
    qsort.argtypes = (POINTER(c_int),c_int, c_int)
    qsort.restype = None

    #arr = [5,1,22,4,5,7,8,-7,841,55]
    array = (c_int * len(arr))()

    for i in range(len(arr)):
        array[i] = arr[i]

    qsort(array,0,len(array)-1)
    return array
