<div align="center">

```
██╗   ██╗███████╗███╗   ██╗██████╗  █████╗ ██╗   ██╗ █████╗ ██╗
██║   ██║██╔════╝████╗  ██║██╔══██╗██╔══██╗██║   ██║██╔══██╗██║
██║   ██║█████╗  ██╔██╗ ██║██║  ██║███████║██║   ██║███████║██║
╚██╗ ██╔╝██╔══╝  ██║╚██╗██║██║  ██║██╔══██║╚██╗ ██╔╝██╔══██║██║
 ╚████╔╝ ███████╗██║ ╚████║██████╔╝██║  ██║ ╚████╔╝ ██║  ██║███████╗
  ╚═══╝  ╚══════╝╚═╝  ╚═══╝╚═════╝ ╚═╝  ╚═╝  ╚═══╝  ╚═╝  ╚═╝╚══════╝
```

**Sistema de Monitorización Meteorológica para España**

[![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Rich](https://img.shields.io/badge/Rich-CLI-00C7B7?style=for-the-badge)](https://rich.readthedocs.io/)
[![WeatherAPI](https://img.shields.io/badge/WeatherAPI-Live_Data-FF6B35?style=for-the-badge)](https://www.weatherapi.com/)
[![pytest](https://img.shields.io/badge/pytest-tested-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white)](https://pytest.org/)

*Registra · Consulta · Alerta · Visualiza*

</div>

---

## 🎬 Ve la app en acción antes de instalarla

> **¿No sabes si te va a gustar? ¡Mira primero!**

| Video | Descripción |
|-------|-------------|
| ▶️ [**Demo de la app 1**](https://youtu.be/3hFjrRq-mt0) | Ve cómo funciona el menú, el registro y las alertas |
| ▶️ [**Demo de la app 2**](https://youtu.be/_EKjp1RLyEs) | Errores de API/Log y comparativa registro manual/ingesta API |

---

## 🌪️ ¿Qué es Proyecto Vendaval?

**Vendaval** es una aplicación de consola hecha en **Python** que monitoriza el tiempo en ciudades de España.

Con ella puedes:

- 📝 **Registrar** datos climáticos manualmente (temperatura, humedad, viento, lluvia)
- 🌐 **Obtener** datos en tiempo real desde la API de WeatherAPI
- 🚨 **Recibir alertas** automáticas cuando los valores son peligrosos
- 📊 **Consultar** el histórico de tiempo y alertas filtrado por ciudad y fecha
- 📈 **Ver estadísticas** en un dashboard gráfico interactivo
- 🔄 **Comparar** tus registros manuales con los datos reales de la API

Todo desde la terminal, con una interfaz colorida y fácil de usar.

---

## 🧠 ¿Tienes dudas? Habla con el Mentor del proyecto

> Hay un **GPT personalizado** que conoce toda la estructura del proyecto. Puedes preguntarle cualquier cosa: cómo instalar, cómo funciona un módulo, qué hace cada función...

### 👉 [Abrir Vendaval Mentor](https://chatgpt.com/g/g-69e7e4fe031881919ba294fa89d471d9-vendaval-mentor)

*Te responde como un profesor o mentor, adaptado al nivel de cada persona.*

---

## 🗺️ Mapa del proyecto

```
Proyecto_Vendaval/
│
├── 🚀 run.py                    ← Arranca todo desde aquí
│
├──  setup.py   
│
├── 📁 cli/                     ← Interfaz de consola (lo que ve el usuario)
│   ├── main.py                  ← Orquesta el flujo: login → menú → salir
│   ├── menu.py                  ← Menú principal y submenús
│   ├── auth.py                  ← Login y registro con contraseña segura
│   ├── display_helpers.py       ← Funciones visuales (tablas, colores, paneles)
│   └── input_helpers.py         ← Funciones de input con validación
│
├── 📁 backend/                  ← Lógica del negocio (el cerebro)
│   ├── api/
│   │   ├── client.py            ← Llama a WeatherAPI
│   │   ├── normalizer.py        ← Limpia y formatea los datos
│   │   ├── ingest_weather.py    ← Orquesta la ingesta automática
│   │   └── manual_register.py  ← Orquesta el registro manual
│   ├── core/
│   │   ├── weather_records.py   ← Molde estándar de un registro
│   │   ├── alerts.py            ← Sistema de alertas por umbrales
│   │   ├── compare.py           ← Comparativa manual vs API
│   │   └── validator.py         ← Valida que los datos son correctos
│   ├── stats/
│   │   ├── data_adapter.py      ← Prepara los datos para el dashboard
│   │   └── cyber_dashboard.py  ← Dashboard gráfico interactivo
│   ├── storage/
│   │   └── json_repo.py         ← Guarda y lee los registros en JSON
│   ├── scheduler/
│   │   └── scheduler.py         ← Ingesta automática cada X minutos
│   └── utils/
│       └── logger_config.py     ← Sistema de logs del proyecto
│
├── 📁 config/
│   └── zones.json               ← Las ciudades y zonas de España configuradas
│
├── 📁 data/                     ← Se crea automáticamente al usar la app
│   ├── weather_cache.json       ← Registros de la API
│   └── manual_records.json      ← Registros manuales
│
├── 📁 logs/                     ← Logs del sistema (se genera automáticamente)
├── 📁 tests/                      ← Tests automáticos del proyecto
├── .env.example                 ← Plantilla de configuración
├── requirements.txt             ← Librerías necesarias
├──README                        ← Como el "manual de intrucciones" del repositorio
├──.gitignore                    ← Lo que git ignorará al subirlo a github
├──.env                          ← lo que permanecera oculto

```

---

## 🛠️ Instalación paso a paso

> **¿Primera vez con Python o con terminal?** No te preocupes. Sigue cada paso en orden y llegará a funcionar.

### Paso 0 — Requisitos previos

> 💡 **¿Qué es una terminal?**
> En Windows: busca `PowerShell` o `cmd` en el menú inicio.
> En Mac: busca `Terminal` en aplicaciones.
> En Linux: `Ctrl + Alt + T`.

Antes de empezar necesitas tener instalado:

- **Python 3.12 o superior** → [Descargar Python](https://www.python.org/downloads/)
- **Git** → [Descargar Git](https://git-scm.com/downloads/)
- **VSCode** → [Descargar VSCode](https://code.visualstudio.com/download/)

Para comprobar si ya los tienes, abre una terminal en VSCode o Windows/Linux/Mac y escribe:

```bash
python3 --version   # Debe mostrar Python 3.12.x o superior
git --version       # Debe mostrar git version x.x.x
```

---

### Paso 1 — Descargar el proyecto desde el terminal

```bash
git clone https://github.com/adryeli/Proyecto_Vendaval.git
cd Proyecto_Vendaval
```

> 💡 **¿Qué hace esto?**
> `git clone` descarga una copia del proyecto en tu ordenador.
> `cd` entra dentro de la carpeta del proyecto.

---

### Paso 2 — Crear el entorno virtual

Un **entorno virtual** es una zona aislada donde instalamos las librerías del proyecto sin mezclarlas con el resto de tu sistema.

```bash
# Crear el entorno virtual
python3 -m venv .venv

# Activarlo (elige según tu sistema operativo)
source .venv/bin/activate        # Mac / Linux
.venv\Scripts\activate           # Windows
```

✅ Sabrás que está activo porque verás **`(.venv)`** al inicio de tu terminal:
```
(.venv) usuario@ordenador:~/Proyecto_Vendaval$
```

> ⚠️ **Importante:** cada vez que abras una terminal nueva para trabajar en el proyecto, tienes que activar el entorno virtual de nuevo.

---

### Paso 3 — Instalar las dependencias

```bash
pip install -r requirements.txt
```

> 💡 **¿Qué hace esto?**
> Lee el archivo `requirements.txt` e instala todas las librerías que necesita el proyecto. Puede tardar un minuto.

---

### Paso 4 — Configurar la API key

El proyecto necesita una clave para obtener datos reales del tiempo. Es **gratis**.

**4.1** Regístrate en [weatherapi.com](https://www.weatherapi.com/) (no pide tarjeta).

**4.2** Una vez dentro, copia tu **API Key** del dashboard (es una cadena de 32 caracteres).

**4.3** Copia el archivo de ejemplo y edítalo:

```bash
cp .env.example .env
```

**4.4** Abre el archivo `.env` con cualquier editor de texto y rellénalo así:

```
WEATHER_API_KEY=tu_clave_de_32_caracteres_aqui
WEATHER_API_BASE_URL=https://api.weatherapi.com/v1
SCHEDULER_INTERVAL_MINUTES=30
```

> ⚠️ **Sin comillas** alrededor de la clave. Solo el valor tal cual.

**4.5** Verifica que funciona pegando esta URL en el navegador (cambia `TU_CLAVE`):
```
https://api.weatherapi.com/v1/current.json?key=TU_CLAVE&q=Madrid
```
Si ves datos de Madrid en formato JSON → ✅ todo listo.

---

### Paso 5 — Ejecutar la aplicación

```bash
python run.py o python run.py
```

Verás el logo de Vendaval y la pantalla de login. **Regístrate** con un usuario y contraseña nuevos para empezar.

---

## 🎮 Cómo usar la aplicación

Una vez dentro, el menú principal tiene estas opciones:

```
1. 📝  Registro manual de datos
2. 🌐  Registro automático de clima
3. 📊  Consultar histórico
4. 🚨  Historial de alertas
5. 📈  Mostrar estadísticas registradas
6. 🗺   Consultar información de una zona
7.     Comparar manual vs dato API
8.     Scheduler (Iniciar/Detener)
9. 🚪  Salir
```

### 📝 Registro manual
Introduce tú mismo los datos climáticos: fecha, ciudad, temperatura, humedad, viento y lluvia. El sistema valida cada dato y te avisa si hay alertas.

### 🌐 Registro automático
Elige una ciudad o ingestad todas las ciudades de una vez. El sistema llama a WeatherAPI y guarda los datos automáticamente.

### 📊 Consultar histórico
Filtra los registros guardados por ciudad, por fecha, o por ciudad y fecha a la vez.

### 🚨 Historial de alertas
Ve qué registros tienen alertas activas. Las alertas se disparan cuando:

| Parámetro | Umbral |
|-----------|--------|
| 🌡️ Temperatura | < -8°C o > 40°C |
| 💨 Viento | ≥ 70 km/h |
| 💧 Humedad | ≤ 20% o > 70% |
| 🌧️ Lluvia | > 10 mm (fuerte) · > 30 mm (riesgo) |

### 📈 Dashboard de estadísticas
Abre una ventana gráfica interactiva con las estadísticas de todas las ciudades. Puedes filtrar por ciudad, por variable (temperatura, humedad, viento, lluvia) y por rango de fechas (día, semana, mes, año).

---

## 🧪 Ejecutar los tests

El proyecto tiene tests automáticos. Para ejecutarlos:

```bash
# Todos los tests
pytest tests/ -v

# Solo los tests de la CLI
pytest tests/test_display_helpers.py tests/test_input_helpers.py tests/test_auth.py -v

# Solo los tests del backend
pytest tests/test_alerts.py tests/test_normalizer.py tests/test_persistencia_json.py -v
```

> 💡 **¿Qué son los tests?**
> Son pequeños programas que comprueban automáticamente que el código funciona bien. Si sale todo en verde (`PASSED`) → el proyecto está sano.

---

## ❓ Problemas frecuentes

<details>
<summary><b>❌ Error: "No module named 'rich'"</b></summary>

El entorno virtual no está activo o las dependencias no están instaladas.

```bash
source .venv/bin/activate   # Mac/Linux
.venv\Scripts\activate       # Windows
pip install -r requirements.txt
```
</details>

<details>
<summary><b>❌ Error 401 al llamar a la API</b></summary>

La API key no es válida o todavía no está activa. WeatherAPI tarda hasta 30 minutos en activar claves nuevas. Comprueba que en el `.env` no hay comillas ni espacios alrededor de la clave.
</details>

<details>
<summary><b>❌ "command not found: python3"</b></summary>

Python no está instalado o no está en el PATH. Descárgalo de [python.org](https://www.python.org/downloads/) y durante la instalación en Windows marca la opción **"Add Python to PATH"**.
</details>

<details>
<summary><b>❌ El dashboard gráfico no abre</b></summary>

Asegúrate de tener `matplotlib` y `mplcyberpunk` instalados:

```bash
pip install matplotlib mplcyberpunk
```
</details>

<details>
<summary><b>❌ "ModuleNotFoundError" al arrancar</b></summary>

Ejecuta siempre desde la carpeta raíz del proyecto (donde está `run.py`), no desde dentro de una subcarpeta:

```bash
cd ~/Proyecto_Vendaval   # asegúrate de estar aquí
python run.py o python3 run.py #según la versión de python que tengas
```
</details>

---

## 🏗️ Estructura del código — explicada para principiantes

> ¿Quieres entender cómo está organizado internamente? Aquí la explicación sencilla.

El proyecto sigue el principio de **separación de responsabilidades**: cada archivo hace **una sola cosa**. Así es más fácil de entender, mantener y testear.

```
El usuario escribe algo en la terminal
         ↓
    cli/menu.py          → recoge la opción y llama al backend
         ↓
backend/api/ o core/     → hace el trabajo (API, validar, alertas)
         ↓
backend/storage/         → guarda o lee del JSON
         ↓
    resultado devuelto a menu.py
         ↓
cli/display_helpers.py   → muestra el resultado bonito en pantalla
```

**No hay clases** — todo el código usa **funciones simples**, lo que hace que sea más fácil de seguir para quien está aprendiendo Python.

---

## 👥 Equipo

Este proyecto ha sido desarrollado por:

| Desarrollador | GitHub |
|---------------|--------|
| 👩‍💻 Laura | [@LauraSilRu](https://github.com/LauraSilRu) |
| 👨‍💻 Joel | [@jowel2701](https://github.com/jowel2701) |
| 👨‍💻 David | [@drojas-7u7](https://github.com/drojas-7u7) |
| 👨‍💻 Yohanna | [@yohperez](https://github.com/yohperez) |
| 👩‍💻 Elizabeth | [@adryeli](https://github.com/adryeli) |

---

## 🤖 Vendaval Mentor — Tu asistente personal del proyecto

> ¿Tienes una duda específica sobre el código? ¿No entiendes cómo funciona un módulo? ¿Quieres que te expliquen algo paso a paso?

Hay un GPT personalizado entrenado con toda la estructura del proyecto. Funciona como un **profesor o mentor** que te guía a tu nivel.

### 👉 [Abrir Vendaval Mentor en ChatGPT](https://chatgpt.com/g/g-69e7e4fe031881919ba294fa89d471d9-vendaval-mentor)

Ejemplos de preguntas que puedes hacerle:
- *"¿Cómo funciona el sistema de alertas?"*
- *"¿Qué hace exactamente `normalize_weather_data`?"*
- *"No entiendo cómo se guarda un registro, explícamelo paso a paso"*
- *"¿Por qué hay dos archivos JSON separados?"*

---

## 🎬 Videos demostrativos

| ▶️ [Demo 1](https://youtu.be/_EKjp1RLyEs) | ▶️ [Demo 2](https://youtu.be/3hFjrRq-mt0) |
|---|---|

---

<div align="center">

**Proyecto Vendaval** · Hecho con 🌪️ y mucho ☕

*Sistema no orientado a objetos · Python 3.12 · WeatherAPI · Rich · Matplotlib*

Academic Use License

Copyright (c) 2026 Proyecto Vendaval

Este software se distribuye exclusivamente con fines académicos y educativos.
No se permite su uso comercial.
Se permite su modificación para uso educativo interno.
No se permite su redistribución sin autorización expresa.
</div>
