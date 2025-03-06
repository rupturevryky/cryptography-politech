import numpy as np


def adjugate_matrix(A):
    if A.shape[0] != A.shape[1]:
        raise ValueError("Матрица должна быть квадратной")

    n = A.shape[0]
    adj_A = np.zeros((n, n))

    for i in range(n):
        for j in range(n):
            minor = np.delete(np.delete(A, i, axis=0), j, axis=1)
            cofactor = ((-1) ** (i + j)) * np.linalg.det(minor)
            adj_A[j, i] = cofactor

    return adj_A


def inverse_matrix(A):
    det_A = np.linalg.det(A)

    if det_A == 0:
        raise ValueError("Матрица необратима (определитель равен 0)")

    adj_A = adjugate_matrix(A)
    inv_A = adj_A / det_A

    return inv_A


def matrix_ym(matrix1, matrix2):
    matrix = []
    for i1 in range(len(matrix1)):
        summ = 0
        for i2 in range(len(matrix2)):
            summ += matrix1[i1][i2] * matrix2[i2]
        matrix.append(round(summ))
    return matrix


def matrix_chifr(crypto_text, key, k=0):
    global n
    alphabet = "абвгдежзийклмнопрстуфхцчшщъыьэюя"
    matrix_d_crypto = []
    crypto_text_encrypt = ''
    if k == 0:
        crypto_text_d = crypto_text.replace(' ', '')
        crypto_text_d = crypto_text_d.replace('.', 'тчк')
        crypto_text_d = crypto_text_d.replace(',', 'зпт')
        if len(crypto_text_d) % len(key) != 0:
            n = (len(key) - len(crypto_text_d) % len(key))
            crypto_text_d += 'ъ' * (len(key) - len(crypto_text_d) % len(key))

        matrix_d = []
        for i in crypto_text_d:
            matrix_d.append(alphabet.index(i) + 1)
        lenght_1 = len(key)
        matrix_d_d = []
        for i in matrix_d:
            if len(matrix_d_d) == lenght_1:
                matrix_d_crypto += matrix_ym(key, matrix_d_d)
                matrix_d_d = []
            matrix_d_d.append(i)
        if len(matrix_d_d) == lenght_1:
            matrix_d_crypto += matrix_ym(key, matrix_d_d)
            matrix_d_d = []
    if k == 1:
        matrix_c = inverse_matrix(np.array(key))
        lenght_1 = len(matrix_c)
        matrix_d_d = []
        for i in crypto_text:
            if len(matrix_d_d) == lenght_1:
                matrix_d_crypto += [alphabet[i1 - 1] for i1 in matrix_ym(matrix_c, matrix_d_d)]
                matrix_d_d = []
            matrix_d_d.append(i)
        if len(matrix_d_d) == lenght_1:
            matrix_d_crypto += [alphabet[i1 - 1] for i1 in matrix_ym(matrix_c, matrix_d_d)]
            matrix_d_d = []
    return matrix_d_crypto



n = 0
input_text = input("введите текст: ").lower()
key_lenght = int(input("введите ключ: "))
matrix_m = []
for i in range(key_lenght):
    m = list(map(int, input().split()))
    matrix_m.append(m)
print("Матричный шифр:")
crypto_encrypto = matrix_chifr(input_text, matrix_m)
print("Зашифрованное сообщение: ", *crypto_encrypto)
crypto_descript = matrix_chifr(crypto_encrypto, matrix_m, k=1)
print("Расшифрованное сообщение: ", ''.join(crypto_descript)[0:len(crypto_descript) - n])
