##Consejos para ejecutar el programa:

#En la carpeta se encuentra dos archivos de prueba para el programa para ejecución rapida, 
#puede correr el programa con la opción 1 y escribir "prueba1.txt" y se generará el archivo para la opción 2.
#Para correr el programa con la opción 2 y introducir: "prueba2.txt" e irá directamente al juego
##

##
#Opción 1: Introducir un .txt con:
#1ra linea: Largo del cuadrado de buscamina
#2da linea: Dificultad a escoger F, M, D, X (aumenta dificultad de izquierda a derecha)
#
#Resultado: Un archivo .sal con el tamaño y las ubicaciones de las bombas
##

##
# Opción 2: Introducir un archivo de texto autogenerado con la opción 1 o un archivo de texto con 1ra linea el largo y el resto con las ubicaciones de bombas separadas por un salto de linea:
##

##
# Opción 3: Salir del juego
##

#Consejo 1: Al introducir archivos debe incluir la extensión de este
#Consejo 2: En caso de usar para la opción 2 un archivo generado por la 1, tenga cuidado con la extensión del archivo, ya que genera un .sal
#Consejo 3: Para abrir casillas escriba primero la letra seguido del número (sin espacio entre estos)
#Consejo 4: Al abrir una casilla le saldrá el número de casillas que tiene alrededor (incluyendo las diagonales)
#Consejo 5: En caso de escribir una casilla invalida no se perderá el juego
#Consejo 6: Si desea salir en medio del juego presionar ctrl + C
#Consejo 7: En caso de liberar todas las casillas, habrá ganado el juego y saldrá el mensaje correspondiente

from random import choice,randint
from io import open

def extraer_archivo(nombre_archivo):
    archivo=open(str(nombre_archivo),"r")
    archivo_listas=archivo.readlines()

    archivo.close()
    return int(archivo_listas[0]),archivo_listas[1]


def cantidad_minas(altura_tablero,dificultad):
    trampas=0
    if dificultad=="F":
        trampas=pow(altura_tablero,2)*0.1
    elif dificultad=="M":
        trampas=pow(altura_tablero,2)*0.15
    elif dificultad=="D":
        trampas=pow(altura_tablero,2)*0.2
    elif dificultad=="X":
        trampas=pow(altura_tablero,2)*0.3
    return int(trampas)

def lugares_minas_funcion(altura_tablero,dificultad,nombre_archivo):
    lugares=[]
    lugares_str_vertical=""
    lugares_str=""
    bombas=cantidad_minas(altura_tablero,dificultad) #Define la cantidad de minas del tablero, dependiendo de la dificultad y altura
    bombas_lista=[]
    for iterante_letras in range(altura_tablero): #Crea la matriz del tablero
        creador_lista_letras=chr(65+iterante_letras)
        lugares.append(creador_lista_letras)
    for cantidad_de_bombas in range(bombas): #Da lugares a las bombas
        fila_bomba=choice(lugares)
        columna_bomba=str(randint(1,altura_tablero))
        if fila_bomba+columna_bomba in bombas_lista:
            while fila_bomba+columna_bomba in bombas_lista:
                fila_bomba=choice(lugares)
                columna_bomba=str(randint(1,altura_tablero))
        bombas_lista.append(fila_bomba+columna_bomba)

    for iterante_bombas_listas in bombas_lista: #Pasa la ubicaciones de las bombas a String
        lugares_str_vertical+=iterante_bombas_listas
        lugares_str_vertical+="\n"
        lugares_str+=iterante_bombas_listas+","
    lugares_str+=";"
    archivo=open(str(nombre_archivo[:-4]+".sal"),"w")
    archivo.write(str(altura_tablero)+"\n"+lugares_str_vertical)
    archivo.close()
    return bombas_lista,lugares_str

def letras(altura_tablero):
    codigo="   "
    for filas_numeros in range(1,altura_tablero+1):
        if filas_numeros<10:
            codigo+=str(filas_numeros)+"  "
        if filas_numeros>=10:
            codigo+=str(filas_numeros)+" "
    return codigo

