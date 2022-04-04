"""Оригинал"""
import random

"""
Выполняет алгоритм Евклида и возвращает НОД(a,b).
"""
#вычисление
def gcd(a, b): #явный вход
    if (b == 0):
        return a #явный выход
    else:
        return gcd(b, a % b) 

""" 
Выполняет расширенный алгоритм Евклида.
Возвращает НОД, коэф. a и  коэф. b.
"""
#вычисление
def xgcd(a, b): #явный вход
    x, cof_a = 0, 1
    y, cof_b = 1, 0

    while (b != 0):
        quotient = a // b
        a, b = b, a - quotient * b
        cof_a, x = x, cof_a - quotient * x #неявный выход
        cof_b, y = y, cof_b - quotient * y #неявный выход

    return a, cof_a, cof_b #явный выход

"""
Выбирает случайное число, 1 < e < phi(n) (значение функции Эйлера), и проверяет, соответствует ли оно
взаимно простым c phi(n), то есть gcd (e, phi(n)) = 1
"""
#действие
def chooseE(phi): #явный вход
    while (True):
        e = random.randrange(2, phi) #неявный вход

        if (gcd(e, phi) == 1):
            return e #явный выход


"""
Прочитать из файла данные
"""
#вычисление/#действие
def readFromFile(file_name):  #явный вход
    data = []

    try:
        file = open(file_name, 'r')
    except FileNotFoundError:
        print('Файл c таким именем не найден')
    else:
        data = file.read().splitlines()
        file.close()
    return data  #явный выход

"""
Записать в файл ключи
"""
#действие
def writeKeysToFile(file_name, a, b): #явный вход
    f_public = open(file_name, 'w')
    f_public.write(str(a) + '\n')
    f_public.write(str(b) + '\n')
    f_public.close()

"""
Вычислить n, phi(n), e
"""
#действие
def getParams(prime1, prime2): #явный вход
    n = prime1 * prime2
    phi = (prime1 - 1) * (prime2 - 1)
    e = chooseE(phi) #побочное действие
    return n, phi, e  #явный выход

"""
Получить часть закрытого ключа
"""
#вычисление
def getD(coaf_a, phi): #явный вход
    if (coaf_a < 0):
        return coaf_a + phi  #явный выход
    else:
        return coaf_a  #явный выход

"""
Выбирает два случайных простых числа из списка простых чисел (значения, доходящие до 100 тыс.)
Используя простые числа,вычисляет и хранит открытый и закрытый ключи в двух отдельных
файлах.
"""
#действие
def chooseKeys():
    # выбираем два случайных числа в диапазоне строк, где
    # простые числа не слишком маленькие и не слишком большие
    rand1 = random.randint(100, 300) #неявный вход
    rand2 = random.randint(100, 300) #неявный вход

    # открываем txt-файл простых чисел и получаем содержимое
    numbers = readFromFile('primes-100k.txt')

    # выбрнные простые числа
    prime1 = int(numbers[rand1]) #неявный вход
    prime2 = int(numbers[rand2]) #неявный вход

    
    # вычисляем n, phi(n), e
    n, phi, e = getParams(prime1, prime2) #неявный вход

    # вычисляем d, 1 < d < phi(n) так, что e*d = 1 (mod phi(n))
    # e и d - обратные (mod phi(n))
    gcd, a, b = xgcd(e, phi) #неявный вход
   
    # убедимся, что d положительный
    d = getD(a, phi) #неявный вход

    # записываем открытый ключ (n,e) в файл
    writeKeysToFile('public_keys.txt', n, e)

    # записываем закрытый ключ (n,d) в файл
    writeKeysToFile('private_keys.txt', n, d)


"""
Разделить сообщение на блоки
"""
#вычисление
def divideMsgOnBlocks(message, block_size): #явный вход
    encrypted_blocks = []
    ciphertext = -1

    if (len(message) > 0):    
        # инициализировать зашифрованный текст ASCII первого символа сообщения
        ciphertext = ord(message[0])

    for i in range(1, len(message)):
        # добавить зашифрованный текст в список, если достигнут максимальный размер блока
        # сбросить зашифрованный текст, чтобы мы могли продолжить добавление кодов ASCII
        if (i % block_size == 0):
            encrypted_blocks.append(ciphertext)
            ciphertext = 0

        # умножем на 10000, чтобы сдвинуть цифры влево на 4 разряда
        # потому что коды ASCII состоят максимум из 4-х десятичных цифр
        ciphertext = ciphertext * 10000 + ord(message[i]) #неявный выход
    # добавляем последний блок в список
    encrypted_blocks.append(ciphertext)
    return encrypted_blocks


"""
Шифрует сообщение (строку), m^e mod n, где m - значение ASCII каждого символа.
Возвращает строку чисел.
file_name - файл c отрытым. Если файла нет
при условии, предполагается, что мы шифруем сообщение, используя собственные
открытые ключи. Иначе можем использовать заданный открытый ключ, то есть хранящиеся в другом файле.
block_size указывает, сколько символов составляют одну группу чисел в
каждый индекс encrypted_blocks.
"""
#вычисление/#действие
def encrypt(message, file_name = 'public_keys.txt', block_size = 1): #явный вход

    public_key = readFromFile(file_name) #вычисление/#действие
    encrypted_blocks = divideMsgOnBlocks(message, block_size) #вычисление

    # m^e mod n
    for i in range(len(encrypted_blocks)):
        encrypted_blocks[i] = str((encrypted_blocks[i]**int(public_key[1])) % int(public_key[0]))

    # создаем строку из чисел
    encrypted_message = " ".join(encrypted_blocks) #неявный выход

    return encrypted_message #явный выход

"""
Представляет сообщение как список целых
"""
#вычисление
def msgInIntBlocks(blocks): #явный вход
   # превращает строку в список целых чисел
    list_blocks = blocks.split(' ')  #неявный вход
    int_blocks = []

    for s in list_blocks:
        int_blocks.append(int(s)) 
    return int_blocks #явный выход

"""
Расшифровывает строку чисел c^d mod n. Возвращает сообщение в виде строки.
block_size указывает, сколько символов составляют одну группу чисел в
каждый индекс блоков.
"""
#вычисление/#действие
def decrypt(blocks, file_name = 'private_keys.txt', block_size = 1): #явный вход

    private_key = readFromFile(file_name) #вычисление/#действие

    int_blocks = msgInIntBlocks(blocks) #вычисление

    message = ""

    # преобразует каждое int в списке в количество символов block_size
    # по умолчанию каждый int представляет два символа
    for i in range(len(int_blocks)):
        # расшифровать все числа c^d mod n
        int_blocks[i] = (int_blocks[i]**int(private_key[1])) % int(private_key[0])
        
        tmp = ""
       
        # разбиваем каждый блок на его коды ASCII для каждого символа
        # и сохраняем его в строке сообщения
        for _ in range(block_size):
            tmp = chr(int_blocks[i] % 10000) + tmp
            int_blocks[i] //= 10000
        message += tmp #неявный выход

    return message #явный выход
