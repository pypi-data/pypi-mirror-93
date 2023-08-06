# Author：liuzikuo (lucien)
# Date ：2020/4/15 2:07 PM
# Editor: liuzikuo, others:{your name}

# import time

import numpy as np
import cython
cimport numpy as np

DTYPE = np.int

ctypedef np.int DTYPE_t

@cython.boundscheck(False)
@cython.wraparound(False)
def convolve1(np.ndarray[np.int32_t, ndim=2] matrix, int rows, int cols, int line_min_width):
#     t1 = time.time()

    cdef int dots = 0
    cdef int start_row = 0
    cdef int start_col = 0
    cdef int kernel_row = 3
    cdef int kernel_col = 1
    cdef int row_steps = rows - kernel_row + 1
    cdef int col_steps = cols - kernel_col + 1
    cdef int stride = 1
    cdef int row
    cdef int col
    cdef np.ndarray[np.int32_t, ndim=2] line_segs = np.zeros([rows, 4], dtype=np.int32)
    cdef int res_index = 0

    for row in range(start_row, start_row + row_steps, 2):
        for col in range(start_col, start_col + col_steps, stride):
            try:
#                 if matrix[row:row + kernel_row, col].any():   # 方法一：注意，在Cython中，numpy.any() 要比循环耗时，而循环比枚举（方法三）耗时。
#                 if nonull(matrix[:,col], row, row + kernel_row):   # 方法二：比方法一快
                if matrix[row,col] > 0 or matrix[row+1,col] > 0 or matrix[row+2,col] > 0 : # 方法三
                    dots = dots + 1
                else:
                    start_dot = col - 1 - dots
                    if dots > line_min_width and nonull(matrix[row], start_dot, col):  # nonull 保证当前行本身不为空行
                        line_segs[res_index,:] = [row, start_dot, row, col - 1]
                        res_index += 1
                    dots = 0
            except:
                dots = 0
        if dots > line_min_width:
            col = start_col + col_steps
            line_segs[res_index,:] = [row, col - 1 - dots, row, col - 1]
            res_index += 1
        dots = 0

    return line_segs[:res_index]

@cython.boundscheck(False)
@cython.wraparound(False)
def convolve2(np.ndarray[np.int32_t, ndim=2] matrix, int rows, int cols, int line_min_width):
#     t1 = time.time()

    cdef int dots = 0
    cdef int start_row = 0
    cdef int start_col = 0
    cdef int kernel_col = 3
    cdef int kernel_row = 1
    cdef int row_steps = rows - kernel_row + 1
    cdef int col_steps = cols - kernel_col + 1
    cdef int stride = 1
    cdef int row
    cdef int col
    cdef np.ndarray[np.int32_t, ndim=2] line_segs = np.zeros([cols, 4], dtype=np.int32)
    cdef int res_index = 0
    for col in range(start_col, start_col + col_steps, 1):
        for row in range(start_row, start_row + row_steps, 1):
            try:
                if matrix[row,col] > 0 or matrix[row,col+1] > 0 or matrix[row,col+2] > 0 :
                    dots = dots + 1
                else:
                    start_dot = row - 1 - dots
#                     if dots > 0:
#                         print('col:{}, rows:{}, dots:{}'.format(col, row, dots))
                    if dots > line_min_width and nonull(matrix[:,col], start_dot, row):  # nonull 保证当前行本身不为空行
                        line_segs[res_index,:] = [start_dot, col, row-1, col]
                        res_index += 1
                    dots = 0
            except:
                dots = 0
        if dots > line_min_width:
            row = start_row + row_steps
            line_segs[res_index,:] = [row - 1 - dots, col, row-1, col]
            res_index += 1
        dots = 0

    return line_segs[:res_index]

cdef int nonull(np.ndarray[np.int32_t, ndim=1] arr, int start, int end):
    for i in range(start, end):
        if arr[i] > 0:
            return 1
    return 0