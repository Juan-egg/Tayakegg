# 🍽️ TAYAKEGG — Sistema de Alertas de Precios

Sistema de monitoreo de precios de mercado para restaurantes de corrientazo en Cali, Colombia. Permite registrar, comparar y analizar precios de ingredientes del mercado mayorista, además de llevar un control de ganancias diarias.

---

## ¿Qué hace?

- **Ingresar Precios** — Registra el precio que pagaste hoy por cada ingrediente, lo compara con el precio de referencia del mercado y muestra la tendencia reciente
- **Alertas** — Compara los precios de hoy vs ayer y clasifica cada ingrediente en rojo, amarillo o verde según su variación, ordenados por nivel de urgencia
- **Sugerencias** — Identifica el ingrediente con mayor descuento y el que más subió, con sustitutos recomendados y ahorro estimado en pesos
- **Historial** — Muestra la evolución del precio de cada ingrediente con gráfico de tendencia, métricas de mínimo, máximo y promedio
- **Ganancias** — Registra ventas y costos diarios, calcula ganancia neta y muestra gráficos por semana, mes e historial completo

---

## Arquitectura del sistema

### Componentes principales

| Componente | Ubicación | Responsabilidad |
|---|---|---|
| **app.py** | `code/` | Interfaz de usuario en Streamlit |
| **pruebas.py** | `code/` | Lógica de negocio: alertas, cálculos, historial |
| **poblar_historial.py** | `code/` | Inicializa la base de datos desde el Excel |
| **historial_precios.json** | `code/data/` | Almacena el histórico de precios por día |
| **ganancias.json** | `code/data/` | Almacena ventas, costos y ganancias por día |
| **Precios_sin_hipervinculos.xlsx** | `code/data/` | Fuente de precios de referencia del mercado |

---

## Tecnologías utilizadas

- **Python 3** — Lenguaje principal
- **Streamlit** — Interfaz web
- **Pandas** — Lectura y análisis del Excel de precios
- **Plotly** — Gráficos interactivos de tendencias y ganancias
- **JSON** — Base de datos del historial de precios y ganancias
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

## Ingredientes monitoreados (16)

| # | Ingrediente | Unidad |
|---|---|---|
| 01 | 🥔 Papa | kg |
| 02 | 🍅 Tomate | kg |
| 03 | 🧅 Cebolla | kg |
| 04 | 🥕 Zanahoria | kg |
| 05 | 🍌 Plátano | kg |
| 06 | 🌿 Yuca | kg |
| 07 | 🫘 Habichuela | kg |
| 08 | 🥚 Huevo | unidad |
| 09 | 🍋 Limón | kg |
| 10 | 🌽 Mazorca | kg |
| 11 | 🍗 Pollo | kg |
| 12 | 🍊 Lulo | kg |
| 13 | 🍚 Arroz | kg |
| 14 | 🫙 Aceite | litro |
| 15 | 🍯 Panela | unidad |
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
|---|---|
| Login con contraseña correcta | ✅ Acceso concedido |
| Login con contraseña incorrecta | ✅ Bloqueo después de 3 intentos |
| Ingreso de precios con valores válidos | ✅ Guarda en JSON correctamente |
| Ingreso de precio cero | ✅ Muestra advertencia |
| Comparación precio usuario vs mercado | ✅ Calcula diferencia correctamente |
| Alerta roja (subida >15%) | ✅ Se muestra en rojo |
| Alerta amarilla (subida 5-15%) | ✅ Se muestra en amarillo |
| Alerta verde (bajada >5%) | ✅ Se muestra en verde |
| Tarjetas ordenadas por urgencia | ✅ Rojas primero |
| Sustitutos con ahorro en pesos | ✅ Muestra valor en COP |
| Historial con gráfico de tendencia | ✅ Gráfico y tabla funcionan |
| Métricas mínimo, máximo, promedio | ✅ Calculadas correctamente |
| Registro de ventas y costos | ✅ Guarda en ganancias.json |
| Gráfico de ganancias por período | ✅ Tabs 7 días, 30 días, todo |
| Cierre de sesión | ✅ Regresa al login |

---

## 🔮 Trabajo futuro

- [ ] Conexión a API del SIPSA-DANE para precios automáticos del mercado mayorista
- [ ] Notificaciones por WhatsApp cuando hay alertas rojas
- [ ] Exportar historial a PDF o Excel
- [ ] Múltiples usuarios con contraseñas individuales
- [ ] Recomendación automática del menú del día basado en precios bajos
- [ ] Predicción de precios con machine learning

---

## Notas

- La contraseña de acceso debe solicitarse al equipo de desarrollo
- Los precios de referencia del mercado provienen del archivo Excel de Coomproriente — Central de Abastos Cali
- El historial de precios se actualiza automáticamente cada vez que el usuario ingresa precios
- El archivo `ganancias.json` se crea automáticamente la primera vez que se registran ventas
