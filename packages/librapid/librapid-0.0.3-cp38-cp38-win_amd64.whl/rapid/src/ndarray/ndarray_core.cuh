#pragma once

#include "../internal.cuh"

#ifndef RAPID_NO_EXPORT
extern "C" {
#endif

	EXPORT int getError_ndarray()
	{
		return 0; // ndarrayError;
	}

	// The core ndarray type
	EXPORT struct ndarray_float
	{
		float *dataStart;		// The array's memory
		float *dataOrigin;		// The origin of the array's memory
		long *originReferences; // Number of objects that have access to the memory origin
		long *shape;				// The shape of the array (rows, cols, depth ...)
		long dims;				// Dimensionality of the array (0D, 1D, 2D, 3D ...)
	};

	// Shutdown CUDA before exiting the program
	EXPORT void shutdown()
	{
		cudaDeviceReset();
	}

	// Allocate a float array on the device
	EXPORT float *allocateDeviceMemory_float(const long length)
	{
		float *res;
		cudaSafeCall(cudaMalloc(&res, sizeof(float) * length));
		return res;
	}

	// Free memory on the device
	EXPORT void freeDeviceMemory_float(float *data)
	{
		cudaSafeCall(cudaFree(data));
	}

	// Copy memory from host to device
	EXPORT void memcpyHostDevice_float(float *dst, const float *src, const long size)
	{
		cudaSafeCall(cudaMemcpy(dst, src, sizeof(float) * size, cudaMemcpyHostToDevice));
	}

	// Copy memory from device to host
	EXPORT void memcpyDeviceHost_float(float *dst, const float *src, const long size)
	{
		cudaSafeCall(cudaMemcpy(dst, src, sizeof(float) * size, cudaMemcpyDeviceToHost));
	}

	// Copy memory from device to device
	EXPORT void memcpyDeviceDevice_float(float *dst, const float *src, const long size)
	{
		cudaSafeCall(cudaMemcpy(dst, src, sizeof(float) * size, cudaMemcpyDeviceToDevice));
	}

	// Set a value in a device array to a particular value
	EXPORT void setDeviceArrVal_float(float *dst, const float val)
	{
		memcpyHostDevice_float(dst, &val, 1);
	}

	// Set a value in a device array to a particular value
	EXPORT void setDeviceArrValIndex_float(float *dst, const float val, const long index)
	{
		memcpyHostDevice_float(dst + index, &val, 1);
	}

	// Set a value in a device array to a particular value
	EXPORT float getDeviceArrVal_float(const float *src)
	{
		float res;
		memcpyDeviceHost_float(&res, src, 1);
		return res;
	}

	// Set a value in a device array to a particular value
	EXPORT float getDeviceArrValIndex_float(const float *src, const long index)
	{
		return getDeviceArrVal_float(src + index);
	}

	// Convert an n-dimensional index to a single scalar position
	EXPORT long ndToScalar(const long iDims, const long sDims, const long *index, const long *shape)
	{
		long sig = 1;
		long pos = 0;

		for (long i = sDims - 1; i >= 0; i--)
		{
			pos += (i < iDims ? index[i] : 0) * sig;
			sig *= shape[i];
		}

		return pos;
	}

	// Create an ndarray object
	EXPORT ndarray_float createArray_float(const long dims, const long *shape)
	{
		long totalSize = 1;
		for (long i = 0; i < dims; i++)
			totalSize *= shape[i];

		auto resData = allocateDeviceMemory_float(totalSize);
		auto originData = resData;

		long *originReferences = new long;
		*originReferences = 1;

		auto resSize = new long[dims];
		memcpy(resSize, shape, sizeof(long) * dims);

		return ndarray_float{
			resData,
			originData,
			originReferences,
			resSize,
			dims
		};
	}

	// Create an empty ndarray object from a given shape
	EXPORT ndarray_float createEmptyArray_float(const long dims, const long *shape)
	{
		auto resSize = new long[dims];
		memcpy(resSize, shape, sizeof(long) * dims);

		return ndarray_float{
			nullptr,
			nullptr,
			nullptr,
			resSize,
			dims
		};
	}

	// Create an ndarray object
	EXPORT void destroyArray_float(ndarray_float arr)
	{
		// Decrement memory counter
		(*arr.originReferences)--;

		// Conditionally free origin data
		if (*arr.originReferences == 0)
		{
			// Free origin data
			freeDeviceMemory_float(arr.dataOrigin);
			delete arr.originReferences;
		}

		// Free shape
		delete[] arr.shape;
	}

	// Access a sub-array of a larger one
	EXPORT ndarray_float getSubArray_float(const ndarray_float arr, const long accessDims, const long *index)
	{
		auto resDims = arr.dims - accessDims;
		auto resShape = new long[resDims];

		for (long i = 0; i < resDims; i++)
			resShape[i] = arr.shape[i + accessDims];

		auto res = createEmptyArray_float(resDims, resShape);

		(*arr.originReferences)++;
		res.dataOrigin = arr.dataOrigin;
		res.dataStart = arr.dataStart + ndToScalar(accessDims, arr.dims, index, arr.shape);
		res.originReferences = arr.originReferences;

		return res;
	}

	// Access a sub-array of a larger one
	EXPORT ndarray_float setSubArray_float(ndarray_float dst, ndarray_float src, const long accessDims, const long *index)
	{
		auto res = createEmptyArray_float(src.dims, src.shape);

		// Copy data from src to dst
		long prod = 1;
		for (long i = 0; i < src.dims; i++)
			prod *= src.shape[i];

		memcpyDeviceDevice_float(dst.dataStart + ndToScalar(accessDims, dst.dims, index, dst.shape), src.dataStart, prod);

		// Destroy src array and replace it
		destroyArray_float(src);

		(*dst.originReferences)++;
		res.dataOrigin = dst.dataOrigin;
		res.dataStart = dst.dataStart + ndToScalar(accessDims, dst.dims, index, dst.shape);
		res.originReferences = dst.originReferences;

		return res;
	}

	EXPORT void printArray_float(const ndarray_float arr)
	{
		long end = 1;
		for (long i = 0; i < arr.dims; i++)
			end *= arr.shape[i];

		auto host = new float[end];
		memcpyDeviceHost_float(host, arr.dataStart, end);

		if (host != nullptr)
			for (long i = 0; i < end; i++)
				std::cout << host[i] << ", ";
		std::cout << "\n";

		delete[] host;
	}

#ifndef RAPID_NO_EXPORT
}
#endif
