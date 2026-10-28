import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Portafolio Interfaces Multimodales | Juan Pablo",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.title("🌌 Estación Multimodal - Diseño Interactivo")
st.markdown("**Juan Pablo Gutiérrez Quintero** | 🖱️ Arrastra para moverte | ⚙️ Rueda del ratón para Zoom")

# Motor actualizado con Zoom, Audio UI y Flujo de Datos
estacion_html = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <style>
        body { margin: 0; padding: 0; background-color: #050505; overflow: hidden; font-family: 'Courier New', Courier, monospace; user-select: none; }
        
        #viewport {
            width: 100vw;
            height: 75vh;
            overflow: hidden; 
            position: relative;
            cursor: grab;
            border: 2px solid #333;
            border-radius: 10px;
            box-shadow: inset 0 0 50px rgba(0,0,0,0.8);
            perspective: 1000px;
        }
        
        #viewport:active { cursor: grabbing; }

        /* Capa de fondo separada para el efecto Parallax */
        #background-grid {
            position: absolute;
            width: 5000px;
            height: 4000px;
            top: -1000px;
            left: -1000px;
            background-image: 
                linear-gradient(rgba(0, 255, 255, 0.03) 2px, transparent 2px),
                linear-gradient(90deg, rgba(0, 255, 255, 0.03) 2px, transparent 2px),
                linear-gradient(rgba(0, 255, 255, 0.01) 1px, transparent 1px),
                linear-gradient(90deg, rgba(0, 255, 255, 0.01) 1px, transparent 1px);
            background-size: 100px 100px, 100px 100px, 20px 20px, 20px 20px;
            z-index: 0;
            transform-origin: center center;
            will-change: transform;
        }

        /* Capa principal interactiva */
        #world {
            position: absolute;
            width: 3500px;
            height: 2500px;
            z-index: 1;
            transform-origin: 0 0;
            will-change: transform;
        }

        /* --- ANIMACIONES --- */
        @keyframes pulseGlow {
            0% { box-shadow: 0 0 10px currentColor, inset 0 0 10px currentColor; }
            50% { box-shadow: 0 0 25px currentColor, inset 0 0 20px currentColor; }
            100% { box-shadow: 0 0 10px currentColor, inset 0 0 10px currentColor; }
        }

        @keyframes dataPulseH {
            0% { left: -10%; opacity: 0; }
            10% { opacity: 1; }
            90% { opacity: 1; }
            100% { left: 100%; opacity: 0; }
        }
        
        @keyframes dataPulseV {
            0% { top: -10%; opacity: 0; }
            10% { opacity: 1; }
            90% { opacity: 1; }
            100% { top: 100%; opacity: 0; }
        }

        /* --- COMPONENTES --- */
        .sector {
            position: absolute;
            border: 2px dashed;
            border-radius: 15px;
            padding: 25px 20px 20px 20px;
            background: rgba(0, 0, 0, 0.75);
            backdrop-filter: blur(8px);
            box-shadow: 0 10px 30px rgba(0,0,0,0.5);
            transition: border-color 0.3s ease;
        }
        
        .sector:hover { border-style: solid; }

        .sector-title {
            position: absolute;
            top: -15px;
            left: 20px;
            background: #0a0e17;
            padding: 0 10px;
            font-weight: bold;
            text-transform: uppercase;
            letter-spacing: 1px;
            font-size: 14px;
        }

        .terminal {
            display: inline-flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            width: 140px;
            height: 100px;
            margin: 10px;
            border: 1px solid currentColor;
            border-radius: 8px;
            text-decoration: none;
            color: currentColor;
            background: rgba(255, 255, 255, 0.02);
            transition: all 0.2s cubic-bezier(0.25, 0.8, 0.25, 1);
            position: relative;
            overflow: hidden;
            text-align: center;
            font-size: 12px;
            font-weight: bold;
            vertical-align: top;
        }

        .terminal:hover {
            transform: translateY(-5px) scale(1.05);
            background: rgba(255, 255, 255, 0.15);
            animation: pulseGlow 1.5s infinite;
            z-index: 10;
        }
        
        .docs { background: rgba(255, 255, 255, 0.08); border-style: dotted; }
        .icon { font-size: 24px; margin-bottom: 8px; }

        /* Cables de datos interactivos */
        .cable {
            position: absolute;
            background: rgba(255,255,255,0.1);
            overflow: hidden;
            z-index: 0;
        }
        .cable-h { height: 2px; }
        .cable-v { width: 2px; }
        
        /* El pulso de luz que viaja por el cable */
        .data-packet-h {
            position: absolute;
            width: 30px;
            height: 100%;
            background: #fff;
            box-shadow: 0 0 10px #fff, 0 0 20px #00d2ff;
            animation: dataPulseH 3s infinite linear;
        }
        .data-packet-v {
            position: absolute;
            width: 100%;
            height: 30px;
            background: #fff;
            box-shadow: 0 0 10px #fff, 0 0 20px #00ff41;
            animation: dataPulseV 3s infinite linear;
        }

        /* Colores por sector */
        #s10 { top: 150px; left: 200px; width: 250px; color: #ffcc00; border-color: #ffcc00; }
        #s11 { top: 400px; left: 550px; width: 550px; color: #00d2ff; border-color: #00d2ff; }
        #s12 { top: 100px; left: 1200px; width: 900px; color: #b829ff; border-color: #b829ff; }
        #s13 { top: 750px; left: 300px; width: 750px; color: #ff8c00; border-color: #ff8c00; }
        #s14 { top: 700px; left: 1300px; width: 850px; color: #00ff41; border-color: #00ff41; }
        
        #easter-egg { top: 1300px; left: 2300px; color: #ff0055; border: 1px dotted #ff0055; padding: 10px; border-radius: 50%; width: 150px; height: 150px; display: flex; flex-direction: column; align-items: center; justify-content: center; position: absolute; font-size: 10px; text-align: center; cursor: pointer; }

    </style>
