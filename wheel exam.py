import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Scientist Quiz Wheel", layout="wide")

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
        body { background: #121212; color: white; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; overflow: hidden; font-family: 'Segoe UI', sans-serif; }
        .game-container { position: relative; text-align: center; width: 600px; }
        
        /* රෝදයේ සැකසුම */
        .wheel-box { position: relative; width: 400px; height: 400px; margin: auto; transition: transform 0.8s ease-in-out; }
        .wheel {
            width: 100%; height: 100%; border-radius: 50%; border: 8px solid gold;
            transition: transform 4s cubic-bezier(0.15, 0, 0.15, 1);
            background: conic-gradient(#ff3b30 0deg 45deg, #4cd964 45deg 90deg, #ffcc00 90deg 135deg, #5ac8fa 135deg 180deg, #ff9500 180deg 225deg, #af52de 225deg 270deg, #5856d6 270deg 315deg, #ff2d55 315deg 360deg);
        }
        
        .pointer { position: absolute; top: -15px; left: 50%; transform: translateX(-50%); width: 0; height: 0; border-left: 20px solid transparent; border-right: 20px solid transparent; border-bottom: 35px solid gold; z-index: 30; }
        .center-text { position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%) scale(0); background: white; color: black; padding: 10px 20px; border-radius: 10px; font-weight: bold; font-size: 24px; z-index: 20; transition: 0.5s; border: 3px solid gold; }
        .center-text.active { transform: translate(-50%, -50%) scale(1); }

        /* MCQ Buttons */
        .options-grid { display: none; grid-template-columns: 1fr 1fr; gap: 15px; margin-top: 30px; animation: fadeIn 0.5s; }
        @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
        .opt-btn { padding: 15px; border: none; border-radius: 12px; color: white; font-weight: bold; cursor: pointer; font-size: 16px; transition: 0.2s; }
        .opt-btn:hover { transform: scale(1.05); filter: brightness(1.2); }

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
