# -*- coding: utf8 -*-
alf = 'абвгдежзийклмнопрстуфхцчшщъыьэюя'

def textToNumbers(text):
    res = []
    for i in range(len(text)):
        res.append(alf.find(text[i])+1)
    return res
def tchk_zpt(n): #Замена символов на буквы
    n = n.replace('.','тчк')
    n = n.replace(',','зпт')
    n = n.lower()
    return n
def hesh(text, module):
    text = textToNumbers(text)
    iters = [0]
    for i in range(len(text)):
        iters.append(((iters[i] + text[i])**2)%module)
    return iters[len(text)]
def is_prime(n):
    flag = 0
    for i in range(2, int(n**(0.5))):
        if n%i == 0:
            flag = 1
    if flag == 1: return False
    else: return True
def check_params(p, q, a, x = 2):
    if not is_prime(p):
        print('Неверное p, введите еще раз, оно должно быть простым')
        return False
    if not is_prime(q) and (p - 1) % q != 0:
        print(f'Неверное q, введите еще раз, оно должно быть простым сомножителем{p-1}')
        return False
    if a <= 1 and a >= (p - 1) and (a ** q) % p != 1:
        print(f'Неверное а, введите еще раз, оно должно быть таким, что 1 < a <{p-1} и (a^{q}) mod {p} = 1')
        return False
    if  x >= q or x <= 1:
         print(f'Неверное x, введите еще раз, оно должно быть меньше {q} и больше 1')
         return False
    return True
def generate_signature(text, p, q, a, x, k):
    res = []
    y = (a**x)%p
    r = ((a**k)%p)%q
    if text%q == 0:
        text = 1
    s = (x*r + k*text)%q
    res.append(r)
    res.append(s)
    return f'Подпись: {res}, Y = {y}'
def check_signature(text, r, s, p, q, a, y):
    res = ''
    v = (text**(q-2))%q
    z1 = (s*v)%q
    z2 = ((q-r)*v)%q
    u = (((a**z1)*(y**z2))%p)%q
    if (u==r):
        res += 'Подпись верна, u = r = '
        res += str(u)
    else:
        res += 'Подпись неверна, u = '
        res += str(u)
        res += 'r = '
        res += str(r)
    return res

def main():
    print("ЭЦП ГОСТ Р 34.10-94")
    what_to_do = int(input('Что делать? (подписать - 1, проверить подпись  - 2):'))
    if what_to_do == 1:
        text = str(input("Введите открытый текст: "))
        while True:
            p = int(input("Введите большое простое p: "))
            print('Возможный вариант для q: ')
            counter = 0
            for i in range(3, 100):
                if ((p - 1) % i == 0):
                    print(i)
                    counter += 1
                    if counter == 5:
                        break
            q = int(input(f"Введите простое q, являющееся сомножителем числа {p-1}: "))
            print('Возможный вариант для a: ')
            counter = 0
            for i in range(2, p-1):
                if (i**q)%p == 1:
                    print(i)
                    counter += 1
                    if counter == 5:
                        break
            a = int(input(f"Введите такое а, что 1 < a < {p-1} и (a^{q}) mod {p} = 1: "))
            x = int(input(f"Введите 1 < x < {q}: "))
            if  check_params(p, q, a, x):
                break
        print(f'Открытые параметры: p = {p}, q = {q}, a = {a}')
        while True:
            k = int(input(f"Введите случайное число k, при этом k < {q}: "))
            if k>=q:
                print(f"Неверное k, введите еще раз, оно должно быть меньше {q}")
            elif (((a**k)%p)%q == 0):
                print(f"r = 0, выберите другое k")
            else:
                break
        print(f'Число k = {k}')
        n = int(input("Введите модуль для хэширования n: "))
        text = hesh(tchk_zpt(text), n)
        print(f'Хэш-образ = {text}')
        print("Подпись: ", generate_signature(text, p, q, a, x, k))
    elif what_to_do == 2:
            text = input("Введите сообщение: ")
            while True:
                p = int(input("Введите большое простое p: "))
                q = int(input(f"Введите простое q, являющееся сомножителем числа {p-1}: "))
                a = int(input("Введите а: "))
                if  check_params(p, q, a):
                    break
            y = int(input("Введите открытый ключ Y: "))
            n = int(input("Введите модуль для хэширования n: "))
            text = hesh(tchk_zpt(text), n)
            print(f'Хэш-образ = {text}')
            r = int(input("Введите r (первый параметр подписи): "))
            s = int(input("Введите s (второй параметр подписи): "))
            print(check_signature(text, r, s, p, q, a, y))

main()
"""
Что делать? (подписать - 1, проверить подпись  - 2):1
Введите открытый текст: невсекотумасленицазптбудетивеликийпосттчк
Введите большое простое p: 47
Возможный вариант для q: 
23
46
Введите простое q, являющееся сомножителем числа 46: 23
Возможный вариант для a: 
2
3
4
6
7
Введите такое а, что 1 < a < 46 и (a^23) mod 47 = 1: 3
Введите x < 23: 2
Открытые параметры: p = 47, q = 23, a = 3
Введите случайное число k, при этом k < 23: 3
Число k = 3
Введите модуль для хэширования n: 47
Хэш-образ = 3
Подпись:  Подпись: [4, 17], Y = 9

Что делать? (подписать - 1, проверить подпись  - 2):2
Введите сообщение: выпущенное слово и камень не имеют возврата.
Введите большое простое p: 47
Введите простое q, являющееся сомножителем числа 46: 23
Введите а: 3
Введите открытый ключ Y: 9
Введите модуль для хэширования n: 47
Хэш-образ = 3
Введите r (первый параметр подписи): 4
Введите s (второй параметр подписи): 17
Подпись верна, u = r = 4
"""

###