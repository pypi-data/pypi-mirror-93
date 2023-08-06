#pragma once

#include <cuda.h>
#include <cublas_v2.h>
#include <curand.h>
#include <curand_kernel.h>
#include <cuda_runtime.h>
#include <device_launch_parameters.h>
#include <omp.h>

#include <cstdlib>

#include <iostream>
#include <array>
#include <string>
#include <vector>

#include <random>
#include <chrono>
#include <ctime>

#include <cassert>

#ifndef RAPID_NO_EXPORT
#pragma comment(lib, "cublas.lib")
#endif

#ifndef RAPID_NO_EXPORT
#if defined(_WIN32) || defined(__CYGWIN__)
#define EXPORT __declspec(dllexport)
#else
#define EXPORT __attribute__ ((visibility("default")))
#endif
#else
#define EXPORT
#endif

#define INLINE inline
#define NODISCARD [[nodiscard]]

// Error tracking values
#define NDARRAY_CUBLAS_SUCCESS 1
#define NDARRAY_CUBLAS_NOT_INITIALIZED 2
#define NDARRAY_CUBLAS_ALLOC_FAILED 3
#define NDARRAY_CUBLAS_INVALID_VALUE 4
#define NDARRAY_CUBLAS_ARCH_MISMATCH 5
#define NDARRAY_CUBLAS_MAPPING_ERROR 6
#define NDARRAY_CUBLAS_EXECUTION_FAILED 7
#define NDARRAY_CUBLAS_INTERNAL_ERROR 8
#define NDARRAY_CUBLAS_NOT_SUPPORTED 9
#define NDARRAY_CUBLAS_LICENSE_ERROR 10

// int ndarrayError = 0;

#ifdef CUBLAS_API_H_

// cuBLAS API errors
static const char *HIDDEN_cudaGetErrorEnum(cublasStatus_t error)
{
	switch (error)
	{
		case CUBLAS_STATUS_SUCCESS:
			return "CUBLAS_STATUS_SUCCESS";
		case CUBLAS_STATUS_NOT_INITIALIZED:
			return "CUBLAS_STATUS_NOT_INITIALIZED";
		case CUBLAS_STATUS_ALLOC_FAILED:
			return "CUBLAS_STATUS_ALLOC_FAILED";
		case CUBLAS_STATUS_INVALID_VALUE:
			return "CUBLAS_STATUS_INVALID_VALUE";
		case CUBLAS_STATUS_ARCH_MISMATCH:
			return "CUBLAS_STATUS_ARCH_MISMATCH";
		case CUBLAS_STATUS_MAPPING_ERROR:
			return "CUBLAS_STATUS_MAPPING_ERROR";
		case CUBLAS_STATUS_EXECUTION_FAILED:
			return "CUBLAS_STATUS_EXECUTION_FAILED";
		case CUBLAS_STATUS_INTERNAL_ERROR:
			return "CUBLAS_STATUS_INTERNAL_ERROR";
		case CUBLAS_STATUS_NOT_SUPPORTED:
			return "CUBLAS_STATUS_NOT_SUPPORTED";
		case CUBLAS_STATUS_LICENSE_ERROR:
			return "CUBLAS_STATUS_LICENSE_ERROR";
	}

	return "UNKNOWN ERROR";
}

#endif

inline void HIDDEN_cublasSafeCall(cublasStatus_t err, const char *file, const int line)
{
	if (CUBLAS_STATUS_SUCCESS != err)
	{
		fprintf(stderr, "cuBLAS error in file '%s', line %d\n \nError: %s \nTERMINATING\n", file, line, HIDDEN_cudaGetErrorEnum(err));
		cudaDeviceReset();
		
		exit(1);
		// ndarrayError = 2;
	}
}

#ifndef cublasSafeCall
#define cublasSafeCall(err) HIDDEN_cublasSafeCall(err, __FILE__, __LINE__)
#endif

