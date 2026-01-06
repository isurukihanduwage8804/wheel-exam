import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="8-Segment Wheel", layout="wide")

# Error එක තිබුණු තැන නිවැරදි කර ඇත: unsafe_allow_html=True
st.markdown("""
    <style>
    .main { background-color: #121212; }
    iframe { width: 100% !important; height: 90vh !important; border: none; }
    </style>
    """, unsafe_allow_html=True)

# HTML/JS Code එක (පෙර පරිදිම)
html_code = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { background: #121212; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; overflow: hidden; font-family: sans-serif; }
        .game-container { position: relative; text-align: center; }
        .wheel-box { position: relative; width: 500px; height: 500px; animation: slideIn 1s ease-out; }
        @keyframes slideIn { from { transform: translateX(100%); opacity: 0; } to { transform: translateX(0); opacity: 1; } }
        .wheel {
            width: 100%; height: 100%; border-radius: 50%; border: 10px solid gold;
            transition: transform 4s cubic-bezier(0.15, 0, 0.15, 1);
            background: conic-gradient(
                #ff3b30 0deg 45deg, #4cd964 45deg 90deg, #ffcc00 90deg 135deg, 
                #5ac8fa 135deg 180deg, #ff9500 180deg 225deg, #af52de 225deg 270deg, 
                #5856d6 270deg 315deg, #ff2d55 315deg 360deg
            );
        }
        .center-text {
            position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%) scale(0);
            background: white; color: black; padding: 15px 30px; border-radius: 15px;
            font-size: 28px; font-weight: bold; z-index: 20; transition: 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        }
        .center-text.active { transform: translate(-50%, -50%) scale(1); }
        .pointer { position: absolute; top: -20px; left: 50%; transform: translateX(-50%); width: 0; height: 0; border-left: 20px solid transparent; border-right: 20px solid transparent; border-bottom: 40px solid gold; z-index: 30; }
        button { padding: 15px 40px; font-size: 20px; font-weight: bold; border: none; border-radius: 50px; cursor: pointer; margin: 10px; }
        .spin-btn { background: gold; color: black; }
        .next-btn { background: #4cd964; color: white; display: none; }
    </style>
</head>
<body>
<div class="game-container">
    <div id="wheel-wrapper" class="wheel-box">
        <div class="pointer"></div>
        <div id="wheel" class="wheel"></div>
        <div id="name-display" class="center-text">NAME</div>
    </div>
    <div style="margin-top: 30px;">
        <button id="spin-btn" class="spin-btn" onclick="spinWheel()">SPIN</button>
        <button id="next-btn" class="next-btn" onclick="nextLevel()">NEXT WHEEL →</button>
    </div>
</div>
<script>
    let rotation = 0;
    let currentLevel = 0;
    const data = ["EINSTEIN", "NEWTON", "TESLA", "CURIE", "GALILEO", "DARWIN", "PASTEUR", "BOHR"];
    function spinWheel() {
        document.getElementById('spin-btn').style.display = 'none';
        rotation += 1800 + Math.random() * 2000;
        document.getElementById('wheel').style.transform = "rotate(" + rotation + "deg)";
        setTimeout(() => {
            let display = document.getElementById('name-display');
            display.innerText = data[currentLevel];
            display.classList.add('active');
            document.getElementById('next-btn').style.display = 'inline-block';
        }, 4100);
    }
    function nextLevel() {
        currentLevel = (currentLevel + 1) % data.length;
        let wrapper = document.getElementById('wheel-wrapper');
        wrapper.style.animation = 'none';
        void wrapper.offsetWidth;
        wrapper.style.animation = 'slideIn 1s ease-out';
        document.getElementById('name-display').classList.remove('active');
        document.getElementById('next-btn').style.display = 'none';
        document.getElementById('spin-btn').style.display = 'inline-block';
    }
</script>
</body>
</html>
"""

components.html(html_code, height=800)
