import streamlit as st
import os
import json
import pandas as pd
from datetime import datetime

# Lo mismo que en pruebas.py — fijar directorio
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Importar todas las funciones del backend

import pruebas


# CONFIGURACIÓN INICIAL DE LA APP
# st.set_page_config SIEMPRE va primero

st.set_page_config(
    page_title="Tayakegg",
    page_icon="🛒",
    layout="wide"
)



# Si estas variables no existen todavía, las creamos

if "autenticado" not in st.session_state:
    st.session_state.autenticado = False

if "intentos" not in st.session_state:
    st.session_state.intentos = 0

if "pagina" not in st.session_state:
    st.session_state.pagina = "Ingresar Precios"



def pagina_login():
    st.title("🍽️ TAYAKEGG")
    st.subheader("Sistema de alertas de precios — Cali")
    st.divider()

    # Bloquear si ya agotó intentos
    if st.session_state.intentos >= pruebas.MAX_INTENTOS:
        st.error("X Demasiados intentos. Reinicia la app.")
        return

    contrasena = st.text_input(
        "Contraseña:",
        type="password",
        placeholder="Ingresa la contraseña del sistema"
    )

    if st.button("Entrar", type="primary"):
        if contrasena.strip() == "":
            st.warning("Por favor, ingresa una contraseña.")
        elif len(contrasena) < 6:
            st.error("La contraseña debe tener al menos 6 caracteres.")
            st.session_state.intentos += 1

        # Validación 3: demasiado larga
        elif len(contrasena) > 12:
            st.error("La contraseña no puede tener más de 12 caracteres.")
            st.session_state.intentos += 1

        # Validación 4: contiene espacios
        elif " " in contrasena:
            st.error("La contraseña no puede contener espacios.")
            st.session_state.intentos += 1

        # Validación 5: comparar con la correcta
        elif contrasena == pruebas.CONTRASENA:
            st.session_state.autenticado = True
            st.session_state.intentos = 0
            st.rerun()
        else:
            st.session_state.intentos += 1
            restantes = pruebas.MAX_INTENTOS - st.session_state.intentos
            if restantes > 0:
                st.error(f"Contraseña incorrecta. Te quedan {restantes} intento(s).")
            else:
                st.error("X Demasiados intentos. Sistema bloqueado.")



# INGRESAR PRECIOS

def pagina_precios():
    st.header("Ingresar Precio del Día")
    st.caption(f"Fecha: {datetime.now().strftime('%d/%m/%Y')}")
    st.divider()

    # Lista de alimentos disponibles
    alimentos_disponibles = [
        "papa", "tomate", "cebolla", "zanahoria",
        "platano", "yuca", "habichuela", "huevo",
        "limon", "mazorca"
    ]

    col1, col2 = st.columns(2)

    with col1:
        alimento = st.selectbox(
            "¿Qué alimento quieres registrar?",
            options=alimentos_disponibles
        )

    with col2:
        precio_usuario = st.number_input(
            "¿Cuánto pagaste por kg? ($)",
            min_value=0,
            step=100,
            value=0
        )

    if st.button("💾 Guardar precio", type="primary"):
        if precio_usuario == 0:
            st.warning(" X Ingresa un precio mayor a cero.")
        else:
            # Buscar precio del mercado
            precio_mercado = pruebas.buscar_precio_mercado(alimento)

            # Guardar en el historial
            pruebas.guardar_precio(alimento, float(precio_usuario))

            st.success(f"✅ Precio guardado: {alimento} = ${precio_usuario:,}/kg")

            # Mostrar comparación con el mercado
            if precio_mercado:
                diferencia = precio_usuario - precio_mercado
                st.divider()
                col1, col2, col3 = st.columns(3)
                col1.metric("Tu precio", f"${precio_usuario:,.0f}")
                col2.metric("Precio mercado", f"${precio_mercado:,.0f}")
                if diferencia > 0:
                    col3.metric(
                        "Diferencia",
                        f"${abs(diferencia):,.0f}",
                        delta=f"+{diferencia:,.0f} más caro",
                        delta_color="inverse"
                    )
                elif diferencia < 0:
                    col3.metric(
                        "Diferencia",
                        f"${abs(diferencia):,.0f}",
                        delta=f"{diferencia:,.0f} más barato",
                        delta_color="normal"
                    )
                else:
                    col3.metric("Diferencia", "$0", delta="Precio exacto")