inline void HIDDEN_cudaSafeCall(cudaError_t err, const char *file, const int line)
{
	if (cudaSuccess != err)
	{
		fprintf(stderr, "CUDA error in file '%s', line %d\n \nError: %s \nTERMINATING\n", file, line, cudaGetErrorString(err));
		cudaDeviceReset();
		
		exit(1);
		// ndarrayError = 1;
	}
}

#ifndef cudaSafeCall
#define cudaSafeCall(err) HIDDEN_cudaSafeCall(err, __FILE__, __LINE__)
#endif

#ifdef __INTELLISENSE__

//    Reverse the bit order of a 32 bit unsigned integer. 
__device__ unsigned int __brev(unsigned int  x)
{};

//Reverse the bit order of a 64 bit unsigned integer.
__device__ unsigned long long int __brevll(unsigned long long int x)
{};


//Return selected bytes from two 32 bit unsigned integers.
__device__ unsigned int __byte_perm(unsigned int  x, unsigned int  y, unsigned int  s)
{};


//Return the number of consecutive high - order zero bits in a 32 bit integer.
__device__ int __clz(int  x)
{};


//Count the number of consecutive high - order zero bits in a 64 bit integer.
__device__ int __clzll(long long int x)
{};


//Find the position of the least significant bit set to 1 in a 32 bit integer.
__device__ int __ffs(int  x)
{};


//Find the position of the least significant bit set to 1 in a 64 bit integer.Concatenate hi : lo, shift left by shift & 31 bits, return the most significant 32 bits.
__device__ int __ffsll(long long int x)
{};


//Concatenate hi : lo, shift left by shift & 31 bits, return the most significant 32 bits.
__device__ unsigned int __funnelshift_l(unsigned int  lo, unsigned int  hi, unsigned int  shift)
{};


//Concatenate hi : lo, shift left by min(shift, 32) bits, return the most significant 32 bits.
__device__ unsigned int __funnelshift_lc(unsigned int  lo, unsigned int  hi, unsigned int  shift)
{};


//Concatenate hi : lo, shift right by shift & 31 bits, return the least significant 32 bits.
__device__ unsigned int __funnelshift_r(unsigned int  lo, unsigned int  hi, unsigned int  shift)
{};


//Concatenate hi : lo, shift right by min(shift, 32) bits, return the least significant 32 bits.
__device__ unsigned int __funnelshift_rc(unsigned int  lo, unsigned int  hi, unsigned int  shift)
{};


//Compute average of signed input arguments, avoiding overflow in the intermediate sum.
__device__ int __hadd(int, int)
{};


//Calculate the least significant 32 bits of the product of the least significant 24 bits of two integers.
__device__ int __mul24(int  x, int  y)
{};


//Calculate the most significant 64 bits of the product of the two 64 bit integers.
__device__ long long int __mul64hi(long long int x, long long int y)
{};


//Calculate the most significant 32 bits of the product of the two 32 bit integers.
__device__ int __mulhi(int  x, int  y)
{};


//Count the number of bits that are set to 1 in a 32 bit integer.
__device__ int __popc(unsigned int  x)
{};


//Count the number of bits that are set to 1 in a 64 bit integer.
__device__ int __popcll(unsigned long long int x)
{};


//Compute rounded average of signed input arguments, avoiding overflow in the intermediate sum.
__device__ int __rhadd(int, int)
{};


//Calculate | x − y | +z, the sum of absolute difference.
__device__ unsigned int __sad(int  x, int  y, unsigned int  z)
{};


//Compute average of unsigned input arguments, avoiding overflow in the intermediate sum.
__device__ unsigned int __uhadd(unsigned int, unsigned int)
{};


//Calculate the least significant 32 bits of the product of the least significant 24 bits of two unsigned integers.
__device__ unsigned int __umul24(unsigned int  x, unsigned int  y)
{};


