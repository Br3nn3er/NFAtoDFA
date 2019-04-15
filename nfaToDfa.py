import re
estadoInicial = []
estadoFinal = []
arestas = []
estados = []
alfabetos = []
entrada = open("input.txt")
linhas = entrada.readlines()

entrada.close()

# ajustando entrada lida
i = 0
while i < len(linhas):
    txt = linhas[i]
    txt = re.sub("\n", "", txt)
    txt = re.sub(" ", "", txt)
    linhas[i] = txt
    i = i+1
#------------------------------------
estadoInicial = linhas[0].split(",")
estadoFinal = linhas[1].split(",")


#obtendo arestas ...
i = 2
j = 0
while i < len(linhas):
    aresta = linhas[i].split(",")
    arestas.append(aresta)
    i = i + 1
    j = j + 1


#pegando estados e alfabetos...
i = 0
while i < len(arestas):
    if not(arestas[i][0] in estados):
        estados.append(arestas[i][0])
    if not(arestas[i][1] in estados):
        estados.append(arestas[i][1])
    if not(arestas[i][2] in alfabetos):
        alfabetos.append(arestas[i][2])
    i = i + 1
i = 0

def printAutomato():
    #print estados...
    i = 0
    print("estados: ")
    while(i < len(estados)):
        if(estados[i] in estadoInicial) and (estados[i] in estadoFinal):
            print(">",estados[i],"<")
        if(estados[i] in estadoInicial) and not(estados[i] in estadoFinal):
            print(">",estados[i])
        if not(estados[i] in estadoInicial) and (estados[i] in estadoFinal):
            print(estados[i],"<")
        if not(estados[i] in estadoInicial) and not(estados[i] in estadoFinal):
            print(estados[i])
        i = i + 1
    #print arestas
    print("arestas: ")
    i = 0
    while i < len(arestas):
        print(arestas[i][0], ":",arestas[i][2], "-> ", arestas[i][1])
        i = i + 1
    #print alfabetos...
    print("Alfabetos: ")
    i = 0
    while i < len(alfabetos):
        print(alfabetos[i])
        i = i + 1
        
#printAutomato()
getEstadoEncontrado = []
novaAresta = []


def getheringStates(s, L):
    L.append(s)
    i = 0
    while i < len(arestas):
        if(arestas[i][0] == s) and (arestas[i][2] == "$"):
            if not( arestas[i][1] in L):
                getheringStates(arestas[i][1], L)
        i = i + 1
    return L
    
i = 0
while i< len(estados):

    l = getheringStates(estados[i], [])
    getEstadoEncontrado.append(l)
    i = i + 1

# gerando novo automato deterministico

#o novo estado inicial
estadoInicialNovo = []
i = 0
while i < len(estados):
    if(estados[i] in estadoInicial):
        for s in getEstadoEncontrado[i]:
            if not(s in estadoInicialNovo):
                estadoInicialNovo.append(s)
    i = i + 1
print("O estado Inicial: ",estadoInicialNovo)

def getGrupoDeEstadosApartirDoPrimeiro(estado):
    for s in getEstadoEncontrado:
        if s[0] == estado:
            returned = s
    return returned
            
def conc(l1,l2):
    for item in l2:
        if not(item in l1):
            l1.append(item)
    return l1
#----------------------------
def combinar(l1, l2):
        b = True
        if not(len(l1) == len(l2)):
                b = False
        else:
                for item in l1:
                        if not(item in l2):
                                b = False
                for item in l2:
                        if not(item in l1):
                                b = False
        return b
def existe(L, i):
        a = novaAresta[i][0]
        b = combinar(L, a)
        if(b == True):
            return True
        else:
                j = i + 1
                if j < len(novaAresta):
                        return existe(L, j)
                else:
                        return False
                        
#----------------------------
    

def criarNovaAresta(alpha, gEstado):
 
    
    L = []
    for s1 in gEstado:
        i = 0
        while i < len(arestas):
            if (s1 == arestas[i][0] and arestas[i][2] == alpha):
        
                if not(arestas[i][1] in L):
                    GEstado = getGrupoDeEstadosApartirDoPrimeiro(arestas[i][1])
                    L = conc(L, GEstado)
            i = i + 1
    if L == []: return
    ne = [gEstado , L, alpha]
    novaAresta.append(ne)

    jahEhRaiz = existe(L, 0)
    print(novaAresta)
    print(L, " jjjj ", jahEhRaiz)
    if jahEhRaiz == False:
        for A in alfabetos:
            if not(A == "$"): criarNovaAresta(A, L)

for L in alfabetos:
    if not(L == "$"): criarNovaAresta(L, estadoInicialNovo)
#-------------------------------
def jahEmLista(L, item):
    B = False
    for I in L:
        if(combinar(I, item) == True):
            B = True
    return B
#--------------------------------
novoEstado = []
Help = []
for aresta1 in novaAresta:
    Help.append(aresta1[0])
    Help.append(aresta1[1])


for n2 in Help:
    if(jahEmLista(novoEstado, n2) == False):
        novoEstado.append(n2)
        

novoEstadoInicial = []
for item1 in novoEstado:
    for item2 in estadoInicial:
        if item2 in item1 and not(item1 in novoEstadoInicial):
            novoEstadoInicial.append(item1)
novoEstadoFinal = []
for item1 in novoEstado:
    for item2 in estadoFinal:
        if item2 in item1 and not(item1 in novoEstadoFinal):
            novoEstadoFinal.append(item1)



setToChar = []
i = 1
for item in novoEstado:
    L = [item, i]
    setToChar.append(L)
    i = i+1
def nomeResumidoEstado(L):
    for item in setToChar:
        if combinar(item[0], L) == True:

            return str(item[1])

print("set to char: ", setToChar)


#guardando no arquivo
f = open("output.txt", "w")

f.write("Novos Estados: ")
for item in setToChar:
    index = item[1]
    f.write("p")
    f.write(str(index))
    f.write(" ")

f.write("\nEstados Iniciais: ")
for item in setToChar:
    if(item[0] in novoEstadoInicial):
        index = item[1]
        f.write("p")
        f.write(str(index))
        f.write(" ")

f.write("\nEstados Finais: ")
for item in setToChar:
    if(item[0] in novoEstadoFinal):
        index = item[1]
        f.write("p")
        f.write(str(index))
        f.write(" ")
f.write("\nNovas Arestas: \n")
for item in novaAresta:
        f.write("\n")
        From = str(nomeResumidoEstado(item[0]))
        f.write("p"+From)
        f.write(" , ")
        to = str(nomeResumidoEstado(item[1]))
        f.write("p"+to)
        f.write(" , "+str(item[2]))
f.close()
