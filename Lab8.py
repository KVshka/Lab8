#Требуется для своего варианта второй части л.р. №6 (усложненной программы) или ее объектно-ориентированной реализации (л.р. №7) разработать реализацию 
#с использованием графического интерфейса. Допускается использовать любую графическую библиотеку питона. Рекомендуется использовать внутреннюю библиотеку 
#питона tkinter. В программе должны быть реализованы минимум одно окно ввода, одно окно вывода, текстовое поле, кнопка.

#Импорт библиотек
from tkinter import *
from tkinter import ttk
import numpy as np
import re
# Тестовые данные
N_test = 10
A_test = np.ones((N_test, N_test), dtype=int)

def Main(A, N, K): #Расчёт и окно вывода
    
    n = N // 2  # Размерность матриц B, C, D, E (n x n)
    Zero = np.zeros((n, n), dtype=int)
    B = A[:n,:n]
    C = A[:n,n::]
    D = A[n::,n::]
    E = A[n::,:n]

    print('\nМатрица A:\n', A)
    print('\nМатрица B:\n', B)
    print('\nРанг матрицы B:\n', np.linalg.matrix_rank(B))
    print('\nМатрица C:\n', C)
    print('\nРанг матрицы C:\n', np.linalg.matrix_rank(C))
    print('\nМатрица D:\n', D)
    print('\nМатрица E:\n', E)

    def F(x, Z):
        if x == 0:
            return np.copy(Zero)
        else:
            return np.copy(Z)

    #Сумма элементов квадрата, составленного из главных и побочных диагоналей подматриц результирующей матрицы, по модулю K должна быть максимальной. K вводится с клавиатуры
    def Sum(x, Z):
        a = 0
        for i in Z:
            a += i%x
        return a

    #заменяем подматрицы нулевыми матрицами
    max = -11
    #Ограничение: первая строка матрицы должна содержать чётное количество нулей

    if np.linalg.matrix_rank(B) % 2 != 0 or np.linalg.matrix_rank(C) % 2 != 0:
        B_copy = np.copy(Zero)
        C_copy = np.copy(Zero)
        for c in range(2):
            E_copy = F(c, E)
            for d in range(2):
                D_copy = F(d, D)
                Matrix = np.vstack((np.hstack((B_copy, C_copy)), np.hstack((E_copy, D_copy))))
                sum = Sum(K, np.diag(np.flip(B_copy, axis = 1))) + Sum(K, np.diag(C_copy)) + Sum(K, np.diag(np.flip(D_copy, axis = 1))) + Sum(K, np.diag(E_copy))
                if max < sum:
                    max = sum
                    Result = np.copy(Matrix)
    else:
        for a in range(2):
            B_copy = F(a, B)
            for b in range(2):
                C_copy = F(b, C)
                for c in range(2):
                    E_copy = F(c, E)
                    for d in range(2):
                        D_copy = F(d, D)
                        Matrix = np.vstack((np.hstack((B_copy, C_copy)), np.hstack((E_copy, D_copy))))
                        if len(re.findall(r'\D[0]', str(Matrix[:1,:N]))) % 2 == 0 and len(re.findall(r'\D[0]', str(Matrix[:1,:N]))) > 0:
                            sum = Sum(K, np.diag(np.flip(B_copy, axis = 1))) + Sum(K, np.diag(C_copy)) + Sum(K, np.diag(np.flip(D_copy, axis = 1))) + Sum(K, np.diag(E_copy))
                            if max < sum:
                                max = sum
                                Result = np.copy(Matrix)
    result = Tk() #создаём окно вывода и выводим результат
    result.title("Вывод результата")
    result.geometry("800x600")
    Res = Label(master=result, text=f'Результат\n {Result}')
    Res.pack()


#Функция для тестовых данных
def test(): 
    def Get():
        K = int(entry.get())
        Main(A, N, K)
    N = N_test
    A = A_test
    window = Tk()
    window.title("Ввод данных")
    window.geometry("800x600")
    entr = Label(master=window, text="Введите число K (модуль)")
    entr.pack()
    entry = ttk.Entry(window)
    entry.pack(anchor=NW, padx=6, pady=6)
    but = ttk.Button(master=window, text='Ввод', command=Get)
    but.pack()

#Функция для случайных данных
def random():
    def GetN():
        def Get():
            K = int(entry.get())
            Main(A, N, K)
        N = int(entry.get())
        if N < 2:
            entr["text"] = 'Число N слишком малое. Введите N >= 2'
        elif N % 2 != 0:
            entr["text"] = 'Введите чётное число N'
        else:
            #Формируем матрицу А
            A = np.random.randint(-10, 10, size=(N, N))
            entr["text"] = 'Введите число K (модуль)'
            entry.delete(0, END)
            but["command"]=Get

    window = Tk()
    window.title("Ввод данных")
    window.geometry("800x600")
    entr = Label(master=window, text="Введите число N")
    entr.pack()
    entry = ttk.Entry(window)
    entry.pack(anchor=NW, padx=6, pady=6)
    but = ttk.Button(master=window, text='Ввод', command=GetN)
    but.pack()

root = Tk()     # создаем корневой объект - окно
root.title("Лабораторная работа №8")     # устанавливаем заголовок окна
root.geometry("800x600")    # устанавливаем размеры окна
label = Label(text="Использовать тестовые данные или случайные?") # создаем текстовую метку
label.pack()    # размещаем метку в окне
btn = ttk.Button(text="Тестовые", command = test) #создаём кнопки и устанавливаем внутри окна
btn.pack() 
btn = ttk.Button(text="Случайные", command = random)
btn.pack() 
root.mainloop()