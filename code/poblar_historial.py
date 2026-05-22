import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import pandas as pd
import json
import re
from datetime import datetime, timedelta

# Rutas
RUTA_EXCEL     = "data/Precios_sin_hipervinculos.xlsx"
RUTA_HISTORIAL = "data/historial_precios.json"

# Alimentos que le interesan al restaurante 
# Nombre que usará el sistema → palabra clave para buscar en el Excel
ALIMENTOS_CLAVE = {
    "papa"      : "Papa úNica",
    "tomate"    : "Tomate Chonto",
    "cebolla"   : "Cebolla Cabezona Roja",
    "zanahoria" : "Zanahoria",
    "platano"   : "Plátano Hartón Verde Llanero Parejo",
    "yuca"      : "Yuca Llanera",
    "habichuela": "Habichuela",
    "huevo"     : "Huevos AA",
    "limon"     : "Limon Tahití",
    "mazorca"   : "Mazorca",
}

def extraer_kg_de_cantidad(texto_cantidad):
   
    resultado = re.search(r'- ([\d.]+)', str(texto_cantidad))
    if resultado:
        return float(resultado.group(1))
    return 1.0  # si no encuentra nada, asume 1 para no dividir por cero

def leer_precios_excel():

    """
    Lee el Excel y devuelve un diccionario con el precio por kg
    de cada alimento clave.
    
    Devuelve algo así:
    {
        "papa":       1300.0,
        "tomate":     4090.9,
        "cebolla":    2400.0,
        ...
    }
    """
    df = pd.read_excel(RUTA_EXCEL)
    precios = {}

    for clave, nombre_excel in ALIMENTOS_CLAVE.items():
        # Buscar filas que contengan el nombre exacto del producto
        filas = df[df["PRODUCTO"] == nombre_excel]

        if filas.empty:
            print(f"  ⚠ No encontrado en Excel: {nombre_excel}")
            continue

        # Si hay varias filas del mismo producto, sacar el promedio
        precio_total_promedio = filas["PRECIO"].mean()
        cantidad_texto        = filas["CANTIDAD"].iloc[0]
        kg                    = extraer_kg_de_cantidad(cantidad_texto)

        # Convertir a precio por kg
        precio_por_kg = round(precio_total_promedio / kg, 2)
        precios[clave] = precio_por_kg

        print(f"  ✓ {clave:12} → ${precio_total_promedio:,.0f} / {kg}kg = ${precio_por_kg:,.0f}/kg")

    return precios

def crear_historial(precios_hoy):
    
    fecha_hoy  = datetime.now().strftime("%Y-%m-%d")
    fecha_ayer = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

    # Simular precios de ayer: entre 5% y 15% diferentes a los de hoy
    # Usamos variaciones fijas para que sean predecibles y realistas
    variaciones_ayer = {
        "papa"      :  0.10,   # ayer era 10% más barata
        "tomate"    : -0.08,   # ayer era 8% más cara
        "cebolla"   :  0.05,
        "zanahoria" : -0.12,
        "platano"   :  0.07,
        "yuca"      : -0.06,
        "habichuela":  0.15,
        "huevo"     : -0.03,
        "limon"     :  0.20,
        "mazorca"   : -0.09,
    }

    precios_ayer = {}
    for alimento, precio in precios_hoy.items():
        variacion   = variaciones_ayer.get(alimento, 0.05)
        precio_ayer = round(precio * (1 + variacion), 2)
        precios_ayer[alimento] = precio_ayer

    # Construir el historial con ambos días
    historial = {
        fecha_ayer : precios_ayer,
        fecha_hoy  : precios_hoy,
    }

    return historial

def principal():
    print("-" * 50)
    print("  POBLAR HISTORIAL INICIAL")
    print("-" * 50)

    # Crear carpeta data/ si no existe
    os.makedirs("data", exist_ok=True)

    # Verificar que el Excel existe
    if not os.path.exists(RUTA_EXCEL):
        print(f"\nX No se encontró el Excel en: {RUTA_EXCEL}")
        print("  Asegúrate de tener el archivo en la carpeta data/")
        return

    # Leer precios del Excel
    print("\nLeyendo precios del Excel...")
    precios_hoy = leer_precios_excel()

    if not precios_hoy:
        print("\nX No se pudieron leer precios del Excel.")
        return

    # Crear historial con hoy y ayer simulado
    print("\nCreando historial...")
    historial = crear_historial(precios_hoy)

    # Guardar en el archivo JSON
    with open(RUTA_HISTORIAL, "w", encoding="utf-8") as archivo:
        json.dump(historial, archivo, indent=4, ensure_ascii=False)

    print(f"\n✓ Historial creado en: {RUTA_HISTORIAL}")
    print(f"  Días registrados: {list(historial.keys())}")
    print(f"  Alimentos: {list(precios_hoy.keys())}")
    print("\n✓ Listo. Ya puedes correr beta.py normalmente.")
    print("-" * 50)

principal()