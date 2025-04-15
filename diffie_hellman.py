def compute_public_key(a, private_key, n):
    """Вычисление открытого ключа."""
    return pow(a, private_key, n)


def compute_shared_secret(public_key, private_key, n):
    """Вычисление общего секретного ключа."""
    return pow(public_key, private_key, n)


def validate_keys(a, n, Ka, Kb, Ya, Yb, shared_secret_A, shared_secret_B):
    """Проверка всех условий для ключей."""
    errors = []

    # Проверка на равенство 1
    if Ya == 1 or Yb == 1:
        errors.append("Открытые ключи не могут быть равны 1")
    if shared_secret_A == 1 or shared_secret_B == 1:
        errors.append("Секретные ключи не могут быть равны 1")

    # Проверка совпадения открытых ключей
    if Ya == Yb:
        errors.append("Открытые ключи не должны совпадать")

    # Проверка совпадения секретных ключей с открытыми
    if shared_secret_A == Ya or shared_secret_A == Yb:
        errors.append("Секретный ключ не должен совпадать с открытыми ключами")
    if shared_secret_B == Ya or shared_secret_B == Yb:
        errors.append("Секретный ключ не должен совпадать с открытыми ключами")

    # Проверка совпадения секретных ключей между собой
    if shared_secret_A != shared_secret_B:
        errors.append("Секретные ключи не совпадают между собой")

    return errors


def main():
    # Ввод параметров
    while True:
        try:
            n = int(input("Введите простое число n (n > 2): "))
            if n <= 2:
                print("Ошибка: n должно быть простым числом > 2!")
                continue
            break
        except ValueError:
            print("Ошибка: введите целое число!")

    while True:
        try:
            a = int(input(f"Введите базу a (1 < a < {n}): "))
            if a <= 1 or a >= n:
                print(f"Ошибка: a должно быть в диапазоне (1, {n})!")
                continue
            break
        except ValueError:
            print("Ошибка: введите целое число!")

    while True:
        try:
            Ka = int(input(f"Введите секретный ключ Ka (1 < Ka < {n - 1}): "))
            if Ka <= 1 or Ka >= n - 1:
                print(f"Ошибка: Ka должно быть в диапазоне (1, {n - 1})!")
                continue
            break
        except ValueError:
            print("Ошибка: введите целое число!")

    while True:
        try:
            Kb = int(input(f"Введите секретный ключ Kb (1 < Kb < {n - 1} и Kb != {Ka}): "))
            if Kb <= 1 or Kb >= n - 1:
                print(f"Ошибка: Kb должно быть в диапазоне (1, {n - 1})!")
                continue
            if Kb == Ka:
                print("Ошибка: Kb не должно быть равно Ka!")
                continue
            break
        except ValueError:
            print("Ошибка: введите целое число!")

    # Вычисление ключей
    Ya = compute_public_key(a, Ka, n)
    Yb = compute_public_key(a, Kb, n)
    shared_secret_A = compute_shared_secret(Yb, Ka, n)
    shared_secret_B = compute_shared_secret(Ya, Kb, n)

    print(f"\nОткрытый ключ Ya: {Ya}")
    print(f"Открытый ключ Yb: {Yb}")
    print(f"\nСекретный ключ у A: {shared_secret_A}")
    print(f"Секретный ключ у B: {shared_secret_B}")

    # Проверка всех условий
    errors = validate_keys(a, n, Ka, Kb, Ya, Yb, shared_secret_A, shared_secret_B)

    if errors:
        print("\nОшибки в ключах:")
        for error in errors:
            print(f"- {error}")
        print("\nРекомендации: измените значения a, Ka или Kb")
    else:
        print("\nПроверка пройдена успешно!")
        print(f"Общий секретный ключ: {shared_secret_A}")


if __name__ == "__main__":
    main()