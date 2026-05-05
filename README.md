<div align="center">

<img src="https://cdn.discordapp.com/attachments/1495826454628270304/1496505425095557262/Logo_Proyecto_Vendaval_v1_sin-fondo.png" width="200">
<img src="https://cdn.discordapp.com/attachments/1495826454628270304/1496505424239788234/Logo_Barlovento_Data_v1_sin-fondo.png" width="200">

# 🌪️ Proyecto Vendaval

Sistema inteligente de monitoreo y alertas meteorológicas para zonas de riesgo

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=flat-square&logo=python)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](LICENSE)
[![GitHub Issues](https://img.shields.io/github/issues/adryeli/Proyecto_Vendaval?style=flat-square)](https://github.com/adryeli/Proyecto_Vendaval/issues)
[![GitHub Stars](https://img.shields.io/github/stars/adryeli/Proyecto_Vendaval?style=flat-square)](https://github.com/adryeli/Proyecto_Vendaval/stargazers)

</div>

---

## 📋 Descripción

**Proyecto Vendaval** es una solución integral diseñada para el monitoreo climático municipal. Permite registrar, consultar y visualizar datos meteorológicos críticos de múltiples zonas geográficas en tiempo real, facilitando la toma de decisiones ante condiciones climáticas adversas.

- 🌡️ **Monitoreo Real:** Datos de temperatura, humedad, viento y presión.
- 🚨 **Alertas Inteligentes:** Sistema automático de detección de riesgos.
- 📊 **Análisis Histórico:** Consulta y filtrado de registros pasados.
- 💾 **Persistencia:** Almacenamiento seguro en formato JSON.
- 🖥️ **Dual Interface:** Operación mediante CLI (Terminal) y Web (Streamlit).

---

## ✨ Características Principales

### 1. Monitoreo en Tiempo Real
- Sincronización automática con la API de **Open-Meteo**.
- Validación de datos mediante rangos climáticos realistas.
- Captura de datos manual y automática (Scheduler).

### 2. Sistema de Alertas Avanzado
- Umbrales configurables por zona (Viento > 80km/h, Temp > 40°C, etc.).
- Clasificación de severidad (Info, Warning, Critical).

### 3. Interfaz de Usuario
- **CLI:** Menú interactivo para gestión rápida desde consola.
- **Web:** Dashboard visual con gráficas de evolución temporal.

---

## 🗂 Estructura del Proyecto

```text
Proyecto_Vendaval/
├── .github/               # Templates de PR e Issues
├── backend/
│   ├── api/
│   │   ├── client.py      # Cliente de conexión API
│   │   ├── ingest.py      # Lógica de ingesta masiva
│   │   └── normalizer.py  # Conversión JSON -> Objetos
│   ├── core/
│   │   ├── alerts.py      # Motor de evaluación de alertas
│   │   ├── validator.py   # Reglas de validación de negocio
│   │   └── weather.py     # Modelos de datos (Dataclasses)
│   ├── storage/
│   │   └── json_repo.py   # Capa de persistencia en disco
│   └── utils/
│       └── logger.py      # Configuración de trazabilidad
├── cli/
│   ├── main.py            # Punto de entrada de terminal
│   ├── menu.py            # Navegación del sistema
│   └── display.py         # Formateo de tablas y colores
├── config/
│   └── zones.json         # Geo-configuración de zonas
├── tests/                 # Suite de pruebas unitarias
├── run.py                 # Lanzador principal
└── requirements.txt       # Dependencias
```

---

## 📦 Instalación

### 1. Clonar el repositorio
```bash
git clone https://github.com/adryeli/Proyecto_Vendaval.git
cd Proyecto_Vendaval
```

### 2. Configurar el entorno virtual
```bash
# Windows
python -m venv venv
source venv/Scripts/activate

# Linux/macOS
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno
Crea un archivo `.env` basado en el ejemplo:
```bash
cp .env.example .env
```

---

## 🚀 Uso

### Ejecutar la Aplicación CLI
```bash
python run.py cli
```

### Ejecutar el Dashboard Web
```bash
streamlit run app.py
```

### Ejemplo de Menú CLI:
```text
╔════════════════════════════════════════╗
║    🌪️  PROYECTO VENDAVAL  🌪️          ║
║   Sistema de Monitoreo Meteorológico   ║
╚════════════════════════════════════════╝
1. Ver datos actuales
2. Registrar datos manuales
3. Gestionar alertas
4. Consultar historial
0. Salir
```

---

## 🧪 Testing

Mantenemos una cobertura de código para asegurar la fiabilidad de las alertas.

```bash
# Ejecutar todos los tests
pytest -v

# Ver cobertura
pytest --cov=backend tests/
```

---

## 🤝 Contribuciones

1. Haz un **Fork** del proyecto.
2. Crea una rama (`git checkout -b feature/NuevaMejora`).
3. Realiza un **Commit** (`git commit -m 'feat: añadir nueva alerta'`).
4. **Push** a la rama (`git push origin feature/NuevaMejora`).
5. Abre un **Pull Request**.

---

## 📝 Licencia

Este proyecto está bajo la Licencia **MIT**. Consulta el archivo `LICENSE` para más detalles.

---

<div align="center">

**Hecho con ❤️ por el equipo de Proyecto Vendaval**  
*Barlovento Data Solutions · SomosF5 / AI4Inclusion 2025*

⭐ Si te gusta este proyecto, ¡danos una estrella en GitHub!

</div>