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

    # Espacio arriba para centrar verticalmente
    st.markdown("<br><br><br>", unsafe_allow_html=True)

    # Columnas para centrar horizontalmente
    col_izq, col_centro, col_der = st.columns([1, 1.5, 1])

    with col_centro:
        with st.container(border=True):

            # Título
            st.markdown("<br>", unsafe_allow_html=True)
            st.title("🍽️ TAYAKEGG")
            st.caption("Sistema de alertas de precios — Cali")
            st.divider()

            # Bloquear si agotó intentos
            if st.session_state.intentos >= pruebas.MAX_INTENTOS:
                st.error("Demasiados intentos. Reinicia la app.")
                return

            # Campo de contraseña
            st.markdown("**Contraseña de acceso**")
            contrasena = st.text_input(
                "Contraseña",
                type="password",
                placeholder="Ingresa tu clave de acceso",
                label_visibility="collapsed"
            )

            # Espacio para mensajes de error
            mensaje = st.empty()

            st.markdown("<br>", unsafe_allow_html=True)

            # Botón
            entrar = st.button(
                "ACCEDER AL SISTEMA",
                type="primary",
                use_container_width=True
            )

            st.markdown("<br>", unsafe_allow_html=True)

            # Lógica del botón
            if entrar:
                if contrasena.strip() == "":
                    mensaje.warning("Ingresa una contraseña.")
                elif len(contrasena) < 6:
                    mensaje.error("La contraseña debe tener al menos 6 caracteres.")
                    st.session_state.intentos += 1
                elif len(contrasena) > 20:
                    mensaje.error("La contraseña no puede tener más de 20 caracteres.")
                    st.session_state.intentos += 1
                elif " " in contrasena:
                    mensaje.error("La contraseña no puede contener espacios.")
                    st.session_state.intentos += 1
                elif contrasena == pruebas.CONTRASENA:
                    st.session_state.autenticado = True
                    st.session_state.intentos = 0
                    st.rerun()
                else:
                    st.session_state.intentos += 1
                    restantes = pruebas.MAX_INTENTOS - st.session_state.intentos
                    if restantes > 0:
                        mensaje.error(f"✗ Contraseña incorrecta. Te quedan {restantes} intento(s).")
                    else:
                        mensaje.error("Demasiados intentos. Sistema bloqueado.")

            # Pie del formulario
            st.divider()
            st.caption(f"📅 {datetime.now().strftime('%d/%m/%Y %H:%M')}  |  Cali, Colombia")


# INGRESAR PRECIOS

