import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Invention Quiz Wheel", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #121212; }
    iframe { width: 100% !important; height: 95vh !important; border: none; }
    </style>
    """, unsafe_allow_html=True)

html_code = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { background: #121212; color: white; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; overflow: hidden; font-family: sans-serif; }
        .game-container { position: relative; text-align: center; width: 600px; }
        .wheel-box { position: relative; width: 380px; height: 380px; margin: auto; transition: transform 0.8s ease-in-out; }
        .wheel {
            width: 100%; height: 100%; border-radius: 50%; border: 8px solid gold;
            transition: transform 4s cubic-bezier(0.15, 0, 0.15, 1);
            background: conic-gradient(#ff3b30 0deg 45deg, #4cd964 45deg 90deg, #ffcc00 90deg 135deg, #5ac8fa 135deg 180deg, #ff9500 180deg 225deg, #af52de 225deg 270deg, #5856d6 270deg 315deg, #ff2d55 315deg 360deg);
        }
        .pointer { position: absolute; top: -15px; left: 50%; transform: translateX(-50%); width: 0; height: 0; border-left: 20px solid transparent; border-right: 20px solid transparent; border-bottom: 35px solid gold; z-index: 30; }
        .center-text { position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%) scale(0); background: white; color: black; padding: 15px; border-radius: 12px; font-weight: bold; font-size: 22px; z-index: 20; transition: 0.5s; border: 4px solid gold; width: 250px; text-align: center; }
        .center-text.active { transform: translate(-50%, -50%) scale(1); }
        .options-grid { display: none; grid-template-columns: 1fr 1fr; gap: 15px; margin-top: 30px; }
        .opt-btn { padding: 15px; border: none; border-radius: 12px; color: white; font-weight: bold; cursor: pointer; font-size: 16px; transition: 0.2s; }
        .spin-btn, .next-btn { padding: 15px 40px; font-size: 20px; font-weight: bold; border: none; border-radius: 50px; cursor: pointer; margin-top: 20px; }
        .spin-btn { background: gold; color: black; }
        .next-btn { background: #4cd964; color: white; display: none; }
    </style>
</head>
<body>
<div class="game-container">
    <div style="font-size: 20px; color: gold; margin-bottom: 15px;">Wheel <span id="cur-lvl">1</span> of 20</div>
    <div id="wheel-wrapper" class="wheel-box">
        <div class="pointer"></div>
        <div id="wheel" class="wheel"></div>
        <div id="name-display" class="center-text"></div>
    </div>
    <button id="spin-btn" class="spin-btn" onclick="spinWheel()">SPIN WHEEL</button>
    <div id="options" class="options-grid">
        <button class="opt-btn" style="background:#e74c3c" onclick="checkAnswer(0)"></button>
        <button class="opt-btn" style="background:#2ecc71" onclick="checkAnswer(1)"></button>
        <button class="opt-btn" style="background:#f39c12" onclick="checkAnswer(2)"></button>
        <button class="opt-btn" style="background:#3498db" onclick="checkAnswer(3)"></button>
    </div>
    <button id="next-btn" class="next-btn" onclick="nextLevel()">NEXT WHEEL →</button>
</div>

<script>
    let rotation = 0;
    let currentLevel = 0;
    const gameData = [
        { inv: "TELEVISION", opts: ["Graham Bell", "J.L. Baird", "Edison", "Tesla"], correct: 1 },
        { inv: "TELEPHONE", opts: ["Newton", "Einstein", "Graham Bell", "Galileo"], correct: 2 },
        { inv: "LIGHT BULB", opts: ["Thomas Edison", "Tesla", "Faraday", "Bohr"], correct: 0 },
        { inv: "PENICILLIN", opts: ["Pasteur", "Fleming", "Curie", "Darwin"], correct: 1 },
        { inv: "RADIO", opts: ["Marconi", "Edison", "Bose", "Hertz"], correct: 0 },
        { inv: "AEROPLANE", opts: ["Ford", "Wright Brothers", "Da Vinci", "Tesla"], correct: 1 },
        { inv: "STEAM ENGINE", opts: ["James Watt", "Newton", "Stephenson", "Diesel"], correct: 0 },
        { inv: "GRAVITY", opts: ["Einstein", "Newton", "Hawking", "Kepler"], correct: 1 },
        { inv: "RADIUM", opts: ["Marie Curie", "Nobel", "Dalton", "Rutherford"], correct: 0 },
        { inv: "TELESCOPE", opts: ["Galileo", "Hubble", "Copernicus", "Cassini"], correct: 0 },
        { inv: "WORLD WIDE WEB", opts: ["Bill Gates", "Tim Berners-Lee", "Jobs", "Zuckerberg"], correct: 1 },
        { inv: "MICROSCOPE", opts: ["Hooke", "Leeuwenhoek", "Janssen", "Pasteur"], correct: 2 },
        { inv: "THERMOMETER", opts: ["Celsius", "Fahrenheit", "Galileo", "Kelvin"], correct: 1 },
        { inv: "PRINTING PRESS", opts: ["Gutenberg", "Franklin", "Caxton", "Edison"], correct: 0 },
        { inv: "DYNAMITE", opts: ["Alfred Nobel", "Tesla", "Oppenheimer", "Einstein"], correct: 0 },
        { inv: "DNA STRUCTURE", opts: ["Mendel", "Darwin", "Watson & Crick", "Franklin"], correct: 2 },
        { inv: "STETHOSCOPE", opts: ["Laennec", "Lister", "Jenner", "Harvey"], correct: 0 },
        { inv: "X-RAY", opts: ["Roentgen", "Bequerel", "Curie", "Tesla"], correct: 0 },
        { inv: "COMPUTER", opts: ["Alan Turing", "Charles Babbage", "Bill Gates", "Ada Lovelace"], correct: 1 },
        { inv: "VACCINATION", opts: ["Edward Jenner", "Salk", "Pasteur", "Sabine"], correct: 0 }
    ];

    function spinWheel() {
        document.getElementById('spin-btn').style.display = 'none';
        rotation += 1800 + Math.random() * 2000;
        document.getElementById('wheel').style.transform = "rotate(" + rotation + "deg)";
        setTimeout(() => {
            // මෙතන තමයි කලින් වැරැද්ද තිබුණේ, දැන් කෙළින්ම Invention එක පේනවා
            document.getElementById('name-display').innerText = gameData[currentLevel].inv;
            document.getElementById('name-display').classList.add('active');
            showOptions();
        }, 4100);
    }

    function showOptions() {
        const btns = document.querySelectorAll('.opt-btn');
        const levelData = gameData[currentLevel];
        btns.forEach((btn, i) => { btn.innerText = levelData.opts[i]; });
        document.getElementById('options').style.display = 'grid';
    }

    function checkAnswer(idx) {
        if(idx === gameData[currentLevel].correct) {
            document.getElementById('name-display').style.background = "#4cd964";
            document.getElementById('name-display').style.color = "white";
            document.getElementById('options').style.display = 'none';
            document.getElementById('next-btn').style.display = 'inline-block';
        } else { alert("වැරදියි! නැවත උත්සාහ කරන්න."); }
    }

    function nextLevel() {
        currentLevel++;
        if(currentLevel >= gameData.length) { alert("Congratulations!"); location.reload(); return; }
        document.getElementById('cur-lvl').innerText = (currentLevel + 1);
        document.getElementById('next-btn').style.display = 'none';
        document.getElementById('spin-btn').style.display = 'inline-block';
        document.getElementById('name-display').classList.remove('active');
        document.getElementById('name-display').style.background = "white";
        document.getElementById('name-display').style.color = "black";
        document.getElementById('options').style.display = 'none';
        let wrapper = document.getElementById('wheel-wrapper');
        wrapper.style.transform = "translateX(-100vw)";
        setTimeout(() => {
            wrapper.style.transition = "none"; wrapper.style.transform = "translateX(100vw)";
            setTimeout(() => {
                wrapper.style.transition = "transform 0.8s ease-in-out"; wrapper.style.transform = "translateX(0)";
            }, 50);
        }, 800);
    }
</script>
</body>
</html>
"""

components.html(html_code, height=900)
