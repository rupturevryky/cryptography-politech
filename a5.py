import sys

class A5_1:
    MASK_R1 = (1 << 19) - 1
    MASK_R2 = (1 << 22) - 1
    MASK_R3 = (1 << 23) - 1

    R1_CLK = 8
    R2_CLK = 10
    R3_CLK = 10

    def __init__(self, key=0, frame=0):
        self.R1 = 0
        self.R2 = 0
        self.R3 = 0
        self.initialize(key, frame)

    def majority_bit(self, x, y, z):
        return (x & y) | (x & z) | (y & z)

    def clock_lfsr(self, reg, mask, feedback_taps):
        feedback = reg & feedback_taps
        new_bit = 0
        while feedback:
            new_bit ^= (feedback & 1)
            feedback >>= 1
        reg = ((reg << 1) & mask) | new_bit
        return reg

    def initialize(self, key, frame=0):
        for i in range(64):
            key_bit = (key >> i) & 1
            self.R1 ^= key_bit
            self.R2 ^= key_bit
            self.R3 ^= key_bit
            self.R1 = self.clock_lfsr(self.R1, self.MASK_R1, (1 << 18) | (1 << 17) | (1 << 16) | (1 << 13))
            self.R2 = self.clock_lfsr(self.R2, self.MASK_R2, (1 << 21) | (1 << 20))
            self.R3 = self.clock_lfsr(self.R3, self.MASK_R3, (1 << 22) | (1 << 21) | (1 << 20) | (1 << 7))

        for i in range(22):
            frame_bit = (frame >> i) & 1
            self.R1 ^= frame_bit
            self.R2 ^= frame_bit
            self.R3 ^= frame_bit
            self.R1 = self.clock_lfsr(self.R1, self.MASK_R1, (1 << 18) | (1 << 17) | (1 << 16) | (1 << 13))
            self.R2 = self.clock_lfsr(self.R2, self.MASK_R2, (1 << 21) | (1 << 20))
            self.R3 = self.clock_lfsr(self.R3, self.MASK_R3, (1 << 22) | (1 << 21) | (1 << 20) | (1 << 7))

        for _ in range(100):
            b1 = (self.R1 >> self.R1_CLK) & 1
            b2 = (self.R2 >> self.R2_CLK) & 1
            b3 = (self.R3 >> self.R3_CLK) & 1
            maj = self.majority_bit(b1, b2, b3)

            if b1 == maj:
                self.R1 = self.clock_lfsr(self.R1, self.MASK_R1, (1 << 18) | (1 << 17) | (1 << 16) | (1 << 13))
            if b2 == maj:
                self.R2 = self.clock_lfsr(self.R2, self.MASK_R2, (1 << 21) | (1 << 20))
            if b3 == maj:
                self.R3 = self.clock_lfsr(self.R3, self.MASK_R3, (1 << 22) | (1 << 21) | (1 << 20) | (1 << 7))

    def get_keystream_bit(self):
        b1 = (self.R1 >> self.R1_CLK) & 1
        b2 = (self.R2 >> self.R2_CLK) & 1
        b3 = (self.R3 >> self.R3_CLK) & 1
        maj = self.majority_bit(b1, b2, b3)

        if b1 == maj:
            self.R1 = self.clock_lfsr(self.R1, self.MASK_R1, (1 << 18) | (1 << 17) | (1 << 16) | (1 << 13))
        if b2 == maj:
            self.R2 = self.clock_lfsr(self.R2, self.MASK_R2, (1 << 21) | (1 << 20))
        if b3 == maj:
            self.R3 = self.clock_lfsr(self.R3, self.MASK_R3, (1 << 22) | (1 << 21) | (1 << 20) | (1 << 7))

        return (self.R1 >> 18) ^ (self.R2 >> 21) ^ (self.R3 >> 22) & 1

    def encrypt_byte(self, byte):
        result = 0
        for bit_index in range(7, -1, -1):
            keystream_bit = self.get_keystream_bit()
            result |= ((byte >> bit_index) & 1) ^ keystream_bit << bit_index
        return result