def reemplazaaar(casilla,lugares_lista,lista_tablero,casillas_marcadas):
    if casilla!="" and casilla not in casillas_marcadas:
        if casilla in lugares_lista:
            for lista_por_filas in lista_tablero[1:]:
                if casilla[0] in lista_por_filas:
                    lista_por_filas[int(casilla[1:])*3]="*"
                    validador=1
        else:
            for lista_por_filas in lista_tablero[1:]:
                if casilla[0] in lista_por_filas:
                    lista_por_filas[int(casilla[1:])*3]=str(definir_numero(casilla,lugares_lista,altura_tablero))
                    validador=0
    if casilla not in casillas_marcadas:
        casillas_marcadas.append(casilla)
    else:
        validador=0
    return lista_tablero,casillas_marcadas,validador

def reemplazaaar2(lista_tablero,lugares_lista):
    for reemplazar_por_minas in lugares_lista:
        for lista_por_filas in lista_tablero[1:]:
            if reemplazar_por_minas[0] in lista_por_filas:
                lista_por_filas[int(reemplazar_por_minas[1:])*3]="*"
    return lista_tablero

def generar_busca_minas(altura_tablero,lugares_lista):
    minimo_chr,lista_tablero=65,[]
    tablero_a_str=""
    numeros_str=letras(altura_tablero)
    lista_tablero.append(list(numeros_str))
    for iterante_creador_listas in range(altura_tablero):
        lista_tablero.append(list(chr(minimo_chr+iterante_creador_listas)+(" "*(altura_tablero*3+1))))

    for lista_por_filas in lista_tablero[1:]:
        for lista_por_columna in range(len(lista_por_filas)//3):
            if lista_por_filas[lista_por_columna*3+3]==" ":
                lista_por_filas[lista_por_columna*3+3]="."
    for listas in lista_tablero[1:]:
        tablero_a_str+="\n"
        for listas_de_listas in listas:
            tablero_a_str+=str(listas_de_listas)

    return numeros_str,tablero_a_str,lista_tablero


def generar_busca_minas2(lista_tablero,casilla,lugares_lista,altura_tablero,casillas_marcadas):
    casilla=casilla.upper()
    codigo=letras(altura_tablero)
    tablero_a_str=""
    lista_tablero,casillas_marcadas,validador=reemplazaaar(casilla,lugares_lista,lista_tablero,casillas_marcadas)
    for lista_por_filas in lista_tablero[1:]:
        tablero_a_str+="\n"
        if lista_por_filas==0:
            break
        for iterante_para_str in lista_por_filas:
            tablero_a_str+=str(iterante_para_str)

    return codigo,tablero_a_str,lista_tablero,casillas_marcadas,validador

def generar_buscaminas3(lista_tablero,lugares_lista):
    tablero_a_str=""
    lista_tablero=reemplazaaar2(lista_tablero,lugares_lista)
    codigo=letras(altura_tablero)
    for lista_por_filas in lista_tablero[1:]:
        tablero_a_str+="\n"
        for iterante_para_str in lista_por_filas:
            tablero_a_str+=str(iterante_para_str)
    return tablero_a_str,lista_tablero,codigo


def extraer_archivo2(nombre_archivo):
    lugares_lista=[]
    lugares_str=""
    archivo=open(str(nombre_archivo),"r")
    archivo_listas=archivo.readlines()
    altura_tablero=int(archivo_listas[0])
    if len(archivo_listas[1:])==1:
        for lista_bombas in archivo_listas[1:]:
            lugares_lista.append(lista_bombas[:])
            lugares_str+=lista_bombas
    else:
        for lista_bombas in archivo_listas[1:]:
            if lista_bombas==archivo_listas[-1]:
                lugares_lista.append(lista_bombas[:])
                lugares_str+=lista_bombas
            else:
                lugares_lista.append(lista_bombas[:-1])
                lugares_str+=lista_bombas
    return altura_tablero,lugares_lista,lugares_str

def minas_lados(coordenada,lugares_lista):
    num=0
    if coordenada[0]+str(int(coordenada[1:])+1) in lugares_lista:
        num+=1
    if coordenada[0]+str(int(coordenada[1:])-1) in lugares_lista:
        num+=1
    return num

def minas_arriba(coordenada,lugares_lista):
    num=0
    if chr(ord(coordenada[0])-1)+str(int(coordenada[1:])) in lugares_lista:
        num+=1
    if chr(ord(coordenada[0])-1)+str(int(coordenada[1:])+1) in lugares_lista:
        num+=1
    if chr(ord(coordenada[0])-1)+str(int(coordenada[1:])-1) in lugares_lista:
        num+=1
    return num

def minas_abajo(coordenada,lugares_lista):
    num=0
    if chr(ord(coordenada[0])+1)+str(int(coordenada[1:])) in lugares_lista:
        num+=1
    if chr(ord(coordenada[0])+1)+str(int(coordenada[1:])+1) in lugares_lista:
        num+=1
    if chr(ord(coordenada[0])+1)+str(int(coordenada[1:])-1) in lugares_lista:
        num+=1
    return num

def definir_numero(coordenada,lugares_lista,cant):

    letra=ord(coordenada[0])-64
    if letra==cant:
        num1=int(minas_lados(coordenada,lugares_lista))
        num2=int(minas_arriba(coordenada,lugares_lista))
        num=num1+num2
    else:
        num1=int(minas_lados(coordenada,lugares_lista))
        num2=int(minas_arriba(coordenada,lugares_lista))
        num3=int(minas_abajo(coordenada,lugares_lista))
        num=num1+num2+num3
    return num

casilla=""
casillas_marcadas=[]
validador=0
a=1
opción=input("Escoge una opción:  (1)  Generar tablero  (2)  Cargar tablero  (3)  Salir: ")
if ((len(opción)>1 or len(opción)<1) or (ord(opción)>51 or ord(opción)<49)):
    while (len(opción)>1 or len(opción)<1) or (ord(opción)>51 or ord(opción)<49):
        print("¡Opción invalida!")
        opción=input("Escoge una opción:  (1)  Generar tablero  (2)  Cargar tablero  (3)  Salir: ")
opción=int(opción)


if opción==1:

    nombre_archivo=input("Ingresa el nombre del archivo: ")
    altura_tablero,dificultad=extraer_archivo(nombre_archivo)
    lugares_lista,lugares_str=lugares_minas_funcion(altura_tablero,dificultad,nombre_archivo)
    exit
elif opción==2:
    nombre_archivo=input("Ingresa el nombre del archivo: ")
    altura_tablero,lugares_lista,lugares_str=extraer_archivo2(nombre_archivo)

    codigo,tablero_a_str,lista_tablero=generar_busca_minas(altura_tablero,lugares_lista)
    print(codigo+tablero_a_str)
    while validador==0:
        if len(casillas_marcadas)==(pow(altura_tablero,2)-len(lugares_lista)):
            tablero_a_str,lista_tablero,codigo=generar_buscaminas3(lista_tablero,lugares_lista)

            print("\n"+codigo+tablero_a_str)
            print("¡GANASTE!")
            break

        casilla=input("Ingresa la casilla del tablero que quieres abrir: ").upper()

        if len(casilla)<2 or len(casilla)>3:
            while len(casilla)<2 or len(casilla)>3:
                print("¡Casilla invalida!, ingrese una casilla de la tabla.")
                if len(casilla)==2 or len(casilla)==3:
                    break
                else:
                    casilla=input("Ingresa la casilla del tablero que quieres abrir: ").upper()

        if (65>ord(casilla[0]) or ord(casilla[0])>=65+altura_tablero) or (0>int(casilla[1:]) or int(casilla[1:])>altura_tablero):
            while (65>ord(casilla[0]) or ord(casilla[0])>=65+altura_tablero) or (0>int(casilla[1:]) or int(casilla[1:])>altura_tablero):
                casilla=input("¡Casilla invalida!, ingrese una casilla de la tabla.").upper()


        if 65<=ord(casilla[0])<altura_tablero+65 and 0<int(casilla[1:])<=altura_tablero:
            codigo,tablero_a_str,lista_tablero,casillas_marcadas,validador=generar_busca_minas2(lista_tablero,casilla,lugares_lista,altura_tablero,casillas_marcadas)
            print(codigo+tablero_a_str)

            if validador==1:
                print("PERDISTE")
                break
        else:
            print("¡Casilla invalida!, ingrese una casilla de la tabla.")
    exit

else: exit

