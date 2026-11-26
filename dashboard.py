import html
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import time
from hydra import ATTACK_PAYLOADS, launch_attack

st.set_page_config(page_title="Hydra // Red Team Command", page_icon="🐍", layout="wide")

# --- GOD TIER RED TEAM CSS ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;700&display=swap');

.stApp {
    background-color: #050000;
    background-image: 
        radial-gradient(at 0% 0%, rgba(255, 0, 60, 0.15) 0px, transparent 50%),
        radial-gradient(at 100% 100%, rgba(255, 0, 60, 0.05) 0px, transparent 50%);
    color: #ff003c;
    font-family: 'Fira Code', monospace;
}
h1, h2, h3 { 
    color: #ff003c !important; 
    text-transform: uppercase; 
    text-shadow: 0 0 10px rgba(255, 0, 60, 0.6);
}
div[data-testid="stMetric"] { 
    background-color: rgba(15, 0, 0, 0.8); 
    border: 1px solid #ff003c; 
    border-top: 4px solid #ff003c;
    padding: 15px; 
    box-shadow: 0 0 15px rgba(255, 0, 60, 0.2);
}
div[data-testid="stMetricValue"] { color: #fff !important; font-weight: bold; font-size: 1.9rem !important; }
div[data-testid="stMetricValue"] > div { overflow: visible !important; text-overflow: clip !important; }
[data-testid="stCaptionContainer"], [data-testid="stCaptionContainer"] * { color: #ff8fa6 !important; }
[data-testid="stSidebar"] { 
    background-color: #0a0000; 
    border-right: 1px solid #ff003c;
}
.stButton > button { 
    background-color: #000 !important; 
    color: #ff003c !important; 
    border: 1px solid #ff003c !important; 
    border-radius: 0 !important; 
    font-weight: bold;
    text-transform: uppercase;
    transition: all 0.3s; 
}
.stButton > button:hover { 
    background-color: #ff003c !important; 
    color: #000 !important; 
    box-shadow: 0 0 20px rgba(255, 0, 60, 0.9); 
}
.terminal-window {
    background-color: #000;
    border: 1px solid #333;
    border-radius: 5px;
    padding: 15px;
    font-family: 'Fira Code', monospace;
    font-size: 14px;
    color: #00ff41;
    height: 380px;
    overflow-y: auto;
    box-shadow: inset 0 0 20px rgba(0,255,65,0.1);
}
.term-red { color: #ff003c; font-weight: bold; }
.term-green { color: #00ff41; font-weight: bold; }
.term-yellow { color: #ffd000; }
</style>
""", unsafe_allow_html=True)


def result_line(r):
    """Return the colored HTML result line for one attack result.
    All dynamic text is escaped because it is rendered with unsafe_allow_html."""
    if r["status"] == "BYPASSED":
        return '<span class="term-red">[LEAK PAST FIREWALL]</span> Canary leaked in a form Layer 5 did not catch!<br><br>'
    if r["status"] == "ERROR":
        return f'<span class="term-yellow">[ERROR]</span> {html.escape(str(r["reason"]))}<br><br>'
    return f'<span class="term-green">[BLOCKED]</span> {html.escape(str(r["reason"]))}<br><br>'


st.title("🐍 HYDRA // Command Center")
st.markdown("**Research Prototype: Automated LLM Red Teaming**")

# Session State Initialization
if "results" not in st.session_state:
    st.session_state.results = []
if "is_running" not in st.session_state:
    st.session_state.is_running = False

# Sidebar
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2885/2885417.png", width=60)
    st.markdown("### ⚔️ Attack Arsenal")
    st.markdown(f"Payloads Loaded: **{len(ATTACK_PAYLOADS)}**")
    
    if st.button("🚀 LAUNCH ATTACK", use_container_width=True):
        st.session_state.results = []
        st.session_state.is_running = True
        st.rerun()
        
    st.markdown("---")
    st.markdown("#### ℹ️ Target Info")
    st.info(
        "Target: Bank Assistant LLM\n\n"
        "Firewall: Aegis Sentinel layers 1–5 (shared guardrails module)\n\n"
        "Layer 4 calls a judge model, so each payload that reaches it costs one extra API call."
    )

# Main Area - Metrics
# Errors (e.g. API failures, rate limits) are excluded from the evasion rate
# so they do not dilute it.
results = st.session_state.results
total_attacks = len(results)
errors = sum(1 for r in results if r["status"] == "ERROR")
evaluated = total_attacks - errors
bypassed = sum(1 for r in results if r["status"] == "BYPASSED")
evasion_rate = (bypassed / evaluated * 100) if evaluated > 0 else 0
avg_latency = round(sum(r.get("latency", 0) for r in results) / total_attacks) if total_attacks > 0 else 0

c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Vectors", total_attacks)
c2.metric("Leaks Past Firewall", bypassed)
c3.metric("Evasion Rate", f"{evasion_rate:.1f}%")
c4.metric("Avg Latency", f"{avg_latency} ms")

if errors:
    st.caption(f"⚠️ {errors} vector(s) ended in ERROR and are excluded from the evasion rate.")

# The model can leak the canary even when the firewall stops it (Layer 5).
model_leaks = sum(1 for r in results if r.get("llm_leaked"))
stopped_by_l5 = sum(1 for r in results if str(r.get("reason", "")).startswith("Blocked by Layer 5"))
if model_leaks:
    st.caption(f"The model itself leaked the canary in {model_leaks} run(s); Layer 5 stopped {stopped_by_l5} of them.")

st.divider()

col_log, col_chart = st.columns([2, 1])

with col_log:
    st.markdown("### 🖥️ Live Execution Log")
    log_container = st.empty()
    
    if st.session_state.is_running:
        log_html = '<div class="terminal-window">'
        
        for attack in ATTACK_PAYLOADS:
            log_html += f'> Initializing {html.escape(attack["id"])} ({html.escape(attack["name"])})...<br>'
            log_container.markdown(log_html + '</div>', unsafe_allow_html=True)
            time.sleep(0.4)
            
            result = launch_attack(attack)
            st.session_state.results.append(result)
            
            log_html += result_line(result)
            log_container.markdown(log_html + '</div>', unsafe_allow_html=True)
        
        log_html += '<span class="term-green">> Sequence Complete. Target disconnected.</span>'
        log_container.markdown(log_html + '</div>', unsafe_allow_html=True)
        
        st.session_state.is_running = False
        time.sleep(1)
        st.rerun()
        
    elif st.session_state.results:
        log_html = '<div class="terminal-window">'
        for r in st.session_state.results:
            log_html += f'> {html.escape(r["id"])} ({html.escape(r["name"])})<br>'
            log_html += result_line(r)
        log_html += '<span class="term-green">> Sequence Complete.</span></div>'
        log_container.markdown(log_html, unsafe_allow_html=True)
    else:
        log_container.markdown('<div class="terminal-window">> Awaiting command...</div>', unsafe_allow_html=True)

with col_chart:
    st.markdown("### 🎯 Evasion Gauge")
    if st.session_state.results:
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = evasion_rate,
            number = {
                'font': {'color': '#ff003c', 'size': 38},
                'suffix': '%',
                'valueformat': '.1f'
            },
            gauge = {
                'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "#ff003c"},
                'bar': {'color': "#ff003c"},
                'bgcolor': "rgba(0,0,0,0)",
                'borderwidth': 2,
                'bordercolor': "#ff003c",
                'steps': [
                    {'range': [0, 50], 'color': 'rgba(0, 255, 65, 0.1)'},
                    {'range': [50, 100], 'color': 'rgba(255, 0, 60, 0.2)'}
                ],
            }
        ))
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font={'color': "#ff003c", 'family': "Fira Code"},
            height=380,
            margin=dict(t=30, b=30, l=10, r=10)
        )
        st.plotly_chart(fig, use_container_width=True)
        st.caption(f"Share of vectors whose leak got past the whole pipeline, in this single run (n = {evaluated}).")
    else:
        st.info("No telemetry data.")

# --- DEEP DIVE AUDIT TABLE ---
st.divider()
st.markdown("### 📋 Deep Dive Audit Log")
if st.session_state.results:
    df = pd.DataFrame(st.session_state.results)
    df_display = df[["id", "name", "status", "latency", "reason", "llm_leaked", "payload"]]
    
    st.dataframe(
        df_display,
        use_container_width=True,
        column_config={
            "status": st.column_config.TextColumn("Result", help="BLOCKED, BYPASSED or ERROR"),
            "llm_leaked": st.column_config.Column("LLM leaked", help="True if the model itself leaked the canary, even when Layer 5 blocked it. Empty if the model was not reached."),
            "latency": st.column_config.NumberColumn("Latency (ms)", format="%d ms"),
            "payload": st.column_config.TextColumn("Payload String", width="large"),
        }
    )
    
    bypasses = [r for r in st.session_state.results if r["status"] == "BYPASSED"]
    if bypasses:
        with st.expander("🔴 View Raw LLM Responses (Detected Leaks)", expanded=True):
            for b in bypasses:
                st.markdown(f"**{b['id']} ({b['name']})**")
                st.code(b["raw_response"], language="text")

    # Raw responses for ALL vectors, so refusals can be verified by eye.
    # An empty response labeled "LLM refused" may actually be a truncated
    # or empty completion (e.g. max_tokens consumed by a reasoning model).
    with st.expander("🔍 View Raw Responses (all vectors)", expanded=False):
        for r in st.session_state.results:
            raw = (r.get("raw_response") or "").strip()
            st.markdown(f"**{r['id']} ({r['name']})** — {r['status']}: {r['reason']}")
            if r["status"] == "BLOCKED" and r["reason"] == "LLM refused" and not raw:
                st.warning(
                    "Empty response labeled 'LLM refused'. This may be truncation "
                    "or an empty completion, not a real refusal."
                )
            st.code(raw if raw else "(empty)", language="text")
else:
    st.write("No attacks executed yet.")