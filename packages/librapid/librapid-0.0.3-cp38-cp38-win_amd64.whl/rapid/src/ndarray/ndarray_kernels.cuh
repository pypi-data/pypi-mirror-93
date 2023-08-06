#pragma once

#include "../internal.cuh"

namespace kernels
{
	__global__
	void ndarrayKernelAdd_float(long size, const float *a, const float *b, float *res)
	{
		long index = blockIdx.x * blockDim.x + threadIdx.x;
		long stride = blockDim.x * gridDim.x;

		for (long i = index; i < size; i += stride)
		{
			res[i] = a[i] + b[i];
		}
	}

	__global__ void ndarrayKernelSub_float(long size, const float *a, const float *b, float *res)
	{
		long index = blockIdx.x * blockDim.x + threadIdx.x;
		long stride = blockDim.x * gridDim.x;

		for (long i = index; i < size; i += stride)
		{
			res[i] = a[i] - b[i];
		}
	}

	__global__
		void ndarrayKernelMul_float(long size, const float *a, const float *b, float *res)
	{
		long index = blockIdx.x * blockDim.x + threadIdx.x;
		long stride = blockDim.x * gridDim.x;

		for (long i = index; i < size; i += stride)
		{
			res[i] = a[i] * b[i];
		}
	}

	__global__
		void ndarrayKernelDiv_float(long size, const float *a, const float *b, float *res)
	{
		long index = blockIdx.x * blockDim.x + threadIdx.x;
		long stride = blockDim.x * gridDim.x;

		for (long i = index; i < size; i += stride)
		{
			res[i] = a[i] / b[i];
		}
	}

	__global__
		void ndarrayKernelAddScalar_float(long size, const float *a, const float b, float *res)
	{
		long index = blockIdx.x * blockDim.x + threadIdx.x;
		long stride = blockDim.x * gridDim.x;

		for (long i = index; i < size; i += stride)
		{
			res[i] = a[i] + b;
		}
	}

	__global__
		void ndarrayKernelSubScalar_float(long size, const float *a, const float b, float *res)
	{
		long index = blockIdx.x * blockDim.x + threadIdx.x;
		long stride = blockDim.x * gridDim.x;

		for (long i = index; i < size; i += stride)
		{
			res[i] = a[i] - b;
		}
	}

	__global__
		void ndarrayKernelMulScalar_float(long size, const float *a, const float b, float *res)
	{
		long index = blockIdx.x * blockDim.x + threadIdx.x;
		long stride = blockDim.x * gridDim.x;

		for (long i = index; i < size; i += stride)
		{
			res[i] = a[i] * b;
		}
	}

	__global__
		void ndarrayKernelDivScalar_float(long size, const float *a, const float b, float *res)
	{
		long index = blockIdx.x * blockDim.x + threadIdx.x;
		long stride = blockDim.x * gridDim.x;

		for (long i = index; i < size; i += stride)
		{
			res[i] = a[i] / b;
		}
	}

	__global__
		void ndarrayKernelScalarFill_float(long size,
										   const float val,
										   float *data)
	{
		long index = blockIdx.x * blockDim.x + threadIdx.x;
		long stride = blockDim.x * gridDim.x;

		for (long i = index; i < size; i += stride)
		{
			data[i] = val;
		}
	}

	__global__
		void ndarrayKernelRandomFill_float(long size,
										   const float min,
										   const float max,
										   float *data)
	{
		long index = blockIdx.x * blockDim.x + threadIdx.x;
		long stride = blockDim.x * gridDim.x;

		long tId = threadIdx.x + (blockIdx.x * blockDim.x);
		
		static curandState state;
		static int initialized = 0;

		if (initialized == 0) {
			curand_init((unsigned long long) clock() + tId, 0, 0, &state);
			initialized = 1;
		}

		for (long i = index; i < size; i += stride)
		{
			data[i] = min + (curand_uniform(&state) * (max - min));
		}
	}

