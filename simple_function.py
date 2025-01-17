from collections import deque

""" Вопрос №1. Способ из примера."""
def isEven(value):
    return value % 2 == 0

# Интуитивно понятный и простой способ.
def isEven2(value):
    return not value % 2

# Быстрый, но менее читабельный способ.
def isEven3(value):
    return value & 1 == 0

"""
Вопрос №2. Буфер в основе которого лежит список.
Простая на вид реализация с исп. фиксированного списка.
Требуется контроль над head и tail.
"""
class Buffer_list:
    def __init__(self, capacity):
        self.buffer = [None] * capacity
        self.capacity = capacity
        self.head = 0
        self.tail = 0
        self.size = 0

    def push(self, value):
        if self.size == self.capacity:
            raise OverflowError('Буфер полон')
        self.buffer[self.tail] = value
        self.tail = (self.tail +1) % self.capacity
        self.size += 1

    def pop(self):
        if self.size == 0:
            raise IndexError('Буфер пуст')
        value = self.buffer[self.head]
        self.head = (self.head +1) % self.capacity
        self.size -= 1
        return value

    def __repr__(self):
        return str(self.buffer)

"""
Буфер на основе импортируемого deque.
Встроенный deque, который автоматически управляет началом и концом.
Он ещё проще предыдущего буфера, но меньше контроля за внутренним процессом.
"""

class Buffer_deque:
    def __init__(self, capacity):
        self.buffer = deque(maxlen=capacity)

    def push(self, value):
        if len(self.buffer) == self.buffer.maxlen:
            raise OverflowError('Буфер полон')
        self.buffer.append(value)

    def pop(self):
        if not self.buffer:
            raise IndexError('Буфер пуст')
        return self.buffer.popleft()

    def __repr__(self):
        return str(list(self.buffer))

# Пример выполнения 1:
buffer_list = Buffer_list(5)
buffer_list.push(1)
buffer_list.push(2)
buffer_list.push(3)
print(buffer_list)  # [1, 2, 3, None, None]
print(buffer_list.pop())  # 1
print(buffer_list)  # [1, 2, 3, None, None]

# Пример выполнения 2:
buffer_deque = Buffer_deque(5)
buffer_deque.push(1)
buffer_deque.push(2)
buffer_deque.push(3)
print(buffer_deque)  # [1, 2, 3]
print(buffer_deque.pop())  # 1
print(buffer_deque)  # [2, 3]

"""
Вопрос №3. Быстрая и простая сортировка массива чисел через встроенную.
функцию sorted(). Из плюсов стоит выделить простоту, но при объёмных массивах
может не хватить памяти, а так же нет полноты возможностей для "кастомизации" функции.
"""
def sort(not_sorted): # Определение функции
    return sorted(not_sorted)

not_sorted = [5, 1, 7, 2, 4, 3, 6, 8] # Задаём импровизированный список
sorted = sort(not_sorted)
print(sorted) # Пример выполнения