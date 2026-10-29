import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Portafolio Interfaces Multimodales | Juan Pablo",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.title("🌌 Estación Multimodal (OS v3.0 - Full Semester)")
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
            position: absolute; top: 0; left: 0; width: 100%; height: 100%;
            background-color: #000; color: #00ff41; z-index: 10000;
            display: flex; flex-direction: column; justify-content: center; align-items: center;
            font-size: 14px; transition: opacity 0.5s ease-out; cursor: pointer;
        }
        .boot-text { margin: 5px; opacity: 0; }
        #start-btn {
            margin-top: 30px; padding: 10px 20px; border: 1px solid #00ff41; 
            background: transparent; color: #00ff41; font-family: inherit;
            cursor: pointer; opacity: 0; animation: blink 1s infinite;
        }

        /* --- FILTRO CRT RETRO-FUTURISTA --- */
        #crt-overlay {
            position: absolute; top: 0; left: 0; width: 100%; height: 100%;
            pointer-events: none; z-index: 9999;
            background: 
                linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.25) 50%),
                radial-gradient(circle, rgba(0,0,0,0) 60%, rgba(0,0,0,0.6) 100%);
            background-size: 100% 4px, 100% 100%; mix-blend-mode: overlay;
        }
        .chromatic { text-shadow: 2px 0px 1px rgba(255,0,0,0.5), -2px 0px 1px rgba(0,255,255,0.5); }

        /* --- HUD: RADAR / MINIMAPA --- */
        #hud-radar {
            position: absolute; bottom: 20px; left: 20px;
            width: 150px; height: 107px; 
            background: rgba(0, 20, 0, 0.8); border: 1px solid #00ff41;
            border-radius: 4px; z-index: 9000; pointer-events: none;
        }
        #radar-viewport {
            position: absolute; border: 1px solid #fff; background: rgba(255, 255, 255, 0.2);
            box-shadow: 0 0 10px #fff; transform-origin: 0 0; transition: all 0.1s;
        }
        .radar-node { position: absolute; background: #00ff41; border-radius: 50%; box-shadow: 0 0 5px #00ff41;}

        /* --- MUNDO Y PARALLAX --- */
        #background-grid {
            position: absolute; width: 7000px; height: 5000px;
            top: -1750px; left: -1750px;
            background-image: 
                linear-gradient(rgba(0, 255, 255, 0.04) 2px, transparent 2px),
                linear-gradient(90deg, rgba(0, 255, 255, 0.04) 2px, transparent 2px);
            background-size: 80px 80px; z-index: 0; transform-origin: center center; will-change: transform;
        }

        #particles {
            position: absolute; width: 3500px; height: 2500px;
            background-image: radial-gradient(#fff 1px, transparent 1px);
            background-size: 150px 150px; background-position: 0 0; opacity: 0.1; z-index: 1;
        }

        #world {
            position: absolute; width: 3500px; height: 2500px;
            z-index: 2; transform-origin: 0 0; will-change: transform;
        }

        /* --- ANIMACIONES --- */
        @keyframes blink { 0%, 100% { opacity: 1; } 50% { opacity: 0; } }
        @keyframes pulseGlow { 0%, 100% { box-shadow: 0 0 10px currentColor, inset 0 0 10px currentColor; } 50% { box-shadow: 0 0 25px currentColor, inset 0 0 20px currentColor; } }
        @keyframes dataPulseH { 0% { left: 0%; opacity: 0; } 10% { opacity: 1; } 90% { opacity: 1; } 100% { left: 100%; opacity: 0; } }
        @keyframes dataPulseV { 0% { top: 0%; opacity: 0; } 10% { opacity: 1; } 90% { opacity: 1; } 100% { top: 100%; opacity: 0; } }
        
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

        /* TOPOLOGÍA MOTHERBOARD V3 (Coordenadas X/Y y Colores del Espectro) */
        /* Columna Izquierda */
        #s6  { top: 200px; left: 300px; width: 400px; color: #ff0055; }
        #s7  { top: 700px; left: 300px; width: 550px; color: #ff5500; }
        #s8  { top: 1200px; left: 300px; width: 550px; color: #ffcc00; }
        #s9  { top: 1700px; left: 300px; width: 400px; color: #aaff00; }
        
        /* Columna Derecha */
        #s10 { top: 200px; left: 2400px; width: 250px; color: #00ffaa; }
        #s11 { top: 700px; left: 2400px; width: 550px; color: #00d2ff; }
        #s12 { top: 1200px; left: 2400px; width: 700px; color: #0055ff; }
        #s13 { top: 1700px; left: 2400px; width: 600px; color: #b829ff; }
        
        /* CORE Ciberfísico en el Centro */
        #s14 { top: 950px; left: 1250px; width: 800px; color: #00ff41; box-shadow: 0 0 80px rgba(0,255,65,0.15); } 
        
        /* Easter Egg */
        #easter-egg { top: 2100px; left: 3000px; color: #ff0055; border: 1px dotted #ff0055; border-radius: 50%; width: 120px; height: 120px; display: flex; flex-direction: column; align-items: center; justify-content: center; position: absolute; font-size: 10px; text-decoration: none; }

    </style>
