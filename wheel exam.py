import streamlit as st
import streamlit.components.v1 as components

# Page Layout එක සැකසීම
st.set_page_config(page_title="Scientist Quiz Wheel", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #121212; }
    iframe { width: 100% !important; height: 95vh !important; border: none; }
    </style>
    """, unsafe_allow_html=True)

# මුළු රෝද 20 සඳහාම දත්ත සහ HTML Code එක
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
        .center-text { position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%) scale(0); background: white; color: black; padding: 10px 20px; border-radius: 10px; font-weight: bold; font-size: 22px; z-index: 20; transition: 0.5s; border: 3px solid gold; width: 200px; }
        .center-text.active { transform: translate(-50%, -50%) scale(1); }
        .options-grid { display: none; grid-template-columns: 1fr 1fr; gap: 15px; margin-top: 30px; }
        .opt-btn { padding: 15px; border: none; border-radius: 12px; color: white; font-weight: bold; cursor: pointer; font-size: 16px; transition: 0.2s; }
        .spin-btn, .next-btn { padding: 15px 40px; font-size: 20px; font-weight: bold; border: none; border-radius: 50px; cursor: pointer; margin-top: 20px; }
        .spin-btn { background: gold; color: black; }
        .next-btn { background: #4cd964; color: white; display: none; }
        .level-info { font-size: 18px; color: gold; margin-bottom: 10px; }
    </style>
</head>
<body>
<div class="game-container">
    <div class="level-info" id="level-display">Wheel 1 of 20</div>
    <div id="wheel-wrapper" class="wheel-box">
        <div class="pointer"></div>
        <div id="wheel" class="wheel"></div>
        <div id="name-display" class="center-text">?</div>
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
        { name: "EINSTEIN", opts: ["NEWTON", "EINSTEIN", "TESLA", "CURIE"], correct: 1 },
        { name: "NEWTON", opts: ["GALILEO", "PASTEUR", "NEWTON", "DARWIN"], correct: 2 },
        { name: "TESLA", opts: ["TESLA", "EDISON", "BELL", "BOYLE"], correct: 0 },
        { name: "CURIE", opts: ["BOHR", "FRANKLIN", "CURIE", "NOBEL"], correct: 2 },
        { name: "GALILEO", opts: ["GALILEO", "COPERNICUS", "KEPLER", "HUYGENS"], correct: 0 },
        { name: "DARWIN", opts: ["LAMARCK", "DARWIN", "WALLACE", "MENDEL"], correct: 1 },
        { name: "PASTEUR", opts: ["KOCH", "LISTER", "PASTEUR", "FLEMING"], correct: 2 },
        { name: "BOHR", opts: ["PLANCK", "BOHR", "SCHRODINGER", "HEISENBERG"], correct: 1 },
        { name: "EDISON", opts: ["TESLA", "EDISON", "MARCONI", "MORSE"], correct: 1 },
        { name: "HAWKING", opts: ["SAGAN", "HAWKING", "TYSON", "HUBBLE"], correct: 1 },
        { name: "FARADAY", opts: ["MAXWELL", "HERTZ", "FARADAY", "OHM"], correct: 2 },
        { name: "MENDEL", opts: ["MENDEL", "WATSON", "CRICK", "MORGAN"], correct: 0 },
        { name: "DA VINCI", opts: ["MICHELANGELO", "DA VINCI", "RAPHAEL", "DONATELLO"], correct: 1 },
        { name: "ARISTOTLE", opts: ["PLATO", "SOCRATES", "ARISTOTLE", "PYTHAGORAS"], correct: 2 },
        { name: "ARCHIMEDES", opts: ["EUCLID", "ARCHIMEDES", "PTOLEMY", "HERON"], correct: 1 },
        { name: "FLEMING", opts: ["PASTEUR", "FLEMING", "JENNER", "SALK"], correct: 1 },
        { name: "HUBBLE", opts: ["HUBBLE", "KEPLER", "CASSINI", "SITTER"], correct: 0 },
        { name: "MAXWELL", opts: ["MAXWELL", "BOLTZMANN", "GIBBS", "CLAUSIUS"], correct: 0 },
        { name: "LOVE LACE", opts: ["HOPPER", "LOVE LACE", "HAMILTON", "BARTIK"], correct: 1 },
        { name: "NOBEL", opts: ["DYER", "NOBEL", "ALFRED", "SOBRERO"], correct: 1 }
    ];

    function spinWheel() {
        document.getElementById('spin-btn').style.display = 'none';
        rotation += 1800 + Math.random() * 2000;
        document.getElementById('wheel').style.transform = "rotate(" + rotation + "deg)";
        setTimeout(() => {
            document.getElementById('name-display').innerText = "WHO IS THIS?";
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
            document.getElementById('name-display').innerText = gameData[currentLevel].name;
            document.getElementById('name-display').style.background = "#4cd964";
            document.getElementById('name-display').style.color = "white";
            document.getElementById('options').style.display = 'none';
            document.getElementById('next-btn').style.display = 'inline-block';
        } else { alert("Wrong! Try again."); }
    }

    function nextLevel() {
        currentLevel++;
        if(currentLevel >= gameData.length) { alert("Done!"); location.reload(); return; }
        document.getElementById('level-display').innerText = "Wheel " + (currentLevel + 1) + " of 20";
        document.getElementById('next-btn').style.display = 'none';
        document.getElementById('spin-btn').style.display = 'inline-block';
        document.getElementById('name-display').classList.remove('active');
        document.getElementById('name-display').style.background = "white";
        document.getElementById('name-display').style.color = "black";
        document.getElementById('options').style.display = 'none';
        let wrapper = document.getElementById('wheel-wrapper');
        wrapper.style.transform = "translateX(-100vw)";
        setTimeout(() => {
            wrapper.style.transition = "none";
            wrapper.style.transform = "translateX(100vw)";
            setTimeout(() => {
                wrapper.style.transition = "transform 0.8s ease-in-out";
                wrapper.style.transform = "translateX(0)";
            }, 50);
        }, 800);
    }
</script>
</body>
</html>
"""

components.html(html_code, height=900)
