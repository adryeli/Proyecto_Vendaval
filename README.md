<div align="center">

<!-- Logos Principales -->
<img src="https://cdn.discordapp.com/attachments/1495826454628270304/1496505425095557262/Logo_Proyecto_Vendaval_v1_sin-fondo.png?ex=69fa9b89&is=69f94a09&hm=3824af3df62bf1f0e37472cae30c3dc6b4ffcc02739eaa97973348f9ca53b2b6&" width="250" alt="Logo Proyecto Vendaval">
<img src="https://cdn.discordapp.com/attachments/1495826454628270304/1496505424239788234/Logo_Barlovento_Data_v1_sin-fondo.png?ex=69fa9b88&is=69f94a08&hm=240436cb4463608dbd4fce12c643336cc8d8ea95cb3ee75d17ec53fc92a20da7&" width="250" alt="Logo Barlovento Data">

<br>

<!-- Banner de Fondo -->
<img src="https://cdn.discordapp.com/attachments/1495826454628270304/1496505423577219192/Fondo-Pantalla-Barlovento3_v1_Zoom_.png?ex=69fa9b88&is=69f94a08&hm=f17cb146b01fb40093f673e7bb39328358c92234fa0c503683ba0c98ee1e869f&" width="100%" alt="Banner Barlovento">

# 🌪️ Proyecto Vendaval
### Sistema inteligente de monitoreo y alertas meteorológicas para zonas de riesgo

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=flat-square&logo=python)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](LICENSE)
[![GitHub Issues](https://img.shields.io/github/issues/adryeli/Proyecto_Vendaval?style=flat-square)](https://github.com/adryeli/Proyecto_Vendaval/issues)

</div>

---

## 📋 Descripción

**Proyecto Vendaval** es una solución integral diseñada para el monitoreo climático municipal. Permite registrar, consultar y visualizar datos meteorológicos críticos de múltiples zonas geográficas en tiempo real, facilitando la toma de decisiones ante condiciones climáticas adversas.

- 🌡️ **Monitoreo Real:** Datos de temperatura, humedad, viento y presión.
- 🚨 **Alertas Inteligentes:** Sistema automático de detección de riesgos.
- 📊 **Análisis Histórico:** Consulta y filtrado de registros pasados.
- 💾 **Persistencia:** Almacenamiento seguro en base de datos PostgreSQL (Neon).
- 🖥️ **Dual Interface:** Operación mediante CLI (Terminal).

---

## ✨ Características Principales

### 1. Monitoreo en Tiempo Real
- Sincronización automática con la API de **WeatherRecord**.
- Validación de datos mediante rangos climáticos realistas.
- Captura de datos manual y automática.

### 2. Sistema de Alertas Avanzado
- Umbrales configurables por zona (Viento > 80km/h, Temp > 40°C, etc.).
- Clasificación de severidad (Info, Warning, Critical).

### 3. Interfaz de Usuario
- **CLI:** Menú interactivo para gestión rápida desde consola.
- **(Futuro) Web:** Dashboard visual con gráficas de evolución temporal.

---

## 🗂 Estructura del Proyecto

```text
Proyecto_Vendaval/
├── backend/
│   ├── api/          # Cliente API y Normalización
│   ├── core/         # Alertas y Validaciones
│   └── storage/      # Persistencia (SQLAlchemy/Postgres)
├── cli/              # Interfaz de Consola
├── config/           # Zonas y Umbrales
├── tests/            # Suite de Pruebas
├── app.py            # Dashboard Streamlit
└── run.py            # Lanzador del sistema
```

---

## 📦 Instalación

```bash
# Clonar y entrar
git clone https://github.com/adryeli/Proyecto_Vendaval.git
cd Proyecto_Vendaval

# Entorno virtual y dependencias
python -m venv .venv
source .venv/Scripts/activate  # Windows
pip install -r requirements.txt
```

---

## 🧪 Testing

```bash
pytest -v
```

---

<div align="center">

**Hecho con ❤️ por el equipo de Proyecto Vendaval**
**Elizabeth Sena (Scrum Master)**
**Laura (Product Owner)**
**David (Coder)**
**Joel (Coder)**
**Yohanna (Coder)**
*Barlovento Data Solutions · SomosF5 / AI4Inclusion 2025*

</div>