</head>
<body>

<div id="viewport" tabindex="0">
    <div id="crt-overlay"></div>
    
    <!-- HUD Minimapa (Con los 9 puntos + Core) -->
    <div id="hud-radar">
        <div id="radar-viewport"></div>
        <!-- Puntos generados proporcionalmente -->
        <div class="radar-node" style="top: 8px; left: 12px; width: 3px; height: 3px;"></div> <!-- S6 -->
        <div class="radar-node" style="top: 30px; left: 12px; width: 3px; height: 3px;"></div> <!-- S7 -->
        <div class="radar-node" style="top: 51px; left: 12px; width: 3px; height: 3px;"></div> <!-- S8 -->
        <div class="radar-node" style="top: 72px; left: 12px; width: 3px; height: 3px;"></div> <!-- S9 -->
        <div class="radar-node" style="top: 8px; left: 102px; width: 3px; height: 3px;"></div> <!-- S10 -->
        <div class="radar-node" style="top: 30px; left: 102px; width: 3px; height: 3px;"></div> <!-- S11 -->
        <div class="radar-node" style="top: 51px; left: 102px; width: 3px; height: 3px;"></div> <!-- S12 -->
        <div class="radar-node" style="top: 72px; left: 102px; width: 3px; height: 3px;"></div> <!-- S13 -->
        <div class="radar-node" style="top: 40px; left: 53px; width: 6px; height: 6px; background:#fff;"></div> <!-- S14 CORE -->
    </div>

    <!-- Pantalla de Arranque -->
    <div id="boot-screen" onclick="initSystem()">
        <div class="boot-text" id="bt1">Initialize M-UI System... [OK]</div>
        <div class="boot-text" id="bt2">Loading Semesters 6-14 Arrays... [OK]</div>
        <div class="boot-text" id="bt3">Syncing Multi-Modal Neural Links... [OK]</div>
        <div class="boot-text" id="bt4">Booting Audio Engine... [OK]</div>
        <button id="start-btn">ACCESS GRANTED. CLICK TO ENTER</button>
    </div>

    <div id="background-grid"></div>
    <div id="world">
        <div id="particles"></div>

        <!-- CABLES DE DATOS AL CORE (Centralizando la info) -->
        <div class="cable cable-h" style="top: 1000px; left: 850px; width: 400px; color: #ff5500;"><div class="data-packet data-h" style="animation-delay: 0.5s;"></div></div>
        <div class="cable cable-h" style="top: 1100px; left: 2050px; width: 350px; color: #00d2ff;"><div class="data-packet data-h" style="animation-direction: reverse; animation-delay: 1.2s;"></div></div>

        <!-- CLASE 6 -->
        <div class="sector" id="s6" data-freq="200">
            <div class="sector-title chromatic">Clase 6: FUNDAMENTOS WEB</div>
            <a href="https://clase-6---desarrollo-de-app-web-97pdkxyvqqnj5luducjg38.streamlit.app/" target="_blank" class="terminal"><span class="icon">🌐</span> Web Intro</a>
            <a href="https://clase-6---text-to-sp-ath9eygyhb2r3rgzjhbxbk.streamlit.app/" target="_blank" class="terminal"><span class="icon">🔊</span> Text to Speech</a>
        </div>

        <!-- CLASE 7 -->
        <div class="sector" id="s7" data-freq="250">
            <div class="sector-title chromatic">Clase 7: TEXTO & OCR</div>
            <a href="https://traductor-ipxgbappqwcw9wmtqddyqvv.streamlit.app/" target="_blank" class="terminal"><span class="icon">🌍</span> Traductor</a>
            <a href="https://ocr-clase-7-8wgd2bf4rhhdnplb52oxpm.streamlit.app/" target="_blank" class="terminal"><span class="icon">🔎</span> OCR Visual</a>
            <a href="https://ocr-audio-clase7-jfz3mwxpp46uwno5xyfutz.streamlit.app/" target="_blank" class="terminal"><span class="icon">🎧</span> OCR + Audio</a>
        </div>

        <!-- CLASE 8 -->
        <div class="sector" id="s8" data-freq="300">
            <div class="sector-title chromatic">Clase 8: NLP & SENTIMENT</div>
            <a href="https://wordcloud-clase8-hxs9htgtrtb9wqfc9z5o59.streamlit.app/" target="_blank" class="terminal"><span class="icon">☁️</span> Wordcloud</a>
            <a href="https://sentimenta---clase-8-uatalbpxsc4zhpjanabgtj.streamlit.app/" target="_blank" class="terminal"><span class="icon">🎭</span> Sentify</a>
            <a href="https://tfidf-clase-8-juc8jdmdrpwghna6f4b8hg.streamlit.app/" target="_blank" class="terminal"><span class="icon">📊</span> Sentify Search</a>
        </div>

        <!-- CLASE 9 -->
        <div class="sector" id="s9" data-freq="350">
            <div class="sector-title chromatic">Clase 9: VISIÓN & ML</div>
            <a href="https://yolov5-clase9-9tg7bdcggnqyapb7p4z8yn.streamlit.app/" target="_blank" class="terminal"><span class="icon">🎯</span> YOLOv5 Object</a>
            <a href="https://tm-clase9-6kcwat3b8fqtgeggtabkaw.streamlit.app/" target="_blank" class="terminal"><span class="icon">🤖</span> Teach. Machine</a>
        </div>

        <!-- CLASE 10 -->
        <div class="sector" id="s10" data-freq="400">
            <div class="sector-title chromatic">Clase 10: GESTOS</div>
            <a href="https://sites.google.com/view/gestos/p%C3%A1gina-principal" target="_blank" class="terminal" style="border-style: dotted;"><span class="icon">📚</span> Docs / Teoría</a>
        </div>
        
        <!-- CLASE 11 -->
        <div class="sector" id="s11" data-freq="450">
            <div class="sector-title chromatic">Clase 11: LLMs</div>
            <a href="https://sites.google.com/view/procesamiento-de-lenguaje-natu/inicio" target="_blank" class="terminal" style="border-style: dotted;"><span class="icon">📚</span> Docs NLP</a>
            <a href="https://chatpdf-clase-11-jy87wpkuwbydsszmx37mtk.streamlit.app/" target="_blank" class="terminal"><span class="icon">📄</span> Chat PDF v1</a>
            <a href="https://chatpdf-clase-11-asnq94pjetrhqqduup3sqb.streamlit.app/" target="_blank" class="terminal"><span class="icon">💬</span> Chat PDF v2</a>
        </div>

        <!-- CLASE 12 -->
        <div class="sector" id="s12" data-freq="500">
            <div class="sector-title chromatic">Clase 12: TÁCTIL/VISIÓN</div>
            <a href="https://sites.google.com/view/handwr?usp=sharing" target="_blank" class="terminal" style="border-style: dotted;"><span class="icon">📚</span> Docs Táctil</a>
            <a href="https://mnistpred-clase12-tnokntyr9x5j5ebbsoqhoa.streamlit.app/" target="_blank" class="terminal"><span class="icon">🔢</span> MNIST Pred</a>
            <a href="https://tablero-clase-12-92e6sliunqhxkuy4vgwgty.streamlit.app/" target="_blank" class="terminal"><span class="icon">✏️</span> Tablero Draw</a>
            <a href="https://drawrecog-clase-12-4cfuntf48mmhrlz97vpydx.streamlit.app/" target="_blank" class="terminal"><span class="icon">👁️</span> DrawRecog</a>
            <a href="https://clase12-taller-kszzd7oqhvpdavw5vkyfjm.streamlit.app/" target="_blank" class="terminal"><span class="icon">🛠️</span> Taller Studio</a>
        </div>

        <!-- CLASE 13 -->
        <div class="sector" id="s13" data-freq="550">
            <div class="sector-title chromatic">Clase 13: IoT & VOZ</div>
            <a href="https://sites.google.com/view/sistemasconiot/p%C3%A1gina-principal" target="_blank" class="terminal" style="border-style: dotted;"><span class="icon">📚</span> Docs IoT</a>
            <a href="https://recepmqtt-clase13-m99szh2udgeecr46cebwu3.streamlit.app/" target="_blank" class="terminal"><span class="icon">📥</span> MQTT RX</a>
            <a href="https://sendcmqtt-clase13-ydyfbaz55vqm73mjnny59x.streamlit.app/" target="_blank" class="terminal"><span class="icon">📤</span> MQTT TX</a>
            <a href="https://ctrlvoice---clase-13-w7zlxchbtedjdurb2hnck2.streamlit.app/" target="_blank" class="terminal"><span class="icon">🎙️</span> Voice Cmd</a>
        </div>

        <!-- CLASE 14 -->
        <div class="sector" id="s14" data-freq="800">
            <div class="sector-title chromatic">Clase 14: CORE CIBERFÍSICO</div>
            <a href="https://drive.google.com/file/d/1L9RMLfuTadEA3OZ2iUIl3spFO-FF0CAp/view?usp=sharing" target="_blank" class="terminal" style="border-style: dotted;"><span class="icon">📚</span> Repo Base</a>
            <a href="https://clase-14-mqtt-multipage-vu46kvdslwh7eetd4vxfgr.streamlit.app/Control_por_voz" target="_blank" class="terminal"><span class="icon">🗣️</span> Voice Mult</a>
            <a href="https://clase14-ciuzhl6lg5ykxmoeqhlrdg.streamlit.app/" target="_blank" class="terminal"><span class="icon">⚙️</span> Main Cyber</a>
            <a href="https://clase14-visioncomb-4kibapppgcfjnvmgmxuyew6.streamlit.app/" target="_blank" class="terminal"><span class="icon">📷</span> Vision Comb</a>
            <a href="https://cerraduragestos-clase14-iuzlc5yhaapha4p9zfphnm.streamlit.app/" target="_blank" class="terminal"><span class="icon">🖐️</span> Gestos Lock</a>
        </div>

        <a href="https://www.instagram.com/ttt.discos" target="_blank" id="easter-egg" data-freq="180">
            <span style="font-size: 24px;">🎛️</span><br>s0lid142<br>Beat Lab
        </a>
    </div>
