import random


def random_operation():
    lista1 = [1, 2, 3, 4, 5, 6]
    lista2 = []
    for i in lista1:
        linea = []
        for j in range(i):
            linea.append(random.randint(1, 100))
        lista2.append(linea)
    print(lista2)

    for i in lista2:
        for j in i:
            print(j, end = " ")
        print()
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
   random_operation()

