import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Portafolio Interfaces Multimodales | Juan Pablo",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.title("🌌 Estación Multimodal (OS v2.0)")
st.markdown("**Juan Pablo Gutiérrez Quintero** | 🖱️ Arrastrar / ⌨️ WASD para moverte | ⚙️ Scroll para Zoom")

# Motor Integral: Renderizado, Audio, UX, UI y Teclado
estacion_html = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <style>
        /* --- ESTILOS BASE --- */
        body { margin: 0; padding: 0; background-color: #000; overflow: hidden; font-family: 'Courier New', Courier, monospace; user-select: none; }
        
        #viewport {
            width: 100vw;
            height: 75vh;
            overflow: hidden; 
            position: relative;
            cursor: crosshair;
            border: 2px solid #222;
            border-radius: 8px;
            perspective: 1000px;
        }

        /* --- SECUENCIA DE ARRANQUE (BOOT-UP) --- */
        #boot-screen {
            position: absolute;
            top: 0; left: 0; width: 100%; height: 100%;
            background-color: #000;
            color: #00ff41;
            z-index: 10000;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            font-size: 14px;
            transition: opacity 0.5s ease-out;
            cursor: pointer;
        }
        .boot-text { margin: 5px; opacity: 0; }
        #start-btn {
            margin-top: 30px; padding: 10px 20px; border: 1px solid #00ff41; 
            background: transparent; color: #00ff41; font-family: inherit;
            cursor: pointer; opacity: 0; animation: blink 1s infinite;
        }

        /* --- FILTRO CRT RETRO-FUTURISTA --- */
        #crt-overlay {
            position: absolute;
            top: 0; left: 0; width: 100%; height: 100%;
            pointer-events: none;
            z-index: 9999;
            background: 
                linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.25) 50%),
                radial-gradient(circle, rgba(0,0,0,0) 60%, rgba(0,0,0,0.6) 100%);
            background-size: 100% 4px, 100% 100%;
            mix-blend-mode: overlay;
        }
        /* Aberración cromática sutil */
        .chromatic { text-shadow: 2px 0px 1px rgba(255,0,0,0.5), -2px 0px 1px rgba(0,255,255,0.5); }

        /* --- HUD: RADAR / MINIMAPA --- */
        #hud-radar {
            position: absolute;
            bottom: 20px; left: 20px;
            width: 150px; height: 107px; /* Proporción 3500x2500 */
            background: rgba(0, 20, 0, 0.8);
            border: 1px solid #00ff41;
            border-radius: 4px;
            z-index: 9000;
            pointer-events: none;
        }
        #radar-viewport {
            position: absolute;
            border: 1px solid #fff;
            background: rgba(255, 255, 255, 0.2);
            box-shadow: 0 0 10px #fff;
            transform-origin: 0 0;
            transition: all 0.1s;
        }
        .radar-node { position: absolute; background: #00ff41; border-radius: 50%; box-shadow: 0 0 5px #00ff41;}

        /* --- MUNDO Y PARALLAX --- */
        #background-grid {
            position: absolute;
            width: 7000px; height: 5000px;
            top: -1750px; left: -1750px;
            background-image: 
                linear-gradient(rgba(0, 255, 255, 0.04) 2px, transparent 2px),
                linear-gradient(90deg, rgba(0, 255, 255, 0.04) 2px, transparent 2px);
            background-size: 80px 80px;
            z-index: 0;
            transform-origin: center center;
            will-change: transform;
        }

        /* Partículas CSS flotantes (Polvo Estelar) */
        #particles {
            position: absolute; width: 3500px; height: 2500px;
            background-image: radial-gradient(#fff 1px, transparent 1px);
            background-size: 150px 150px;
            background-position: 0 0;
            opacity: 0.1;
            z-index: 1;
        }

        #world {
            position: absolute;
            width: 3500px; height: 2500px;
            z-index: 2;
            transform-origin: 0 0;
            will-change: transform;
        }

        /* --- ANIMACIONES --- */
        @keyframes blink { 0%, 100% { opacity: 1; } 50% { opacity: 0; } }
        @keyframes pulseGlow { 0%, 100% { box-shadow: 0 0 10px currentColor, inset 0 0 10px currentColor; } 50% { box-shadow: 0 0 25px currentColor, inset 0 0 20px currentColor; } }
        @keyframes dataPulseH { 0% { left: 0%; opacity: 0; } 10% { opacity: 1; } 90% { opacity: 1; } 100% { left: 100%; opacity: 0; } }
        @keyframes dataPulseV { 0% { top: 0%; opacity: 0; } 10% { opacity: 1; } 90% { opacity: 1; } 100% { top: 100%; opacity: 0; } }
        
        /* CABLES DE PLACA BASE */
        .cable { position: absolute; background: rgba(255,255,255,0.08); z-index: 0; overflow: hidden; }
        .cable-h { height: 2px; }
        .cable-v { width: 2px; }
        .data-packet { position: absolute; background: #fff; box-shadow: 0 0 15px currentColor; }
        .data-h { width: 40px; height: 100%; animation: dataPulseH 2s infinite linear; }
        .data-v { width: 100%; height: 40px; animation: dataPulseV 2s infinite linear; }

        /* --- COMPONENTES UI --- */
        .sector {
            position: absolute; border: 2px solid; border-radius: 12px; padding: 30px 20px 20px 20px;
            background: rgba(5, 10, 15, 0.85); backdrop-filter: blur(10px);
            box-shadow: 0 10px 40px rgba(0,0,0,0.8); transition: transform 0.3s;
        }
        .sector-title {
            position: absolute; top: -12px; left: 20px; background: #0a0e17;
            padding: 0 10px; font-weight: bold; font-size: 14px; border: 1px solid currentColor;
        }
        .terminal {
            display: inline-flex; flex-direction: column; justify-content: center; align-items: center;
            width: 120px; height: 90px; margin: 8px; border: 1px solid currentColor; border-radius: 6px;
            text-decoration: none; color: currentColor; background: rgba(255, 255, 255, 0.02);
            transition: all 0.2s; position: relative; font-size: 11px; font-weight: bold; text-align: center;
        }
        .terminal:hover { transform: translateY(-5px); background: rgba(255, 255, 255, 0.1); animation: pulseGlow 1.5s infinite; z-index: 10; }
        .icon { font-size: 22px; margin-bottom: 5px; }

        /* TOPOLOGÍA MOTHERBOARD (Coordenadas X/Y) */
        #s10 { top: 400px; left: 400px; width: 200px; color: #ffcc00; } /* Input: Gestos */
        #s11 { top: 400px; left: 2500px; width: 450px; color: #00d2ff; } /* Brain: LLMs */
        #s12 { top: 1600px; left: 400px; width: 700px; color: #b829ff; } /* Input: Tactil/Vision */
        #s13 { top: 1600px; left: 2400px; width: 600px; color: #ff8c00; } /* Output/Input: IoT */
        #s14 { top: 1000px; left: 1350px; width: 800px; color: #00ff41; box-shadow: 0 0 50px rgba(0,255,65,0.2); } /* NÚCLEO CIBERFÍSICO */
        
        #easter-egg { top: 2200px; left: 3200px; color: #ff0055; border: 1px dotted #ff0055; border-radius: 50%; width: 120px; height: 120px; display: flex; flex-direction: column; align-items: center; justify-content: center; position: absolute; font-size: 10px; text-decoration: none; }

    </style>
</head>
<body>

<div id="viewport" tabindex="0">
    <!-- Capas de Efectos Visuales -->
    <div id="crt-overlay"></div>
    
    <!-- HUD Minimapa -->
    <div id="hud-radar">
        <div id="radar-viewport"></div>
        <!-- Puntos del radar proporcionales (3500x2500 a 150x107, factor ~0.042) -->
        <div class="radar-node" style="top: 17px; left: 17px; width: 4px; height: 4px;"></div>
        <div class="radar-node" style="top: 17px; left: 107px; width: 4px; height: 4px;"></div>
        <div class="radar-node" style="top: 68px; left: 17px; width: 4px; height: 4px;"></div>
        <div class="radar-node" style="top: 68px; left: 102px; width: 4px; height: 4px;"></div>
        <div class="radar-node" style="top: 42px; left: 57px; width: 6px; height: 6px; background:#fff;"></div>
    </div>

    <!-- Pantalla de Arranque -->
    <div id="boot-screen" onclick="initSystem()">
        <div class="boot-text" id="bt1">Initialize M-UI System... [OK]</div>
        <div class="boot-text" id="bt2">Loading Input Perceptors... [OK]</div>
        <div class="boot-text" id="bt3">Connecting to Cyberphysical Core... [OK]</div>
        <div class="boot-text" id="bt4">Booting Audio Engine... [OK]</div>
        <button id="start-btn">ACCESS GRANTED. CLICK TO ENTER</button>
    </div>

    <div id="background-grid"></div>
    <div id="world">
        <div id="particles"></div>

        <!-- CABLES DE DATOS (Motherboard Layout) -->
        <!-- Desde S10 a S14 -->
        <div class="cable cable-h" style="top: 450px; left: 600px; width: 750px; color: #ffcc00;"><div class="data-packet data-h" style="animation-delay: 0s;"></div></div>
        <div class="cable cable-v" style="top: 450px; left: 1350px; height: 550px; color: #ffcc00;"><div class="data-packet data-v" style="animation-delay: 2s;"></div></div>
        
        <!-- Desde S11 a S14 -->
        <div class="cable cable-h" style="top: 450px; left: 2150px; width: 350px; color: #00d2ff;"><div class="data-packet data-h" style="animation-direction: reverse; animation-delay: 0.5s;"></div></div>
        <div class="cable cable-v" style="top: 450px; left: 2150px; height: 550px; color: #00d2ff;"><div class="data-packet data-v" style="animation-delay: 2.5s;"></div></div>

        <!-- Desde S12 a S14 -->
        <div class="cable cable-h" style="top: 1700px; left: 1100px; width: 250px; color: #b829ff;"><div class="data-packet data-h" style="animation-delay: 1s;"></div></div>
        <div class="cable cable-v" style="top: 1350px; left: 1350px; height: 350px; color: #b829ff;"><div class="data-packet data-v" style="animation-direction: reverse; animation-delay: 3s;"></div></div>

        <!-- Desde S13 a S14 -->
        <div class="cable cable-h" style="top: 1700px; left: 2150px; width: 250px; color: #ff8c00;"><div class="data-packet data-h" style="animation-direction: reverse; animation-delay: 1.5s;"></div></div>
        <div class="cable cable-v" style="top: 1350px; left: 2150px; height: 350px; color: #ff8c00;"><div class="data-packet data-v" style="animation-direction: reverse; animation-delay: 3.5s;"></div></div>


        <!-- SECTORES (Módulos de la Placa Base) -->
        <div class="sector" id="s10" data-freq="300">
            <div class="sector-title chromatic">Clase 10: GESTOS [IN]</div>
            <a href="https://sites.google.com/view/gestos/p%C3%A1gina-principal" target="_blank" class="terminal"><span class="icon">📚</span> Docs</a>
        </div>
        
        <div class="sector" id="s11" data-freq="400">
            <div class="sector-title chromatic">Clase 11: LLMs [BRAIN]</div>
            <a href="https://sites.google.com/view/procesamiento-de-lenguaje-natu/inicio" target="_blank" class="terminal"><span class="icon">📚</span> Docs NLP</a>
            <a href="https://chatpdf-clase-11-jy87wpkuwbydsszmx37mtk.streamlit.app/" target="_blank" class="terminal"><span class="icon">📄</span> Chat PDF v1</a>
            <a href="https://chatpdf-clase-11-asnq94pjetrhqqduup3sqb.streamlit.app/" target="_blank" class="terminal"><span class="icon">💬</span> Chat PDF v2</a>
        </div>

        <div class="sector" id="s12" data-freq="500">
            <div class="sector-title chromatic">Clase 12: TÁCTIL/VISIÓN [IN]</div>
            <a href="https://sites.google.com/view/handwr?usp=sharing" target="_blank" class="terminal"><span class="icon">📚</span> Docs Táctil</a>
            <a href="https://mnistpred-clase12-tnokntyr9x5j5ebbsoqhoa.streamlit.app/" target="_blank" class="terminal"><span class="icon">🔢</span> MNIST Pred</a>
            <a href="https://tablero-clase-12-92e6sliunqhxkuy4vgwgty.streamlit.app/" target="_blank" class="terminal"><span class="icon">✏️</span> Tablero Draw</a>
            <a href="https://drawrecog-clase-12-4cfuntf48mmhrlz97vpydx.streamlit.app/" target="_blank" class="terminal"><span class="icon">👁️</span> DrawRecog</a>
            <a href="https://clase12-taller-kszzd7oqhvpdavw5vkyfjm.streamlit.app/" target="_blank" class="terminal"><span class="icon">🛠️</span> Taller Studio</a>
        </div>

        <div class="sector" id="s13" data-freq="600">
            <div class="sector-title chromatic">Clase 13: IoT & VOZ [NET]</div>
            <a href="https://sites.google.com/view/sistemasconiot/p%C3%A1gina-principal" target="_blank" class="terminal"><span class="icon">📚</span> Docs IoT</a>
            <a href="https://recepmqtt-clase13-m99szh2udgeecr46cebwu3.streamlit.app/" target="_blank" class="terminal"><span class="icon">📥</span> MQTT RX</a>
            <a href="https://sendcmqtt-clase13-ydyfbaz55vqm73mjnny59x.streamlit.app/" target="_blank" class="terminal"><span class="icon">📤</span> MQTT TX</a>
            <a href="https://ctrlvoice---clase-13-w7zlxchbtedjdurb2hnck2.streamlit.app/" target="_blank" class="terminal"><span class="icon">🎙️</span> Voice Cmd</a>
        </div>

        <div class="sector" id="s14" data-freq="800">
            <div class="sector-title chromatic">Clase 14: CORE CIBERFÍSICO [INTEGRATION]</div>
            <a href="https://drive.google.com/file/d/1L9RMLfuTadEA3OZ2iUIl3spFO-FF0CAp/view?usp=sharing" target="_blank" class="terminal"><span class="icon">📚</span> Repo Base</a>
            <a href="https://clase-14-mqtt-multipage-vu46kvdslwh7eetd4vxfgr.streamlit.app/Control_por_voz" target="_blank" class="terminal"><span class="icon">🗣️</span> Voice Mult</a>
            <a href="https://clase14-ciuzhl6lg5ykxmoeqhlrdg.streamlit.app/" target="_blank" class="terminal"><span class="icon">⚙️</span> Main Cyber</a>
            <a href="https://clase14-visioncomb-4kibapppgcfjnvmgmxuyew6.streamlit.app/" target="_blank" class="terminal"><span class="icon">📷</span> Vision Comb</a>
            <a href="https://cerraduragestos-clase14-iuzlc5yhaapha4p9zfphnm.streamlit.app/" target="_blank" class="terminal"><span class="icon">🖐️</span> Gestos Lock</a>
        </div>

        <a href="https://www.instagram.com/ttt.discos" target="_blank" id="easter-egg" data-freq="220">
            <span style="font-size: 24px;">🎛️</span><br>s0lid142<br>Beat Lab
        </a>
    </div>
</div>

<script>
    // --- 1. BOOT SEQUENCE ---
    setTimeout(() => document.getElementById('bt1').style.opacity = 1, 500);
    setTimeout(() => document.getElementById('bt2').style.opacity = 1, 1200);
    setTimeout(() => document.getElementById('bt3').style.opacity = 1, 1800);
    setTimeout(() => document.getElementById('bt4').style.opacity = 1, 2400);
    setTimeout(() => document.getElementById('start-btn').style.opacity = 1, 3000);

    // --- 2. MOTOR DE AUDIO MULTIFRECUENCIA ---
    const AudioContext = window.AudioContext || window.webkitAudioContext;
    let audioCtx;
    let droneOsc;

    function initSystem() {
        document.getElementById('boot-screen').style.opacity = 0;
        setTimeout(() => document.getElementById('boot-screen').style.display = 'none', 500);
        document.getElementById('viewport').focus(); // Habilitar teclado

        // Iniciar el Drone (Ambiente espacial de fondo)
        if (!audioCtx) audioCtx = new AudioContext();
        if (audioCtx.state === 'suspended') audioCtx.resume();
        
        droneOsc = audioCtx.createOscillator();
        const droneGain = audioCtx.createGain();
        droneOsc.type = 'sine';
        droneOsc.frequency.setValueAtTime(55, audioCtx.currentTime); // Sub-bass (Nota A1)
        droneGain.gain.setValueAtTime(0.015, audioCtx.currentTime); // Muy silencioso
        droneOsc.connect(droneGain);
        droneGain.connect(audioCtx.destination);
        droneOsc.start();
    }

    function playHoverSound(freq) {
        if (!audioCtx) return;
        const osc = audioCtx.createOscillator();
        const gainNode = audioCtx.createGain();
        const panner = audioCtx.createStereoPanner(); // Audio 3D simulado
        
        osc.type = 'square'; // Tono más retro
        osc.frequency.setValueAtTime(freq, audioCtx.currentTime);
        osc.frequency.exponentialRampToValueAtTime(freq/2, audioCtx.currentTime + 0.15);
        
        gainNode.gain.setValueAtTime(0.03, audioCtx.currentTime);
        gainNode.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 0.15);
        
        // Paneo aleatorio para inmersión
        panner.pan.value = (Math.random() * 2) - 1; 
        
        osc.connect(panner);
        panner.connect(gainNode);
        gainNode.connect(audioCtx.destination);
        
        osc.start();
        osc.stop(audioCtx.currentTime + 0.15);
    }

    document.querySelectorAll('.sector, #easter-egg').forEach(el => {
        el.addEventListener('mouseenter', () => {
            let freq = parseInt(el.getAttribute('data-freq') || 440);
            playHoverSound(freq);
        });
    });

    // --- 3. FÍSICAS DE MOVIMIENTO, ZOOM Y HUD ---
    const viewport = document.getElementById('viewport');
    const world = document.getElementById('world');
    const bgGrid = document.getElementById('background-grid');
    const radarView = document.getElementById('radar-viewport');
    
    // Posición inicial centrada en el CORE Ciberfísico (S14)
    let currentX = -900, currentY = -600, scale = 0.7; 
    let isDragging = false, startX, startY;

    // Estado del Teclado (WASD)
    const keys = { w: false, a: false, s: false, d: false, ArrowUp: false, ArrowLeft: false, ArrowDown: false, ArrowRight: false };

    viewport.addEventListener('keydown', (e) => { if(keys.hasOwnProperty(e.key)) keys[e.key] = true; });
    viewport.addEventListener('keyup', (e) => { if(keys.hasOwnProperty(e.key)) keys[e.key] = false; });

    function updateTransform() {
        world.style.transform = `translate3d(${currentX}px, ${currentY}px, 0) scale(${scale})`;
        bgGrid.style.transform = `translate3d(${currentX * 0.4}px, ${currentY * 0.4}px, 0) scale(${scale})`;

        // Actualizar HUD Minimapa
        const radarScaleFactor = 150 / 3500; // 0.0428
        const viewW = (viewport.clientWidth / scale) * radarScaleFactor;
        const viewH = (viewport.clientHeight / scale) * radarScaleFactor;
        const viewX = (-currentX / scale) * radarScaleFactor;
        const viewY = (-currentY / scale) * radarScaleFactor;
        
        radarView.style.width = `${viewW}px`;
        radarView.style.height = `${viewH}px`;
        radarView.style.transform = `translate(${viewX}px, ${viewY}px)`;
    }

    // Bucle de renderizado para movimiento por teclado suave (60FPS)
    function gameLoop() {
        const speed = 15 / scale;
        if(keys.w || keys.ArrowUp) currentY += speed;
        if(keys.s || keys.ArrowDown) currentY -= speed;
        if(keys.a || keys.ArrowLeft) currentX += speed;
        if(keys.d || keys.ArrowRight) currentX -= speed;
        
        // Limitar bordes
        const minX = -(3500 * scale - viewport.clientWidth);
        const minY = -(2500 * scale - viewport.clientHeight);
        if (currentX > 100) currentX = 100;
        if (currentY > 100) currentY = 100;
        if (currentX < minX - 100) currentX = minX - 100;
        if (currentY < minY - 100) currentY = minY - 100;

        if(keys.w || keys.a || keys.s || keys.d || keys.ArrowUp || keys.ArrowLeft || keys.ArrowDown || keys.ArrowRight) {
            updateTransform();
        }
        requestAnimationFrame(gameLoop);
    }
    requestAnimationFrame(gameLoop);

    // Zoom
    viewport.addEventListener('wheel', (e) => {
        e.preventDefault();
        scale += e.deltaY * -0.001;
        scale = Math.min(Math.max(0.3, scale), 1.5);
        updateTransform();
    });

    // Panning por Mouse
    viewport.addEventListener('mousedown', (e) => {
        isDragging = true; viewport.style.cursor = 'grabbing';
        startX = e.clientX - currentX; startY = e.clientY - currentY;
    });
    window.addEventListener('mouseup', () => { isDragging = false; viewport.style.cursor = 'crosshair'; });
    window.addEventListener('mousemove', (e) => {
        if (!isDragging) return;
        currentX = e.clientX - startX; currentY = e.clientY - startY;
        updateTransform();
    });

    updateTransform();
</script>

</body>
</html>
"""

components.html(estacion_html, height=750, scrolling=False)

st.write("---")
st.caption("Terminal Core (OS v2.0): Topología Hub-and-Spoke, Filtro CRT, Navegación WASD, Radar HUD y Motor de Audio Espacial.")