</div>

<script>
    // --- 1. BOOT SEQUENCE ---
    setTimeout(() => document.getElementById('bt1').style.opacity = 1, 500);
    setTimeout(() => document.getElementById('bt2').style.opacity = 1, 1000);
    setTimeout(() => document.getElementById('bt3').style.opacity = 1, 1500);
    setTimeout(() => document.getElementById('bt4').style.opacity = 1, 2000);
    setTimeout(() => document.getElementById('start-btn').style.opacity = 1, 2500);

    // --- 2. MOTOR DE AUDIO ---
    const AudioContext = window.AudioContext || window.webkitAudioContext;
    let audioCtx;

    function initSystem() {
        document.getElementById('boot-screen').style.opacity = 0;
        setTimeout(() => document.getElementById('boot-screen').style.display = 'none', 500);
        document.getElementById('viewport').focus(); 

        if (!audioCtx) audioCtx = new AudioContext();
        if (audioCtx.state === 'suspended') audioCtx.resume();
        
        let droneOsc = audioCtx.createOscillator();
        const droneGain = audioCtx.createGain();
        droneOsc.type = 'sine';
        droneOsc.frequency.setValueAtTime(55, audioCtx.currentTime); 
        droneGain.gain.setValueAtTime(0.015, audioCtx.currentTime); 
        droneOsc.connect(droneGain);
        droneGain.connect(audioCtx.destination);
        droneOsc.start();
    }

    function playHoverSound(freq) {
        if (!audioCtx) return;
        const osc = audioCtx.createOscillator();
        const gainNode = audioCtx.createGain();
        const panner = audioCtx.createStereoPanner(); 
        
        osc.type = 'square'; 
        osc.frequency.setValueAtTime(freq, audioCtx.currentTime);
        osc.frequency.exponentialRampToValueAtTime(freq/2, audioCtx.currentTime + 0.15);
        
        gainNode.gain.setValueAtTime(0.02, audioCtx.currentTime);
        gainNode.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 0.15);
        
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
    
    let currentX = -800, currentY = -600, scale = 0.65; 
    let isDragging = false, startX, startY;
    const keys = { w: false, a: false, s: false, d: false, ArrowUp: false, ArrowLeft: false, ArrowDown: false, ArrowRight: false };

    viewport.addEventListener('keydown', (e) => { if(keys.hasOwnProperty(e.key)) keys[e.key] = true; });
    viewport.addEventListener('keyup', (e) => { if(keys.hasOwnProperty(e.key)) keys[e.key] = false; });

    function updateTransform() {
        world.style.transform = `translate3d(${currentX}px, ${currentY}px, 0) scale(${scale})`;
        bgGrid.style.transform = `translate3d(${currentX * 0.4}px, ${currentY * 0.4}px, 0) scale(${scale})`;

        const radarScaleFactor = 150 / 3500; 
        const viewW = (viewport.clientWidth / scale) * radarScaleFactor;
        const viewH = (viewport.clientHeight / scale) * radarScaleFactor;
        const viewX = (-currentX / scale) * radarScaleFactor;
        const viewY = (-currentY / scale) * radarScaleFactor;
        
        radarView.style.width = `${viewW}px`;
        radarView.style.height = `${viewH}px`;
        radarView.style.transform = `translate(${viewX}px, ${viewY}px)`;
    }

    function gameLoop() {
        const speed = 15 / scale;
        if(keys.w || keys.ArrowUp) currentY += speed;
        if(keys.s || keys.ArrowDown) currentY -= speed;
        if(keys.a || keys.ArrowLeft) currentX += speed;
        if(keys.d || keys.ArrowRight) currentX -= speed;
        
        const minX = -(3500 * scale - viewport.clientWidth);
        const minY = -(2500 * scale - viewport.clientHeight);
        if (currentX > 200) currentX = 200;
        if (currentY > 200) currentY = 200;
        if (currentX < minX - 200) currentX = minX - 200;
        if (currentY < minY - 200) currentY = minY - 200;

        if(keys.w || keys.a || keys.s || keys.d || keys.ArrowUp || keys.ArrowLeft || keys.ArrowDown || keys.ArrowRight) {
            updateTransform();
        }
        requestAnimationFrame(gameLoop);
    }
    requestAnimationFrame(gameLoop);

    viewport.addEventListener('wheel', (e) => {
        e.preventDefault();
        scale += e.deltaY * -0.001;
        scale = Math.min(Math.max(0.3, scale), 1.5);
        updateTransform();
    });

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
st.caption("Terminal Core (OS v3.0): Todas las entregas (Clase 6 a 14) conectadas al Hub Ciberfísico Central.")
