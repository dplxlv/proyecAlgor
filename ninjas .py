import random
usuario_actual = {"usuario": None,
                  "rol": None}
USUARIOS = "usuarios.txt"
NINJAS = "ninjas.txt"
ARBOL_H = "habilidades_ninja.txt"
COMBATES = "combates.txt"

def crear_admin_por_defecto():
    try:
        with open(USUARIOS, "r") as f:
            if any ("adminpolininja" in linea for linea in f):
                return
    except FileNotFoundError:
        pass
    with open(USUARIOS, "a",encoding="utf-8") as f:
        f.write("adminpolininja, Admin123, admin\n")

def registrar_usuario():
    print("\n--- REGISTRO DE USUARIO ---")
    nombre = input("Nombres y Apellidos: ").strip()
    identificacion = input("Ingrese su identificación: ").strip()
    edad = input("Ingrese su edad: ").strip()
    usuario = input("usuario: ").strip()
    contraseña = input("Contraseña (mínimo 8 caracteres, 1 mayúscula, 1 número): ").strip()
    rol = input("Rol (admin/jugador): ").strip().lower()

    if len(contraseña) < 8 or not any(c.isupper() for c in contraseña) or not any(c.isdigit() for c in contraseña):
        print("La contraseña no cumple con los requisitos.")
        return

    with open(USUARIOS, "a", encoding="utf-8") as archivo:
        archivo.write(f"{usuario},{contraseña},{nombre},{rol},{identificacion},{edad}\n")

    print("Usuario registrado exitosamente.")

def iniciar_sesion():
    print("\n--- INICIO DE SESIÓN ---")
    usuario = input("usuario: ").strip()
    contraseña = input("Contraseña: ").strip()

    with open(USUARIOS, "r", encoding="utf-8") as archivo:
        for linea in archivo:
            datos = linea.strip().split(",")
            if len(datos) >= 6:
                usuario_guardado, clave_guardada, nombre, rol, cedula, edad = datos
                if usuario == usuario_guardado and contraseña == clave_guardada:
                    usuario_actual["usuario"] = usuario
                    usuario_actual["rol"] = rol
                    usuario_actual["nombre"] = nombre
                    print(f"Sesión iniciada como {nombre}")
                    return True
    print("usuario o contraseña incorrectas.")
    return False


class NodoHabilidad:
    def __init__(self, valor):
        self.valor = valor
        self.izquierda = None
        self.derecha = None
def crear_arbol_habilidades(fuerza, agilidad, resistencia):
    raiz = NodoHabilidad(fuerza)
    raiz.izquierda = NodoHabilidad(agilidad)
    raiz.derecha = NodoHabilidad(resistencia)
    return raiz
def guardar_arbol(nombre, arbol):
    with open(ARBOL_H, "a", encoding="utf-8") as f:
        f.write(f"{nombre}: {arbol.valor}, {arbol.izquierda.valor},{arbol.derecha.valor}\n")
def recorrido_por_estrategia(arbol, status, lista):
    if status == "ganando":
        preorden(arbol, lista)
    elif status == "empatado":
        inorden(arbol, lista)
    else:
        postorden(arbol,lista)

def preorden(nodo, lista):
    if nodo:
        lista.append(nodo.valor)
        preorden(nodo.izquierda, lista)
        preorden(nodo.derecha, lista)

def inorden(nodo, lista):
    if nodo:
        inorden(nodo.izquierda, lista)
        lista.append(nodo.valor)
        inorden(nodo.derecha, lista)

def postorden(nodo, lista):
    if nodo:
        postorden(nodo.izquierda, lista)
        postorden(nodo.derecha, lista)
        lista.append(nodo.valor)

def cargar_ninjas():
    ninjas = []
    try:
        with open(NINJAS, "r", encoding="utf-8") as f:
            for linea in f:
                datos = linea.strip().split(",")
                if datos and len(datos) >= 6:
                    ninjas.append(datos)
    except FileNotFoundError:
        pass
    return ninjas