class A5_2:
    MASK_R1 = (1 << 19) - 1
    MASK_R2 = (1 << 22) - 1
    MASK_R3 = (1 << 23) - 1
    MASK_R4 = (1 << 17) - 1

    R4_CLK1 = 3
    R4_CLK2 = 7
    R4_CLK3 = 10

    def __init__(self, key=0, frame=0):
        self.R1 = self.R2 = self.R3 = self.R4 = 0
        self.last_output_bit = 0
        self.initialize(key, frame)

    def majority_bit(self, x, y, z):
        return (x & y) | (x & z) | (y & z)

    def clock_lfsr(self, reg, mask, feedback_taps):
        feedback = reg & feedback_taps
        new_bit = 0
        while feedback:
            new_bit ^= (feedback & 1)
            feedback >>= 1
        reg = ((reg << 1) & mask) | new_bit
        return reg



    def initialize(self, key, frame=0):
        for i in range(64):
            key_bit = (key >> i) & 1
            self.R1 ^= key_bit
            self.R2 ^= key_bit
            self.R3 ^= key_bit
            self.R4 ^= key_bit
            self.R1 = self.clock_lfsr(self.R1, self.MASK_R1, (1 << 18) | (1 << 17) | (1 << 16) | (1 << 13))
            self.R2 = self.clock_lfsr(self.R2, self.MASK_R2, (1 << 21) | (1 << 20))
            self.R3 = self.clock_lfsr(self.R3, self.MASK_R3, (1 << 22) | (1 << 21) | (1 << 20) | (1 << 7))
            self.R4 = self.clock_lfsr(self.R4, self.MASK_R4, (1 << 16) | (1 << 11))

        for i in range(22):
            frame_bit = (frame >> i) & 1
            self.R1 ^= frame_bit
            self.R2 ^= frame_bit
            self.R3 ^= frame_bit
            self.R4 ^= frame_bit
            self.R1 = self.clock_lfsr(self.R1, self.MASK_R1, (1 << 18) | (1 << 17) | (1 << 16) | (1 << 13))
            self.R2 = self.clock_lfsr(self.R2, self.MASK_R2, (1 << 21) | (1 << 20))
            self.R3 = self.clock_lfsr(self.R3, self.MASK_R3, (1 << 22) | (1 << 21) | (1 << 20) | (1 << 7))
            self.R4 = self.clock_lfsr(self.R4, self.MASK_R4, (1 << 16) | (1 << 11))

        for _ in range(99):
            self.R4 = self.clock_lfsr(self.R4, self.MASK_R4, (1 << 16) | (1 << 11))
            x = (self.R4 >> self.R4_CLK1) & 1
            y = (self.R4 >> self.R4_CLK2) & 1
            z = (self.R4 >> self.R4_CLK3) & 1
            maj = self.majority_bit(x, y, z)

            if ((self.R4 >> self.R4_CLK3) & 1) == maj:
                self.R1 = self.clock_lfsr(self.R1, self.MASK_R1, (1 << 18) | (1 << 17) | (1 << 16) | (1 << 13))
            if ((self.R4 >> self.R4_CLK1) & 1) == maj:
                self.R2 = self.clock_lfsr(self.R2, self.MASK_R2, (1 << 21) | (1 << 20))
            if ((self.R4 >> self.R4_CLK2) & 1) == maj:
                self.R3 = self.clock_lfsr(self.R3, self.MASK_R3, (1 << 22) | (1 << 21) | (1 << 20) | (1 << 7))

        self.last_output_bit = 0

    def get_keystream_bit(self):
        self.R4 = self.clock_lfsr(self.R4, self.MASK_R4, (1 << 16) | (1 << 11))
        x = (self.R4 >> self.R4_CLK1) & 1
        y = (self.R4 >> self.R4_CLK2) & 1
        z = (self.R4 >> self.R4_CLK3) & 1
        maj = self.majority_bit(x, y, z)

        if ((self.R4 >> self.R4_CLK3) & 1) == maj:
            self.R1 = self.clock_lfsr(self.R1, self.MASK_R1, (1 << 18) | (1 << 17) | (1 << 16) | (1 << 13))
        if ((self.R4 >> self.R4_CLK1) & 1) == maj:
            self.R2 = self.clock_lfsr(self.R2, self.MASK_R2, (1 << 21) | (1 << 20))
        if ((self.R4 >> self.R4_CLK2) & 1) == maj:
            self.R3 = self.clock_lfsr(self.R3, self.MASK_R3, (1 << 22) | (1 << 21) | (1 << 20) | (1 << 7))

        topR1 = (self.R1 >> 18) & 1
        topR2 = (self.R2 >> 21) & 1
        topR3 = (self.R3 >> 22) & 1

        b1_R1 = (self.R1 >> 15) & 1
        b2_R1 = (self.R1 >> 14) & 1
        b3_R1 = (self.R1 >> 12) & 1
        majR1 = self.majority_bit(b1_R1, b2_R1 ^ 1, b3_R1)

        b1_R2 = (self.R2 >> 16) & 1
        b2_R2 = (self.R2 >> 13) & 1
        b3_R2 = (self.R2 >> 9) & 1
        majR2 = self.majority_bit(b1_R2 ^ 1, b2_R2, b3_R2)

        b1_R3 = (self.R3 >> 18) & 1
        b2_R3 = (self.R3 >> 16) & 1
        b3_R3 = (self.R3 >> 13) & 1
        majR3 = self.majority_bit(b1_R3, b2_R3, b3_R3 ^ 1)

        new_output = topR1 ^ topR2 ^ topR3 ^ majR1 ^ majR2 ^ majR3

        output_bit = self.last_output_bit
        self.last_output_bit = new_output
        return output_bit

    def encrypt_byte(self, byte):
        result = 0
        for bit_index in range(7, -1, -1):
            keystream_bit = self.get_keystream_bit()
            result |= ((byte >> bit_index) & 1) ^ keystream_bit << bit_index
        return result



