import math

num_a = int(input('Введите число переменной a '))
num_b = int(input('Введите число переменной b '))
num_c = int(input('Введите число переменной c '))

d = (num_b*num_b)-4*num_a*num_c

if d > 0:
    a1 = (-num_b - math.sqrt(d)) / (2 * num_a)
    a2 = (-num_b + math.sqrt(d)) / (2 * num_a)
    print(f"Ответ: a1 = {a1}, a2 = {a2}")
if d == 0:
    a1 = -num_b / (2 * num_a)
    print(f"Ответ: a1 = {a1}")
if d < 0:
    print("Ответ: нет")