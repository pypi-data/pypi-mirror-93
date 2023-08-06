import warnings
import ctypes as ct
import math

from rapid import config, utils
from rapid.ndarray import backend, pretty_print

def array(data):
   return ndarray(data=data)

class ndarray:
    def __init__(self, **kwargs):
        self.array = None

        if "data" in kwargs:
        # Parse from a python list
         
        # Create temporary copy for improved speed
            tmpData = tuple(kwargs["data"])
         
            valid, depth = backend.checkData(tmpData, 1)

            if not valid:
                raise ValueError("Invalid data for array creation")

            shape = []
            current = tmpData
            for _ in range(depth):
                shape.append(len(current))
                current = current[0]

            self.array = backend._librapid.createArray_float(len(shape), (ct.c_long * len(shape))(*shape))

            flattened = utils.flatten(tmpData)
            backend.memcpyHostDevice_float(self.array.dataStart, (ct.c_float * len(flattened))(*flattened), len(flattened))

        if "shape" in kwargs:
            # Create array from shape
            shape = tuple(kwargs["shape"])
            self.array = backend._librapid.createArray_float(len(shape), (ct.c_long * len(shape))(*shape))

    def __del__(self):
        backend._librapid.destroyArray_float(self.array)

    def shape(self, axis=None):
        if axis is not None:
            if axis >= 0 and axis < self.array.dims:
                return self.array.shape[axis]
            raise IndexError("Index {} is out of range for array with {} dimensions".format(axis, self.array.dims))
        return [self.array.shape[i] for i in range(self.array.dims)]

    def pyArr(self):
        host = (ct.c_float * math.prod(self.shape()))(*[0 for _ in range(math.prod(self.shape()))])
        backend.memcpyDeviceHost_float(host, self.array.dataStart, math.prod(self.shape()))

        res, _ = backend.toArr(host, self.shape(), 0)
        return res

    def __iter__(self):
        for i in range(self.shape(axis=0)):
            yield self[i]

    def __getitem__(self, index):
        if (index >= self.shape()[0]):
             raise ValueError("array subscript {} out of range for array of width {}".format(index, self.shape()[0]))

        if not isinstance(index, int):
            raise ValueError("array subscript must be of type int")

        # Check if should return a scalar
        if len(self.shape()) == 1:
            return backend.getDeviceArrValIndex_float(self.array.dataStart, index)
        else:
            res = ndarray()
            res.array = backend.getSubArray_float(self.array, 1, (ct.c_long * 1)(*[index]))
            return res

    def __setitem__(self, index, val):
        if (index >= self.shape()[0]):
            raise ValueError("array subscript {} out of range for array of width {}".format(index, self.shape()[0]))

        if not isinstance(index, int):
            raise ValueError("array subscript must be of type int")

        if len(self.shape()) == 1:
            backend.setDeviceArrValIndex_float(self.array.dataStart, ct.c_float(val), index)
        else:
            val.array = backend.setSubArray_float(self.array, val.array, 1, (ct.c_long * 1)(*[index]))

    def toString(self, **kwargs):
        host = (ct.c_float * math.prod(self.shape()))(*[0 for _ in range(math.prod(self.shape()))])
        backend.memcpyDeviceHost_float(host, self.array.dataStart, math.prod(self.shape()))
        processed = list(host)

        depth = 1
        prefix = ""
        postfix = ""
        if "isRepr" in kwargs:
            prefix = "rapid.ndarray("
            postfix = ", dtype=float32)"
            depth = len(prefix)

        return prefix + pretty_print.arrayToString(processed, self.shape(), "float32", depth + 1) + postfix

    def __str__(self):
        return self.toString()

    def __repr__(self):
        return self.toString(isRepr=True)

    def __add__(self, other):
        if not isinstance(other, (ndarray, int, float)):
            raise TypeError("Cannot add rapid.ndarray and {}".format(type(other)))

        if isinstance(other, ndarray):
            if self.shape() != other.shape():
                raise ValueError("Incompatible shapes {} and {}. Arrays must be the same size to perform addition".format(self.shape(), other.shape()))

        res = ndarray(shape=self.shape())
        if isinstance(other, ndarray):
            backend.ndarrayKernelAdd_float(math.prod(self.shape()), self.array.dataStart, other.array.dataStart, res.array.dataStart)
        else:
            backend.ndarrayKernelAddScalar_float(math.prod(self.shape()), self.array.dataStart, ct.c_float(other), res.array.dataStart)
        backend.syncDeviceThreads()

        return res

    def __sub__(self, other):
        if not isinstance(other, (ndarray, int, float)):
            raise TypeError("Cannot add rapid.ndarray and {}".format(type(other)))

        if isinstance(other, ndarray):
            if self.shape() != other.shape():
                raise ValueError("Incompatible shapes {} and {}. Arrays must be the same size to perform subtraction".format(self.shape(), other.shape()))

        res = ndarray(shape=self.shape())
        if isinstance(other, ndarray):
            backend.ndarrayKernelSub_float(math.prod(self.shape()), self.array.dataStart, other.array.dataStart, res.array.dataStart)
        else:
            backend.ndarrayKernelSubScalar_float(math.prod(self.shape()), self.array.dataStart, ct.c_float(other), res.array.dataStart)   
        backend.syncDeviceThreads()

        return res

    def __mul__(self, other):
        if not isinstance(other, (ndarray, int, float)):
            raise TypeError("Cannot add rapid.ndarray and {}".format(type(other)))

        if isinstance(other, ndarray):
            if self.shape() != other.shape():
                raise ValueError("Incompatible shapes {} and {}. Arrays must be the same size to perform multiplication".format(self.shape(), other.shape()))

        res = ndarray(shape=self.shape())
        if isinstance(other, ndarray):
            backend.ndarrayKernelMul_float(math.prod(self.shape()), self.array.dataStart, other.array.dataStart, res.array.dataStart)
        else:
            backend.ndarrayKernelMulScalar_float(math.prod(self.shape()), self.array.dataStart, ct.c_float(other), res.array.dataStart)
        backend.syncDeviceThreads()

        return res

    def __truediv__(self, other):
        if not isinstance(other, (ndarray, int, float)):
            raise TypeError("Cannot add rapid.ndarray and {}".format(type(other)))

        if isinstance(other, ndarray):
            if self.shape() != other.shape():
                raise ValueError("Incompatible shapes {} and {}. Arrays must be the same size to perform division".format(self.shape(), other.shape()))

        res = ndarray(shape=self.shape())
        if isinstance(other, ndarray):
            backend.ndarrayKernelDiv_float(math.prod(self.shape()), self.array.dataStart, other.array.dataStart, res.array.dataStart)
        else:
            backend.ndarrayKernelDivScalar_float(math.prod(self.shape()), self.array.dataStart, ct.c_float(other), res.array.dataStart)
        backend.syncDeviceThreads()

        return res

    def __floordiv__(self, other):
        warnings.warn("Floored division is not supported by rapid.ndarray -- using true division instead")
        return self / other

    def __iadd__(self, other):
        if not isinstance(other, (ndarray, int, float)):
            raise TypeError("Cannot add rapid.ndarray and {}".format(type(other)))

        if isinstance(other, ndarray):
            if self.shape() != other.shape():
                raise ValueError("Incompatible shapes {} and {}. Arrays must be the same size to perform addition".format(self.shape(), other.shape()))

        if isinstance(other, ndarray):
            backend.ndarrayKernelAdd_float(math.prod(self.shape()), self.array.dataStart, other.array.dataStart, self.array.dataStart)
        else:
            backend.ndarrayKernelAddScalar_float(math.prod(self.shape()), self.array.dataStart, ct.c_float(other), self.array.dataStart)
        backend.syncDeviceThreads()

        return self

    def __isub__(self, other):
        if not isinstance(other, (ndarray, int, float)):
            raise TypeError("Cannot add rapid.ndarray and {}".format(type(other)))

        if isinstance(other, ndarray):
            if self.shape() != other.shape():
                raise ValueError("Incompatible shapes {} and {}. Arrays must be the same size to perform subtraction".format(self.shape(), other.shape()))

        if isinstance(other, ndarray):
            backend.ndarrayKernelSub_float(math.prod(self.shape()), self.array.dataStart, other.array.dataStart, self.array.dataStart)
        else:
            backend.ndarrayKernelSubScalar_float(math.prod(self.shape()), self.array.dataStart, ct.c_float(other), self.array.dataStart)   
        backend.syncDeviceThreads()

        return self

    def __imul__(self, other):
        if not isinstance(other, (ndarray, int, float)):
            raise TypeError("Cannot add rapid.ndarray and {}".format(type(other)))

        if isinstance(other, ndarray):
            if self.shape() != other.shape():
                raise ValueError("Incompatible shapes {} and {}. Arrays must be the same size to perform multiplication".format(self.shape(), other.shape()))

        if isinstance(other, ndarray):
            backend.ndarrayKernelMul_float(math.prod(self.shape()), self.array.dataStart, other.array.dataStart, self.array.dataStart)
        else:
            backend.ndarrayKernelMulScalar_float(math.prod(self.shape()), self.array.dataStart, ct.c_float(other), self.array.dataStart)
        backend.syncDeviceThreads()

        return self

    def __itruediv__(self, other):
        if not isinstance(other, (ndarray, int, float)):
            raise TypeError("Cannot add rapid.ndarray and {}".format(type(other)))

        if isinstance(other, ndarray):
            if self.shape() != other.shape():
                raise ValueError("Incompatible shapes {} and {}. Arrays must be the same size to perform division".format(self.shape(), other.shape()))

        if isinstance(other, ndarray):
            backend.ndarrayKernelDiv_float(math.prod(self.shape()), self.array.dataStart, other.array.dataStart, self.array.dataStart)
        else:
            backend.ndarrayKernelDivScalar_float(math.prod(self.shape()), self.array.dataStart, ct.c_float(other), self.array.dataStart)
        backend.syncDeviceThreads()

        return self

    def __ifloordiv__(self, other):
        warnings.warn("Floored division is not supported by rapid.ndarray -- using true division instead")
        return self / other


