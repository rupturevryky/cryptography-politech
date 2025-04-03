import random
from typing import Tuple
import math


def extended_gcd(a: int, b: int) -> Tuple[int, int, int]:
    """Расширенный алгоритм Евклида"""
    if a == 0:
        return b, 0, 1

    gcd, x1, y1 = extended_gcd(b % a, a)

    x = y1 - (b // a) * x1
    y = x1

    return gcd, x, y


def modular_inverse(e: int, phi: int) -> int:
    """Нахождение мультипликативной обратной величины"""
    _, x, _ = extended_gcd(e, phi)
    return x % phi


def is_prime(num: int) -> bool:
    """Проверка на простоту"""
    if num < 2:
        return False
    for i in range(2, int(num ** 0.5) + 1):
        if num % i == 0:
            return False
    return True


class RSASignature:
    def __init__(self):
        self.p = None
        self.q = None
        self.n = None
        self.phi = None
        self.public_key = None
        self.private_key = None

    def generate_keys_manual(self, p: int, q: int):
        """Генерация пары ключей из заданных простых чисел"""
        if not (is_prime(p) and is_prime(q)):
            raise ValueError("Оба числа должны быть простыми")
        if p == q:
            raise ValueError("Числа p и q не могут быть равными")

        self.p = p
        self.q = q

        # Вычисление N и φ(N)
        self.n = self.p * self.q
        self.phi = (self.p - 1) * (self.q - 1)

        # Выбор E и вычисление D
        self.public_key = self._generate_public_key()
        self.private_key = self._generate_private_key(self.public_key[1])

        return self.public_key, self.private_key

    def _generate_public_key(self) -> Tuple[int, int]:
        """Генерация открытого ключа"""
        e = random.randint(2, self.phi - 1)
        while math.gcd(e, self.phi) != 1:
            e = random.randint(2, self.phi - 1)
        return (self.n, e)

    def _generate_private_key(self, e: int) -> int:
        """Генерация закрытого ключа"""
        return modular_inverse(e, self.phi)

    def hash_quadratic(self, message: str, mod: int) -> int:
        """Вычисление хэша методом квадратичной свертки"""
        h = 0
        print(f"Промежуточные значения хэша:")
        for char in message:
            h = (h + ord(char)) ** 2 % mod
            print(f"После символа '{char}': {h}")
        return h

    def sign_message(self, message: str) -> int:
        """Создание цифровой подписи"""
        print("\nШаг 1: Создание подписи")
        print("------------------------")

        # Вычисление хэша
        hash_value = self.hash_quadratic(message, self.n)
        print(f"\nХэш при создании подписи: {hash_value}")

        # Создание подписи
        signature = pow(hash_value, self.private_key, self.n)
        return signature

    def verify_signature(self, message: str, signature: int) -> bool:
        """Проверка цифровой подписи"""
        print("\nШаг 2: Проверка подписи")
        print("------------------------")

        # Вычисление хэша для проверки
        hash_value = self.hash_quadratic(message, self.n)
        print(f"\nХэш при проверке подписи: {hash_value}")

        # Проверка подписи
        recovered_hash = pow(signature, self.public_key[1], self.n)
        print(f"Восстановленный хэш из подписи: {recovered_hash}")

        return hash_value == recovered_hash


# Пример использования
rsa = RSASignature()

try:
    # Получаем простые числа от пользователя
    p = int(input("Введите первое простое число p: "))
    q = int(input("Введите второе простое число q: "))

    # Генерируем ключи с использованием введенных чисел
    print("\nГенерация пары ключей...")
    public_key, private_key = rsa.generate_keys_manual(p, q)

    print(f"\nОткрытый ключ (n, e): {public_key}")
    print(f"Закрытый ключ (d): {private_key}")

    # Получаем сообщение для подписи
    message = input("\nВведите сообщение для подписи: ")

    # Создание подписи
    signature = rsa.sign_message(message)
    print(f"\nСоздана подпись: {signature}")

    # Проверка подписи
    is_valid = rsa.verify_signature(message, signature)
    print(f"\nПроверка подписи для исходного сообщения: {is_valid}")

except ValueError as e:
    print(f"\nОшибка: {str(e)}")
except Exception as e:
    print(f"\nПроизошла ошибка: {str(e)}")