# 🍽️ TAYAKEGG — Sistema de Alertas de Precios

Sistema de monitoreo de precios de mercado para restaurantes de corrientazo en Cali, Colombia. Permite registrar, comparar y analizar precios de ingredientes del mercado mayorista.

---

## ¿Qué hace?

- **Ingresar Precios** — Registra el precio que pagaste hoy por cada ingrediente y lo compara automáticamente con el precio de referencia
- **Alertas** — Compara los precios de hoy vs ayer y clasifica cada ingrediente en rojo, amarillo o verde según su variación
- **Sugerencias** — Identifica el ingrediente con mayor descuento del día y el que más subió, con recomendaciones de acción
- **Historial** — Muestra la evolución del precio de cada ingrediente a lo largo del tiempo con gráfico y tabla detallada

---

## Arquitectura del sistema

### Componentes principales

| Componente | Ubicación | Responsabilidad |
|------------|-----------|-----------------|
| **app.py** | `code/` | Interfaz de usuario en Streamlit |
| **pruebas.py** | `code/` | Lógica de negocio: alertas, sugerencias |
| **poblar_historial.py** | `code/` | Inicializa base de datos desde Excel |
| **historial_precios.json** | `code/data/` | Almacena histórico de precios |
| **Precios_sin_hipervinculos.xlsx** | `code/data/` | Fuente de datos del mercado |


---

## Tecnologías utilizadas

- **Python 3** — Lenguaje principal
- **Streamlit** — Interfaz web
- **Pandas** — Lectura y análisis del Excel de precios
- **JSON** — Base de datos del historial de precios
- **openpyxl** — Lectura de archivos Excel
- **Git / GitHub** — Control de versiones

---



## Cómo correrlo

### 1. Clonar el repositorio
```bash
git clone https://github.com/Juan-egg/Tayakegg.git
cd Tayakegg
```

### 2. Crear entorno virtual
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Instalar dependencias
```bash
pip install streamlit pandas openpyxl plotly
```

### 4. Inicializar el historial (solo la primera vez)
```bash
python code/poblar_historial.py
```

### 5. Correr la app
```bash
streamlit run code/app.py
```

La app abre automáticamente en `http://localhost:8501`

---

## Ingredientes monitoreados

| # | Ingrediente | Unidad |
|---|---|---|
| 01 | 🥔 Papa | kg |
| 02 | 🍅 Tomate | kg |
| 03 | 🧅 Cebolla | kg |
| 04 | 🥕 Zanahoria | kg |
| 05 | 🍌 Plátano | kg |
| 06 | 🌿 Yuca | kg |
| 07 | 🫘 Habichuela | kg |
| 08 | 🥚 Huevo | kg |
| 09 | 🍋 Limón | kg |
| 10 | 🌽 Mazorca | kg |
| 11 | 🍗 Pollo | kg |
| 12 | 🍊 Lulo | kg |
| 13 | 🍚 Arroz | kg |
| 14 | 🫙 Aceite | litro |
| 15 | 🍯 Panela | und |
| 16 | 🌱 Cilantro | atado |

---

## Sistema de alertas

| Color | Condición | Acción recomendada |
|---|---|---|
| 🔴 Rojo | Subió más del 15% | Buscar sustituto urgente |
| 🟡 Amarillo | Subió entre 5% y 15% | Monitorear de cerca |
| 🟢 Verde | Bajó más del 5% | Buen momento para comprar |
| ⚪ Estable | Cambio menor al 5% | Sin acción necesaria |

---

## ✅ Pruebas realizadas

| Prueba | Resultado |
|--------|-----------|
| Login con contraseña correcta | ✅ Acceso concedido |
| Login con contraseña incorrecta | ✅ Bloqueo después de 3 intentos |
| Ingreso de precios (números válidos) | ✅ Guarda correctamente |
| Ingreso de precios (texto en lugar de números) | ✅ Muestra error y pide reintentar |
| Alerta roja (>15% subida) | ✅ Se muestra correctamente |
| Alerta amarilla (5-15% subida) | ✅ Se muestra correctamente |
| Alerta verde (>5% bajada) | ✅ Se muestra correctamente |
| Cálculo de ahorro en sustitutos | ✅ Muestra valor en pesos |
| Historial con múltiples días | ✅ Gráfico y tabla funcionan |


## 🔮 Trabajo futuro

- [ ] Conexión a API real de precios de la Central de Abastos
- [ ] Notificaciones por WhatsApp cuando hay alertas rojas
- [ ] Exportar historial a PDF o Excel
- [ ] Modo oscuro / claro en la interfaz
- [ ] Múltiples usuarios con sus propios precios
- [ ] Recomendación automática del menú del día basado en precios bajos

## Notas

- La contraseña de acceso debe solicitarse al equipo de desarrollo
- Los precios de referencia del mercado provienen del archivo Excel de Coomproriente
- El historial se actualiza automáticamente cada vez que el usuario ingresa precios
