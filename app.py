import streamlit as st
import streamlit.components.v1 as components

# 1. Configuración de la página (Wide para aprovechar toda la pantalla)
st.set_page_config(
    page_title="Portafolio Estación Multimodal | Juan Pablo",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.title("🌌 Estación Multimodal - Diseño Interactivo EAFIT")
st.markdown("**Juan Pablo Gutiérrez Quintero** | Navega por la estación arrastrando el mapa. Haz clic en las terminales para abrir los proyectos.")

# 2. El "Motor" del juego/mapa en HTML/CSS/JS puro (Sin imágenes externas)
estacion_html = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <style>
        /* --- ESTILOS DEL CONTENEDOR Y EL MUNDO --- */
        body { margin: 0; padding: 0; background-color: #050505; overflow: hidden; font-family: 'Courier New', Courier, monospace; }
        
        #viewport {
            width: 100vw;
            height: 75vh;
            overflow: hidden; /* Ocultamos el scroll nativo */
            position: relative;
            cursor: grab;
            border: 2px solid #333;
            border-radius: 10px;
            box-shadow: inset 0 0 50px rgba(0,0,0,0.8);
        }
        
        #viewport:active { cursor: grabbing; }

        #world {
            position: absolute;
            width: 3000px;
            height: 2000px;
            /* Fondo procedural creado solo con CSS (Estilo Blueprint / Grid Sci-Fi) */
            background-color: #0a0e17;
            background-image: 
                linear-gradient(rgba(0, 255, 255, 0.05) 2px, transparent 2px),
                linear-gradient(90deg, rgba(0, 255, 255, 0.05) 2px, transparent 2px),
                linear-gradient(rgba(0, 255, 255, 0.02) 1px, transparent 1px),
                linear-gradient(90deg, rgba(0, 255, 255, 0.02) 1px, transparent 1px);
            background-size: 100px 100px, 100px 100px, 20px 20px, 20px 20px;
            transform-origin: 0 0;
            transition: transform 0.1s ease-out; /* Suaviza el paneo */
        }

        /* --- ANIMACIONES GLOBALES --- */
        @keyframes pulseGlow {
            0% { box-shadow: 0 0 10px currentColor, inset 0 0 10px currentColor; }
            50% { box-shadow: 0 0 25px currentColor, inset 0 0 20px currentColor; }
            100% { box-shadow: 0 0 10px currentColor, inset 0 0 10px currentColor; }
        }

        @keyframes scanline {
            0% { top: -10%; opacity: 0; }
            50% { opacity: 0.2; }
            100% { top: 110%; opacity: 0; }
        }

        /* Efecto de escáner pasando por todo el mundo */
        .scanner {
            position: absolute;
            width: 100%;
            height: 20px;
            background: linear-gradient(to bottom, transparent, rgba(0, 255, 255, 0.5), transparent);
            animation: scanline 8s linear infinite;
            pointer-events: none;
            z-index: 999;
        }

        /* --- ESTILOS DE LOS SECTORES (Clases) --- */
        .sector {
            position: absolute;
            border: 2px dashed;
            border-radius: 15px;
            padding: 20px;
            background: rgba(0, 0, 0, 0.4);
            backdrop-filter: blur(4px);
        }

        .sector-title {
            position: absolute;
            top: -15px;
            left: 20px;
            background: #0a0e17;
            padding: 0 10px;
            font-weight: bold;
            text-transform: uppercase;
            letter-spacing: 2px;
        }

        /* --- ESTILOS DE LAS TERMINALES (Links a los proyectos) --- */
        .terminal {
            display: inline-flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            width: 140px;
            height: 100px;
            margin: 15px;
            border: 1px solid currentColor;
            border-radius: 8px;
            text-decoration: none;
            color: currentColor;
            background: rgba(255, 255, 255, 0.03);
            transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
            position: relative;
            overflow: hidden;
            text-align: center;
            font-size: 12px;
            font-weight: bold;
        }

        .terminal:hover {
            transform: translateY(-5px) scale(1.05);
            background: rgba(255, 255, 255, 0.1);
            animation: pulseGlow 1.5s infinite;
            z-index: 10;
        }

        .icon { font-size: 24px; margin-bottom: 8px; }

        /* --- COLORES POR SECTOR --- */
        /* Sector 11: Documentos (Azul) */
        #s11 { top: 300px; left: 400px; width: 400px; color: #00d2ff; border-color: #00d2ff; }
        #s11 .terminal { color: #00d2ff; }

        /* Sector 12: Visión y Dibujo (Morado) */
        #s12 { top: 200px; left: 1000px; width: 750px; color: #b829ff; border-color: #b829ff; }
        #s12 .terminal { color: #b829ff; }

        /* Sector 13: IoT y Voz (Naranja) */
        #s13 { top: 800px; left: 500px; width: 600px; color: #ff8c00; border-color: #ff8c00; }
        #s13 .terminal { color: #ff8c00; }

        /* Sector 14: Core Multimodal (Verde Matrix) */
        #s14 { top: 750px; left: 1300px; width: 750px; color: #00ff41; border-color: #00ff41; }
        #s14 .terminal { color: #00ff41; }

        /* Easter Egg */
        #easter-egg { top: 1200px; left: 1800px; color: #ff0055; border: 1px dotted #ff0055; padding: 10px; border-radius: 50%; width: 150px; height: 150px; display: flex; flex-direction: column; align-items: center; justify-content: center; position: absolute; font-size: 10px; text-align: center; }
        
        /* Conectores (Líneas entre sectores) */
        .cable {
            position: absolute;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
            height: 2px;
            z-index: 0;
        }

    </style>
