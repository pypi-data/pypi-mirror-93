import os
import platform
import sysconfig
import ctypes as ct

from rapid import config

NDARRAY_CUBLAS_SUCCESS = 1
NDARRAY_CUBLAS_NOT_INITIALIZED = 2
NDARRAY_CUBLAS_ALLOC_FAILED = 3
NDARRAY_CUBLAS_INVALID_VALUE = 4
NDARRAY_CUBLAS_ARCH_MISMATCH = 5
NDARRAY_CUBLAS_MAPPING_ERROR = 6
NDARRAY_CUBLAS_EXECUTION_FAILED = 7
NDARRAY_CUBLAS_INTERNAL_ERROR = 8
NDARRAY_CUBLAS_NOT_SUPPORTED = 9
NDARRAY_CUBLAS_LICENSE_ERROR = 10

# Extract the correct extension type for the OS
def extractExtension():
    if platform.system() == "Windows":
        return ".dll"
    else:
        return sysconfig.get_config_var("SO")

# Load a libary
def loadLibraryHalf(basename):
    basedir = os.path.join(os.path.dirname(__file__) or os.path.curdir) + "\\..\\"

    directory = basename[:-basename[::-1].find("/")]
    filename = basename[-basename[::-1].find("/"):]

    basedir += directory

    files = os.listdir(path=basedir)

    ext = extractExtension()

    matching_file = ""

    for file in files:
        if file[:len(filename)] == filename and file[-len(ext):] == ext:
            matching_file = file

    if matching_file == "":
        raise FileNotFoundError("Unable to locate file \"" + filename + "\"")

    return ct.cdll.LoadLibrary(os.path.join(
        os.path.dirname(__file__) or os.path.curdir,
        basedir + matching_file.rstrip(ext) + ext))

# Load the rapid dll and store it
try:
    _librapid = loadLibraryHalf("bin/librapid_ndarray")
except FileNotFoundError:
    raise FileNotFoundError("Unable to load compiled DLL. Ensure it is located in the rapid/bin folder in site-packages")


class rapid_ndarray_float(ct.Structure):
    _fields_ = [("dataStart", ct.POINTER(ct.c_float)),
                ("dataOrigin", ct.POINTER(ct.c_float)),
                ("originReferences", ct.POINTER(ct.c_long)),
                ("shape", ct.POINTER(ct.c_long)),
                ("dims", ct.c_long)]

# Set the return types of functions

_librapid.getError_ndarray.restype = ct.c_int

# Memory processes
_librapid.allocateDeviceMemory_float.restype = ct.POINTER(ct.c_float)
_librapid.ndToScalar.restype = ct.c_long

# Array creation and destruction
_librapid.createArray_float.restype = rapid_ndarray_float
_librapid.createEmptyArray_float.restype = rapid_ndarray_float

# Array getters and setters
_librapid.getDeviceArrVal_float.restype = ct.c_float
_librapid.getSubArray_float.restype = rapid_ndarray_float
_librapid.setSubArray_float.restype = rapid_ndarray_float
_librapid.getDeviceArrValIndex_float.restype = ct.c_float

_librapid.getCudaError.restype = ct.POINTER(ct.c_char)

# Kernels all return void

# Provide wrappers for the dll functions

def allocateDeviceMemory_float(size):
    return _librapid.allocateDeviceMemory_float(size)

def freeDeviceMemory_float(ptr):
    _librapid.freeDeviceMemory_float(ptr)

def memcpyHostDevice_float(dst, src, size):
    _librapid.memcpyHostDevice_float(dst, src, size)

def memcpyDeviceHost_float(dst, src, size):
    _librapid.memcpyDeviceHost_float(dst, src, size)

def memcpyDeviceDevice_float(dst, src, size):
    _librapid.memcpyDeviceDevice_float(dst, src, size)

def ndToScalar(indexDims, shapeDims, index, shape):
    return _librapid.ndToScalar(indexDims, shapeDims, index, shape)


def createArray_float(dims, size):
    return _librapid.createArray_float(dims, size)

def createEmptyArray_float(dims, size):
    return _librapid.createEmptyArray_float(dims, size)

def destroyArray_float(arr):
    _librapid.destroyArray_float(arr)


def getDeviceArrVal_float(src):
    return _librapid.getDeviceArrVal_float(src)

def setDeviceArrVal_float(src, val):
    _librapid.setDeviceArrVal_float(src, val)

def getDeviceArrValIndex_float(src, index):
    return _librapid.getDeviceArrValIndex_float(src, index)