def guardar_ninjas(ninjas):
    with open(NINJAS, "w", encoding="utf-8") as f:
        for ninja in ninjas:
            f.write(",".join(ninja) + "\n")

def agregar_ninja():
    if usuario_actual["rol"] != "admin":
        print("Solo los admninistradores pueden agregar ninjas.")
        return
    nombre = input("Nombre del ninja:")
    fuerza = int(input("Fuerza (0 - 100):"))
    agilidad = int(input("Agilidad (0 - 100):"))
    resistencia = int(input("Resistencia (0 - 100):"))
    estilo = input("Estilo (Ofensivo/ Deefensivo/Equilibrado):")
    ninjas = cargar_ninjas()
    ninjas.append([nombre, str(fuerza),str(agilidad), str(resistencia), estilo, "0"])
    guardar_ninjas(ninjas)
    arbol = crear_arbol_habilidades(fuerza, agilidad, resistencia)
    guardar_arbol(nombre, arbol)
    print("Ninja agregado exitosamente.")

def buscar_ninja():
    ninjas = cargar_ninjas()
    clave = input("Buscar ninja por nombre:").lower()
    for n in ninjas:
        if clave in n[0].lower():
            print(f"{n[0]} – Fuerza:{n[1]} Agilidad:{n[2]} Resistencia:{n[3]} Estilo:{n[4]} Puntos:{n[5]}")


def eliminar_ninja():
    if usuario_actual["rol"] != "admin":
        print("Solo los administradores pueden eliminar ninjas.")
        return
    nombre = input("Nombre del ninja a eliminar: ")
    ninjas = cargar_ninjas()
    nuevos = [n for n in ninjas if n[0].lower() != nombre.lower()]
    if len(nuevos) < len(ninjas):
        guardar_ninjas(nuevos)
        print(f"Ninja eliminado correctamente.")
    else:
        print("Ninja no encontrado.")

def actualizar_ninja():
    if usuario_actual["rol"] != "admin":
        print("Solo administradores pueden actualizar.")
        return
    nombre = input("Nombre del ninja a actualizar:")
    ninjas = cargar_ninjas()
    for n in ninjas:
        if n[0].lower() == nombre.lower():
            n[1] =input("Nueva fuerza (0 -100):")
            n[2] =input("Nueva agilidad (0 - 100):")
            n[3] =input("Nueva resistencia (0 - 100):")
            n[4] =input("Nuevo estilo (Ofensivo/ Defensivo/ Equilibrado):")
            guardar_ninjas(ninjas)
            print("Actualizado correctamente.")
            return
    print("Ninja no encontrado.")

def ordenar(lista):
    tamano_de_lista = len(lista)
    if tamano_de_lista > 0:
        quicksort(lista, 0, tamano_de_lista - 1)

def quicksort(lista, inicio, fin):
    if inicio >= fin:
        return
    pivo = int(lista[fin][1]) 
    anterior = inicio
    posterior = fin - 1

    while anterior <= posterior:
        while anterior <= posterior and int(lista[anterior][1]) >= pivo:
            anterior += 1
        while anterior <= posterior and int(lista[posterior][1]) <= pivo:
            posterior -= 1
        if anterior < posterior:
            lista[anterior], lista[posterior] = lista[posterior], lista[anterior]
    lista[anterior], lista[fin] = lista[fin], lista[anterior]
    quicksort(lista, inicio, anterior - 1)
    quicksort(lista, anterior + 1, fin)


