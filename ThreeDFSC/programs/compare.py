import cuda_kernels
import jittest
import math
import numpy as np
from numba import cuda
import time


def test():

    start = time.time()

# Host code
    NumOnSurf = 30000
    End = 15000
    Start = 0
    Thresh = 0.93

# Instantiate test values
    kXNow = np.random.randint(0,9,size=(NumOnSurf))
    kYNow = np.random.randint(0,9,size=(NumOnSurf))
    kZNow = np.random.randint(0,9,size=(NumOnSurf))

# Copy the arrays to the device
    kXNow_global_mem = cuda.to_device(kXNow)
    kYNow_global_mem = cuda.to_device(kYNow)
    kZNow_global_mem = cuda.to_device(kZNow)


# Allocate memory on the device for the result
    NumAtROutPre_global_mem = cuda.device_array((NumOnSurf,End-Start))
    Prod11_global_mem = cuda.device_array(NumOnSurf)


# Configure the blocks
    threadsperblock = (16,1,1)
    blockspergrid_x = int(math.ceil(kXNow.shape[0] / threadsperblock[0]))
    blockspergrid = (blockspergrid_x,1,1)

    print("blockspergrid_x = ",blockspergrid_x)
    print("blockspergrid = ",blockspergrid)

    start_cuda = time.time()
# Start the kernel 
    cuda_kernels.cuda_calcProd11[blockspergrid, threadsperblock](kXNow,kYNow,kZNow,Prod11_global_mem)

    cuda_kernels.cuda_calcInner2[blockspergrid, threadsperblock](\
            kXNow,\
            kYNow,\
            kZNow,\
            Prod11_global_mem,\
            NumAtROutPre_global_mem,\
            End,\
            Start,\
            Thresh)


# Copy the result back to the host
    NumAtROutPre = NumAtROutPre_global_mem.copy_to_host()
    end_cuda = time.time()

    print("AveragesOnShells CUDA: ")
    print(NumAtROutPre)

    print("CUDA version completed in %.3f seconds."%(end_cuda - start_cuda))

    print("shape of NumAtROutPre is ",np.shape(NumAtROutPre))

    start_jit = time.time()
    C2 = jittest.AveragesOnShells(kXNow,kYNow,kZNow, NumOnSurf, Thresh,Start, End)
    end_jit = time.time()
    print("AveragesOnShells jit: ")
    print(C2)

    print(type(NumAtROutPre))
    print(type(C2))

    print(sum(sum(NumAtROutPre==C2)))
    print(NumOnSurf*(End-Start))

    end = time.time()
    print("CUDA version completed in %.3f seconds."%(end_cuda - start_cuda))
    print("AUTOJIT version completed in %.3f seconds."%(end_jit - start_jit))
    print("Completed in %.3f seconds."%(end-start))

    return NumAtROutPre,C2

if __name__ == "__main__":
    test()