# Functions

def sigmoid(x):
    if isinstance(x, ndarray):
        res = ndarray(shape=x.shape())
        backend.ndarrayKernelMapSigmoid_float(math.prod(x.shape()), x.array.dataStart, res.array.dataStart)
        return res
    
    return 1 / (1 + math.exp(-x))

def tanh(x):
    if isinstance(x, ndarray):
        res = ndarray(shape=x.shape())
        backend.ndarrayKernelMapTanh_float(math.prod(x.shape()), x.array.dataStart, res.array.dataStart)
        return res
    
    return math.tanh(x)

def relu(x):
    if isinstance(x, ndarray):
        res = ndarray(shape=x.shape())
        backend.ndarrayKernelMapReLU_float(math.prod(x.shape()), x.array.dataStart, res.array.dataStart)
        return res
    
    return x if x > 0 else 0

def leakyRelu(x):
    if isinstance(x, ndarray):
        res = ndarray(shape=x.shape())
        backend.ndarrayKernelMapLeakyReLU_float(math.prod(x.shape()), x.array.dataStart, res.array.dataStart)
        return res
    
    return x if x > 0 else x * 0.2

def dSigmoid(y):
    if isinstance(y, ndarray):
        res = ndarray(shape=y.shape())
        backend.ndarrayKernelMapSigmoidDerivative_float(math.prod(y.shape()), y.array.dataStart, res.array.dataStart)
        return res
    
    return 1 / (1 + math.exp(-y))

def dTanh(y):
    if isinstance(y, ndarray):
        res = ndarray(shape=y.shape())
        backend.ndarrayKernelMapTanhDerivative_float(math.prod(y.shape()), y.array.dataStart, res.array.dataStart)
        return res
    
    return y * (1 - y)

def dRelu(y):
    if isinstance(y, ndarray):
        res = ndarray(shape=y.shape())
        backend.ndarrayKernelMapReLUDerivative_float(math.prod(y.shape()), y.array.dataStart, res.array.dataStart)
        return res
    
    return 1 if y > 0 else 0

def dLeakyRelu(y):
    if isinstance(y, ndarray):
        res = ndarray(shape=y.shape())
        backend.ndarrayKernelMapLeakyReLUDerivative_float(math.prod(y.shape()), y.array.dataStart, res.array.dataStart)
        return res
    
    return 1 if y > 0 else 0.2
