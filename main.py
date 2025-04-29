from Trithemia_Cipher import The_Trithemia_Cipher
from Atbash_Cipher import Atbash_Cipher
from matrix_chifr import matrix_chifr_introduction
from feistel import feistel
from a5 import a5
from kuznechik import kuznechik
from RSA import RSA
from RSA_ds import RSA_ds
from gost_P_34_10_94 import gost_P_34_10_94
from diffie_hellman import diffie_hellman
from gamirovanie_magma import gamma_magma

def main():

    while True:
        print("\n\n\n--------------------------------------------------------\n")
        print("Выберите шифр:")
        print("1. Шифр Атбаш")
        print("2. Шифр Тритемия")
        print("3. Матричный шифр")
        print("4. Шифр Сеть Фейстеля")
        print("5. Гамирование")
        print("6. Шифр А5")
        print("7. Шифр Кузнечек")
        print("8. Шифр RSA")
        print("9. Генерация цифровой подписи RSA")
        print("10. Гост Р 34.10-94")
        print("11. Шифр Диффи-Хеллмана")
        print("12. Выход")
        choice = input("\n\nВведите номер: ")  # Запрашиваем выбор шифра
        
        print("\n\n\n")
        match choice:
            case '1':
                Atbash_Cipher()
            case '2':
                The_Trithemia_Cipher()
            case '3':
                matrix_chifr_introduction()
            case '4':
                feistel()
                # сообщение fedcba9876543210
                # ключ ffeeddccbbaa99887766554433221100f0f1f2f3f4f5f6f7f8f9fafbfcfdfeff
                # хэш 4ee901e5c2d8ca3d
            case '5':
                gamma_magma()
                # сообщ 92def06b3c130a59db54c704f8189d204a98fb2e67a8024c8912409b17b57e41  
                # ключ ffeeddccbbaa99887766554433221100f0f1f2f3f4f5f6f7f8f9fafbfcfdfeff  
                # 12345678
            case '6':
                a5()
                # ключ 1011111010010100010110101010101110100100101001010101101010101101  
            case '7':
                kuznechik()
                # сообщение 1122334455667700ffeeddccbbaa9988
                # ключ 8899aabbccddeeff0011223344556677fedcba98765432100123456789abcdef
            case '8':
                RSA()
            case '9':
                RSA_ds()
            case '10':
                gost_P_34_10_94()
            case '11':
                diffie_hellman()
            case '12':
                print("Всего хорошего!")  
                break

if __name__ == "__main__":
    main()