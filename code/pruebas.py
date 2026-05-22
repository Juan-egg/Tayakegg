import os
import json
import pandas as pd
from datetime import datetime

# Fijar directorio de trabajo al lugar donde está este script
# Esto garantiza que data/historial_precios.json siempre se encuentre
os.chdir(os.path.dirname(os.path.abspath(__file__)))


CONTRASENA = "HUEVOS"
MAX_INTENTOS = 3
RUTA_HISTORIAL = "data/historial_precios.json"
RUTA_EXCEL = "data/Precios_sin_hipervinculos.xlsx"

#Opciones


def guardar_precio(alimento, precio):
    
    #Guarda el precio que pagó el usuario en el historial JSON.
    #alimento → "tomate", "papa", etc.
    #precio   → 4500, 1300, etc.

    fecha_hoy = datetime.now().strftime("%Y-%m-%d")

    # Leer historial existente, o empezar vacío si no existe
    if os.path.exists(RUTA_HISTORIAL):
        with open(RUTA_HISTORIAL, "r", encoding="utf-8") as archivo:
            historial = json.load(archivo)
    else:
        historial = {}  

    # Si hoy no existe en el historial, crearlo vacío
    if fecha_hoy not in historial:
        historial[fecha_hoy] = {}

    # Guardar el precio del alimento en la fecha de hoy
    historial[fecha_hoy][alimento] = precio

    # Escribir el historial actualizado en el archivo
    with open(RUTA_HISTORIAL, "w", encoding="utf-8") as archivo:
        json.dump(historial, archivo, indent=4, ensure_ascii=False)

    print(f"Guardado: {alimento} = ${precio:,} el {fecha_hoy}")

def buscar_precio_mercado(alimento):
    
    #Busca el precio de un alimento en el Excel del mercado.
    #Devuelve el precio promedio, o None si no lo encuentra.
    

    # Leer el Excel completo
    datos = pd.read_excel(RUTA_EXCEL)

    # Buscar filas donde el nombre del producto contenga el alimento
    fila = datos[datos["PRODUCTO"].str.contains(alimento, case=False, na=False)]

    # Si no encontró nada, avisar
    if fila.empty:
        return None

    # Si encontró varios, devolver el promedio
    return fila["PRECIO"].mean()

def Precios(alimento, precio_usuario):
    
    #1. Busca el precio del mercado para ese alimento
    #2. Compara con lo que pagó el usuario
    #3. Guarda el precio del usuario en el historial
    

    print(f"\n--- Consultando: {alimento} ---")

    # Buscar precio en el Excel
    precio_mercado = buscar_precio_mercado(alimento)

    if precio_mercado is None:
        print(f"'{alimento}' no se encontró en el Excel del mercado.")
    else:
        print(f"Precio de mercado:  ${precio_mercado:,.0f}")
        print(f"Precio que pagaste: ${precio_usuario:,.0f}")

        # Calcular diferencia
        diferencia = precio_usuario - precio_mercado

        if diferencia > 0:
            print(f"Estás pagando ${diferencia:,.0f} MÁS que el mercado.")
        elif diferencia < 0:
            print(f"Estás pagando ${abs(diferencia):,.0f} MENOS que el mercado.")
        else:
            print("Estás pagando exactamente el precio del mercado.")

    # Guardar precio del usuario en el historial
    guardar_precio(alimento, precio_usuario)


def calcular_porcentaje_cambio(precio_actual, precio_anterior):
    if precio_anterior == 0:
        return 0.0
    return ((precio_actual - precio_anterior) / precio_anterior) * 100


def clasificar_alerta(porcentaje):
    if porcentaje > 15:
        return "ALERTA ROJA"        # subió más del 15% → crítico
    elif porcentaje >= 5:
        return "ALERTA AMARILLA"    # subió entre 5% y 15% → precaución
    elif porcentaje < -5:
        return "OPORTUNIDAD VERDE"  # bajó más del 5% → buena noticia
    elif porcentaje < 0:
        return "BAJADA LEVE"        # bajó menos del 5% → informativo
    else:
        return "PRECIO ESTABLE"     # cambio menor al 5% → tranquilo

#Alertas (2)

