# 🚛 MULTIMOORA - Transporte Intermodal

Este proyecto forma parte de la tesis de título desarrollada por Catalina Soto Pavez y Antonia Novoa. El trabajo propone un modelo de análisis multicriterio aplicado al contexto del **transporte intermodal**, utilizando el método **MULTIMOORA** para comparar distintas funciones objetivo en la toma de decisiones estratégicas.

## 🎯 Objetivo de la plataforma

Desarrollar una herramienta web interactiva que permita:

1. Transformar automáticamente resultados de modelos GAMS en archivos `.csv` estandarizados.
2. Aplicar el método MULTIMOORA a distintos escenarios y funciones objetivo.
3. Explorar visualmente las soluciones intermodales obtenidas, con tablas, KPIs y grafos.
4. Visualizar el paso a paso de los métodos RS (Ratio System), RP (Reference Point) y FMF (Full Multiplicative Form).

---

## 🌐 Deploy público

La plataforma está disponible en:

🔗 [https://intermoora.streamlit.app/](https://intermoora.streamlit.app/)

---

## 🛠️ Funcionalidades principales

### 1️⃣ GAMS ➜ CSV Transformer

- Subida de archivos `.zip` con resultados de GAMS en `.xlsx`.
- Extracción automática de valores clave: `lambda`, `z`, `ent`, `varianza`.
- Exportación de archivos `.csv` listos para ser usados en el análisis MULTIMOORA.

### 2️⃣ Análisis MULTIMOORA Interactivo

- Carga de múltiples archivos `.csv` con distintas funciones objetivo.
- Definición personalizada de pesos por criterio.
- Visualización del paso a paso de los métodos:
  - 📈 Ratio System (RS)
  - 📏 Reference Point (RP)
  - ✴️ Full Multiplicative Form (FMF)
- Resultados finales y rankings comparativos.

### 3️⃣ Comparación de soluciones intermodales

- Visualización de indicadores clave (`z`, `ent`, `varianza`, `lambda`).
- Tablas de flujos utilizados por tipo y terminales activadas.
- Representación gráfica de la red de transporte:
  - Por tipo de flujo: directo, con terminales T/S, o entre terminales.
  - Visualización consolidada de toda la red, con colores por modo (carretera, tren, fluvial).

---

## 📁 Estructura del repositorio

```
📂 app/
├── pages/
│   ├── 1- GAMS_TO_CSV.py              # Conversor de resultados GAMS
│   ├── 2- Análisis MULTIMOORA.py      # Implementación interactiva de MULTIMOORA
│   ├── 3- Comparacion.py              # Comparación visual y grafo de soluciones
│
├── utils/
│   ├── utils.py                       # Funciones auxiliares y visualización
│   └── __pycache__/
│
📄 requirements.txt
📄 README.md
📄 .streamlit/config.toml
```

---

## 🧪 Tecnologías utilizadas

- [Streamlit](https://streamlit.io/) para la interfaz web.
- [Pandas](https://pandas.pydata.org/) para manejo de datos.
- [NetworkX](https://networkx.org/) y [Matplotlib](https://matplotlib.org/) para visualización de grafos.
- Python 3.11+

---

## ✍️ Autoras

- Catalina Soto Pavez  
- Antonia Novoa

Facultad de Ingeniería – Universidad de los Andes (Chile)  
Tesis de pregrado

---

## 🚧 En desarrollo

Este proyecto está en desarrollo activo como parte de la tesis. Comentarios y sugerencias son bienvenidos.