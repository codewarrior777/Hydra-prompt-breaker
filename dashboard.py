import streamlit as st
import pandas as pd
import plotly.express as px
import time
from hydra import ATTACK_PAYLOADS, launch_attack

st.set_page_config(page_title="Hydra Command Center", page_icon="🐍", layout="wide")

# --- RED TEAM CSS ---
st.markdown("""
<style>
.stApp {
    background-color: #0a0000;
    background-image: radial-gradient(at 50% 50%, rgba(255, 0, 60, 0.05) 0px, transparent 50%);
    color: #ff003c;
    font-family: 'Courier New', monospace;
}
h1, h2, h3 { color: #ff003c !important; text-transform: uppercase; }
div[data-testid="stMetric"] {
    background-color: #1a0000;
    border: 1px solid #ff003c;
    border-left: 5px solid #ff003c;
    padding: 15px;
}
.stButton > button {
    background-color: #000 !important;
    color: #ff003c !important;
    border: 1px solid #ff003c !important;
    border-radius: 0 !important;
    transition: all 0.3s;
}
.stButton > button:hover {
    background-color: #ff003c !important;
    color: #000 !important;
    box-shadow: 0 0 15px rgba(255, 0, 60, 0.8);
}
</style>
""", unsafe_allow_html=True)

st.title("🐍 HYDRA // AI Red Team Console")
st.markdown("**Offensive Security Tool for LLM Vulnerability Testing**")

# Session State Initialization
if "results" not in st.session_state:
    st.session_state.results = []
if "is_running" not in st.session_state:
    st.session_state.is_running = False

# Sidebar
with st.sidebar:
    st.markdown("### ⚔️ Attack Arsenal")
    st.markdown(f"Payloads Loaded: **{len(ATTACK_PAYLOADS)}**")
    
    if st.button("🚀 EXECUTE ATTACK SEQUENCE", use_container_width=True):
        st.session_state.results = []
        st.session_state.is_running = True
        st.rerun()

# Main Area
c1, c2, c3 = st.columns(3)

total_attacks = len(st.session_state.results)
bypassed = sum(1 for r in st.session_state.results if r["status"] == "BYPASSED")
blocked = sum(1 for r in st.session_state.results if r["status"] == "BLOCKED")
evasion_rate = (bypassed / total_attacks * 100) if total_attacks > 0 else 0

c1.metric("Total Attacks", total_attacks)
c2.metric("Bypasses (Success)", bypassed)
c3.metric("Evasion Rate", f"{evasion_rate:.1f}%")

st.divider()

col_log, col_chart = st.columns([2, 1])

with col_log:
    st.markdown("### 🖥️ Execution Log")
    if st.session_state.is_running:
        log_container = st.empty()
        log_text = ""
        
        # Execute attacks one by one
        for attack in ATTACK_PAYLOADS:
            log_text += f"> Initializing {attack['id']} ({attack['name']})...\n"
            log_container.code(log_text, language="bash")
            time.sleep(0.5)
            
            # Launch attack
            result = launch_attack(attack)
            st.session_state.results.append(result)
            
            if result["status"] == "BYPASSED":
                log_text += f"🔴 [VULNERABILITY FOUND] {result['reason']}\n\n"
            else:
                log_text += f"🟢 [BLOCKED] {result['reason']}\n\n"
            
            log_container.code(log_text, language="bash")
        
        st.session_state.is_running = False
        st.success("Attack Sequence Complete.")
        
    elif st.session_state.results:
        # Display saved results
        for r in st.session_state.results:
            if r["status"] == "BYPASSED":
                st.error(f"🔴 {r['id']} ({r['name']}): {r['reason']}")
            else:
                st.success(f"🟢 {r['id']} ({r['name']}): {r['reason']}")
    else:
        st.info("Ready to launch attacks. Click 'EXECUTE ATTACK SEQUENCE' in the sidebar.")

with col_chart:
    st.markdown("### 📊 Attack Surface")
    if st.session_state.results:
        df = pd.DataFrame(st.session_state.results)
        fig = px.pie(df, names="status", hole=0.6, 
                     color="status", 
                     color_discrete_map={"BYPASSED": "#ff003c", "BLOCKED": "#00ff41", "ERROR": "#ffd000"})
        fig.update_layout(
            plot_bgcolor="rgba(0,0,0,0)", 
            paper_bgcolor="rgba(0,0,0,0)",
            font_color="#ff003c",
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.write("No data yet.")