//Calculate the most significant 64 bits of the product of the two 64 unsigned bit integers.
__device__ unsigned long long int __umul64hi(unsigned long long int x, unsigned long long int y)
{};


//Calculate the most significant 32 bits of the product of the two 32 bit unsigned integers.
__device__ unsigned int __umulhi(unsigned int  x, unsigned int  y)
{};


//Compute rounded average of unsigned input arguments, avoiding overflow in the intermediate sum.
__device__ unsigned int __urhadd(unsigned int, unsigned int)
{};


//Calculate | x − y | +z, the sum of absolute difference.
__device__ unsigned int __usad(unsigned int  x, unsigned int  y, unsigned int  z)
{};

//////////////////////////////////////////////////////
//atomic functions

int atomicAdd(int *address, int val)
{};
unsigned int atomicAdd(unsigned int *address, unsigned int val)
{};
unsigned long long int atomicAdd(unsigned long long int *address, unsigned long long int val)
{};
float atomicAdd(float *address, float val)
{};
double atomicAdd(double *address, double val)
{};

typedef int __half2;
typedef short __half;
__half2 atomicAdd(__half2 *address, __half2 val)
{};
__half atomicAdd(__half *address, __half val)
{};

int atomicSub(int *address, int val)
{};
unsigned int atomicSub(unsigned int *address, unsigned int val)
{};

int atomicExch(int *address, int val)
{};
unsigned int atomicExch(unsigned int *address, unsigned int val)
{};
unsigned long long int atomicExch(unsigned long long int *address, unsigned long long int val)
{};
float atomicExch(float *address, float val)
{};

int atomicMin(int *address, int val)
{};
unsigned int atomicMin(unsigned int *address, unsigned int val)
{};
unsigned long long int atomicMin(unsigned long long int *address, unsigned long long int val)
{};

int atomicMax(int *address, int val)
{};
unsigned int atomicMax(unsigned int *address, unsigned int val)
{};
unsigned long long int atomicMax(unsigned long long int *address, unsigned long long int val)
{};

unsigned int atomicInc(unsigned int *address, unsigned int val)
{};

unsigned int atomicDec(unsigned int *address, unsigned int val)
{};

int atomicCAS(int *address, int compare, int val)
{};
unsigned int atomicCAS(unsigned int *address, unsigned int compare, unsigned int val)
{};
unsigned long long int atomicCAS(unsigned long long int *address,
								 unsigned long long int compare,
								 unsigned long long int val)
{};
unsigned short int atomicCAS(unsigned short int *address,
							 unsigned short int compare,
							 unsigned short int val)
{};

int atomicAnd(int *address, int val)
{};
unsigned int atomicAnd(unsigned int *address,
					   unsigned int val)
{};
unsigned long long int atomicAnd(unsigned long long int *address,
								 unsigned long long int val)
{};

int atomicOr(int *address, int val)
{};
unsigned int atomicOr(unsigned int *address,
					  unsigned int val)
{};
unsigned long long int atomicOr(unsigned long long int *address,
								unsigned long long int val)
{};

int atomicXor(int *address, int val)
{};
unsigned int atomicXor(unsigned int *address, unsigned int val)
{};
unsigned long long int atomicXor(unsigned long long int *address, unsigned long long int val)
{};

template <typename T>
unsigned int __match_any_sync(unsigned mask, T value)
{};
template <typename T>
unsigned int __match_all_sync(unsigned mask, T value, int *pred)
{};

template <typename T>
T __shfl_sync(unsigned mask, T var, int srcLane, int width = warpSize)
{};
template <typename T>
T __shfl_up_sync(unsigned mask, T var, unsigned int delta, int width = warpSize)
{};
template <typename T>
T __shfl_down_sync(unsigned mask, T var, unsigned int delta, int width = warpSize)
{};
template <typename T>
T __shfl_xor_sync(unsigned mask, T var, int laneMask, int width = warpSize)
{};
#endif
