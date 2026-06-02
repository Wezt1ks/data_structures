import numpy as np
import time
from numba import jit, prange
import scipy.linalg.blas as blas
# 1. Генерация матриц
def generate_matrices(n):
    A = (np.random.randn(n, n).astype(np.float32) +
         1j * np.random.randn(n, n).astype(np.float32))
    B = (np.random.randn(n, n).astype(np.float32) +
         1j * np.random.randn(n, n).astype(np.float32))
    return A, B
# Вариант 1: Наивный алгоритм (Линейная алгебра)
@jit(nopython=True, fastmath=True)
def naive_matmul(A, B):
    n = A.shape[0]
    C = np.zeros((n, n), dtype=np.complex64)
    for i in range(n):
        for k in range(n):
            aik = A[i, k]
            for j in range(n):
                C[i, j] += aik * B[k, j]
    return C

# Вариант 2: Явный вызов cblas_cgemm из BLAS
def blas_matmul(A, B):
    # cgemm — это версия gemm для single precision complex (complex64)
    return blas.cgemm(alpha=1.0, a=A, b=B)

# Вариант 3: Оптимизированный блочный алгоритм, НАПИСАННЫЙ ВАМИ (через Numba)
@jit(nopython=True, fastmath=True, parallel=True)
def block_matmul_optimized(A, B):
    BLOCK_SIZE = 32
    n = A.shape[0]
    C = np.zeros((n, n), dtype=np.complex64)
    num_blocks = n // BLOCK_SIZE  # Количество блоков по одной оси
    # prange идет по сетке блоков со стандартным шагом 1, что полностью устраивает Numba
    for bi in prange(num_blocks):
        i0 = bi * BLOCK_SIZE
        for bk in range(num_blocks):
            k0 = bk * BLOCK_SIZE
            for bj in range(num_blocks):
                j0 = bj * BLOCK_SIZE
                # Локальное перемножение внутри выбранных блоков
                for i in range(i0, i0 + BLOCK_SIZE):
                    for k in range(k0, k0 + BLOCK_SIZE):
                        aik = A[i, k]
                        for j in range(j0, j0 + BLOCK_SIZE):
                            C[i, j] += aik * B[k, j]
    return C

# Измерение производительности
def measure_performance(matmul_func, A, B, name, n, ref_mflops=None):
    c = 2 * (n ** 3)

    _ = matmul_func(A, B)
    time.sleep(0.1)

    start = time.perf_counter()
    C = matmul_func(A, B)
    end = time.perf_counter()

    elapsed = end - start
    mflops = (c / elapsed) * 1e-6

    if ref_mflops is not None:
        rel = (mflops / ref_mflops) * 100
        print(f"{name:35} | Время: {elapsed:.3f} с | MFLOPS: {mflops:.2f} | Отн. BLAS: {rel:.1f}%")
    else:
        print(f"{name:35} | Время: {elapsed:.3f} с | MFLOPS: {mflops:.2f}")

    return elapsed, mflops

def main():
    n = 1024
    print(f"Умножение комплексных матриц {n}×{n}, тип complex64")
    A, B = generate_matrices(n)
    # Вариант 2 (BLAS)
    print("Измерение варианта 2 (cblas_cgemm)...")
    _, ref_mflops = measure_performance(blas_matmul, A, B, "2. BLAS (cblas_cgemm)", n)
    print()
    # Вариант 1 (Наивный)
    print("Измерение варианта 1 (наивный алгоритм)...")
    measure_performance(naive_matmul, A, B, "1. Наивный (Линейная алгебра)", n, ref_mflops=ref_mflops)
    print()
    # Вариант 3 (Блочный ручной)
    print("Измерение варианта 3 (Оптимизированный блочный ручной)...")
    # Для ручного блочного алгоритма на CPU размер блока 64 обычно оптимален
    measure_performance(block_matmul_optimized, A, B, "3. Блочный (собственный)", n,
                        ref_mflops=ref_mflops)
if __name__ == "__main__":
    main()
    print("\nМироненко Егор Сергеевич")
    print("гр: 090301-ПОВа-о25")