from termcolor import colored
from typing import List

table = [
    [1, 7, 14, 13, 0, 5, 8, 3, 4, 15, 10, 6, 9, 12, 11, 2],
    [8, 14, 2, 5, 6, 9, 1, 12, 15, 4, 11, 0, 13, 10, 3, 7],
    [5, 13, 15, 6, 9, 2, 12, 10, 11, 7, 8, 1, 4, 3, 14, 0],
    [7, 15, 5, 10, 8, 1, 6, 13, 0, 9, 3, 14, 11, 4, 2, 12],
    [12, 8, 2, 1, 13, 4, 15, 6, 7, 0, 10, 5, 3, 14, 9, 11],
    [11, 3, 5, 8, 2, 15, 10, 13, 14, 1, 7, 4, 12, 9, 6, 0],
    [6, 8, 2, 3, 9, 10, 5, 12, 1, 14, 4, 7, 11, 13, 0, 15],
    [12, 4, 6, 2, 10, 5, 11, 9, 14, 8, 13, 7, 0, 3, 15, 1]
]


def split_key(key: str) -> List[str]:
    """Split key in 32 parts:param key: str:return: List[arr]"""
    return [key[i:i + 8] for j in range(3) for i in range(0, len(key), 8)] + [(key)[::-1][i:i + 8][::-1] for i in
                                                                              range(0, len(key), 8)]


def t(a: str) -> str:
    """Perform t permutation (S-table):param a::return: str"""
    return ''.join([hex(table[index][int(i, 16)])[2:] for index, i in enumerate(a)])


def cyclic_shift_left(value: int, shift: int, bits=32):
    """Perform cycle shift_lift:param value: int:param shift: int:param bits: int (default: 32):return:"""
    return ((value << shift % bits) & ((1 << bits) - 1) | (value >> (bits - shift % bits))) & ((1 << bits) - 1)


def g(key: str, a: str) -> str:
    """Perform g-permutation:param key: str:param a: str:return: str"""
    return hex(cyclic_shift_left(int(t(hex((int(key, 16) + int(a, 16)) % 2 ** 32)[2:].zfill(8)), 16), 11))[2:]


def G(a1, a0, key) -> str:
    return hex(int(g(key, a0), 16) ^ int(a1, 16))[2:]


class KeyError(Exception):
    pass


def check_params(input: str, key: str):
    try:
        tmp = int(input, 16)
        tmp = int(input, 16)
        assert len(input) == 16
        assert len(key) == 64
    except Exception as _:
        raise KeyError("Неправильные входные параметры")


def encrypt(message: str, keys: List[str]) -> str:
    """Encrypt message on feistel network:param message: str:param keys: str:return: str"""
    a1, a0 = message[0:8], message[8:]
    cnt = 0
    for index, key in enumerate(keys):
        a1, a0 = a0, G(a1, a0, key)
        cnt += 1
    return a0 + a1


def to_hex(input: str) -> str:
    try:
        return hex(int(input, 16))[2:]
    except Exception as _:
        return input.encode('utf-8').hex()


def gamma_magma():
    if input("Вы вводите сообщение в hex? Y/N: ") == "Y":
        message = input("Введите сообщение: ")
    else:
        message = input("Введите сообщение: ")
        message = to_hex(message)

    key = input("Введите ключ: ")
    IV = input("Введите инициализирующий вектор: ")
    while len(IV) <= 16:
        IV += '0'
    keys = split_key(key)

    print("Результаты шифрования:")
    for i in range(len(message) // 16):
        p_i = message[i * 16:(i + 1) * 16]

        print(f"P_{i + 1} = {p_i}")
        print(f"Входной блок = {IV}")

        ek = encrypt(IV, keys)
        print(f"Выходной блок = {ek}")

        c_i = hex(int(ek, 16) ^ int(p_i, 16))[2:]  ###
        print(f"C_{i + 1} = {c_i}")

        IV = hex(int(IV, 16) + 1)[2:]
        print()

    if len(message) % 16 != 0:
        p_i = message[-(len(message) % 16):].ljust(16, '0')
        print(f"P_{len(message) // 16 + 1} = {p_i}")
        print(f"Входной блок = {IV}")

        ek = encrypt(IV, keys)
        print(f"Выходной блок = {ek}")

        c_i = hex(int(ek, 16) ^ int(p_i, 16))[2:].zfill(16)
        print(f"C_{len(message) // 16 + 1} = {c_i}")
        print()


if __name__ == "__main__":
    gamma_magma()

# 92def06b3c130a59db54c704f8189d204a98fb2e67a8024c8912409b17b57e41  сообщ
# ffeeddccbbaa99887766554433221100f0f1f2f3f4f5f6f7f8f9fafbfcfdfeff  ключ
# 12345678