</head>
<body>

<div id="viewport">
    <div id="world">
        <div class="scanner"></div>

        <!-- Cables de conexión visual -->
        <div class="cable" style="top: 450px; left: 800px; width: 200px;"></div>
        <div class="cable" style="top: 600px; left: 600px; width: 2px; height: 200px; background: linear-gradient(180deg, transparent, rgba(255,255,255,0.2), transparent);"></div>
        <div class="cable" style="top: 900px; left: 1100px; width: 200px;"></div>

        <!-- SECTOR 11 -->
        <div class="sector" id="s11">
            <div class="sector-title">Clase 11: Document Core</div>
            <a href="https://chatpdf-clase-11-jy87wpkuwbydsszmx37mtk.streamlit.app/" target="_blank" class="terminal">
                <span class="icon">📄</span> Chat PDF v1
            </a>
            <a href="https://chatpdf-clase-11-asnq94pjetrhqqduup3sqb.streamlit.app/" target="_blank" class="terminal">
                <span class="icon">💬</span> Chat PDF v2
            </a>
        </div>

        <!-- SECTOR 12 -->
        <div class="sector" id="s12">
            <div class="sector-title">Clase 12: Vision Studio</div>
            <a href="https://mnistpred-clase12-tnokntyr9x5j5ebbsoqhoa.streamlit.app/" target="_blank" class="terminal">
                <span class="icon">🔢</span> Predicción MNIST
            </a>
            <a href="https://tablero-clase-12-92e6sliunqhxkuy4vgwgty.streamlit.app/" target="_blank" class="terminal">
                <span class="icon">✏️</span> Tablero Interactivo
            </a>
            <a href="https://drawrecog-clase-12-4cfuntf48mmhrlz97vpydx.streamlit.app/" target="_blank" class="terminal">
                <span class="icon">👁️</span> DrawRecog
            </a>
            <a href="https://clase12-taller-kszzd7oqhvpdavw5vkyfjm.streamlit.app/" target="_blank" class="terminal">
                <span class="icon">🛠️</span> Taller Visión
            </a>
        </div>

        <!-- SECTOR 13 -->
        <div class="sector" id="s13">
            <div class="sector-title">Clase 13: Comms & Voice</div>
            <a href="https://recepmqtt-clase13-m99szh2udgeecr46cebwu3.streamlit.app/" target="_blank" class="terminal">
                <span class="icon">📥</span> Rx MQTT
            </a>
            <a href="https://sendcmqtt-clase13-ydyfbaz55vqm73mjnny59x.streamlit.app/" target="_blank" class="terminal">
                <span class="icon">📤</span> Tx MQTT
            </a>
            <a href="https://ctrlvoice---clase-13-w7zlxchbtedjdurb2hnck2.streamlit.app/" target="_blank" class="terminal">
                <span class="icon">🎙️</span> Control Voice
            </a>
        </div>

        <!-- SECTOR 14 -->
        <div class="sector" id="s14">
            <div class="sector-title">Clase 14: Multimodal Hub</div>
            <a href="https://clase-14-mqtt-multipage-vu46kvdslwh7eetd4vxfgr.streamlit.app/Control_por_voz" target="_blank" class="terminal">
                <span class="icon">🗣️</span> Voice Multipage
            </a>
            <a href="https://clase14-ciuzhl6lg5ykxmoeqhlrdg.streamlit.app/" target="_blank" class="terminal">
                <span class="icon">⚙️</span> App Principal
            </a>
            <a href="https://clase14-visioncomb-4kibapppgcfjnvmgmxuyew6.streamlit.app/" target="_blank" class="terminal">
                <span class="icon">📷</span> Vision Comb
            </a>
            <a href="https://cerraduragestos-clase14-iuzlc5yhaapha4p9zfphnm.streamlit.app/" target="_blank" class="terminal">
                <span class="icon">🖐️</span> Cerradura Gestos
            </a>
        </div>

        <!-- EASTER EGG STUDIO -->
        <div id="easter-egg" title="Tres Tristes Tigres">
            <span style="font-size: 20px;">🎹</span>
            <br>s0lid142<br>Beat Lab
            <div style="font-size: 8px; margin-top:5px; opacity: 0.5;">Ableton Live running...</div>
        </div>

    </div>
