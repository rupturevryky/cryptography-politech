def trithemius_encrypt(text):
    result = ""
    shift = 0
    
    for char in text.upper():
        # Пропуск пробелов
        if not char.isalpha():
            result += char
            continue
            
        # Находим позицию буквы в алфавите (A=0, B=1, ..., Я=31)
        pos = ord(char) - ord('А')
        
        # Вычисляем новый сдвиг
        new_pos = (pos + shift) % 32
        
        # Получаем зашифрованную букву
        encrypted_char = chr(new_pos + ord('А'))
        
        result += encrypted_char
        shift = (shift + 1) % 32
    
    return result

def trithemius_decrypt(text):
    result = ""
    shift = 0
    
    for char in text.upper():
        # Пропуск пробелов
        if not char.isalpha():
            result += char
            continue
            
        # Находим позицию буквы в алфавите
        pos = ord(char) - ord('А')
        
        # Вычисляем обратный сдвиг
        new_pos = (pos - shift + 32) % 32
        
        # Получаем расшифрованную букву
        decrypted_char = chr(new_pos + ord('А'))
        
        result += decrypted_char
        shift = (shift + 1) % 32
    
    return result

def main():
    while True:
        print("\nШифр Тритемия")
        print("1. Зашифровать текст")
        print("2. Расшифровать текст")
        print("3. Выход")
        
        choice = input("Выберите действие (1-3): ")
        
        if choice == '3':
            break
            
        text = input("Введите текст: ")
        
        if choice == '1':
            encrypted = trithemius_encrypt(text)
            print(f"Зашифрованный текст: {encrypted}")
        elif choice == '2':
            decrypted = trithemius_decrypt(text)
            print(f"Расшифрованный текст: {decrypted}")
        else:
            print("Неверный выбор")

if __name__ == "__main__":
    main()