def Alertas():
    
    if os.path.exists(RUTA_HISTORIAL):
        with open(RUTA_HISTORIAL, "r", encoding="utf-8") as archivo:
            historial = json.load(archivo)
    else:
        historial = {}

    if historial:
        fechas = sorted(historial.keys())
        precios_hoy = historial[fechas[-1]]
        precios_ayer = historial[fechas[-2]] if len(fechas) > 1 else {}
    else:
        precios_hoy = {}
        precios_ayer = {}

    print("\n" + "-"*50)
    print(f"   📊 ANÁLISIS DE PRECIOS - {datetime.now().strftime('%d/%m/%Y')}")
    print("-"*50)
    
    # Verificar que recibimos datos
    if not precios_hoy:
        print("X No hay precios para analizar. Primero ingresa los precios del día.")
        return
    
    # Contadores para el resumen final
    contador_rojas = 0
    contador_amarillas = 0
    contador_verdes = 0
    
    # Recorremos cada ingrediente que el usuario ingresó
    for ingrediente, precio_actual in precios_hoy.items():
    
        # Buscamos cuánto costaba ayer
        if ingrediente in precios_ayer:
            precio_anterior = precios_ayer[ingrediente]
            
            # PASO 1: Calcular porcentaje de cambio
            porcentaje = calcular_porcentaje_cambio(precio_actual, precio_anterior)
            
            # PASO 2: Clasificar alerta
            alerta = clasificar_alerta(porcentaje)
            
            # PASO 3: Mostrar resultado
            print(f"\n {ingrediente.upper()}")
            print(f"   Ayer: ${precio_anterior:,.0f} → Hoy: ${precio_actual:,.0f}")
            print(f"   Variación: {porcentaje:+.1f}%")
            print(f"   Alerta: {alerta}")
            
            # Contar para resumen (opcional)
            if "ROJA" in alerta:
                contador_rojas += 1
            elif "AMARILLA" in alerta:
                contador_amarillas += 1
            elif "VERDE" in alerta:
                contador_verdes += 1
                
        else:
            # Ingrediente nuevo que no estaba ayer
            print(f"\n {ingrediente.upper()} (NUEVO)")
            print(f"   Precio actual: ${precio_actual:,.0f}")
            print(f"   ⚠️ No hay registro del día anterior para comparar.")
    
    # Resumen final
    print("\n" + "-"*50)
    print("📋 RESUMEN DEL DÍA")
    print("-"*50)
    print(f"🔴 Alertas ROJAS (>15%): {contador_rojas}")
    print(f"🟡 Alertas AMARILLAS (5-15%): {contador_amarillas}")
    print(f"🟢 Oportunidades VERDES (<-5%): {contador_verdes}")

#Sugerencias (3)

def Sugerencias():

    
    #Analiza el historial y muestra el mayor descuento y la mayor subida.
    

    if not os.path.exists(RUTA_HISTORIAL):
        print("No hay historial guardado todavía.")
        return

    with open(RUTA_HISTORIAL, "r", encoding="utf-8") as archivo:
        historial = json.load(archivo)

    #Verificar que haya al menos 2 días para comparar
    fechas = sorted(historial.keys())

    if len(fechas) < 2:
        print("Necesitas al menos 2 días de precios para ver sugerencias.")
        print("Sigue registrando precios cada día.")
        return

    #Sacar precios de hoy y ayer
    precios_hoy  = historial[fechas[-1]]
    precios_ayer = historial[fechas[-2]]

    # Calcular el cambio porcentual de cada alimento
    # Solo calculamos los que existen en AMBOS días
    cambios = {}

    for alimento in precios_hoy:
        if alimento in precios_ayer:
            porcentaje = calcular_porcentaje_cambio(
                precios_hoy[alimento],
                precios_ayer[alimento]
            )
            cambios[alimento] = porcentaje

    # Verificar que haya alimentos para comparar
    if not cambios:
        print("No hay alimentos en común entre hoy y ayer para comparar.")
        return

    # Encontrar el que más bajó y el que más subió
    alimento_baja  = min(cambios, key=cambios.get)
    alimento_sube  = max(cambios, key=cambios.get)

    porcentaje_baja = cambios[alimento_baja]
    porcentaje_sube = cambios[alimento_sube]

    # Mostrar resultados
    print("\n" + "-"*50)
    print(" SUGERENCIAS DEL DÍA")
    print("-"*50)

    print("\n🟢 MAYOR DESCUENTO DEL DÍA:")
    print(f"   {alimento_baja.upper()}")
    print(f"   Variación: {porcentaje_baja:+.1f}%")
    print(f"   Precio hoy: ${precios_hoy[alimento_baja]:,.0f}")
    print(f"   → Buen momento para comprar más cantidad.")

    print("\n🔴 MAYOR SUBIDA DEL DÍA:")
    print(f"   {alimento_sube.upper()}")
    print(f"   Variación: {porcentaje_sube:+.1f}%")
    print(f"   Precio hoy: ${precios_hoy[alimento_sube]:,.0f}")
    print(f"   → Considera buscar un sustituto o reducir uso.")

    print("\n" + "-"*50)

