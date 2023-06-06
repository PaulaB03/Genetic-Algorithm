import copy
import math
import random


# Functia de maximizat, coeficientii fiind cititi la input
def functie_polinomiala(x):
    return a * (x**2) + b * x + c


# Citim input-ul
n = int(input("dimensiunea populatiei = "))
print("Domeniul functiei:")
A = int(input("A = "))
B = int(input("B = "))
print("Parametrii functiei: ")
a = int(input("a = "))
b = int(input("b = "))
c = int(input("c = "))
precision = int(input("precizia = "))
pr = float(input("probabilitatea de incrucisare = "))
pm = float(input("probabilitatea de mutatie = "))
stages = int(input("numarul de etape = "))

g = open("Evolutie.txt", "w")

# Formula pentru discretizarea intervalului si calculul lungimii cromozomului
dimC = math.ceil(math.log2((B-A)*(10**precision)))
# Generam aleator genele
chromosomes = [[random.randint(0, 1) for j in range(dimC)] for i in range(n)]

for stage in range(stages):
    if stage == 0:
        g.write("Populatia initiala\n")

    sumF, fittest, fittestF = 0, 0, float('-inf')
    X = []
    
    for i in range(n):
        b2string = ''.join([str(x) for x in chromosomes[i]])
        # Formula pentru valoarea decimala a unui cromozom
        x = ((B - A) / (2**dimC - 1)) * int(b2string, 2) + A
        X.append(x)
        
        if stage == 0:
            g.write(str(i+1) + " : " + b2string + " x = " + str(round(x, precision)) + " f = " + str(functie_polinomiala(round(x, precision))))
            g.write('\n')
            
        sumF += functie_polinomiala(x)
        # Calculam cel mai bun cromozom din generatia curenta
        if functie_polinomiala(round(x, precision)) > fittestF:
            fittestF = functie_polinomiala(round(x, precision))
            fittest = i

    fittestCopy = chromosomes[fittest].copy()

    if stage == 0:
        g.write("\nProbabilitati selectie\n")

    probSelection = []
    for i in range(n):
        # Probabilitatile de selectie proportionala (metoda ruletei)
        probSelection.append(functie_polinomiala(X[i]) / sumF)

        if stage == 0:
            g.write("Cromozom " + str(i+1) + " probabilitate " + str(functie_polinomiala(X[i]) / sumF))
            g.write('\n')

    intervalsProbSel = [0]
    sumI = probSelection[0]
    intervalsProbSel.append(sumI)

    if stage == 0:
        g.write("\nIntervale probabilitate selectie\n")
        g.write("0 " + str(sumI) + " ")

    for i in range(1, n):
        sumI += probSelection[i]
        # Intervalele ca fiind suma probabilitatilor
        intervalsProbSel.append(sumI)
        if stage == 0:
            g.write(str(sumI) + " ")

    # Cautarea binara pentru a gasi intervalul potrivit pentru un u dat
    def find_interval(u, v, st, dr):
        last = 0
        while st <= dr:
            mij = (st + dr) // 2
            if v[mij] <= u:
                last = mij
                st = mij+1
            elif v[mij] > u:
                dr = mij-1
        return last+1

    if stage == 0:
        g.write("\n\n")

    selected = [0 for _ in range(n)]
    for i in range(n):
        # Generam un u random ce va fi cautat binar in lista de probabilitati de selectie
        u = random.random()
        cr = find_interval(u, intervalsProbSel, 0, n) - 1

        # Folosim selected pentru a memora cromozomii care trec de selectie
        selected[i] = cr

        if stage == 0:
            g.write("u= " + str(u) + " selectam cromozomul " + str(cr+1))
            g.write('\n')

    if stage == 0:
        g.write("\nDupa selectie\n")

    cc = []
    for i in range(n):
        if stage == 0:
            g.write(str(i+1) + ": " + ''.join([str(x) for x in chromosomes[selected[i]]]) + " x= " + str(round(X[selected[i]], precision)) + " f= " + str(functie_polinomiala(X[selected[i]])))
            g.write('\n')

        cc.append(chromosomes[selected[i]])
    chromosomes = copy.deepcopy(cc)

    if stage == 0:
        g.write("\nProbabilitatea de incrucisare = " + str(pr) + "\n")

    recomb = []
    for i in range(n):
        # Pentru fiecare cromozom, daca u este mai mic decat probabilitatea de incrucisare trec indicele cromozomului intr-un vector recombinare
        u = random.random()
        if u < pr:
            if stage == 0:
                g.write(str(i+1) + ": " + ''.join([str(x) for x in chromosomes[i]]) + " u= " + str(u) + " < " + str(pr) + " participa\n")
            recomb.append(i)
        else:
            if stage == 0:
                g.write(str(i+1) + ": " + ''.join([str(x) for x in chromosomes[i]]) + " u= " + str(u) + "\n")

    if stage == 0:
        g.write('\n')
    while len(recomb) > 1:
        # Generam i si j pentru a incrucisa cromozomii recomb[i] recomb[j]
        i = random.randrange(len(recomb))
        j = len(recomb)-i-1

        if i == j:
            continue

        # Generam un punct de incrucisare
        pct = random.randrange(1, dimC-1)
        if stage == 0:
            g.write("Recombinare dintre cromozomul " + str(recomb[i]+1) + " cu cromozomul " + str(recomb[j]+1) + "\n")
            g.write("         " + ''.join([str(x) for x in chromosomes[recomb[i]]]) + " " + ''.join([str(x) for x in chromosomes[recomb[j]]]) + " punct " + str(pct) + "\n")

        # Incrucisam cromozomii
        chcopy = chromosomes[recomb[i]][:pct+1].copy()
        chromosomes[recomb[i]][:pct+1] = chromosomes[recomb[j]][:pct+1].copy()
        chromosomes[recomb[j]][:pct+1] = chcopy.copy()
        if stage == 0:
            g.write("Rezultat " + ''.join([str(x) for x in chromosomes[recomb[i]]]) + " " + ''.join([str(x) for x in chromosomes[recomb[j]]]) + "\n")

        # Eliminam din recombinare indicii i si j incrucisati
        aux = [recomb[k] for k in range(len(recomb)) if k != i and k != j]
        recomb = aux.copy()

    if stage == 0:
        g.write("\nDupa recombinare\n")

    for i in range(n):
        b2string = ''.join([str(x) for x in chromosomes[i]])
        x = int(b2string, 2)
        x = ((B-A) / (2 ** dimC - 1)) * x + A
        X[i] = x
        if stage == 0:
            g.write(str(i + 1) + " : " + b2string + " x= " + str(round(x, precision)) + " f= " + str(functie_polinomiala(round(x, precision))))
            g.write('\n')

    if stage == 0:
        g.write("\nProbabilitate de mutatie = " + str(pm) + "\n")
        g.write("Au fost modificati cromozomii:\n")

    for i in range(n):
        # Pentru fiecare cromozom, daca u este mai mic decat probabilitatea de mutatie cromozomul va fi modificat
        u = random.random()
        if u < pm:
            # Generam o pozitie random unde se schimba gena cromozomului
            poz = random.randrange(dimC)
            chromosomes[i][poz] = 1 - chromosomes[i][poz]

            if stage == 0:
                g.write(str(i+1) + " ")

    if stage == 0:
        g.write("\n\nDupa mutatie:\n")

    Max, worstVal, worst = float('-inf'), float('inf'), 0

    for i in range(n):
        # Calculam din nou valorile lui x dupa mutatie
        b2string = ''.join([str(x) for x in chromosomes[i]])
        x = int(b2string, 2)
        x = ((B-A) / (2 ** dimC - 1)) * x + A
        X[i] = x
        if stage == 0:
            g.write(str(i + 1) + " : " + b2string + " x= " + str(round(x, precision)) + " f= " + str(functie_polinomiala(round(x, precision))))
            g.write('\n')

        # Valoarea maxima a functiei f in generatia curent
        Max = max(Max, functie_polinomiala(round(x, precision)))

        # Aflam cromozomul cu performanta cea mai proasta
        if functie_polinomiala(round(x, precision)) < worstVal:
            worstVal = functie_polinomiala(round(x, precision))
            worst = i

    chromosomes[worst] = fittestCopy.copy()
    Max = max(Max, fittestF)

    if stage == 0:
        g.write("\nEvolutia maximului\n")
    g.write("Generatia " + str(stage+1) + ": f(max) = " + str(Max) + "\n")

g.close()
