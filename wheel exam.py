import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="විද්‍යාත්මක සොයාගැනීම් - රෝදය", layout="wide")

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
        
        /* රෝදය සහ ඊතලය */
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

        /* මැද පෙනෙන Invention එක */
        .center-text { position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%) scale(0); background: white; color: black; padding: 15px; border-radius: 12px; font-weight: bold; font-size: 20px; z-index: 20; transition: 0.5s; border: 4px solid gold; width: 220px; text-align: center; }
        .center-text.active { transform: translate(-50%, -50%) scale(1); }

        /* Options */
        .options-grid { display: none; grid-template-columns: 1fr 1fr; gap: 15px; margin-top: 30px; }
        .opt-btn { padding: 15px; border: none; border-radius: 12px; color: white; font-weight: bold; cursor: pointer; font-size: 16px; transition: 0.2s; }
        
        .spin-btn, .next-btn { padding: 15px 40px; font-size: 20px; font-weight: bold; border: none; border-radius: 50px; cursor: pointer; margin-top: 20px; }
        .spin-btn { background: gold; color: black; }
        .next-btn { background: #4cd964; color: white; display: none; }

        /* Custom Notification Popup (Alert වෙනුවට) */
        #msg-popup {
            position: fixed; top: 20%; left: 50%; transform: translate(-50%, -50%) scale(0);
            padding: 20px 40px; border-radius: 15px; font-size: 24px; font-weight: bold;
            z-index: 1000; transition: 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        }
        #msg-popup.show { transform: translate(-50%, -50%) scale(1); }

        .score-board { position: fixed; bottom: 20px; right: 20px; background: rgba(0,0,0,0.6); padding: 10px 20px; border-radius: 15px; border: 2px solid gold; font-size: 24px; color: gold; font-weight: bold; }
    </style>
</head>
<body>

<div id="msg-popup"></div>

<div class="game-container">
    <div style="font-size: 20px; color: gold; margin-bottom: 20px;">රෝදය <span id="cur-lvl">1</span> / 20</div>
    <div id="wheel-wrapper" class="wheel-box">
        <div class="pointer"></div>
        <div id="wheel" class="wheel"></div>
        <div id="name-display" class="center-text"></div>
    </div>
    
    <button id="spin-btn" class="spin-btn" onclick="spinWheel()">රෝදය කරකවන්න</button>
    
    <div id="options" class="options-grid">
        <button class="opt-btn" style="background:#e74c3c" onclick="checkAnswer(0)"></button>
        <button class="opt-btn" style="background:#2ecc71" onclick="checkAnswer(1)"></button>
        <button class="opt-btn" style="background:#f39c12" onclick="checkAnswer(2)"></button>
        <button class="opt-btn" style="background:#3498db" onclick="checkAnswer(3)"></button>
    </div>

    <button id="next-btn" class="next-btn" onclick="nextLevel()">මීළඟ රෝදය →</button>
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
        { inv:
