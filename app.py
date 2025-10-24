import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# Configuración de la página
st.set_page_config(
    page_title="Softwareal - Simulador de Cotizaciones",
    page_icon="💻",
    layout="wide"
)

# Título principal
st.title("🚀 Softwareal - Simulador de Cotizaciones")
st.markdown("---")

# DATOS DE MÓDULOS PREDEFINIDOS
MODULOS = {
    "Autenticación de usuarios": {
        "horas": 40,
        "complejidad": "Media",
        "descripcion": "Sistema de login, registro y recuperación de contraseña"
    },
    "Base de datos": {
        "horas": 60, 
        "complejidad": "Alta",
        "descripcion": "Modelado e implementación de base de datos"
    },
    "Interfaz web responsive": {
        "horas": 80,
        "complejidad": "Alta",
        "descripcion": "Diseño adaptable para desktop y móviles"
    },
    "API REST": {
        "horas": 50,
        "complejidad": "Media",
        "descripcion": "Servicios web para comunicación con frontend"
    },
    "Panel administrativo": {
        "horas": 45,
        "complejidad": "Media", 
        "descripcion": "Interfaz para gestión del sistema"
    },
    "Reportes y estadísticas": {
        "horas": 35,
        "complejidad": "Baja",
        "descripcion": "Generación de reportes en PDF y gráficos"
    }
}

# FUNCIONES DE CÁLCULO EN PESOS CHILENOS
def calcular_horas_totales(modulos_seleccionados):
    total_horas = 0
    for modulo in modulos_seleccionados:
        total_horas += MODULOS[modulo]["horas"]
    return total_horas

def calcular_tiempo_proyecto(horas_totales, horas_por_dia=8):
    dias_totales = horas_totales / horas_por_dia
    semanas = dias_totales / 5
    return dias_totales, semanas

def calcular_costo_total(horas_totales, costo_por_hora):
    return horas_totales * costo_por_hora

def calcular_fecha_fin(fecha_inicio, dias_totales):
    dias_laborales = int(dias_totales)
    fecha_fin = fecha_inicio + timedelta(days=dias_laborales)
    return fecha_fin

def formatear_pesos_chilenos(monto):
    """Formatea el monto en pesos chilenos con separadores de miles"""
    return f"${monto:,.0f}".replace(",", ".")

# INTERFAZ PRINCIPAL
def main():
    # SIDEBAR - Configuración
    st.sidebar.header("⚙️ Configuración del Proyecto")
    
    costo_por_hora = st.sidebar.number_input(
        "Costo por hora desarrollador (CLP $)",
        min_value=5000,
        max_value=50000,
        value=15000,
        step=1000,
        help="Costo horario del desarrollador en pesos chilenos"
    )
    
    horas_por_dia = st.sidebar.slider(
        "Horas de trabajo por día",
        min_value=4,
        max_value=12,
        value=8
    )
    
    fecha_inicio = st.sidebar.date_input(
        "Fecha de inicio del proyecto",
        datetime.now()
    )
    
    # SECCIÓN PRINCIPAL - Selección de Módulos
    st.header("📦 Selección de Módulos")
    st.write("Selecciona los módulos que incluirá tu proyecto:")
    
    modulos_seleccionados = []
    col1, col2 = st.columns(2)
    
    for i, (modulo, detalles) in enumerate(MODULOS.items()):
        col = col1 if i % 2 == 0 else col2
        
        with col:
            if st.checkbox(f"**{modulo}**", key=modulo):
                modulos_seleccionados.append(modulo)
                costo_modulo = detalles['horas'] * costo_por_hora
                st.caption(f"⏱️ {detalles['horas']} horas | 🎯 {detalles['complejidad']}")
                st.caption(f"💰 {formatear_pesos_chilenos(costo_modulo)} | 📝 {detalles['descripcion']}")
    
    # CÁLCULOS Y RESULTADOS
    if modulos_seleccionados:
        st.markdown("---")
        st.header("📊 Resultados de la Cotización")
        
        # Realizar cálculos
        horas_totales = calcular_horas_totales(modulos_seleccionados)
        dias_totales, semanas_totales = calcular_tiempo_proyecto(horas_totales, horas_por_dia)
        costo_total = calcular_costo_total(horas_totales, costo_por_hora)
        fecha_fin = calcular_fecha_fin(fecha_inicio, dias_totales)
        
        # Mostrar resultados en columnas
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Horas totales", f"{horas_totales} h")
            
        with col2:
            st.metric("Tiempo estimado", f"{dias_totales:.1f} días")
            
        with col3:
            st.metric("Semanas", f"{semanas_totales:.1f} sem")
            
        with col4:
            st.metric("Costo total", formatear_pesos_chilenos(costo_total))
        
        # Detalles de la cotización
        st.subheader("📋 Detalles de la Cotización")
        
        # Tabla de módulos seleccionados
        datos_modulos = []
        for modulo in modulos_seleccionados:
            costo_modulo = MODULOS[modulo]["horas"] * costo_por_hora
            datos_modulos.append({
                "Módulo": modulo,
                "Horas": MODULOS[modulo]["horas"],
                "Complejidad": MODULOS[modulo]["complejidad"],
                "Costo (CLP)": formatear_pesos_chilenos(costo_modulo)
            })
        
        df = pd.DataFrame(datos_modulos)
        st.dataframe(df, use_container_width=True)
        
        # Información adicional
        st.write(f"**Fechas estimadas:**")
        st.write(f"- Inicio: {fecha_inicio.strftime('%d/%m/%Y')}")
        st.write(f"- Finalización: {fecha_fin.strftime('%d/%m/%Y')}")
        st.write(f"- Días hábiles: {int(dias_totales)} días")
        
        # Resumen ejecutivo
        st.subheader("📄 Resumen Ejecutivo")
        st.write(f"**Cotización para proyecto de software**")
        st.write(f"- **Total horas de desarrollo:** {horas_totales} horas")
        st.write(f"- **Costo total:** {formatear_pesos_chilenos(costo_total)}")
        st.write(f"- **Tiempo de entrega:** {semanas_totales:.1f} semanas")
        st.write(f"- **Módulos incluidos:** {len(modulos_seleccionados)}")
        
        # Botones de acción
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("💾 Guardar Cotización", use_container_width=True):
                st.success("Cotización guardada exitosamente")
                
        with col2:
            if st.button("📧 Enviar por Email", use_container_width=True):
                st.info("Funcionalidad de email en desarrollo")
                
        with col3:
            if st.button("🔄 Nueva Cotización", use_container_width=True):
                st.rerun()  
    
    else:
        st.info("👆 Selecciona al menos un módulo para generar la cotización")
        
    # PIE DE PÁGINA
    st.markdown("---")
    st.caption("Desarrollado con Streamlit • Equipo Softwareal • Metodología Ágil")

if __name__ == "__main__":
    main()

# Ejecutar Normalmente con "py -m streamlit run app.py"
# Ejecutar con cmd "python -m streamlit run app.py"