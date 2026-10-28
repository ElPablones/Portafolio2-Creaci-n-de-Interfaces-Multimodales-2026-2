import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Portafolio Interactivo | Juan Pablo Gutiérrez",
    page_icon="👾",
    layout="wide" # Importante para dar más espacio a la exploración
)

st.title("👾 Portafolio: Estación Multimodal")
st.markdown("**Juan Pablo Gutiérrez Quintero** | Explora la estación para descubrir los proyectos.")

# Aquí inyectamos todo el HTML, CSS y JavaScript
# Este es un "mundo" de 2000x2000 píxeles dentro de un contenedor navegable
interactive_world_html = """
<!DOCTYPE html>
<html>
<head>
<style>
    /* El contenedor que el usuario ve (la ventana) */
    .viewport {
        width: 100%;
        height: 600px;
        overflow: auto; /* Permite hacer scroll libremente */
        border: 2px solid #444;
        background-color: #111;
        position: relative;
        cursor: grab;
    }
    
    /* El mundo gigante adentro (Floor 796 style) */
    .world {
        width: 2000px;
        height: 1500px;
        /* Aquí deberías cargar tu imagen pixel art de fondo */
        /* background-image: url('URL_DE_TU_PIXEL_ART_GIGANTE.png'); */
        background-color: #222;
        background-size: cover;
        position: relative;
        /* Un patrón de cuadrícula temporal para dar idea de espacio */
        background-image: linear-gradient(#333 1px, transparent 1px), linear-gradient(90deg, #333 1px, transparent 1px);
        background-size: 50px 50px;
    }

    /* Las "Habitaciones" o "Personajes" interactivos */
    .room {
        position: absolute;
        width: 120px;
        height: 120px;
        background-color: rgba(255, 255, 255, 0.1);
        border: 2px dashed #00ff00;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #00ff00;
        font-family: monospace;
        font-size: 14px;
        text-align: center;
        transition: 0.3s;
        cursor: pointer;
        text-decoration: none;
    }

    .room:hover {
        background-color: rgba(0, 255, 0, 0.3);
        transform: scale(1.1);
        z-index: 10;
        box-shadow: 0 0 15px #00ff00;
    }

    /* Posicionamiento de las clases en el mapa gigante */
    #clase11 { top: 200px; left: 300px; }
    #clase12 { top: 500px; left: 800px; }
    #clase13 { top: 900px; left: 400px; }
    #clase14 { top: 700px; left: 1400px; }
</style>
</head>
<body>

<div class="viewport" id="viewport">
    <div class="world">
        <!-- Zonas interactivas -->
        <a href="https://chatpdf-clase-11-jy87wpkuwbydsszmx37mtk.streamlit.app/" target="_blank" class="room" id="clase11">
            🤖 Clase 11<br>Chat PDF
        </a>
        
        <a href="https://tablero-clase-12-92e6sliunqhxkuy4vgwgty.streamlit.app/" target="_blank" class="room" id="clase12">
            🎨 Clase 12<br>Tablero / MNIST
        </a>
        
        <a href="https://ctrlvoice---clase-13-w7zlxchbtedjdurb2hnck2.streamlit.app/" target="_blank" class="room" id="clase13">
            🎙️ Clase 13<br>Control por Voz
        </a>
        
        <a href="https://clase14-ciuzhl6lg5ykxmoeqhlrdg.streamlit.app/" target="_blank" class="room" id="clase14">
            🧠 Clase 14<br>Sistema Multimodal
        </a>
        
        <!-- Puedes añadir pequeños "easter eggs" que no hagan nada pero den vida -->
        <div style="position: absolute; top: 1000px; left: 1200px; color: white; font-family: monospace;">
            👾 [Animación de un perrito caminando por aquí]
        </div>
    </div>
</div>

<script>
    // Pequeño script para permitir arrastrar (pan) el mapa con el mouse 
    // en lugar de usar solo las barras de scroll
    const viewport = document.getElementById('viewport');
    let isDown = false;
    let startX, startY, scrollLeft, scrollTop;

    viewport.addEventListener('mousedown', (e) => {
        isDown = true;
        viewport.style.cursor = 'grabbing';
        startX = e.pageX - viewport.offsetLeft;
        startY = e.pageY - viewport.offsetTop;
        scrollLeft = viewport.scrollLeft;
        scrollTop = viewport.scrollTop;
    });
    viewport.addEventListener('mouseleave', () => {
        isDown = false;
        viewport.style.cursor = 'grab';
    });
    viewport.addEventListener('mouseup', () => {
        isDown = false;
        viewport.style.cursor = 'grab';
    });
    viewport.addEventListener('mousemove', (e) => {
        if (!isDown) return;
        e.preventDefault();
        const x = e.pageX - viewport.offsetLeft;
        const y = e.pageY - viewport.offsetTop;
        const walkX = (x - startX) * 2; 
        const walkY = (y - startY) * 2;
        viewport.scrollLeft = scrollLeft - walkX;
        viewport.scrollTop = scrollTop - walkY;
    });
</script>

</body>
</html>
"""

# Renderizar el componente HTML en Streamlit
components.html(interactive_world_html, height=620)

st.caption("Usa el mouse para arrastrar y explorar el mapa. Haz clic en las zonas iluminadas para ir a los proyectos.")
