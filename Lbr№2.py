import numpy as np
import time
from numba import jit, prange
import scipy.linalg.blas as blas


# 1. Генерация матриц (тип double / float64)
def generate_matrices(n):
    A = np.random.randn(n, n).astype(np.float64)
    B = np.random.randn(n, n).astype(np.float64)
    return A, B


# Вариант 1: Наивный алгоритм по формуле из линейной алгебры
@jit(nopython=True, fastmath=True)
def naive_matmul(A, B):
    n = A.shape[0]
    C = np.zeros((n, n), dtype=np.float64)
    for i in range(n):
        for k in range(n):
            aik = A[i, k]
            for j in range(n):
                C[i, j] += aik * B[k, j]
    return C


# Вариант 2: Явный вызов cblas_dgemm из библиотеки BLAS
def blas_matmul(A, B):
    return blas.dgemm(alpha=1.0, a=A, b=B)


# Вариант 3: Оптимизированный блочный алгоритм
@jit(nopython=True, fastmath=True, parallel=True)
def block_matmul_optimized(A, B):
    BLOCK_SIZE = 64
    n = A.shape[0]
    C = np.zeros((n, n), dtype=np.float64)
    num_blocks = n // BLOCK_SIZE

    for bi in prange(num_blocks):
        i0 = bi * BLOCK_SIZE
        for bk in range(num_blocks):
            k0 = bk * BLOCK_SIZE
            for bj in range(num_blocks):
                j0 = bj * BLOCK_SIZE
                # Локальное блочное перемножение
                for i in range(i0, i0 + BLOCK_SIZE):
                    for k in range(k0, k0 + BLOCK_SIZE):
                        aik = A[i, k]
                        for j in range(j0, j0 + BLOCK_SIZE):
                            C[i, j] += aik * B[k, j]
    return C


# Измерение производительности
def measure_performance(matmul_func, A, B, name, n, ref_mflops=None):
    c = 2 * (n ** 3)  # Число операций согласно условию

    # Прогрев JIT-компилятора Numba
    _ = matmul_func(A, B)
    time.sleep(0.1)

    start = time.perf_counter()
    C = matmul_func(A, B)
    end = time.perf_counter()

    elapsed = end - start
    mflops = (c / elapsed) * 1e-6  # p = c / t * 10^-6

    if ref_mflops is not None:
        rel = (mflops / ref_mflops) * 100
        print(f"{name:35} | Время: {elapsed:.3f} с | MFLOPS: {mflops:.2f} | Отн. BLAS: {rel:.1f}%")
    else:
        print(f"{name:35} | Время: {elapsed:.3f} с | MFLOPS: {mflops:.2f}")

    return elapsed, mflops


def main():
    n = 1024
    print(f"Умножение матриц {n}×{n}, тип double (float64)")
    A, B = generate_matrices(n)

    # Вариант 2 (BLAS — эталон для сравнения)
    print("Измерение варианта 2 (cblas_dgemm)...")
    _, ref_mflops = measure_performance(blas_matmul, A, B, "2. BLAS (cblas_dgemm)", n)
    print()

    # Вариант 1 (Наивный)
    print("Измерение варианта 1 (наивный алгоритм)...")
    measure_performance(naive_matmul, A, B, "1. Наивный (Линейная алгебра)", n, ref_mflops=ref_mflops)
    print()

    # Вариант 3 (Блочный ручной)
    print("Измерение варианта 3 (Оптимизированный блочный ручной)...")
    measure_performance(block_matmul_optimized, A, B, "3. Блочный (собственный)", n, ref_mflops=ref_mflops)

if __name__ == "__main__":
    main()
    print("\nМироненко Егор Сергеевич")
    print("гр: 090301-ПОВа-о25")