def bin_to_letters(bin_str, rus_alphabet):
    result = []
    for i in range(0, len(bin_str), 5):
        chunk = bin_str[i:i + 5]
        index = int(chunk, 2)
        if index < len(rus_alphabet):
            result.append(rus_alphabet[index])
        else:
            result.append('?')
    return ''.join(result)


def a5():
    print("Введите сообщение:")
    test_data = input()

    print("Введите ключ (64-битное число в двоичном формате):")
    key_binary = input().strip()
    key = int(key_binary, 2)

    frame = 0

    algos = [
        {"name": "A5/1", "type": 1},
        {"name": "A5/2", "type": 2}
    ]

    rus_alphabet = "АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"

    for algo in algos:
        print("Тестирование алгоритма {}...".format(algo["name"]))

        letter_bin = ""
        for ch in test_data:
            pos = rus_alphabet.find(ch)
            if pos != -1:
                bits = format(pos, '05b')
                letter_bin += bits

        gamma = ""
        if algo["type"] == 1:
            cipher = A5_1(key, frame)
        else:
            cipher = A5_2(key, frame)

        for _ in letter_bin:
            bit = cipher.get_keystream_bit()
            gamma += str(bit)

        xor_result = ''.join('0' if letter_bin[i] == gamma[i] else '1' for i in range(len(letter_bin)))

        cipher_text = bin_to_letters(xor_result, rus_alphabet)

        decrypted_bin = ''.join('0' if xor_result[i] == gamma[i] else '1' for i in range(len(xor_result)))
        decrypted_text = bin_to_letters(decrypted_bin, rus_alphabet)

        print("Исходный текст:                        {}".format(test_data))
        print("Бинарное представление букв:           {}".format(letter_bin))
        print("Гамма:                                 {}".format(gamma))
        print("Результат XOR (бинарный):              {}".format(xor_result))
        print("Результат XOR (буквенный, шифротекст): {}".format(cipher_text))
        print("Расшифрованный текст (бинарный):       {}".format(decrypted_bin))
        print("Расшифрованный текст (буквенный):      {}".format(decrypted_text))
        print()



#1010101010101010101010101010101010101010101010101010101010101010
