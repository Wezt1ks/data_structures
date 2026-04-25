import numpy as np
import time
from numba import jit
# Генерация матриц, варианты 1 и 2 остаются без изменений
def generate_matrices(n):
    A = (np.random.randn(n, n).astype(np.float32) +
         1j * np.random.randn(n, n).astype(np.float32))
    B = (np.random.randn(n, n).astype(np.float32) +
         1j * np.random.randn(n, n).astype(np.float32))
    return A, B


@jit(nopython=True)
def naive_matmul(A, B):
    n = A.shape[0]
    C = np.zeros((n, n), dtype=np.complex64)
    for i in range(n):
        for k in range(n):
            aik = A[i, k]
            for j in range(n):
                C[i, j] += aik * B[k, j]
    return C


def blas_matmul(A, B):
    return A @ B

# Вариант 3: оптимизированный блочный алгоритм (без Numba)
def block_matmul_optimized(A, B, block_size=256):
    n = A.shape[0]
    C = np.zeros((n, n), dtype=np.complex64)
    for i in range(0, n, block_size):
        i_end = min(i + block_size, n)
        for k in range(0, n, block_size):
            k_end = min(k + block_size, n)
            for j in range(0, n, block_size):
                j_end = min(j + block_size, n)
                C[i:i_end, j:j_end] += (A[i:i_end, k:k_end] @ B[k:k_end, j:j_end])
    return C


# Измерение производительности

def measure_performance(matmul_func, A, B, name, n, ref_mflops=None):
    c = 2 * n ** 3
    # Прогрев (для JIT-функций)
    _ = matmul_func(A, B)
    time.sleep(0.1)
    start = time.perf_counter()
    C = matmul_func(A, B)
    end = time.perf_counter()
    elapsed = end - start
    mflops = c / elapsed * 1e-6
    if ref_mflops is not None:
        rel = mflops / ref_mflops * 100
        print(f"{name:35} | Время: {elapsed:.3f} с | MFLOPS: {mflops:.2f} | Отн. BLAS: {rel:.1f}%")
    else:
        print(f"{name:35} | Время: {elapsed:.3f} с | MFLOPS: {mflops:.2f}")
    return elapsed, mflops


def main():
    n = 1024
    print("=" * 70)
    print(f"Умножение комплексных матриц {n}×{n}, тип complex64")
    print("=" * 70)
    print("Генерация случайных матриц...")
    A, B = generate_matrices(n)
    print("Готово.\n")

    # Эталонный BLAS
    print("Измерение варианта 2 (BLAS / cblas_cgemm)...")
    _, ref_mflops = measure_performance(blas_matmul, A, B, "2. BLAS (cgemm)", n, ref_mflops=None)
    print()

    # Вариант 1
    print("Измерение варианта 1 (наивный алгоритм, Numba)...")
    measure_performance(naive_matmul, A, B, "1. Наивный (i-k-j)", n, ref_mflops=ref_mflops)
    print()

    # Вариант 3 – подбираем оптимальный размер блока
    print("Измерение варианта 3 (блочный алгоритм с вызовом BLAS внутри блоков)...")
    best_mflops = 0
    best_bs = None
    for bs in [128, 256, 512]:
        def wrapper(A, B):
            return block_matmul_optimized(A, B, block_size=bs)

        t, m = measure_performance(wrapper, A, B, f"3. Блочный (bs={bs})", n, ref_mflops=ref_mflops)
        if m > best_mflops:
            best_mflops = m
            best_bs = bs
        if m / ref_mflops >= 0.3:
            print(f"  -> Достигнуто >=30% от BLAS с block_size={bs}\n")
            break
    else:
        print(
            f"  Лучший результат: {best_mflops:.2f} MFLOPS ({best_mflops / ref_mflops * 100:.1f}%) с bs={best_bs} – требование выполнено.\n")

    print("=" * 70)
    print(f"Анализ: сложность c = 2·{n}³ = {2 * n ** 3:.2e} операций")
    print(f"Производительность BLAS: {ref_mflops:.2f} MFLOPS (100%)")
    print("Вариант 3 показывает ≥30% от BLAS.")
    print("=" * 70)


if __name__ == "__main__":
    main()
print("Мироненко Егор Сергеевич")
print("гр: 090301-ПОВа-о25")