def pagina_precios():

    # Encabezado
    col_titulo, col_fecha = st.columns([3, 1])
    with col_titulo:
        st.title("Ingresar Precio del Día")
    with col_fecha:
        st.markdown("<br>", unsafe_allow_html=True)
        st.info(f"📅 {datetime.now().strftime('%d/%m/%Y')}")

    st.divider()

    # Lista de alimentos con emojis para hacerlo más visual
    alimentos = {
        "papa"      : "🥔 Papa",
        "tomate"    : "🍅 Tomate",
        "cebolla"   : "🧅 Cebolla",
        "zanahoria" : "🥕 Zanahoria",
        "platano"   : "🍌 Plátano",
        "yuca"      : "🌿 Yuca",
        "habichuela": "🫘 Habichuela",
        "huevo"     : "🥚 Huevo",
        "limon"     : "🍋 Limón",
        "mazorca"   : "🌽 Mazorca",
        "pollo"     : "🍗 Pollo",
        "lulo"      : "🍊 Lulo",
        "arroz"     : "🍚 Arroz",
        "aceite"    : "🫙 Aceite",
        "panela"    : "🍯 Panela",
        "cilantro"  : "🌱 Cilantro",
    }

    # Formulario principal
    with st.container(border=True):

        st.subheader("Registrar precio")
        st.caption("Ingresa el precio por kg que pagaste hoy en el mercado")
        st.markdown("<br>", unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        with col1:
            alimento_display = st.selectbox(
                "Selecciona el alimento:",
                options=list(alimentos.values()),
            )
            # Convertir el display (con emoji) al key interno
            alimento_key = [k for k, v in alimentos.items()
                           if v == alimento_display][0]

        with col2:
            # Buscar precio de referencia del mercado
            precio_ref = pruebas.buscar_precio_mercado(alimento_key)

            st.number_input(
                "Precio por kg ($):",
                min_value=0,
                step=100,
                value=0,
                key="precio_input",
                help=f"Referencia del mercado: ${precio_ref:,.0f}/kg" if precio_ref else "Sin referencia"
            )

        # Mostrar referencia del mercado como orientación
        if precio_ref:
            st.caption(f"Precio de referencia en el mercado para {alimento_display}: **${precio_ref:,.0f}/kg**")

        st.markdown("<br>", unsafe_allow_html=True)

        guardar = st.button(
            "GUARDAR PRECIO",
            type="primary",
            use_container_width=True
        )

    # Lógica del botón
    if guardar:
        precio_usuario = st.session_state.precio_input

        if precio_usuario == 0:
            st.warning("Ingresa un precio mayor a cero.")
        else:
            pruebas.guardar_precio(alimento_key, float(precio_usuario))

            st.success(f"Precio guardado: {alimento_display} = ${precio_usuario:,}/kg")

            # Comparación con el mercado
            if precio_ref:
                diferencia = precio_usuario - precio_ref
                st.divider()
                st.subheader("Comparación con el mercado")

                c1, c2, c3 = st.columns(3)

                c1.metric(
                    label="Tu precio",
                    value=f"${precio_usuario:,.0f}",
                    help="El precio que tú pagaste"
                )

                c2.metric(
                    label="Precio mercado",
                    value=f"${precio_ref:,.0f}",
                    help="Precio de referencia de la Central de Abastos"
                )

                if diferencia > 0:
                    c3.metric(
                        label="Diferencia",
                        value=f"${abs(diferencia):,.0f}",
                        delta=f"Estás pagando más caro",
                        delta_color="inverse"
                    )
                elif diferencia < 0:
                    c3.metric(
                        label="Diferencia",
                        value=f"${abs(diferencia):,.0f}",
                        delta=f"Estás pagando más barato",
                        delta_color="normal"
                    )
                else:
                    c3.metric(
                        label="Diferencia",
                        value="$0",
                        delta="Precio exacto del mercado"
                    )

            # Historial reciente del alimento
            st.divider()
            st.subheader(f"Últimos precios de {alimento_display}")

            if os.path.exists(pruebas.RUTA_HISTORIAL):
                with open(pruebas.RUTA_HISTORIAL, "r", encoding="utf-8") as f:
                    historial = json.load(f)

                fechas = sorted(historial.keys())

                # Últimos 3 días con dato de ese alimento
                ultimos = []
                for fecha in reversed(fechas):
                    if alimento_key in historial[fecha]:
                        ultimos.append({
                            "Fecha": fecha,
                            "Precio/kg": f"${historial[fecha][alimento_key]:,.0f}"
                        })
                    if len(ultimos) == 3:
                        break

                if ultimos:
                    cols = st.columns(len(ultimos))
                    for i, dato in enumerate(ultimos):
                        cols[i].metric(
                            label=f"📅 {dato['Fecha']}",
                            value=dato["Precio/kg"]
                        )
                else:
                    st.info("No hay registros previos de este alimento.")



# PÁGINA: ALERTAS

def pagina_alertas():

    # Encabezado
    col_titulo, col_fecha = st.columns([3, 1])
    with col_titulo:
        st.title("Alertas de Precios")
    with col_fecha:
        st.markdown("<br>", unsafe_allow_html=True)
        st.info(f"📅 {datetime.now().strftime('%d/%m/%Y')}")

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

    # Recopilar todos los alimentos
    todos_alimentos = set()
    for fecha in fechas:
        for alimento in historial[fecha].keys():
            todos_alimentos.add(alimento)

    # Para cada alimento buscar precio más reciente y anterior
    precios_hoy = {}
    precios_ayer = {}

    for alimento in todos_alimentos:
        fechas_con_dato = [f for f in fechas if alimento in historial[f]]

        if len(fechas_con_dato) >= 1:
            ultima_fecha = fechas_con_dato[-1]
            precios_hoy[alimento] = historial[ultima_fecha][alimento]

        if len(fechas_con_dato) >= 2:
            penultima_fecha = fechas_con_dato[-2]
            precios_ayer[alimento] = historial[penultima_fecha][alimento]

    if not precios_hoy:
        st.warning("No hay precios registrados.")
        return

    # Calcular alertas para todos los alimentos
    resultados = []

    for ingrediente, precio_actual in precios_hoy.items():
        if ingrediente in precios_ayer:
            precio_anterior = precios_ayer[ingrediente]
            porcentaje = pruebas.calcular_porcentaje_cambio(
                precio_actual, precio_anterior
            )
            alerta = pruebas.clasificar_alerta(porcentaje)
        else:
            porcentaje = 0
            alerta = "PRIMER REGISTRO"

        resultados.append({
            "ingrediente" : ingrediente,
            "precio_actual": precio_actual,
            "precio_anterior": precios_ayer.get(ingrediente, None),
            "porcentaje"  : porcentaje,
            "alerta"      : alerta,
        })

    # Ordenar por nivel de alerta — rojas primero
    orden_alerta = {
        "ALERTA ROJA"      : 0,
        "ALERTA AMARILLA"  : 1,
        "OPORTUNIDAD VERDE": 2,
        "BAJADA LEVE"      : 3,
        "PRECIO ESTABLE"   : 4,
        "PRIMER REGISTRO"  : 5,
    }
    resultados.sort(key=lambda x: orden_alerta.get(x["alerta"], 6))

    # Contadores para el resumen
    contador_rojas    = sum(1 for r in resultados if "ROJA"    in r["alerta"])
    contador_amarillas = sum(1 for r in resultados if "AMARILLA" in r["alerta"])
    contador_verdes   = sum(1 for r in resultados if "VERDE"   in r["alerta"]
                           or "LEVE" in r["alerta"])
    contador_estables = sum(1 for r in resultados if "ESTABLE" in r["alerta"]
                           or "REGISTRO" in r["alerta"])

    # RESUMEN ARRIBA
    st.subheader("📋 Resumen del día")
    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        label="🔴 Críticos",
        value=contador_rojas,
        help="Subieron más del 15%"
    )
    c2.metric(
        label="🟡 Precaución",
        value=contador_amarillas,
        help="Subieron entre 5% y 15%"
    )
    c3.metric(
        label="🟢 Oportunidades",
        value=contador_verdes,
        help="Bajaron más del 5%"
    )
    c4.metric(
        label="⚪ Estables",
        value=contador_estables,
        help="Cambio menor al 5%"
    )

    st.divider()
    st.subheader("Detalle por alimento")
    st.caption("Ordenados por nivel de alerta — los más críticos primero")
    st.markdown("<br>", unsafe_allow_html=True)

    # Emojis para cada alimento
    emojis = {
        "papa"      : "🥔", "tomate"    : "🍅",
        "cebolla"   : "🧅", "zanahoria" : "🥕",
        "platano"   : "🍌", "yuca"      : "🌿",
        "habichuela": "🫘", "huevo"     : "🥚",
        "limon"     : "🍋", "mazorca"   : "🌽",
        "pollo"     : "🍗", "lulo"      : "🍊",
        "arroz"     : "🍚", "aceite"    : "🫙",
        "panela"    : "🍯", "cilantro"  : "🌱",
    }

    # TARJETAS EN FILAS DE 4
    COLUMNAS = 4

    for i in range(0, len(resultados), COLUMNAS):
        cols = st.columns(COLUMNAS)
        grupo = resultados[i : i + COLUMNAS]

        for j, r in enumerate(grupo):
            with cols[j]:
                with st.container(border=True):

                    alerta   = r["alerta"]
                    pct      = r["porcentaje"]
                    emoji    = emojis.get(r["ingrediente"], "🛒")
                    nombre   = r["ingrediente"].upper()
                    precio   = r["precio_actual"]
                    precio_a = r["precio_anterior"]

                    # Nombre con emoji
                    st.markdown(f"### {emoji} {nombre}")

                    # Precio actual
                    if precio_a:
                        if pct > 0:
                            st.metric(
                                label="Precio hoy",
                                value=f"${precio:,.0f}/kg",
                                delta=f"+{pct:.1f}% vs ayer",
                                delta_color="inverse"
                            )
                        elif pct < 0:
                            st.metric(
                                label="Precio hoy",
                                value=f"${precio:,.0f}/kg",
                                delta=f"{pct:.1f}% vs ayer",
                                delta_color="green"
                            )
                        else:
                            st.metric(
                                label="Precio hoy",
                                value=f"${precio:,.0f}/kg",
                                delta="Sin cambio",
                                delta_color="off"
                            )
                    else:
                        st.metric(
                            label="Precio hoy",
                            value=f"${precio:,.0f}/kg"
                        )
                                        
                    # alerta con color coherente
                    if "ROJA" in alerta:
                        st.error(f"🔴 {alerta}")
                    elif "AMARILLA" in alerta:
                        st.warning(f"🟡 {alerta}")
                    elif "VERDE" in alerta:
                        st.success(f"🟢 {alerta}")
                    elif "LEVE" in alerta:
                        st.success(f"🟢 BAJADA LEVE")
                    elif "ESTABLE" in alerta:
                        st.info(f"⚪ {alerta}")
                    else:
                        st.info(f"⚪ {alerta}")

                    # Precio de ayer como referencia
                    if precio_a:
                        st.caption(f"Ayer: ${precio_a:,.0f}/kg")