</head>
<body>

<div id="viewport">
    <div id="background-grid"></div>
    <div id="world">

        <!-- Enrutamiento de Cables con Flujo de Datos -->
        <div class="cable cable-h" style="top: 250px; left: 450px; width: 100px;"><div class="data-packet-h" style="animation-delay: 0s;"></div></div>
        <div class="cable cable-v" style="top: 250px; left: 550px; height: 150px;"><div class="data-packet-v" style="animation-delay: 1.5s;"></div></div>
        <div class="cable cable-h" style="top: 500px; left: 1100px; width: 100px;"><div class="data-packet-h" style="animation-delay: 0.5s;"></div></div>
        <div class="cable cable-h" style="top: 850px; left: 1050px; width: 250px;"><div class="data-packet-h" style="animation-delay: 2s; background: #00ff41;"></div></div>

        <!-- SECTORES (Mismo contenido, omitido por brevedad en visualización, pero completo en render) -->
        <div class="sector" id="s10">
            <div class="sector-title">Clase 10: Gestos</div>
            <a href="https://sites.google.com/view/gestos/p%C3%A1gina-principal" target="_blank" class="terminal docs"><span class="icon">📚</span> Teoría</a>
        </div>
        
        <div class="sector" id="s11">
            <div class="sector-title">Clase 11: LLMs</div>
            <a href="https://sites.google.com/view/procesamiento-de-lenguaje-natu/inicio" target="_blank" class="terminal docs"><span class="icon">📚</span> Teoría</a>
            <a href="https://chatpdf-clase-11-jy87wpkuwbydsszmx37mtk.streamlit.app/" target="_blank" class="terminal"><span class="icon">📄</span> Chat PDF v1</a>
            <a href="https://chatpdf-clase-11-asnq94pjetrhqqduup3sqb.streamlit.app/" target="_blank" class="terminal"><span class="icon">💬</span> Chat PDF v2</a>
        </div>

        <div class="sector" id="s12">
            <div class="sector-title">Clase 12: Táctiles</div>
            <a href="https://sites.google.com/view/handwr?usp=sharing" target="_blank" class="terminal docs"><span class="icon">📚</span> Teoría</a>
            <a href="https://mnistpred-clase12-tnokntyr9x5j5ebbsoqhoa.streamlit.app/" target="_blank" class="terminal"><span class="icon">🔢</span> MNIST Pred</a>
            <a href="https://tablero-clase-12-92e6sliunqhxkuy4vgwgty.streamlit.app/" target="_blank" class="terminal"><span class="icon">✏️</span> Tablero App</a>
            <a href="https://drawrecog-clase-12-4cfuntf48mmhrlz97vpydx.streamlit.app/" target="_blank" class="terminal"><span class="icon">👁️</span> DrawRecog</a>
            <a href="https://clase12-taller-kszzd7oqhvpdavw5vkyfjm.streamlit.app/" target="_blank" class="terminal"><span class="icon">🛠️</span> Taller App</a>
        </div>

        <div class="sector" id="s13">
            <div class="sector-title">Clase 13: IoT</div>
            <a href="https://sites.google.com/view/sistemasconiot/p%C3%A1gina-principal" target="_blank" class="terminal docs"><span class="icon">📚</span> Teoría</a>
            <a href="https://recepmqtt-clase13-m99szh2udgeecr46cebwu3.streamlit.app/" target="_blank" class="terminal"><span class="icon">📥</span> Recep MQTT</a>
            <a href="https://sendcmqtt-clase13-ydyfbaz55vqm73mjnny59x.streamlit.app/" target="_blank" class="terminal"><span class="icon">📤</span> Send MQTT</a>
            <a href="https://ctrlvoice---clase-13-w7zlxchbtedjdurb2hnck2.streamlit.app/" target="_blank" class="terminal"><span class="icon">🎙️</span> Ctrl Voice</a>
        </div>

        <div class="sector" id="s14">
            <div class="sector-title">Clase 14: Ciberfísicos</div>
            <a href="https://drive.google.com/file/d/1L9RMLfuTadEA3OZ2iUIl3spFO-FF0CAp/view?usp=sharing" target="_blank" class="terminal docs"><span class="icon">📚</span> Repo Base</a>
            <a href="https://clase-14-mqtt-multipage-vu46kvdslwh7eetd4vxfgr.streamlit.app/Control_por_voz" target="_blank" class="terminal"><span class="icon">🗣️</span> Voice Mult</a>
            <a href="https://clase14-ciuzhl6lg5ykxmoeqhlrdg.streamlit.app/" target="_blank" class="terminal"><span class="icon">⚙️</span> App Ciber</a>
            <a href="https://clase14-visioncomb-4kibapppgcfjnvmgmxuyew6.streamlit.app/" target="_blank" class="terminal"><span class="icon">📷</span> Vision Comb</a>
            <a href="https://cerraduragestos-clase14-iuzlc5yhaapha4p9zfphnm.streamlit.app/" target="_blank" class="terminal"><span class="icon">🖐️</span> Cerradura</a>
        </div>

        <a href="https://www.instagram.com/ttt.discos" target="_blank" id="easter-egg" title="Tres Tristes Tigres">
            <span style="font-size: 24px;">🎛️</span><br>s0lid142<br>Beat Lab
            <div style="font-size: 8px; margin-top:5px; opacity: 0.5;">Ableton Sync...</div>
        </a>
    </div>
</div>

<script>
    // --- 1. SINTETIZADOR DE AUDIO (Web Audio API) ---
    // Genera un sonido sin necesidad de archivos externos. Perfecto para un Beat Lab.
    const AudioContext = window.AudioContext || window.webkitAudioContext;
    let audioCtx;

    function playHoverSound() {
        if (!audioCtx) audioCtx = new AudioContext();
        if (audioCtx.state === 'suspended') audioCtx.resume();
        
        const osc = audioCtx.createOscillator();
        const gainNode = audioCtx.createGain();
        
        osc.type = 'sine'; // Sonido digital puro
        osc.frequency.setValueAtTime(880, audioCtx.currentTime); // Tono alto
        osc.frequency.exponentialRampToValueAtTime(440, audioCtx.currentTime + 0.1); // Caída rápida
        
        gainNode.gain.setValueAtTime(0.05, audioCtx.currentTime); // Volumen muy sútil
        gainNode.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 0.1);
        
        osc.connect(gainNode);
        gainNode.connect(audioCtx.destination);
        
        osc.start();
        osc.stop(audioCtx.currentTime + 0.1);
    }

    // Asignar el sonido a todas las terminales
    document.querySelectorAll('.terminal, #easter-egg').forEach(el => {
        el.addEventListener('mouseenter', playHoverSound);
    });

    // --- 2. LÓGICA DE MOVIMIENTO, ZOOM Y PARALLAX ---
    const viewport = document.getElementById('viewport');
    const world = document.getElementById('world');
    const bgGrid = document.getElementById('background-grid');
    
    let isDragging = false;
    let currentX = -50, currentY = -50; 
    let startX, startY;
    let scale = 0.8; // Iniciamos con un poco de zoom out para ver mejor el panorama

    function updateTransform() {
        // GPU acceleration para el mundo interactivo
        world.style.transform = `translate3d(${currentX}px, ${currentY}px, 0) scale(${scale})`;
        // Efecto Parallax: el fondo se mueve a la mitad de velocidad (0.5)
        bgGrid.style.transform = `translate3d(${currentX * 0.5}px, ${currentY * 0.5}px, 0) scale(${scale})`;
    }

    // Zoom con la rueda del ratón
    viewport.addEventListener('wheel', (e) => {
        e.preventDefault();
        const zoomSensitivity = 0.001;
        scale += e.deltaY * -zoomSensitivity;
        // Limitar el zoom entre 0.3x y 2x
        scale = Math.min(Math.max(0.3, scale), 2);
        updateTransform();
    });

    // Panning (Arrastrar)
    viewport.addEventListener('mousedown', (e) => {
        isDragging = true;
        startX = e.clientX - currentX;
        startY = e.clientY - currentY;
        world.style.transition = 'none';
        bgGrid.style.transition = 'none';
    });

    window.addEventListener('mouseup', () => {
        isDragging = false;
        world.style.transition = 'transform 0.1s ease-out';
        bgGrid.style.transition = 'transform 0.1s ease-out';
    });

    window.addEventListener('mousemove', (e) => {
        if (!isDragging) return;
        e.preventDefault();
        
        currentX = e.clientX - startX;
        currentY = e.clientY - startY;
        updateTransform();
    });

    // Render inicial
    updateTransform();
</script>

</body>
</html>
"""

components.html(estacion_html, height=750, scrolling=False)

st.write("---")
st.caption("Arquitectura interactiva V2: Incorpora control de Zoom, efecto Parallax, animaciones de tráfico de red y síntesis de audio UI nativa.")
