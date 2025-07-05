
# 🚛 MULTIMOORA - Transporte Intermodal

Este proyecto forma parte de la tesis de título desarrollada por Catalina Soto Pavez y Antonia Novoa. El trabajo propone un modelo de análisis multicriterio aplicado al contexto del **transporte intermodal**, utilizando el método **MULTIMOORA** para comparar distintas funciones objetivo en la toma de decisiones estratégicas.

## 🎯 Objetivo de la plataforma

Desarrollar una herramienta web interactiva que permita:

1. Transformar automáticamente resultados de modelos GAMS en archivos `.csv` estandarizados.
2. Aplicar el método MULTIMOORA a distintos escenarios y funciones objetivo.
3. Explorar el paso a paso de los métodos RS (Ratio System), RP (Reference Point) y FMF (Full Multiplicative Form).

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

---

## 🧪 Tecnologías utilizadas

- [Streamlit](https://streamlit.io/) para la interfaz web.
- [Pandas](https://pandas.pydata.org/) para manejo de datos.
- Python 3.11+

---

## 📁 Estructura del repositorio

```
📂 app/
├── 1_HOME.py              # Página de inicio de la plataforma
├── 2_GAMS_TO_CSV.py       # Conversor GAMS ➜ CSV
├── 3_MULTI.py             # Módulo de análisis MULTIMOORA
├── utils/
│   └── utils.py           # Funciones de limpieza, normalización y MULTIMOORA
```

---

## ✍️ Autoras

- Catalina Soto Pavez  
- Antonia Novoa

Facultad de Ingeniería – Universidad de los Andes (Chile)  
Tesis de pregrado

---

## 🚧 En desarrollo

Este proyecto está en desarrollo activo como parte de la tesis. Comentarios y sugerencias son bienvenidos.