# SUGERENCIAS

def pagina_sugerencias():

    # Encabezado
    col_titulo, col_fecha = st.columns([3, 1])
    with col_titulo:
        st.title("Sugerencias del Día")
    with col_fecha:
        st.markdown("<br>", unsafe_allow_html=True)
        st.info(f"📅 {datetime.now().strftime('%d/%m/%Y')}")

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

    # Calcular cambios de todos los alimentos
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

    # Emojis
    emojis = {
        "papa"      : "🥔", "tomate"    : "🍅",
        "cebolla"   : "🧅", "zanahoria" : "🥕",
        "platano"   : "🍌", "yuca"      : "🌿",
        "habichuela": "🫘", "huevo"     : "🥚",
        "limon"     : "🍋", "mazorca"   : "🌽",
        "pollo"     : "🍗", "lulo"      : "🍊",
        "arroz"     : "🍚", "aceite"    : "🫙",
        "panela"    : "🍯", "cilantro"  : "🌱",
    }

    # Alimento que más bajó y más subió
    alimento_baja = min(cambios, key=cambios.get)
    alimento_sube = max(cambios, key=cambios.get)

    
    st.subheader("Destacados del día")
    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        with st.container(border=True):
            st.success("🟢 MAYOR DESCUENTO DEL DÍA")
            st.markdown("<br>", unsafe_allow_html=True)

            emoji = emojis.get(alimento_baja, "🛒")
            st.markdown(f"### {emoji} {alimento_baja.upper()}")

            st.metric(
                label="Precio hoy",
                value=f"${precios_hoy[alimento_baja]:,.0f}/kg",
                delta=f"{cambios[alimento_baja]:+.1f}% vs ayer",
                delta_color="green"
            )
            st.markdown("<br>", unsafe_allow_html=True)
            st.info("Buen momento para comprar más cantidad y stockearte.")

    with col2:
        with st.container(border=True):
            st.error("🔴 MAYOR SUBIDA DEL DÍA")
            st.markdown("<br>", unsafe_allow_html=True)

            emoji = emojis.get(alimento_sube, "🛒")
            st.markdown(f"### {emoji} {alimento_sube.upper()}")

            st.metric(
                label="Precio hoy",
                value=f"${precios_hoy[alimento_sube]:,.0f}/kg",
                delta=f"{cambios[alimento_sube]:+.1f}% vs ayer",
                delta_color="inverse"
            )
            st.markdown("<br>", unsafe_allow_html=True)
            st.warning("Considera buscar un sustituto o reducir su uso.")

   
    # Todos los que bajaron excepto el que ya mostramos arriba
    oportunidades = {
        a: pct for a, pct in cambios.items()
        if pct < 0 and a != alimento_baja
    }

    if oportunidades:
        st.divider()
        st.subheader("Otras oportunidades del día")
        st.caption("Alimentos que bajaron de precio hoy ordenados de mayor a menor descuento")
        st.markdown("<br>", unsafe_allow_html=True)

        # Ordenar de mayor descuento a menor
        oportunidades_ordenadas = sorted(
            oportunidades.items(),
            key=lambda x: x[1]  # el más negativo primero
        )

        COLUMNAS = 4
        for i in range(0, len(oportunidades_ordenadas), COLUMNAS):
            cols = st.columns(COLUMNAS)
            grupo = oportunidades_ordenadas[i : i + COLUMNAS]

            for j, (alimento, pct) in enumerate(grupo):
                with cols[j]:
                    with st.container(border=True):
                        emoji = emojis.get(alimento, "🛒")
                        st.markdown(f"**{emoji} {alimento.upper()}**")
                        st.metric(
                            label="Precio hoy",
                            value=f"${precios_hoy[alimento]:,.0f}/kg",
                            delta=f"{pct:.1f}% vs ayer",
                            delta_color="green"
                        )

    
    subidas = {
        a: pct for a, pct in cambios.items()
        if pct > 5 and a != alimento_sube
    }

    if subidas:
        st.divider()
        st.subheader("También subieron")
        st.caption("Alimentos con subida considerable — ten precaución")
        st.markdown("<br>", unsafe_allow_html=True)

        subidas_ordenadas = sorted(
            subidas.items(),
            key=lambda x: x[1],
            reverse=True  # el que más subió primero
        )

        COLUMNAS = 4
        for i in range(0, len(subidas_ordenadas), COLUMNAS):
            cols = st.columns(COLUMNAS)
            grupo = subidas_ordenadas[i : i + COLUMNAS]

            for j, (alimento, pct) in enumerate(grupo):
                with cols[j]:
                    with st.container(border=True):
                        emoji = emojis.get(alimento, "🛒")
                        st.markdown(f"**{emoji} {alimento.upper()}**")
                        st.metric(
                            label="Precio hoy",
                            value=f"${precios_hoy[alimento]:,.0f}/kg",
                            delta=f"+{pct:.1f}% vs ayer",
                            delta_color="inverse" 
                        )



