import math
import random


def is_prime(n):
    if n < 2:
        return False
    for p in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31]:
        if n % p == 0:
            return n == p
    d = n - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for a in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31]:
        if a >= n:
            continue
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True


def encrypt(text, n, e):
    alha = 'абвгдежзийклмнопрстуфхцчшщъыьэюя'
    text = text.replace(',', 'зпт').replace('.', 'тчк').replace(' ', '')
    message = ''
    for i in text:
        if i not in alha:
            raise ValueError(f"Символ '{i}' не найден в алфавите")
        index1 = alha.index(i) + 1
        num = pow(index1, e, n)
        message += '0' * (2 - len(str(num))) + str(num)
    return message


def phi(p, q):
    return (p - 1) * (q - 1)


def modinv(e, phi):
    g, x, y = extended_gcd(e, phi)
    if g != 1:
        raise Exception('Обратный элемент не существует')
    else:
        return x % phi


def extended_gcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = extended_gcd(b % a, a)
        return (g, x - (b // a) * y, y)


def des(text, p, q, e):
    alha = 'абвгдежзийклмнопрстуфхцчшщъыьэюя'
    n = p * q
    phi_n = phi(p, q)
    d = modinv(e, phi_n)
    message = ''
    for i in range(0, len(text), 2):
        c = int(text[i:i + 2])
        m = pow(c, d, n)
        if m < 1 or m > len(alha):
            raise ValueError(f"Некорректное значение при дешифровке: {m}")
        message += alha[m - 1]
    return message


def get_prime_input(prompt, min_n=0):
    while True:
        try:
            num = int(input(prompt))
            if not is_prime(num):
                print("Число должно быть простым!")
                continue
            if min_n > 0 and num < min_n:
                print(f"Число должно быть не меньше {min_n}")
                continue
            return num
        except ValueError:
            print("Пожалуйста, введите целое число.")


def get_e_input(phi_n):
    while True:
        try:
            e = int(input(f"Введите e (1 < e < {phi_n}, взаимно простое с {phi_n}): "))
            if e <= 1 or e >= phi_n:
                print(f"e должно быть в диапазоне 1 < e < {phi_n}")
                continue
            if math.gcd(e, phi_n) != 1:
                print(f"e должно быть взаимно простым с {phi_n}")
                continue
            return e
        except ValueError:
            print("Пожалуйста, введите целое число.")


def main():
    # Ввод простых чисел с проверкой минимального произведения
    while True:
        p = get_prime_input("Введите первое простое число p (минимум 3): ", 3)
        q = get_prime_input("Введите второе простое число q (минимум 3): ", 3)

        if p == q:
            print("p и q должны быть разными простыми числами!")
            continue

        n = p * q
        if n < 33:
            print(f"Произведение p*q = {n} должно быть не менее 33!")
            print("Пожалуйста, выберите большие простые числа.")
            continue

        break

    phi_n = phi(p, q)

    print(f"\nВычисленные параметры:")
    print(f"N = p * q = {p} * {q} = {n}")
    print(f"φ(N) = (p-1)*(q-1) = {phi_n}")

    # Ввод e с проверками
    print("\nВыберите открытую экспоненту e:")
    e = get_e_input(phi_n)

    # Вычисление d
    try:
        d = modinv(e, phi_n)
        if d == e:
            print("Секретная экспонента d не должна быть равна открытой экспоненте e.")
            print("Пожалуйста, выберите другое значение для e.")
            return
        print(f"\nСекретная экспонента d = {d}")
    except Exception:
        print("Не удалось вычислить обратный элемент для e")
        return

    # Ввод текста
    text = input("\nВведите текст для шифрования: ").lower()

    try:
        # Шифрование
        encrypted = encrypt(text, n, e)
        print("\nЗашифрованный текст:", encrypted)

        # Дешифрование
        decrypted = des(encrypted, p, q, e)
        print("Расшифрованный текст:", decrypted)
    except Exception as e:
        print("Ошибка:", str(e))


if __name__ == "__main__":
    main()