	__global__
		void ndarrayKernelMapBinary_float(long size, const float *a, float *res)
	{
		long index = blockIdx.x * blockDim.x + threadIdx.x;
		long stride = blockDim.x * gridDim.x;


		for (long i = index; i < size; i += stride)
		{
			res[i] = a[i] > 0 ? 1 : 0;
		}
	}

	__global__
		void ndarrayKernelMapSigmoid_float(long size, const float *a, float *res)
	{
		long index = blockIdx.x * blockDim.x + threadIdx.x;
		long stride = blockDim.x * gridDim.x;

		for (long i = index; i < size; i += stride)
		{
			res[i] = 1 / (1 + exp(-a[i]));
		}
	}

	__global__
		void ndarrayKernelMapTanh_float(long size, const float *a, float *res)
	{
		long index = blockIdx.x * blockDim.x + threadIdx.x;
		long stride = blockDim.x * gridDim.x;

		for (long i = index; i < size; i += stride)
		{
			res[i] = tanh(a[i]);
		}
	}

	__global__
		void ndarrayKernelMapReLU_float(long size, const float *a, float *res)
	{
		long index = blockIdx.x * blockDim.x + threadIdx.x;
		long stride = blockDim.x * gridDim.x;

		for (long i = index; i < size; i += stride)
		{
			res[i] = a[i] > 0 ? a[i] : 0;
		}
	}

	__global__
		void ndarrayKernelMapLeakyReLU_float(long size, const float *a, float *res)
	{
		long index = blockIdx.x * blockDim.x + threadIdx.x;
		long stride = blockDim.x * gridDim.x;

		for (long i = index; i < size; i += stride)
		{
			res[i] = a[i] > 0 ? a[i] : (a[i] * 0.2f);
		}
	}

	__global__
		void ndarrayKernelMapExp_float(long size, const float *a, float *res)
	{
		long index = blockIdx.x * blockDim.x + threadIdx.x;
		long stride = blockDim.x * gridDim.x;

		for (long i = index; i < size; i += stride)
		{
			res[i] = exp(a[i]);
		}
	}

	__global__
		void ndarrayKernelMapSigmoidDerivative_float(long size, const float *a, float *res)
	{
		long index = blockIdx.x * blockDim.x + threadIdx.x;
		long stride = blockDim.x * gridDim.x;

		for (long i = index; i < size; i += stride)
		{
			res[i] = a[i] * (1 - a[i]);
		}
	}

	__global__
		void ndarrayKernelMapTanhDerivative_float(long size, const float *a, float *res)
	{
		long index = blockIdx.x * blockDim.x + threadIdx.x;
		long stride = blockDim.x * gridDim.x;

		for (long i = index; i < size; i += stride)
		{
			res[i] = 1 - a[i] * a[i];
		}
	}

	__global__
		void ndarrayKernelMapReLUDerivative_float(long size, const float *a, float *res)
	{
		long index = blockIdx.x * blockDim.x + threadIdx.x;
		long stride = blockDim.x * gridDim.x;

		for (long i = index; i < size; i += stride)
		{
			res[i] = a[i] > 0 ? 1 : 0;
		}
	}

	__global__
		void ndarrayKernelMapLeakyReLUDerivative_float(long size, const float *a, float *res)
	{
		long index = blockIdx.x * blockDim.x + threadIdx.x;
		long stride = blockDim.x * gridDim.x;

		for (long i = index; i < size; i += stride)
		{
			res[i] = a[i] > 0.f ? 1.f : 0.2f;
		}
	}

	__global__
		void ndarrayKernelMapExpDerivative_float(long size, const float *a, float *res)
	{
		long index = blockIdx.x * blockDim.x + threadIdx.x;
		long stride = blockDim.x * gridDim.x;

		for (long i = index; i < size; i += stride)
		{
			res[i] = exp(a[i]);
		}
	}

