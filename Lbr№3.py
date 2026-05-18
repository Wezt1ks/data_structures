import time
import random
from collections import deque

# Информация об авторе (замените на свои данные)
def print_author():
    print("Автор: Мироненко Егор Сергеевич")
    print("Группа: 090301-ПОВа-о25")
    print("Лабораторная работа №3")
    print("Тема: Стек. Замена на следующий больший элемент")

# ---------- 1. Стек на массиве (динамический) ----------
class ArrayStack:
    def __init__(self, initial_capacity=16):
        self._data = [None] * initial_capacity
        self._size = 0
        self._capacity = initial_capacity

    def _resize(self, new_capacity):
        new_data = [None] * new_capacity
        for i in range(self._size):
            new_data[i] = self._data[i]
        self._data = new_data
        self._capacity = new_capacity

    def push(self, value):
        if self._size == self._capacity:
            self._resize(2 * self._capacity)
        self._data[self._size] = value
        self._size += 1

    def pop(self):
        if self.is_empty():
            raise IndexError("pop from empty stack")
        self._size -= 1
        return self._data[self._size]

    def peek(self):
        if self.is_empty():
            raise IndexError("peek from empty stack")
        return self._data[self._size - 1]

    def is_empty(self):
        return self._size == 0

# ---------- 2. Стек на связном списке ----------
class Node:
    def __init__(self, value):
        self.value = value
        self.next = None

class LinkedListStack:
    def __init__(self):
        self._head = None

    def push(self, value):
        new_node = Node(value)
        new_node.next = self._head
        self._head = new_node

    def pop(self):
        if self.is_empty():
            raise IndexError("pop from empty stack")
        value = self._head.value
        self._head = self._head.next
        return value

    def peek(self):
        if self.is_empty():
            raise IndexError("peek from empty stack")
        return self._head.value

    def is_empty(self):
        return self._head is None

# ---------- 3. Стек через стандартную библиотеку (deque) ----------
class DequeStack:
    def __init__(self):
        self._deque = deque()

    def push(self, value):
        self._deque.append(value)

    def pop(self):
        if self.is_empty():
            raise IndexError("pop from empty stack")
        return self._deque.pop()

    def peek(self):
        if self.is_empty():
            raise IndexError("peek from empty stack")
        return self._deque[-1]

    def is_empty(self):
        return len(self._deque) == 0

# ---------- Алгоритм замены на следующий больший элемент ----------
def next_greater_element(arr, stack):
    """
    Возвращает новый список, где каждый элемент заменён на ближайший следующий
    больший элемент (справа). Использует переданный стек (любой реализации).
    """
    n = len(arr)
    result = [0] * n
    # Идём справа налево
    for i in range(n - 1, -1, -1):
        # Удаляем из стека элементы, не большие текущего
        while not stack.is_empty() and stack.peek() <= arr[i]:
            stack.pop()
        # Если стек не пуст, верхушка – искомый элемент
        if not stack.is_empty():
            result[i] = stack.peek()
        else:
            result[i] = 0
        # Помещаем текущий элемент в стек
        stack.push(arr[i])
    return result

# ---------- Тестирование на примере из задания ----------
def test_example():
    print("\n--- Проверка на примере из задания ---")
    A = [1, 3, 2, 5, 3, 4]
    expected = [3, 5, 5, 0, 4, 0]

    print("Исходный массив:", A)
    print("Ожидаемый ответ:", expected)

    # Проверяем все три реализации
    for name, StackClass in [("Стек на массиве", ArrayStack),
                             ("Стек на связном списке", LinkedListStack),
                             ("стек через collections.deque", DequeStack)]:
        stack = StackClass()
        result = next_greater_element(A, stack)
        print(f"{name:18} -> {result}  {'✅' if result == expected else '❌'}")

# ---------- Сравнение производительности ----------
def performance_test(size=100000, runs=5):
    print(f"\n--- Сравнение производительности (размер массива = {size}, прогонов = {runs}) ---")
    # Генерируем случайный массив
    random.seed(42)
    test_array = [random.randint(0, 10000) for _ in range(size)]

    results = {}
    for name, StackClass in [("Стек на массиве", ArrayStack),
                             ("Стек на связном списке", LinkedListStack),
                             ("стек через collections.deque", DequeStack)]:
        times = []
        for _ in range(runs):
            stack = StackClass()
            start = time.perf_counter()
            _ = next_greater_element(test_array, stack)
            end = time.perf_counter()
            times.append(end - start)
        avg_time = sum(times) / runs
        results[name] = avg_time
        print(f"{name:18} : среднее {avg_time:.6f} сек")

    # Определяем самого быстрого
    fastest = min(results, key=results.get)
    print(f"\nСамая быстрая реализация: {fastest} ({results[fastest]:.6f} сек)")

def main():
    print_author()
    test_example()
    performance_test()

if __name__ == "__main__":
    main()