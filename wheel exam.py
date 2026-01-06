import streamlit as st
import streamlit.components.v1 as components

# Page configurations
st.set_page_config(page_title="isuru_wheel - නිපැයුම් රෝදය", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #121212; }
    iframe { width: 100% !important; height: 95vh !important; border: none; }
    </style>
    """, unsafe_allow_html=True)

html_code = """
<!DOCTYPE html>
<html lang="si">
<head>
    <style>
        body { background: #121212; color: white; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; overflow: hidden; font-family: sans-serif; }
        .game-container { position: relative; text-align: center; width: 600px; }
        .title { color: gold; font-size: 32px; font-weight: bold; margin-bottom: 10px; text-shadow: 2px 2px 10px rgba(255,215,0,0.5); }
        
        .wheel-box { position: relative; width: 360px; height: 360px; margin: auto; transition: transform 0.8s ease-in-out; }
        .wheel {
            width: 100%; height: 100%; border-radius: 50%; border: 8px solid white;
            transition: transform 4s cubic-bezier(0.15, 0, 0.15, 1);
            background: conic-gradient(#ff3b30 0deg 45deg, #4cd964 45deg 90deg, #ffcc00 90deg 135deg, #5ac8fa 135deg 180deg, #ff9500 180deg 225deg, #af52de 225deg 270deg, #5856d6 270deg 315deg, #ff2d55 315deg 360deg);
        }
        .pointer { 
            position: absolute; top: -25px; left: 50%; transform: translateX(-50%); 
            width: 0; height: 0; border-left: 20px solid transparent; border-right: 20px solid transparent; 
            border-top: 40px solid gold; z-index: 100;
        }

        /* රෝදය මැද පෙනෙන කොටස */
        .center-text { position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%) scale(0); background: white; color: black; padding: 15px; border-radius: 12px; font-weight: bold; font-size: 22px; z-index: 20; transition: 0.5s; border: 4px solid gold; width: 220px; text-align: center; box-shadow: 0 10px 20px rgba(0,0,0,0.5); }
        .center-text.active { transform: translate(-50%, -50%) scale(1); }

        .options-grid { display: none; grid-template-columns: 1fr 1fr; gap: 15px; margin-top: 30px; }
        .opt-btn { padding: 15px; border: none; border-radius: 12px; color: white; font-weight: bold; cursor: pointer; font-size: 16px; transition: 0.2s; }
        
        .spin-btn, .next-btn { padding: 15px 40px; font-size: 20px; font-weight: bold; border: none; border-radius: 50px; cursor: pointer; margin-top: 20px; }
        .spin-btn { background: gold; color: black; }
        .next-btn { background: #4cd964; color: white; display: none; }

        #msg-popup {
            position: fixed; bottom: 20px; left: 20px; 
            padding: 15px 30px; border-radius: 15px; font-size: 22px; font-weight: bold;
            z-index: 1000; transform: translateY(100px); transition: 0.4s ease;
            box-shadow: 0 4px 15px rgba(0,0,0,0.5);
        }
        #msg-popup.show { transform: translateY(0); }

        .score-board { position: fixed; bottom: 20px; right: 20px; background: rgba(0,0,0,0.6); padding: 10px 20px; border-radius: 15px; border: 2px solid gold; font-size: 24px; color: gold; font-weight: bold; }
    </style>
</head>
<body>

<div id="msg-popup"></div>

<div class="game-container">
    <div class="title">ඉසුරුගේ නිපැයුම් රෝදය</div>
    <div style="font-size: 18px; color: #aaa; margin-bottom: 20px;">ප්‍රශ්නය <span id="cur-lvl">1</span> / 20</div>
    
    <div id="wheel-wrapper" class="wheel-box">
        <div class="pointer"></div>
        <div id="wheel" class="wheel"></div>
        <div id="name-display" class="center-text"></div>
    </div>
    
    <button id="spin-btn" class="spin-btn" onclick="spinWheel()">නිපැයුම් රෝදය කරකවන්න</button>
    
    <div id="options" class="options-grid">
        <button class="opt-btn" style="background:#e74c3c" onclick="checkAnswer(0)"></button>
        <button class="opt-btn" style="background:#2ecc71" onclick="checkAnswer(1)"></button>
        <button class="opt-btn" style="background:#f39c12" onclick="checkAnswer(2)"></button>
        <button class="opt-btn" style="background:#3498db" onclick="checkAnswer(3)"></button>
    </div>

    <button id="next-btn" class="next-btn" onclick="nextLevel()">මීළඟ ප්‍රශ්නය →</button>
</div>

<div class="score-board">ලකුණු: <span id="score">0</span></div>

<script>
    let rotation = 0;
    let currentLevel = 0;
    let totalScore = 0;

    const gameData = [
        { inv: "රූපවාහිනිය", opts: ["ග්‍රැහැම් බෙල්", "ජෝන් ලොගී බෙයාර්ඩ්", "තෝමස් එඩිසන්", "නිකොලා ටෙස්ලා"], correct: 1 },
        { inv: "දුරකථනය", opts: ["අයිසැක් නිව්ටන්", "ඇල්බට් අයින්ස්ටයින්", "ග්‍රැහැම් බෙල්", "ගැලීලියෝ"], correct: 2 },
        { inv: "විදුලි බුබුල", opts: ["තෝමස් එඩිසන්", "නිකොලා ටෙස්ලා", "මයිකල් ෆැරඩේ", "නීල්ස් බෝර්"], correct: 0 },
        { inv: "පෙනිසිලින්", opts: ["ලුවී පාස්චර්", "ඇලෙක්සැන්ඩර් ෆ්ලෙමින්", "මාරි කියුරි", "චාල්ස් ඩාවින්"], correct: 1 },
        { inv: "ගුවන් විදුලිය", opts: ["මාකෝනි", "එඩිසන්", "ජේ.සී. බෝස්", "හර්ට්ස්"], correct: 0 },
        { inv: "ගුවන් යානය", opts: ["හෙන්රි ෆෝඩ්", "රයිට් සහෝදරයෝ", "ඩා වින්චි", "ටෙස්ලා"], correct: 1 },
        { inv: "වාෂ්ප එන්ජිම", opts: ["ජේම්ස් වොට්", "නිව්ටන්", "ස්ටීවන්සන්", "ඩීසල්"], correct: 0 },
        { inv: "ගුරුත්වාකර්ෂණය", opts: ["අයින්ස්ටයින්", "නිව්ටන්", "හෝකින්", "කෙප්ලර්"], correct: 1 },
        { inv: "රේඩියම්", opts: ["මාරි කියුරි", "නොබෙල්", "ඩෝල්ටන්", "රදර්ෆර්ඩ්"], correct: 0 },
        { inv: "දුරේක්ෂය", opts: ["ගැලීලියෝ", "හබල්", "කොපර්නිකස්", "කැසිනි"], correct: 0 },
        { inv: "අන්තර්ජාලය (WWW)", opts: ["බිල් ගේට්ස්", "ටිම් බර්නර්ස් ලී", "ස්ටීව් ජොබ්ස්", "සකර්බර්ග්"], correct: 1 },
        { inv: "අන්වීක්ෂය", opts: ["හුක්", "ලීවන්හුක්", "සෙකරියස් ජැන්සන්", "පාස්චර්"], correct: 2 },
        { inv: "උෂ්ණත්වමානය", opts: ["සෙල්සියස්", "ෆැරන්හයිට්", "ගැලීලියෝ", "කෙල්වින්"], correct: 1 },
        { inv: "මුද්‍රණ යන්ත්‍රය", opts: ["ගුටෙන්බර්ග්", "ෆ්‍රැන්ක්ලින්", "කැක්ස්ටන්", "එඩිසන්"], correct: 0 },
        { inv: "ඩයිනමයිට්", opts: ["ඇල්ෆ්‍රඩ් නොබෙල්", "ටෙස්ලා", "ඕපන්හයිමර්", "අයින්ස්ටයින්"], correct: 0 },
        { inv: "DNA ව්‍යුහය", opts: ["මෙන්ඩල්", "ඩාවින්", "වොට්සන් සහ ක්‍රික්", "ෆ්‍රැන්ක්ලින්"], correct: 2 },
        { inv: "වෙද නළාව", opts: ["රෙනේ ලෙනෙක්", "ලිස්ටර්", "ජෙනර්", "හාවි"], correct: 0 },
        { inv: "X-කිරණ", opts: ["රොන්ට්ජන්", "හෙන්රි බෙකරල්", "මාරි කියුරි", "ටෙස්ලා"], correct: 0 },
        { inv: "පරිගණකය", opts: ["ටියුරින්", "චාල්ස් බැබේජ්", "බිල් ගේට්ස්", "ලව්ලේස්"], correct: 1 },
        { inv: "එන්නත්කරණය", opts: ["එඩ්වඩ් ජෙනර්", "සෝල්ක්", "පාස්චර්", "සැබීන්"], correct: 0 }
    ];

    function showMsg(text, type) {
        const popup = document.getElementById('msg-popup');
        popup.innerText = text;
        popup.style.background = (type === 'success') ? '#2ecc71' : '#e74c3c';
        popup.classList.add('show');
        setTimeout(() => popup.classList.remove('show'), 3000);
    }

    function spinWheel() {
        document.getElementById('spin-btn').style.display = 'none';
        rotation += 1800 + Math.random() * 2000;
        document.getElementById('wheel').style.transform = `rotate(${rotation}deg)`;
        setTimeout(() => {
            document.getElementById('name-display').innerText = gameData[currentLevel].inv;
            document.getElementById('name-display').classList.add('active');
            showOptions();
        }, 4100);
    }

    function showOptions() {
        const btns = document.querySelectorAll('.opt-btn');
        btns.forEach((btn, i) => { btn.innerText = gameData[currentLevel].opts[i]; });
        document.getElementById('options').style.display = 'grid';
    }

    function checkAnswer(idx) {
        if(idx === gameData[currentLevel].correct) {
            totalScore += 10;
            document.getElementById('score').innerText = totalScore;
            showMsg("නිවැරදියි! ✅", "success");
            document.getElementById('options').style.display = 'none';
            document.getElementById('next-btn').style.display = 'inline-block';
        } else {
            showMsg("වැරදියි! ❌", "error");
        }
    }

    function nextLevel() {
        currentLevel++;
        if(currentLevel >= gameData.length) {
            showMsg("අවසන්! ලකුණු: " + totalScore, "success");
            setTimeout(() => location.reload(), 4000);
            return;
        }
        document.getElementById('cur-lvl').innerText = (currentLevel + 1);
        document.getElementById('next-btn').style.display = 'none';
        document.getElementById('spin-btn').style.display = 'inline-block';
        document.getElementById('name-display').classList.remove('active');
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