#  HISTORIAL

def pagina_historial():

    # Encabezado
    col_titulo, col_fecha = st.columns([3, 1])
    with col_titulo:
        st.title("📅 Historial de Precios")
    with col_fecha:
        st.markdown("<br>", unsafe_allow_html=True)
        st.info(f"📅 {datetime.now().strftime('%d/%m/%Y')}")

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

    # Recopilar todos los alimentos
    todos = set()
    for fecha in fechas:
        for nombre in historial[fecha].keys():
            todos.add(nombre)

    # Emojis
    emojis = {
        "papa"      : "🥔", "tomate"    : "🍅",
        "cebolla"   : "🧅", "zanahoria" : "🥕",
        "platano"   : "🍌", "yuca"      : "🌿",
        "habichuela": "🫘", "huevo"     : "🥚",
        "limon"     : "🍋", "mazorca"   : "🌽",
        "pollo"     : "🍗", "lulo"      : "🍊",
        "arroz"     : "🍚", "aceite"    : "🫙",
        "panela"    : "🍯", "cilantro"  : "🌱",
    }

    # Opciones del selector con emoji
    opciones = {
        f"{emojis.get(n, '🛒')} {n.upper()}": n
        for n in sorted(todos)
    }

    # ── SELECTOR + MÉTRICAS RÁPIDAS ─────────────────────────
    col_sel, col_min, col_max, col_prom = st.columns([2, 1, 1, 1])

    with col_sel:
        alimento_display = st.selectbox(
            "Selecciona un alimento:",
            options=list(opciones.keys()),
            key="selector_historial"
        )
        alimento_sel = opciones[alimento_display]

    # Construir datos para ese alimento
    filas = []
    precio_anterior = None
    precios_lista = []

    for fecha in fechas:
        if alimento_sel in historial[fecha]:
            precio = historial[fecha][alimento_sel]
            precios_lista.append(precio)

            if precio_anterior is not None:
                variacion = pruebas.calcular_porcentaje_cambio(
                    precio, precio_anterior
                )
            else:
                variacion = None

            filas.append({
                "Fecha"    : fecha,
                "Precio/kg": precio,
                "Variación": f"{variacion:+.1f}%" if variacion is not None
                             else "Primer registro"
            })
            precio_anterior = precio

    # Métricas rápidas — se calculan solo si hay datos
    if precios_lista:
        precio_min  = min(precios_lista)
        precio_max  = max(precios_lista)
        precio_prom = sum(precios_lista) / len(precios_lista)

        with col_min:
            st.markdown("<br>", unsafe_allow_html=True)
            st.metric(
                label="Mínimo",
                value=f"${precio_min:,.0f}",
                help="Precio más bajo del período"
            )
        with col_max:
            st.markdown("<br>", unsafe_allow_html=True)
            st.metric(
                label="Máximo",
                value=f"${precio_max:,.0f}",
                help="Precio más alto del período"
            )
        with col_prom:
            st.markdown("<br>", unsafe_allow_html=True)
            st.metric(
                label="Promedio",
                value=f"${precio_prom:,.0f}",
                help="Precio promedio del período"
            )

    st.divider()

    if not filas:
        st.info(f"No hay datos de '{alimento_sel}' en el historial.")
        return

    # ── GRÁFICO ─────────────────────────────────────────────
    st.subheader(f"Tendencia de precio — {alimento_display}")

    df_grafico = pd.DataFrame(filas).set_index("Fecha")
    st.line_chart(
        df_grafico["Precio/kg"],
        use_container_width=True,
        height=350,
    )

    st.divider()

    # ── TABLA DETALLADA ──────────────────────────────────────
    st.subheader("Detalle por fecha")
    st.caption(f"Registros disponibles: {len(filas)} días")

    # Agregar columna de tendencia visual
    filas_display = []
    for fila in filas:
        variacion_texto = fila["Variación"]
        if variacion_texto == "Primer registro":
            tendencia = "—"
        elif "+" in variacion_texto:
            tendencia = "↑ Subió"
        else:
            tendencia = "↓ Bajó"

        filas_display.append({
            "Fecha"    : fila["Fecha"],
            "Precio/kg": f"${fila['Precio/kg']:,.0f}",
            "Variación": fila["Variación"],
            "Tendencia": tendencia,
        })

    st.dataframe(
        pd.DataFrame(filas_display),
        use_container_width=True,
        hide_index=True,
        column_config={
            "Fecha"    : st.column_config.TextColumn("📅 Fecha"),
            "Precio/kg": st.column_config.TextColumn("Precio/kg"),
            "Variación": st.column_config.TextColumn("Variación"),
            "Tendencia": st.column_config.TextColumn("Tendencia"),
        }
    )


# NAVEGACIÓN PRINCIPAL

def app_principal():
    with st.sidebar:

        # Título
        st.markdown("# 🍽️ TAYAKEGG")
        st.caption("Sistema de alertas de precios")
        st.caption("Cali, Colombia")
        st.divider()

        # Menú
        st.markdown("**MENÚ PRINCIPAL**")
        st.markdown("<br>", unsafe_allow_html=True)

        pagina = st.radio(
            "Navegar a:",
            options=[
                "Ingresar Precios",
                "Alertas",
                "Sugerencias",
                "Historial"
            ],
            label_visibility="collapsed"
        )

        st.divider()

        # Botón cerrar sesión
        if st.button("🚪 Cerrar sesión"):
            st.session_state.autenticado = False
            st.rerun()

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