</div>

<script>
    // --- LÓGICA DE MOVIMIENTO (PANNING) ---
    const viewport = document.getElementById('viewport');
    const world = document.getElementById('world');
    
    let isDragging = false;
    let currentX = -300; // Posición inicial X (para centrar la vista un poco)
    let currentY = -100; // Posición inicial Y
    let startX, startY;

    // Aplicar posición inicial
    world.style.transform = `translate(${currentX}px, ${currentY}px)`;

    viewport.addEventListener('mousedown', (e) => {
        isDragging = true;
        startX = e.clientX - currentX;
        startY = e.clientY - currentY;
        world.style.transition = 'none'; // Quitar transición al arrastrar para que sea instantáneo
    });

    window.addEventListener('mouseup', () => {
        isDragging = false;
        world.style.transition = 'transform 0.1s ease-out'; // Devolver suavizado
    });

    window.addEventListener('mousemove', (e) => {
        if (!isDragging) return;
        e.preventDefault();
        
        currentX = e.clientX - startX;
        currentY = e.clientY - startY;

        // Límites del mundo (para no salirse del mapa)
        // El viewport mide 100vw/75vh y el mundo 3000x2000
        const maxX = 50;
        const maxY = 50;
        const minX = -(3000 - viewport.clientWidth + 50);
        const minY = -(2000 - viewport.clientHeight + 50);

        if (currentX > maxX) currentX = maxX;
        if (currentY > maxY) currentY = maxY;
        if (currentX < minX) currentX = minX;
        if (currentY < minY) currentY = minY;

        // Usamos translate3d para usar aceleración por hardware (GPU)
        world.style.transform = `translate3d(${currentX}px, ${currentY}px, 0)`;
    });
</script>

</body>
</html>
"""

# Renderizar el componente HTML en Streamlit
components.html(estacion_html, height=700, scrolling=False)

st.write("---")
st.caption("Arquitectura interactiva construida 100% con HTML/CSS/JS procedural, renderizada sobre Streamlit.")