def simular_combate():
    if usuario_actual["rol"] != "jugador":
        print(" Solo jugadores pueden combatir.")
        return
    ninjas = cargar_ninjas()
    if len(ninjas) < 2:
        print("Se necesitan 2 ninjas.")
        return
    for i, n in enumerate(ninjas, 1):
        print(f"{i}. {n[0]} – Puntos: {n[5]}")
    n1 = int(input("Selecciona 1er ninja: ")) - 1
    n2 = int(input("Selecciona 2do ninja: ")) - 1
    if n1 == n2:
        print("No puede ser el mismo ninja.")
        return
    j1, j2 = ninjas[n1], ninjas[n2]
    arbol1 = crear_arbol_habilidades(int(j1[1]), int(j1[2]), int(j1[3]))
    arbol2 = crear_arbol_habilidades(int(j2[1]), int(j2[2]), int(j2[3]))
    suma1, suma2 = sum([int(j1[i]) for i in range(1,4)]), sum([int(j2[i]) for i in range(1,4)])
    estado = "empatado"
    if suma1 > suma2: 
        estado = "ganando"
    elif suma2 > suma1: 
        estado = "perdiendo"
    lista1, lista2 = [], []
    recorrido_por_estrategia(arbol1, estado, lista1)
    recorrido_por_estrategia(arbol2, estado, lista2)
    puntos1 = sum(lista1) + random.randint(0, 10)
    puntos2 = sum(lista2) + random.randint(0, 10)
    print(f"{j1[0]}: {puntos1} vs {j2[0]} : {puntos2}")
    if puntos1 > puntos2:
        ganador, indice = j1[0], n1
    elif puntos2 > puntos1:
        ganador, indice = j2[0], n2
    else:
        ganador, indice = random.choice([(j1[0], n1), (j2[0], n2)])
    print(f"Gana {ganador}")
    ninjas[indice][5] = str(int(ninjas[indice][5])+ 1)
    guardar_ninjas(ninjas)
    linea = f"{j1[0]} ({puntos1}) vs {j2[0]} ({puntos2}) → Ganador: {ganador}\n"
    with open(COMBATES, "a", encoding="utf-8") as f:
        f.write(linea)
    personal = f"combates_{usuario_actual['usuario']}.txt"
    with open(personal, "a", encoding="utf-8") as f:
        f.write(linea)


def mostrar_ranking():
    ninjas = cargar_ninjas()
    if not ninjas:
        print("No hay ninjas")
        return
    ordenar(ninjas)
    print("\n --- Ranking por victorias ---")
    for i, n in enumerate(ninjas, 1):
        print(f"{i}. {n[0]} - Puntos: {n[5]}")

def menu_admin():
    while True:
        print("\n--- MENÚ ADMIN ---")
        print("1. Agregar Ninja")
        print("2. Eliminar Ninja")
        print("3. Actualizar Ninja")
        print("4. Ver Ranking de Ninjas")
        print("5. Cerrar sesión")
        opcion = input("Seleccione una opción: ")
        if opcion == "1":
            agregar_ninja()
        elif opcion == "2":
            eliminar_ninja()
        elif opcion == "3":
            actualizar_ninja()
        elif opcion == "4":
            mostrar_ranking()
        elif opcion == "5":
            print("Sesión cerrada.")
            break
        else:
            print("Opción inválida.")

def menu_jugador():
    while True:
        print("\n--- MENÚ JUGADOR ---")
        print("1. Combatir")
        print("2. Ver ranking")
        print("3. Buscar Ninja")
        print("4. Cerrar sesión")
        opcion = input("Seleccione una opción: ")
        if opcion == "1":
            simular_combate()
        elif opcion == "2":
            mostrar_ranking()
        elif opcion == "3":
            buscar_ninja()
        elif opcion == "4":
            print("Sesión cerrada.")
            break
        else:
            print("Opción inválida.")
        
def menu_principal():
    crear_admin_por_defecto()
    while True:
        print("\n ==== BIENVENIDO A POLININJAGAMES ====")
        print("1. Registrar Usuario")
        print("2. Iniciar Sesion")
        print("3. Salir")
        opcion = input("Seleccione una opcion: ")

        if opcion == "1":
            registrar_usuario()
        elif opcion == "2":
            if iniciar_sesion():
                if usuario_actual["rol"] == "admin":
                    menu_admin()
                elif usuario_actual["rol"] == "jugador":
                    menu_jugador()
                else:
                    print("Rol desconocido.")
        elif opcion == "3":
            break
        else:
            print("Opción no válida.")

menu_principal()