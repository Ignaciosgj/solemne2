import random
from sys import stdin
diametro = 7
matriz = []
road = []
num = 10
objetos = []
pressure = 5 
mutation_chance = 0.05

class Objeto():
    rueda = []
    fitness = 0

def crear_rueda():
    objeto = Objeto()
    individuo = []
    for i in range(diametro):
        individuo.append([])
        for j in range(diametro):
            individuo[i].append([])

    for i in range(diametro):
        for j in range(diametro):
            individuo[i][j] = random.randint(0, 1)
    objeto.rueda = individuo
    return objeto

def crear_poblacion():
    return [crear_rueda() for i in range(num)]

def dibujar_rueda(objeto):
    for i in range(diametro):
        for j in range(diametro):
            print("%s "%(objeto[i][j]), end = '')
        print ("\n", end = '')
    print("\n", end = '')

def mostrar_poblacion():
    for i in range(num):
        dibujar_rueda(population[i])

def crear_camino():
    pre_road = []
    for i in range(35):
        line = stdin.readline() #.strip()
        pre_road.append([])
        for j in range(3):
            pre_road[i].append(line[j])

    for i in range(3):
        road.append([])
        for j in range(35):
            road[i].append([])

    for i in range(35):
        for j in range(3):
            if (pre_road[i][j]) == 'x':
                road[2-j][i] = 2
            else:
                road[2-j][i] = 0

def dibujar_camino():
    for i in range(3):
        for j in range(35):
            print("%s "%(road[i][j]), end = '')
        print ("\n", end = '')
    print("\n", end = '')

def rotar_rueda(objeto):
    matriz_rotada = []
    for i in range(diametro):
        matriz_rotada.append([])
        for j in range(diametro):
            matriz_rotada[i].append([])

    for i in range(diametro):
        for j in range(diametro):
            matriz_rotada[j][(diametro - 1 - i)] = objeto[i][j]

    for i in range(diametro):
        for j in range(diametro):
            objeto[i][j] = matriz_rotada[i][j]

def destruccion_rueda(objeto):
    for giros in range(5):
        for j in range (7):
            for i in range(3):
                if(objeto.rueda[6-i][j] == 1):
                    break
                if(road[2-i][j+(giros*7)] == 2):
                    objeto.rueda[6-i][j] = 2
        print("rotación numero %s"%(giros+1))
        dibujar_rueda(objeto.rueda)
        rotar_rueda(objeto.rueda)

def destruccion_poblacion(population):
    for i in range(num):
        destruccion_rueda(population[i])
    return population

def reparar_ruedas(population):
    for individuo in population:
        for i in range(diametro):
            for j in range(diametro):
                if(individuo.rueda[i][j] == 2):
                    individuo.rueda[i][j] = 0
    return population

def calcular_fitness(objeto):
    fitness = 0

    for i in range(diametro):
        for j in range(diametro):
            if(objeto.rueda[i][j] != 0):
                fitness = fitness + 1
                objeto.fitness = fitness
    print("Fitness: %s"%fitness)

def poblacion_fitness(population):
    for i in range(num):
        dibujar_rueda(population[i].rueda)
        calcular_fitness(population[i])
    return population

def selection_and_reproduction(population):
    puntuados = [(i.fitness, i.rueda) for i in population]
    population = []
    for i in sorted(puntuados):
        obj = Objeto()
        obj.fitness = i[0]
        obj.rueda = i[1]
        population.append(obj)
    selected =  population[:(len(population)-pressure)]
    selected = reparar_ruedas(selected)
    
    hijos = []
    for individuo in selected:
        madre = 0
        padre = 0
        rueda = []
        while padre == madre:
            padre = random.randint(0, len(selected)-1)
            madre = random.randint(0, len(selected)-1)
        for i in range(diametro):
            rueda.append([])
            for j in range(diametro):
                rueda[i].append([])
        for i in range(diametro):
            for j in range(diametro):
                if (random.randint(0,1) == 0):
                    rueda[i][j] = selected[padre].rueda[i][j]
                else :
                    rueda[i][j] = selected[madre].rueda[i][j]
        hijo = Objeto()
        hijo.rueda = rueda
        hijos.append(hijo)
    for hijo in hijos:
        selected.append(hijo)
    return selected

def mutacion(selected): 
    for k in range(len(selected)-pressure):
        if random.random() <= mutation_chance:
            randi = random.randint(0, diametro-1)
            randj = random.randint(0, diametro-1)
            while (randi == 3 & randj == 3):
                randi = random.randint(0, diametro-1)
                randj = random.randint(0, diametro-1)
            selected[k+pressure].rueda[randi][randj] = 1-(selected[k+pressure].rueda[randi][randj])
    return selected

population = crear_poblacion()
crear_camino()
dibujar_camino()
for i in range(100):
    population = destruccion_poblacion(population)
    population = poblacion_fitness(population)
    population = selection_and_reproduction(population)
    population = mutacion(population)