def Historial(alimento=None):
    
    #Muestra el historial de precios guardados.
      
    #El parámetro =None significa que es opcional.
    #Se puede llamar la función así:
        #Historial()           → muestra todos
        #Historial("tomate")   → muestra solo tomate
    

    # Leer el historial
    if not os.path.exists(RUTA_HISTORIAL):
        print("No hay historial guardado todavía.")
        return

    with open(RUTA_HISTORIAL, "r", encoding="utf-8") as archivo:
        historial = json.load(archivo)

    if not historial:
        print("El historial está vacío.")
        return

    # Ordenar las fechas de más antigua a más reciente
    fechas = sorted(historial.keys())

    print("\n" + "-"*50)
    print("   📅 HISTORIAL DE PRECIOS")
    print("-"*50)

    # Leer todos los alimentos que existen en el historial
    # Recorremos todas las fechas y juntamos todos los nombres
    todos_los_alimentos = set()
    for fecha in fechas:
        for nombre in historial[fecha].keys():
            todos_los_alimentos.add(nombre)

    # Si pidieron un alimento específico, filtramos solo ese
    if alimento:
        if alimento not in todos_los_alimentos:
            print(f"No se encontró '{alimento}' en el historial.")
            return
        todos_los_alimentos = [alimento]

    # Mostrar el historial por alimento
    for nombre in sorted(todos_los_alimentos):
        print(f"\n{nombre.upper()}:")

        precio_anterior = None

        for fecha in fechas:
            # Verificar si ese alimento tiene dato en esa fecha
            if nombre in historial[fecha]:
                precio_actual = historial[fecha][nombre]

                # Calcular variación si hay precio anterior
                if precio_anterior is not None:
                    porcentaje = calcular_porcentaje_cambio(
                        precio_actual, precio_anterior
                    )
                    print(f"   {fecha}  →  ${precio_actual:,.0f}  ({porcentaje:+.1f}%)")
                else:
                    # Primera vez que aparece este alimento
                    print(f"   {fecha}  →  ${precio_actual:,.0f}  (primer registro)")

                precio_anterior = precio_actual

def menu_principal():
    while True:

        print("-----MENÚ PRINCIPAL----\n")
        print(datetime.now().strftime("  %Y-%m-%d %H:%M:%S\n "))
        print("  1. Ingresar precios del día")
        print("  2. Ver alertas de precios")
        print("  3. Ver sugerencia de sustitutos")
        print("  4. Ver historial de precios")
        print("  5. Salir")
        opcion = input("Selecciona una opción: ").strip()

        if opcion == "1":
            alimento = input("  ¿Qué alimento quieres registrar? ").strip().lower()
            precio_usuario = float(input("  ¿Cuánto pagaste por kg? $").strip())
            Precios(alimento, precio_usuario)

        elif opcion == "2":
          Alertas()

        elif opcion == "3":
          Sugerencias()

        elif opcion == "4":
          Historial()

        elif opcion == "5":
          print("Muchas gracias por utilizar nuestro sevicios, tayakesrestaurantes le desea un feliz dia.")
          break

        else:
          print("\n  Opción no válida. Por favor, intenta de nuevo.\n")
          return
#  Login
def menu_login():

    print("----SISTEMA DE ALERTAS DE PRECIOS----")
    print("\n   Tayakegg, Cali")

    intentos = 0

    while intentos < MAX_INTENTOS:
        contrasena = input("\n  Ingresa la contraseña: ")

        # Validar entrada vacía
        if contrasena.strip() == "":
            print("\n  X Error: No ingresaste ninguna contraseña.")
            intentos += 1
            restantes = MAX_INTENTOS - intentos
            if restantes > 0:
                print(f"  Te quedan {restantes} intento(s).")
            else:
                print("\n  X Demasiados intentos. Sistema bloqueado.")
                return False
            continue

        # Validar longitud mínima
        if len(contrasena) < 6:
            print("\n  X Error: La contraseña es demasiado corta.")
            intentos += 1
            restantes = MAX_INTENTOS - intentos
            if restantes > 0:
                print(f"  Te quedan {restantes} intento(s).")
            else:
                print("\n  X Demasiados intentos. Sistema bloqueado.")
                return False
            continue

        # Comparar con la contraseña correcta
        if contrasena == CONTRASENA:
            print("\n  ✓ Acceso concedido. Bienvenido.\n")
            menu_principal()  # el menú maneja sus propios errores
            return True
        else:
            intentos += 1
            restantes = MAX_INTENTOS - intentos
            if restantes > 0:
                print(f"  X Contraseña incorrecta. Te quedan {restantes} intento(s).")
            else:
                print("\n  X Demasiados intentos. Sistema bloqueado.")
                return False
            
if __name__ == "__main__":
    menu_login()