import streamlit as st
import streamlit.components.v1 as components

# Page configuration
st.set_page_config(page_title="20 Wheels Challenge", layout="centered")

st.title("🎡 Scientist Wheel Challenge")

# රෝද 20 සඳහා දත්ත (Data for 20 Wheels)
if 'current_wheel' not in st.session_state:
    st.session_state.current_wheel = 1

# මෙතනට ඔයාගේ විද්‍යාඥයින් 20 දෙනාගේ නම් සහ Options දාන්න
wheel_data = [
    {"name": "EINSTEIN", "opts": ["NEWTON", "EINSTEIN", "TESLA", "CURIE"], "correct": 1},
    {"name": "NEWTON", "opts": ["GALILEO", "PASTEUR", "NEWTON", "DARWIN"], "correct": 2},
    {"name": "TESLA", "opts": ["TESLA", "EDISON", "BELL", "BOYLE"], "correct": 0},
    # ... තව 17ක් මේ විදියටම ලැයිස්තුවට එකතු කරන්න
]

# HTML/JavaScript Code එක (Wheel Logic එක ඇතුළුව)
html_code = f"""
<div id="game-container" style="text-align:center; color:white; font-family:sans-serif;">
    <h3 id="level-txt">Wheel: {st.session_state.current_wheel} / 20</h3>
    <div style="position:relative; width:300px; height:300px; margin:auto;">
        <div id="wheel" style="width:100%; height:100%; border-radius:50%; border:5px solid white; transition: transform 4s cubic-bezier(0.15, 0, 0.15, 1); background: conic-gradient(#ff3b30 0% 25%, #4cd964 25% 50%, #ffcc00 50% 75%, #5ac8fa 75% 100%);"></div>
        <div id="center-text" style="position:absolute; top:50%; left:50%; transform:translate(-50%, -50%) scale(0); background:white; color:black; padding:10px; border-radius:10px; font-weight:bold; transition:0.5s; z-index:10;">{wheel_data[st.session_state.current_wheel-1]['name']}</div>
        <div style="position:absolute; top:-10px; left:50%; transform:translateX(-50%); width:0; height:0; border-left:15px solid transparent; border-right:15px solid transparent; border-top:20px solid gold;"></div>
    </div>
    <br>
    <button id="spin-btn" onclick="spin()" style="padding:10px 30px; border-radius:20px; border:none; background:gold; font-weight:bold; cursor:pointer;">SPIN WHEEL</button>
</div>

<script>
    let rotation = 0;
    function spin() {{
        document.getElementById('spin-btn').style.display = 'none';
        rotation += Math.floor(2000 + Math.random() * 2000);
        document.getElementById('wheel').style.transform = "rotate(" + rotation + "deg)";
        
        setTimeout(() => {{
            document.getElementById('center-text').style.transform = "translate(-50%, -50%) scale(1)";
            window.parent.postMessage({{type: 'wheel_stopped'}}, '*');
        }}, 4100);
    }}
</script>
"""

# HTML එක Display කිරීම
components.html(html_code, height=450)

# Options පෙන්වීම සඳහා Streamlit Buttons
current_data = wheel_data[st.session_state.current_wheel - 1]

st.write("### Choose the Correct Name:")
cols = st.columns(2)
for i, opt in enumerate(current_data['opts']):
    with cols[i % 2]:
        if st.button(opt, key=f"btn_{st.session_state.current_wheel}_{i}"):
            if i == current_data['correct']:
                st.success("Correct!")
                if st.button("Next Wheel ➡️"):
                    if st.session_state.current_wheel < 20:
                        st.session_state.current_wheel += 1
                        st.rerun()
                    else:
                        st.balloons()
                        st.write("Congratulations! You finished all 20!")
            else:
                st.error("Wrong! Try again.")