	__global__
		void ndarrayKernelSum_float(long size, const float *array, float *result)
	{
		long index = blockIdx.x * blockDim.x + threadIdx.x;
		long stride = blockDim.x * gridDim.x;

		float blockSum = 0;

		for (long i = index; i < size; i += stride)
		{
			blockSum += array[i];
		}

		atomicAdd(result, blockSum);
	}
}

#ifndef RAPID_NO_EXPORT
extern "C" {
#endif

	EXPORT void syncDeviceThreads()
	{
		cudaSafeCall(cudaDeviceSynchronize());
	}

	EXPORT const char *getCudaError() {
		cudaError_t err = cudaGetLastError();
		if (err != cudaSuccess) 
			return (char *) cudaGetErrorString(err);
		return "Success";
	}

	EXPORT void ndarrayKernelAdd_float(const long size, const float *a, const float *b, float *res)
	{
		long blockSize = 256;
		long numBlocks = (size + blockSize - 1) / blockSize;
		kernels::ndarrayKernelAdd_float<< <numBlocks, blockSize >> > (size, a, b, res);
	}

	EXPORT void ndarrayKernelSub_float(const long size, const float *a, const float *b, float *res)
	{
		long blockSize = 256;
		long numBlocks = (size + blockSize - 1) / blockSize;
		kernels::ndarrayKernelSub_float<< <numBlocks, blockSize >> > (size, a, b, res);
	}

	EXPORT void ndarrayKernelMul_float(const long size, const float *a, const float *b, float *res)
	{
		long blockSize = 256;
		long numBlocks = (size + blockSize - 1) / blockSize;
		kernels::ndarrayKernelMul_float<< <numBlocks, blockSize >> > (size, a, b, res);
	}

	EXPORT void ndarrayKernelDiv_float(const long size, const float *a, const float *b, float *res)
	{
		long blockSize = 256;
		long numBlocks = (size + blockSize - 1) / blockSize;
		kernels::ndarrayKernelDiv_float<< <numBlocks, blockSize >> > (size, a, b, res);
	}

	EXPORT void ndarrayKernelAddScalar_float(const long size, const float *a, const float b, float *res)
	{
		long blockSize = 256;
		long numBlocks = (size + blockSize - 1) / blockSize;
		kernels::ndarrayKernelAddScalar_float<< <numBlocks, blockSize >> > (size, a, b, res);
	}

	EXPORT void ndarrayKernelSubScalar_float(const long size, const float *a, const float b, float *res)
	{
		long blockSize = 256;
		long numBlocks = (size + blockSize - 1) / blockSize;
		kernels::ndarrayKernelSubScalar_float<< <numBlocks, blockSize >> > (size, a, b, res);
	}

	EXPORT void ndarrayKernelMulScalar_float(const long size, const float *a, const float b, float *res)
	{
		long blockSize = 256;
		long numBlocks = (size + blockSize - 1) / blockSize;
		kernels::ndarrayKernelMulScalar_float<< <numBlocks, blockSize >> > (size, a, b, res);
	}

	EXPORT void ndarrayKernelDivScalar_float(const long size, const float *a, const float b, float *res)
	{
		long blockSize = 256;
		long numBlocks = (size + blockSize - 1) / blockSize;
		kernels::ndarrayKernelDivScalar_float<< <numBlocks, blockSize >> > (size, a, b, res);
	}

	EXPORT void ndarrayKernelScalarFill_float(const long size, const float val, float *data)
	{
		long blockSize = 256;
		long numBlocks = (size + blockSize - 1) / blockSize;
		kernels::ndarrayKernelScalarFill_float<< <numBlocks, blockSize >> > (size, val, data);
	}

	EXPORT void ndarrayKernelRandomFill_float(const long size, const float min, const float max, float *data)
	{
		long blockSize = 256;
		long numBlocks = (size + blockSize - 1) / blockSize;
		kernels::ndarrayKernelRandomFill_float<< <numBlocks, blockSize >> > (size, min, max, data);
	}

	EXPORT void ndarrayKernelMapBinary_float(const long size, const float *a, float *data)
	{
		long blockSize = 256;
		long numBlocks = (size + blockSize - 1) / blockSize;
		kernels::ndarrayKernelMapBinary_float<< <numBlocks, blockSize >> > (size, a, data);
	}

	EXPORT void ndarrayKernelMapSigmoid_float(const long size, const float *a, float *data)
	{
		long blockSize = 256;
		long numBlocks = (size + blockSize - 1) / blockSize;
		kernels::ndarrayKernelMapSigmoid_float<< <numBlocks, blockSize >> > (size, a, data);
	}

	EXPORT void ndarrayKernelMapTanh_float(const long size, const float *a, float *data)
	{
		long blockSize = 256;
		long numBlocks = (size + blockSize - 1) / blockSize;
		kernels::ndarrayKernelMapTanh_float<< <numBlocks, blockSize >> > (size, a, data);
	}

	EXPORT void ndarrayKernelMapReLU_float(const long size, const float *a, float *data)
	{
		long blockSize = 256;
		long numBlocks = (size + blockSize - 1) / blockSize;
		kernels::ndarrayKernelMapReLU_float<< <numBlocks, blockSize >> > (size, a, data);
	}

	EXPORT void ndarrayKernelMapLeakyReLU_float(const long size, const float *a, float *data)
	{
		long blockSize = 256;
		long numBlocks = (size + blockSize - 1) / blockSize;
		kernels::ndarrayKernelMapLeakyReLU_float<< <numBlocks, blockSize >> > (size, a, data);
	}

	EXPORT void ndarrayKernelMapExp_float(const long size, const float *a, float *data)
	{
		long blockSize = 256;
		long numBlocks = (size + blockSize - 1) / blockSize;
		kernels::ndarrayKernelMapExp_float<< <numBlocks, blockSize >> > (size, a, data);
	}

	EXPORT void ndarrayKernelMapSigmoidDerivative_float(const long size, const float *a, float *data)
	{
		long blockSize = 256;
		long numBlocks = (size + blockSize - 1) / blockSize;
		kernels::ndarrayKernelMapSigmoidDerivative_float<< <numBlocks, blockSize >> > (size, a, data);
	}

	EXPORT void ndarrayKernelMapTanhDerivative_float(const long size, const float *a, float *data)
	{
		long blockSize = 256;
		long numBlocks = (size + blockSize - 1) / blockSize;
		kernels::ndarrayKernelMapTanhDerivative_float<< <numBlocks, blockSize >> > (size, a, data);
	}

	EXPORT void ndarrayKernelMapReLUDerivative_float(const long size, const float *a, float *data)
	{
		long blockSize = 256;
		long numBlocks = (size + blockSize - 1) / blockSize;
		kernels::ndarrayKernelMapReLUDerivative_float<< <numBlocks, blockSize >> > (size, a, data);
	}

	EXPORT void ndarrayKernelMapLeakyReLUDerivative_float(const long size, const float *a, float *data)
	{
		long blockSize = 256;
		long numBlocks = (size + blockSize - 1) / blockSize;
		kernels::ndarrayKernelMapReLU_float<< <numBlocks, blockSize >> > (size, a, data);
	}

	EXPORT void ndarrayKernelMapExpDerivative_float(const long size, const float *a, float *data)
	{
		long blockSize = 256;
		long numBlocks = (size + blockSize - 1) / blockSize;
		kernels::ndarrayKernelMapExpDerivative_float<< <numBlocks, blockSize >> > (size, a, data);
	}

	EXPORT void ndarrayKernelSum_float(const long size, const float *data, float *result)
	{
		long blockSize = 256;
		long numBlocks = (size + blockSize - 1) / blockSize;
		kernels::ndarrayKernelMapExp_float<< <numBlocks, blockSize >> > (size, data, result);
	}

	EXPORT int test() {
		return 123;
	}

#ifndef RAPID_NO_EXPORT
}
#endif
