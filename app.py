import streamlit as st

# 1. Configuración inicial de la página
st.set_page_config(
    page_title="Portafolio Interfaces Multimodales | Juan Pablo Gutiérrez",
    page_icon="🚀",
    layout="centered"
)

# 2. Encabezado principal del portafolio
st.title("🚀 Portafolio: Interfaces Multimodales")
st.markdown("### Juan Pablo Gutiérrez Quintero")
st.markdown("**Diseño Interactivo - Universidad EAFIT**")
st.write("---")
st.write("Bienvenido a mi portafolio del curso. Aquí encontrarás un recopilatorio de las aplicaciones desarrolladas en Streamlit a lo largo del semestre, explorando diferentes modalidades de interacción como visión computacional, voz, y protocolos de comunicación IoT.")

# 3. Creación de pestañas para organizar las clases
tab11, tab12, tab13, tab14 = st.tabs(["Clase 11", "Clase 12", "Clase 13", "Clase 14"])

# Contenido Clase 11
with tab11:
    st.header("📚 Clase 11")
    st.write("Exploración de interfaces para procesamiento de documentos.")
    st.link_button("💬 Chat PDF - Versión 1", "https://chatpdf-clase-11-jy87wpkuwbydsszmx37mtk.streamlit.app/", use_container_width=True)
    st.link_button("💬 Chat PDF - Versión 2", "https://chatpdf-clase-11-asnq94pjetrhqqduup3sqb.streamlit.app/", use_container_width=True)

# Contenido Clase 12
with tab12:
    st.header("🎨 Clase 12")
    st.write("Aplicaciones de reconocimiento y tableros de dibujo interactivos.")
    st.link_button("🔢 Predicción MNIST", "https://mnistpred-clase12-tnokntyr9x5j5ebbsoqhoa.streamlit.app/", use_container_width=True)
    st.link_button("✏️ Tablero Interactivo", "https://tablero-clase-12-92e6sliunqhxkuy4vgwgty.streamlit.app/", use_container_width=True)
    st.link_button("👁️ Reconocimiento de Dibujo (DrawRecog)", "https://drawrecog-clase-12-4cfuntf48mmhrlz97vpydx.streamlit.app/", use_container_width=True)
    st.link_button("🛠️ Taller Clase 12", "https://clase12-taller-kszzd7oqhvpdavw5vkyfjm.streamlit.app/", use_container_width=True)

# Contenido Clase 13
with tab13:
    st.header("📡 Clase 13")
    st.write("Integración de comunicación MQTT y control por voz (gTTS/Reconocimiento).")
    st.link_button("📥 Recepción MQTT", "https://recepmqtt-clase13-m99szh2udgeecr46cebwu3.streamlit.app/", use_container_width=True)
    st.link_button("📤 Envío MQTT", "https://sendcmqtt-clase13-ydyfbaz55vqm73mjnny59x.streamlit.app/", use_container_width=True)
    st.link_button("🎙️ Control por Voz", "https://ctrlvoice---clase-13-w7zlxchbtedjdurb2hnck2.streamlit.app/", use_container_width=True)

# Contenido Clase 14
with tab14:
    st.header("🧠 Clase 14")
    st.write("Sistemas multimodales avanzados combinando visión, voz y gestos.")
    st.link_button("🗣️ Control por Voz (Multipage)", "https://clase-14-mqtt-multipage-vu46kvdslwh7eetd4vxfgr.streamlit.app/Control_por_voz", use_container_width=True)
    st.link_button("⚙️ Clase 14 - App Principal", "https://clase14-ciuzhl6lg5ykxmoeqhlrdg.streamlit.app/", use_container_width=True)
    st.link_button("📷 Combinación con Visión", "https://clase14-visioncomb-4kibapppgcfjnvmgmxuyew6.streamlit.app/", use_container_width=True)
    st.link_button("🖐️ Cerradura por Gestos", "https://cerraduragestos-clase14-iuzlc5yhaapha4p9zfphnm.streamlit.app/", use_container_width=True)

# Footer
st.write("---")
st.caption("Repositorio alojado en GitHub y desplegado en Streamlit Community Cloud.")
