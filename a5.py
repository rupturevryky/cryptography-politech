def get_r1():
    while True:
        rstr = input("Введите ключ 64 символа 0 и 1: ")
        
        if len(rstr) != 64:
            print("Ключ должен быть 64 символов")
            continue
        
        if not all(char in '01' for char in rstr):
            print("Ключ должен состоять только из 1 и 0")
            continue
        r1 = [0]*19
        r2 = [0]*22
        r3 = [0]*23

        for i in range(64):
            r1t = r1[18]^r1[17]^r1[16]^r1[13]^int(rstr[i]) # xot byte
            r1p = r1[18]
            r1.insert(0,r1t)
            r1.pop(19)

            r2t = r2[21]^r2[20]^int(rstr[i]) # xot byte
            r2p = r2[21]
            r2.insert(0,r2t)
            r2.pop(22)
        
        #work with r3
        
            r3t = r3[22]^r3[21]^r3[20]^r3[7]^int(rstr[i]) # xot byte
            r3p = r3[22]
            r3.insert(0,r3t)
            r3.pop(23)
            
        print(r1)
        print(r2)
        print(r3)

        break
    return r1,r2,r3
        
# ключ 1011111010010100010110101010101110100100101001010101101010101101         

r1, r2, r3 = get_r1()

def gamma(r1,r2,r3):

    for i in range(100):

        F = (r1[8] and r2[10]) or (r1[8]and r3[10]) or (r2[10] and r3[10])

        if r1[8] == F:
            r1t = r1[18]^r1[17]^r1[16]^r1[13] # xot byte
            r1.insert(0,r1t)
            r1.pop(19)

        if r2[10] == F:
            r2t = r2[21]^r2[20] # xot byte
            r2.insert(0,r2t)
            r2.pop(22)

        if r3[10] == F:
            r3t = r3[22]^r3[21]^r3[20]^r3[7] # xot byte
            r3.insert(0,r3t)
            r3.pop(23)

        

    gam = []
        
    for i in range(114):
        F = (r1[8] and r2[10]) or (r1[8]and r3[10]) or (r2[10] and r3[10])

        if r1[8] == F:
            r1t = r1[18]^r1[17]^r1[16]^r1[13] # xot byte
            r1.insert(0,r1t)
            r1.pop(19)

        if r2[10] == F:
            r2t = r2[21]^r2[20] # xot byte
            r2.insert(0,r2t)
            r2.pop(22)

        if r3[10] == F:
            r3t = r3[22]^r3[21]^r3[20]^r3[7] # xot byte
            r3.insert(0,r3t)
            r3.pop(23)

        gam.append(r1[19]^r2[21]^r3[22])

    return gam

r1 =[1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1]

'''
r1 = get_r1()

r2 = get_r2()

r3 = get_r3()

'''

def encrypt_message(message, binary_array):
    encrypted_array = []
    
    for i, char in enumerate(message):
        # Преобразуем символ в его ASCII код и затем в двоичное представление
        ascii_value = ord(char)
        # Выполняем XOR с элементом массива
        xor_result = ascii_value ^ binary_array[i]
        # Добавляем результат в новый массив в двоичном формате
        encrypted_array.append(format(xor_result, '08b'))  # 8-битное представление
        
    return encrypted_array

def decrypt_message(encrypted_array, binary_array):
    decrypted_message = ""
    
    for i, binary_str in enumerate(encrypted_array):
        # Преобразуем двоичную строку в число
        xor_result = int(binary_str, 2)
        # Выполняем XOR с элементом массива обратно, чтобы получить ASCII код
        ascii_value = xor_result ^ binary_array[i]
        # Преобразуем ASCII код обратно в символ и добавляем к результату
        decrypted_message += chr(ascii_value)
        
    return decrypted_message

# Пример использования
message = input("Введите сообщение: ")
binary_array = gamma(r1,r2,r3)
print(binary_array)
# Шифруем сообщение
encrypted = encrypt_message(message, binary_array)
print("Зашифрованное сообщение:", encrypted)

# Расшифровываем сообщение
decrypted = decrypt_message(encrypted, binary_array)
print("Расшифрованное сообщение:", decrypted)