# PÁGINA: ALERTAS

def pagina_alertas():
    st.header("Alertas de Precios")
    st.caption(f"Análisis del {datetime.now().strftime('%d/%m/%Y')}")
    st.divider()

    # Leer historial
    if not os.path.exists(pruebas.RUTA_HISTORIAL):
        st.warning("No hay historial. Ingresa precios primero.")
        return

    with open(pruebas.RUTA_HISTORIAL, "r", encoding="utf-8") as archivo:
        historial = json.load(archivo)

    if not historial:
        st.warning("El historial está vacío.")
        return

    fechas = sorted(historial.keys())

    # Recopilar todos los alimentos que existen en cualquier fecha
    todos_alimentos = set()
    for fecha in fechas:
        for alimento in historial[fecha].keys():
            todos_alimentos.add(alimento)

    # Para cada alimento, buscar su precio más reciente
    # y el precio del día anterior a ese
    precios_hoy = {}
    precios_ayer = {}

    for alimento in todos_alimentos:
        # Buscar en qué fechas aparece este alimento
        fechas_con_dato = [f for f in fechas if alimento in historial[f]]
        
        if len(fechas_con_dato) >= 1:
            # Precio más reciente
            ultima_fecha = fechas_con_dato[-1]
            precios_hoy[alimento] = historial[ultima_fecha][alimento]
        
        if len(fechas_con_dato) >= 2:
            # Precio anterior al más reciente
            penultima_fecha = fechas_con_dato[-2]
            precios_ayer[alimento] = historial[penultima_fecha][alimento]

    if not precios_hoy:
        st.warning("No hay precios de hoy. Ve a Ingresar Precios primero.")
        return

    # Contadores para el resumen
    contador_rojas = 0
    contador_amarillas = 0
    contador_verdes = 0

    # Mostrar cada alimento
    for ingrediente, precio_actual in precios_hoy.items():
        if ingrediente in precios_ayer:
            precio_anterior = precios_ayer[ingrediente]
            porcentaje = pruebas.calcular_porcentaje_cambio(precio_actual, precio_anterior)
            alerta = pruebas.clasificar_alerta(porcentaje)

            # Elegir color según alerta
            if "ROJA" in alerta:
                color = "🔴"
                contador_rojas += 1
            elif "AMARILLA" in alerta:
                color = "🟡"
                contador_amarillas += 1
            elif "VERDE" in alerta:
                color = "🟢"
                contador_verdes += 1
            else:
                color = "⚪"

            st.metric(
                label=f"{color} {ingrediente.upper()} — {alerta}",
                value=f"${precio_actual:,.0f}/kg",
                delta=f"{porcentaje:+.1f}% vs ayer (${precio_anterior:,.0f})",
                delta_color="inverse" if porcentaje > 0 else "normal"
            )
        else:
            st.info(f"⚪ {ingrediente.upper()} — Primer registro: ${precio_actual:,.0f}/kg")

    # Resumen final
    st.divider()
    st.subheader("📋 Resumen del día")
    c1, c2, c3 = st.columns(3)
    c1.metric("🔴 Alertas Rojas",    contador_rojas)
    c2.metric("🟡 Alertas Amarillas", contador_amarillas)
    c3.metric("🟢 Oportunidades",     contador_verdes)


# SUGERENCIAS

