import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Configuración de la página
st.set_page_config(page_title="Análisis de Intrusión Salina", page_icon="🌊", layout="wide")
st.title("🌊 Análisis de Intrusión Salina en Acuíferos")

# Parámetros fijos
st.sidebar.header("Parámetros del Modelo")
ancho = st.sidebar.number_input("Ancho del medio poroso (m)", value=0.025, step=0.001)
porosidad = st.sidebar.slider("Porosidad del medio", 0.0, 1.0, 0.488)
cota_extraccion = st.sidebar.number_input("Cota de extracción del pozo (m)", value=0.1, step=0.01)

# Carga de archivos
st.header("Carga de Datos")
col1, col2 = st.columns(2)
with col1:
    st.subheader("CONDICIÓN 1 (Con bombeo)")
    archivo1 = st.file_uploader("Subir CSV 1", type="csv", key="file1")
    
with col2:
    st.subheader("CONDICIÓN 2 (Sin bombeo)")
    archivo2 = st.file_uploader("Subir CSV 2", type="csv", key="file2")

# Procesamiento de datos
if archivo1 and archivo2:
    try:
        df1 = pd.read_csv(archivo1, encoding='latin-1')
        df2 = pd.read_csv(archivo2, encoding='latin-1')
        
        # Validación de datos
        required_cols = ["Abscisa (m)", "cota de superficie de agua dulce (m)", 
                         "Superficie de medio poroso (m)", "ubicación del pozo de extracción"]
        if not all(col in df1.columns for col in required_cols) or not all(col in df2.columns for col in required_cols):
            st.error("Error: Los archivos CSV deben contener las columnas requeridas")
            st.stop()
        
        # Cálculos para CONDICIÓN 1
        with st.spinner("Calculando condición 1..."):
            x1 = df1["Abscisa (m)"]
            agua_dulce = df1["cota de superficie de agua dulce (m)"]
            
            tabla_sin_na = df1.dropna(subset=["cota de superficie de cuña salina (m)"])
            agua_salada = tabla_sin_na["cota de superficie de cuña salina (m)"]
            x2 = tabla_sin_na["Abscisa (m)"]
            
            superficie = df1["Superficie de medio poroso (m)"]
            
            area1 = np.trapz(agua_dulce, x1)
            area2 = np.trapz(agua_salada, x2)
            area3 = np.trapz(superficie, x1)
            
            area1_agua_dulce = area1 - area2
            volumen1_agua_dulce = area1_agua_dulce * ancho * porosidad * 1000
            volumen1_agua_salada = area2 * ancho * porosidad * 1000
            volumen1_insaturado = (area3 - area1) * ancho * porosidad * 1000
            cota1_maxima = df1["cota de superficie de agua dulce (m)"].max() * 100
            
            df3 = df1.dropna(subset=["cota de superficie de cuña salina (m)"])
            pie1_inicio = df3["Abscisa (m)"].iloc[0]
            pie1_final = df3["Abscisa (m)"].iloc[-1]
            longitud1_pie = (pie1_final - pie1_inicio) * 100
            
            punto1 = df1.loc[df1["ubicación del pozo de extracción"] == True]
            p1 = df3["Abscisa (m)"].iloc[0]
            p2 = df3["cota de superficie de cuña salina (m)"].iloc[0]
            q1 = punto1["Abscisa (m)"].iloc[0]
            distancia1_cm = np.sqrt((cota_extraccion - p2)**2 + (q1 - p1)**2) * 100
        
        # Cálculos para CONDICIÓN 2
        with st.spinner("Calculando condición 2..."):
            x3 = df2["Abscisa (m)"]
            agua2_dulce = df2["cota de superficie de agua dulce (m)"]
            
            tabla2_sin_na = df2.dropna(subset=["cota de superficie de cuña salina (m)"])
            agua2_salada = tabla2_sin_na["cota de superficie de cuña salina (m)"]
            x4 = tabla2_sin_na["Abscisa (m)"]
            
            superficie2 = df2["Superficie de medio poroso (m)"]
            
            area4 = np.trapz(agua2_dulce, x3)
            area5 = np.trapz(agua2_salada, x4)
            area6 = np.trapz(superficie2, x3)
            
            area2_agua_dulce = area4 - area5
            volumen2_agua_dulce = area2_agua_dulce * ancho * porosidad * 1000
            volumen2_agua_salada = area5 * ancho * porosidad * 1000
            volumen2_insaturado = (area4 - area5) * ancho * porosidad * 1000
            cota2_maxima = df2["cota de superficie de agua dulce (m)"].max() * 100
            
            df4 = df2.dropna(subset=["cota de superficie de cuña salina (m)"])
            pie2_inicio = df4["Abscisa (m)"].iloc[0]
            pie2_final = df4["Abscisa (m)"].iloc[-1]
            longitud2_pie = (pie2_final - pie2_inicio) * 100
            
            punto2 = df2.loc[df2["ubicación del pozo de extracción"] == True]
            p1_2 = df4["Abscisa (m)"].iloc[0]
            p2_2 = df4["cota de superficie de cuña salina (m)"].iloc[0]
            q1_2 = punto2["Abscisa (m)"].iloc[0]
            distancia2_cm = np.sqrt((cota_extraccion - p2_2)**2 + (q1_2 - p1_2)**2) * 100
        
        # Cálculos finales
        volumen_total1 = volumen1_agua_dulce + volumen1_agua_salada + volumen1_insaturado
        volumen_total2 = volumen2_agua_dulce + volumen2_agua_salada + volumen2_insaturado
        porcentaje_intrusion1 = (volumen1_agua_salada / volumen_total1) * 100
        porcentaje_intrusion2 = (volumen2_agua_salada / volumen_total2) * 100
        
        # Visualización de resultados
        st.success("¡Cálculos completados!")
        st.divider()
        
        # Gráfico comparativo
        st.header("Comparación de Perfiles Hidráulicos")
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # CONDICIÓN 1 (Con bombeo)
        ax.plot(df1["Abscisa (m)"], df1["Superficie de medio poroso (m)"], 'k-', label="Superficie con bombeo")
        ax.plot(df1["Abscisa (m)"], df1["cota de superficie de agua dulce (m)"], 'b-', label="Agua dulce con bombeo")
        ax.plot(df1["Abscisa (m)"], df1["cota de superficie de cuña salina (m)"], 'r-', label="Cuña salina con bombeo")
        
        # CONDICIÓN 2 (Sin bombeo)
        ax.plot(df2["Abscisa (m)"], df2["Superficie de medio poroso (m)"], 'k--', label="Superficie sin bombeo")
        ax.plot(df2["Abscisa (m)"], df2["cota de superficie de agua dulce (m)"], 'b--', label="Agua dulce sin bombeo")
        ax.plot(df2["Abscisa (m)"], df2["cota de superficie de cuña salina (m)"], 'r--', label="Cuña salina sin bombeo")
        
        # Pozo de extracción
        px1 = punto1["Abscisa (m)"].iloc[0]
        py1 = punto1["Superficie de medio poroso (m)"].iloc[0]
        ax.plot([px1, px1], [py1, cota_extraccion], 'g-', linewidth=3, marker='^', label="Pozo de extracción")
        
        ax.set_title("Perfiles Hidráulicos y de Intrusión Salina")
        ax.set_xlabel("Abscisa (m)")
        ax.set_ylabel("Cota (m)")
        ax.set_ylim(0, 0.5)
        ax.set_xlim(0, 0.8)
        ax.grid(True, alpha=0.3)
        ax.legend(loc='upper right')
        
        st.pyplot(fig)
        
        # Métricas comparativas
        st.header("Resultados Comparativos")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Diferencia Intrusión Salina", 
                     f"{abs(porcentaje_intrusion1 - porcentaje_intrusion2):.2f}%",
                     f"{'Mayor con bombeo' if porcentaje_intrusion1 > porcentaje_intrusion2 else 'Menor con bombeo'}")
            
        with col2:
            cambio = volumen2_agua_dulce - volumen1_agua_dulce
            st.metric("Cambio Agua Dulce", 
                     f"{abs(cambio):.2f} L",
                     f"{'Aumento' if cambio > 0 else 'Disminución'} con bombeo")
            
        with col3:
            dist_diff = distancia2_cm - distancia1_cm
            st.metric("Distancia al Pie de Cuña", 
                     f"{abs(dist_diff):.2f} cm",
                     f"{'Mayor con bombeo' if dist_diff < 0 else 'Menor con bombeo'}")
        
        # Tablas de resultados
        st.subheader("📊 Resultados Detallados")
        tab1, tab2 = st.tabs(["CONDICIÓN 1 (Con bombeo)", "CONDICIÓN 2 (Sin bombeo)"])
        
        with tab1:
            st.write(f"**Porcentaje de intrusión salina:** {porcentaje_intrusion1:.2f}%")
            data1 = {
                "Parámetro": ["Agua Dulce", "Agua Salada", "Zona Insaturada", "Cota Máxima Agua", "Longitud Pie Cuña", "Distancia al Pozo"],
                "Valor": [
                    f"{volumen1_agua_dulce:.2f} L",
                    f"{volumen1_agua_salada:.2f} L",
                    f"{volumen1_insaturado:.2f} L",
                    f"{cota1_maxima:.2f} cm",
                    f"{longitud1_pie:.2f} cm",
                    f"{distancia1_cm:.2f} cm"
                ]
            }
            st.table(pd.DataFrame(data1))
        
        with tab2:
            st.write(f"**Porcentaje de intrusión salina:** {porcentaje_intrusion2:.2f}%")
            data2 = {
                "Parámetro": ["Agua Dulce", "Agua Salada", "Zona Insaturada", "Cota Máxima Agua", "Longitud Pie Cuña", "Distancia al Pozo"],
                "Valor": [
                    f"{volumen2_agua_dulce:.2f} L",
                    f"{volumen2_agua_salada:.2f} L",
                    f"{volumen2_insaturado:.2f} L",
                    f"{cota2_maxima:.2f} cm",
                    f"{longitud2_pie:.2f} cm",
                    f"{distancia2_cm:.2f} cm"
                ]
            }
            st.table(pd.DataFrame(data2))
        
        # Conclusión
        st.divider()
        st.header("Conclusiones")
        if porcentaje_intrusion1 > porcentaje_intrusion2:
            st.warning(f"⚠️ La intrusión salina aumenta con el bombeo en un {porcentaje_intrusion1 - porcentaje_intrusion2:.2f}%")
            st.write(f"La distancia entre el pozo y el pie de cuña disminuye de {distancia2_cm:.2f} cm a {distancia1_cm:.2f} cm con el bombeo")
        else:
            st.success(f"✅ La intrusión salina disminuye con el bombeo en un {porcentaje_intrusion2 - porcentaje_intrusion1:.2f}%")
            st.write(f"La distancia entre el pozo y el pie de cuña aumenta de {distancia2_cm:.2f} cm a {distancia1_cm:.2f} cm con el bombeo")
            
        st.write(f"**Volumen total de agua dulce:**")
        st.write(f"- Con bombeo: {volumen1_agua_dulce:.2f} L")
        st.write(f"- Sin bombeo: {volumen2_agua_dulce:.2f} L")
        
    except Exception as e:
        st.error(f"Error en el procesamiento: {str(e)}")
else:
    st.info("Por favor, suba ambos archivos CSV para comenzar el análisis")

# Instrucciones
st.sidebar.divider()
st.sidebar.header("Instrucciones")
st.sidebar.info("""
1. Configure los parámetros en el panel izquierdo
2. Suba dos archivos CSV:
   - Condición 1: Con bombeo
   - Condición 2: Sin bombeo
3. Los archivos deben contener las columnas requeridas
4. Espere a que se procesen los resultados
""")