def setDeviceArrValIndex_float(src, val, index):
    _librapid.setDeviceArrValIndex_float(src, val, index)

def getSubArray_float(arr, accessDims, index):
    return _librapid.getSubArray_float(arr, accessDims, index)

def setSubArray_float(dst, src, accessDims, index):
    return _librapid.setSubArray_float(dst, src, accessDims, index)

def printArray_float(arr):
    _librapid.printArray_float(arr)

def cudaShutdown():
    _librapid.shutdown()

def syncDeviceThreads():
    _librapid.syncDeviceThreads()

def getCudaError():
    return _librapid.getCudaError()

# Kernels

def ndarrayKernelAdd_float(size, a, b, c):
    _librapid.ndarrayKernelAdd_float(size, a, b, c)

def ndarrayKernelSub_float(size, a, b, c):
    _librapid.ndarrayKernelSub_float(size, a, b, c)

def ndarrayKernelMul_float(size, a, b, c):
    _librapid.ndarrayKernelMul_float(size, a, b, c)

def ndarrayKernelDiv_float(size, a, b, c):
    _librapid.ndarrayKernelDiv_float(size, a, b, c)

def ndarrayKernelAddScalar_float(size, a, b, c):
    _librapid.ndarrayKernelAddScalar_float(size, a, b, c)

def ndarrayKernelSubScalar_float(size, a, b, c):
    _librapid.ndarrayKernelSubScalar_float(size, a, b, c)

def ndarrayKernelMulScalar_float(size, a, b, c):
    _librapid.ndarrayKernelMulScalar_float(size, a, b, c)

def ndarrayKernelDivScalar_float(size, a, b, c):
    _librapid.ndarrayKernelDivScalar_float(size, a, b, c)

def ndarrayKernelScalarFill_float(size, val, data):
    _librapid.ndarrayKernelScalarFill_float(size, val, data)

def ndarrayKernelRandomFill_float(size, min, max, res):
    _librapid.ndarrayKernelRandomFill_float(size, min, max, res)

def ndarrayKernelMapBinary_float(size, a, b):
    _librapid.ndarrayKernelMapBinary_float(size, a, b)

def ndarrayKernelMapSigmoid_float(size, a, b):
    _librapid.ndarrayKernelMapSigmoid_float(size, a, b)

def ndarrayKernelMapTanh_float(size, a, b):
    _librapid.ndarrayKernelMapTanh_float(size, a, b)

def ndarrayKernelMapReLU_float(size, a, b):
    _librapid.ndarrayKernelMapReLU_float(size, a, b)

def ndarrayKernelMapLeakyReLU_float(size, a, b):
    _librapid.ndarrayKernelMapLeakyReLU_float(size, a, b)

def ndarrayKernelMapExp_float(size, a, b):
    _librapid.ndarrayKernelMapExp_float(size, a, b)

def ndarrayKernelMapSigmoidDerivative_float(size, a, b):
    _librapid.ndarrayKernelMapSigmoidDerivative_float(size, a, b)

def ndarrayKernelMapTanhDerivative_float(size, a, b):
    _librapid.ndarrayKernelMapTanhDerivative_float(size, a, b)

def ndarrayKernelMapReLUDerivative_float(size, a, b):
    _librapid.ndarrayKernelMapReLUDerivative_float(size, a, b)

def ndarrayKernelMapLeakyReLUDerivative_float(size, a, b):
    _librapid.ndarrayKernelMapLeakyReLUDerivative_float(size, a, b)

def ndarrayKernelMapExpDerivative_float(size, a, b):
    _librapid.ndarrayKernelMapExpDerivative_float(size, a, b)

def ndarrayKernelSum_float(size, a, res):
    _librapid.ndarrayKernelSum_float(size, a, res)

# Check a given input is valid
def checkData(data, depth):
    length = 0

    if isinstance(data[0], config.ndarray["creationTypes"]):
        length = len(data[0])

    for val in data:
        if type(val) != type(data[0]):
            return False, None
        if isinstance(val, config.ndarray["creationTypes"]):
            if len(val) != length:
                return False, None
            return checkData(val, depth + 1)

    return True, depth

# Convert a 1D list into an array with a given shape
def toArr(data, shape, index):
    if len(shape) == 1:
        res = [data[i] for i in range(index, index + shape[0])]
        index += shape[0]
    else:
        res = []
        tmpIndex = index
        for i in range(shape[0]):
            tmpRes, tmpIndex = toArr(data, shape[1:], tmpIndex)
            res.append(tmpRes)
        index = tmpIndex
   
    return res, index