def pagina_sugerencias():
    st.header("Sugerencias del Día")
    st.divider()

    if not os.path.exists(pruebas.RUTA_HISTORIAL):
        st.warning("No hay historial todavía.")
        return

    with open(pruebas.RUTA_HISTORIAL, "r", encoding="utf-8") as archivo:
        historial = json.load(archivo)

    fechas = sorted(historial.keys())

    if len(fechas) < 2:
        st.info("Necesitas al menos 2 días de precios para ver sugerencias.")
        return

    precios_hoy  = historial[fechas[-1]]
    precios_ayer = historial[fechas[-2]]

    cambios = {}
    for alimento in precios_hoy:
        if alimento in precios_ayer:
            cambios[alimento] = pruebas.calcular_porcentaje_cambio(
                precios_hoy[alimento],
                precios_ayer[alimento]
            )

    if not cambios:
        st.warning("No hay alimentos en común entre hoy y ayer.")
        return

    alimento_baja = min(cambios, key=cambios.get)
    alimento_sube = max(cambios, key=cambios.get)

    col1, col2 = st.columns(2)

    with col1:
        st.success("🟢 MAYOR DESCUENTO DEL DÍA")
        st.metric(
            label=alimento_baja.upper(),
            value=f"${precios_hoy[alimento_baja]:,.0f}/kg",
            delta=f"{cambios[alimento_baja]:+.1f}%",
            delta_color="normal"
        )
        st.caption("→ Buen momento para comprar más cantidad.")

    with col2:
        st.error("🔴 MAYOR SUBIDA DEL DÍA")
        st.metric(
            label=alimento_sube.upper(),
            value=f"${precios_hoy[alimento_sube]:,.0f}/kg",
            delta=f"{cambios[alimento_sube]:+.1f}%",
            delta_color="inverse"
        )
        st.caption("→ Considera buscar un sustituto o reducir uso.")



#  HISTORIAL

def pagina_historial():
    st.header(" Historial de Precios")
    st.divider()

    if not os.path.exists(pruebas.RUTA_HISTORIAL):
        st.warning("No hay historial todavía.")
        return

    with open(pruebas.RUTA_HISTORIAL, "r", encoding="utf-8") as archivo:
        historial = json.load(archivo)

    if not historial:
        st.warning("El historial está vacío.")
        return

    fechas = sorted(historial.keys())

    todos = set()
    for fecha in fechas:
        for nombre in historial[fecha].keys():
            todos.add(nombre)

    alimento_sel = st.selectbox(
        "Selecciona un alimento:",
        options=sorted(todos),
        key="selector_historial"
    )

    filas = []
    precio_anterior = None

    for fecha in fechas:
        if alimento_sel in historial[fecha]:
            precio = historial[fecha][alimento_sel]
            if precio_anterior is not None:
                variacion = pruebas.calcular_porcentaje_cambio(precio, precio_anterior)
            else:
                variacion = None
            filas.append({
                "Fecha":     fecha,
                "Precio/kg": precio,
                "Variación": f"{variacion:+.1f}%" if variacion is not None else "Primer registro"
            })
            precio_anterior = precio

    if not filas:
        st.info(f"No hay datos de '{alimento_sel}' en el historial.")
        return

    # Gráfico
    df_grafico = pd.DataFrame(filas).set_index("Fecha")
    st.line_chart(df_grafico["Precio/kg"], use_container_width=True)

    # Tabla — una sola vez
    st.subheader("Detalle por fecha")
    st.dataframe(
        pd.DataFrame(filas),
        use_container_width=True,
        hide_index=True
    )


# NAVEGACIÓN PRINCIPAL

def app_principal():
    with st.sidebar:
        st.markdown("## 🍽️ TAYAKEGG")
        st.caption("Sistema de alertas de precios")
        st.divider()

        pagina = st.radio(
            "Navegar a:",
            options=[
                "Ingresar Precios",
                "Alertas",
                "Sugerencias",
                "Historial"
            ]
        )

        st.divider()
        if st.button("Cerrar sesión"):
            st.session_state.autenticado = False
            st.session_state.intentos = 0
            st.rerun()

        st.caption(f" {datetime.now().strftime('%d/%m/%Y %H:%M')}")

    # Mostrar la página seleccionada
    if pagina == "Ingresar Precios":
        pagina_precios()
    elif pagina == "Alertas":
        pagina_alertas()
    elif pagina == "Sugerencias":
        pagina_sugerencias()
    elif pagina == "Historial":
        pagina_historial()



if st.session_state.autenticado:
    app_principal()
else:
    pagina_login()