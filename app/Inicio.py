
import streamlit as st

st.set_page_config(page_title="Inicio MULTIMOORA", layout="wide")

st.markdown("""
<style>
h1 {
    font-size: 42px;
}
h2 {
    color: #444;
    font-size: 28px;
    margin-top: 1.5em;
}
.section {
    background-color: #f2f2f2;
    padding: 1.2em;
    border-radius: 12px;
    margin-bottom: 1.5em;
    border-left: 6px solid #4CAF50;
}
.note {
    background-color: #e8f0fe;
    padding: 1em;
    border-radius: 10px;
    border-left: 4px solid #1a73e8;
    font-size: 16px;
}
</style>
""", unsafe_allow_html=True)

st.markdown("# 🎯 Bienvenid@ a la Plataforma MULTIMOORA")
st.markdown("Esta plataforma interactiva te permite convertir resultados de GAMS a CSV y analizarlos con el método MULTIMOORA.")

st.markdown("---")

st.markdown("""
<div class='section'>
  <h2>1️⃣ Transformador GAMS ➜ CSV</h2>
  <p>Convierte archivos <code>.xlsx</code> de resultados GAMS dentro de un <code>.zip</code> en archivos <code>.csv</code> compatibles con MULTIMOORA.</p>
  <ul>
    <li>🧭 <b>Ir a la página:</b> menú lateral izquierdo ➡️ <b>2. GAMS TO CSV</b></li>
  </ul>
</div>

<div class='section'>
  <h2>2️⃣ Análisis MULTIMOORA</h2>
  <p>Sube múltiples archivos <code>.csv</code> exportados y realiza el análisis de decisión multicriterio con pesos definidos por ti.</p>
  <ul>
    <li>🧭 <b>Ir a la página:</b> menú lateral izquierdo ➡️ <b>3. MULTI</b></li>
  </ul>
</div>

<div class='note'>
  💡 <b>Consejo:</b> Usa el menú lateral izquierdo para comenzar a trabajar con las herramientas disponibles.
</div>
""", unsafe_allow_html=True)
