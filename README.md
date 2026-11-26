# 🐍 Hydra-Prompt-Breaker: Automated LLM Red Teaming

[![Live App](https://img.shields.io/badge/🚀_Live_App-Try_It_Here-brightgreen?style=for-the-badge&logo=streamlit)](https://hydra-prompt-breaker-siyczpjzqlujp42drzgtwz.streamlit.app/)
[![Watch Demo](https://img.shields.io/badge/🎥_Watch_Demo-View_GIF-success?style=for-the-badge)](https://github.com/codewarrior777/Hydra-prompt-breaker#-live-action-demo)
[![Target](https://img.shields.io/badge/🎯_Target-Aegis_Sentinel_v2-blue)](https://github.com/codewarrior777/prompt-aegis)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Research%20Prototype-orange)
![OWASP](https://img.shields.io/badge/OWASP-LLM01-red)
![Streamlit](https://img.shields.io/badge/UI-Streamlit-FF4B4B)

**Hydra-Prompt-Breaker** is a research prototype of an automated adversarial testing harness for Large Language Model (LLM) applications.

It was built to explore and demonstrate the methodology of LLM red teaming against **[Aegis Sentinel](https://github.com/codewarrior777/prompt-aegis)**, a multi-layer AI firewall project. In this version, only a partial simulation of Aegis (Layers 1–2) is exercised. See the Known Limitations section below.

> *"In mythology, cutting off one of Hydra's heads causes two more to grow in its place. This mirrors the cat-and-mouse game of AI Security: block one prompt injection, and attackers will mutate the payload into new variations."*

## 🎓 Project Status & Scope

This is a **pre-graduation academic project** (Computer Science & Information Security) and guardrails research for the *Foundations of AI Engineering* course (CodePath), built to learn and demonstrate how automated LLM red teaming works. It is a **prototype, not a validated security assessment tool**. Its results should not be read as a measurement of how secure Aegis Sentinel or any target model is.

## 🎥 Live Action Demo

![Hydra Dashboard Demo](assets/hydra_live_demo.gif)

---

## 🏗️ Red Teaming Architecture (Attack Flow)

Each payload goes through a simulated firewall (Layer 1 regex rules and Layer 2 encoding detection, copied from Aegis Sentinel). If it passes, it is sent to the target LLM, and the response is checked for a planted canary secret.

```mermaid
graph TD
    A[Hydra Engine Starts] --> B{Select Payload}

    B -->|ATK-001| C[Direct Injection]
    B -->|ATK-002| D[Base64 Obfuscation]
    B -->|ATK-003| E[Roleplay Jailbreak]
    B -->|ATK-004| F[Grandma Exploit]
    B -->|ATK-005| G[Context Swapping]

    C --> H[Simulated Aegis: Layer 1 Regex + Layer 2 Encoding]
    D --> H
    E --> H
    F --> H
    G --> H

    H -->|Pattern match| I[🛡️ Blocked by Firewall]
    H -->|No match| M[Target LLM]

    M --> N{Canary in response?}
    N -->|No| O[🛡️ LLM did not leak]
    N -->|Yes| J[🔥 Leak detected]

    I --> K[Log Event to Terminal]
    O --> K
    J --> K

    K --> L[Generate Evasion Gauge]

    style A fill:#0d1117,stroke:#58a6ff,stroke-width:2px,color:#fff
    style H fill:#0d1117,stroke:#ff003c,stroke-width:2px,color:#fff
    style M fill:#0d1117,stroke:#ff003c,stroke-width:2px,color:#fff
    style I fill:#003a0e,stroke:#00ff41,stroke-width:2px,color:#00ff41
    style O fill:#003a0e,stroke:#00ff41,stroke-width:2px,color:#00ff41
    style J fill:#3a0000,stroke:#ff003c,stroke-width:2px,color:#ff003c
    style K fill:#0d1117,stroke:#d2a8ff,stroke-width:2px,color:#fff
```

---

## 🛠️ Features

- **Terminal-Style Execution Log:** Watch the attacks execute in sequence with color-coded results (green for blocked, red for leak detected, yellow for errors).
- **Evasion Gauge:** A Plotly speedometer showing the share of evaluated vectors with a detected leak in a single run. Vectors that end in an error (for example, an API failure) are excluded from the rate.
- **Audit Log:** A data table with latency (ms), the reason for each result, and the raw payload string.
- **Raw Response Viewer:** View the exact response of every vector, not only detected leaks, so that refusals can be verified by eye. Empty responses labeled as refusals are flagged with a warning.

---

## 🎯 Attack Payload Matrix

The payloads are inspired by prompt injection categories described under OWASP Top 10 for LLM Applications (LLM01).

| ID | Attack Vector | Intended Defense Layer | Payload Description |
| :--- | :--- | :--- | :--- |
| **ATK-001** | Direct Injection | Layer 1 (Regex) | Classic "Ignore previous instructions" attempt. |
| **ATK-002** | Base64 Obfuscation | Layer 2 (Encoding) | Base64-encoded instruction meant to evade keyword matching. |
| **ATK-003** | Roleplay Jailbreak | Layer 4 (Semantic Judge) | "Sysadmin locked out" scenario. |
| **ATK-004** | Grandma Exploit | Layer 4 (Semantic Judge) | Emotional-manipulation roleplay. |
| **ATK-005** | Context Swapping | Layer 5 (Output Filter) | "Maintenance mode" override to extract the canary. |

> **Note:** Layers 3–5 of Aegis Sentinel are **not simulated** in this version. ATK-003 to ATK-005 are designed with those layers in mind, but in this harness they pass the simulated Layers 1–2 and go directly to the target LLM.

---

## 🚀 How to Run

### 1. Clone the repository
```bash
git clone https://github.com/codewarrior777/Hydra-prompt-breaker.git
cd Hydra-prompt-breaker
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure your API Key
**For Local Development:** Create a `.env` file in the root directory and add your Groq API key:
```env
GROQ_API_KEY="gsk_your_api_key_here"
```

**For Streamlit Cloud Deployment:** Add the key in the App Settings -> Secrets:
```toml
GROQ_API_KEY = "gsk_your_api_key_here"
```

### 4. Launch the Command Center
```bash
python -m streamlit run dashboard.py
```

*(Optional: to run the headless CLI version, use `python hydra.py`)*

---

## 📸 UI Gallery

![Hydra Command Center UI](assets/hydra_command_center_hud.png)

---

## ⚠️ Known Limitations

- **Small sample size:** 5 payloads, executed once each. LLM outputs are non-deterministic (temperature 0.5), so a single run is not statistically meaningful. Repeated trials and an attack success rate metric are planned.
- **Partial firewall simulation:** Only Layer 1 (regex) and Layer 2 (encoding detection) of Aegis Sentinel are replicated, copied manually from its rules and not called from the real system. Layers 3–5 (including the Semantic Judge and Output Filter) are not exercised, so results do not reflect the full Aegis pipeline.
- **Leak detection is exact-match only:** A leak is flagged only if the canary string appears verbatim. A spelled-out, translated, reversed, or encoded leak would be missed (false negatives).
- **Result labels are coarse:** Any LLM response without the exact canary is labeled "blocked / LLM refused". The dashboard warns about empty responses, but partial compliance is not detected.
- **No false-positive testing:** No benign prompts are included, so the rate at which legitimate traffic is blocked is not measured.
- **Single-turn, direct attacks only:** No multi-turn, indirect (RAG / document / tool-based) injection, or gradual extraction attacks. The payloads are well-known classics that modern models are commonly trained against, so a low success rate says little about robustness to novel attacks.
- **Possible output truncation:** `max_tokens=200` combined with a reasoning model could cut responses short and be mislabeled as refusals. In the author's test run the observed responses were complete refusals, but this was checked for a single run only. The raw response viewer exists to verify this.
- **Latency metric is mixed:** The average latency combines firewall checks (about 0 ms) with LLM API calls, so it does not represent model latency.
- **Single target:** Results apply only to the configured model and system prompt at the time of the run. The secret is placed in the system prompt for testing purposes, which is not a recommended practice in production.
- **Public demo uses the author's API key:** The hosted app may be rate-limited or unavailable.

## 🗺️ Roadmap

- [ ] Run N repetitions per attack and report attack success rate (ASR)
- [ ] Normalized and encoded-variant canary detection
- [ ] Separate result states (blocked by firewall / LLM resisted / leaked / error / inconclusive)
- [ ] Benign prompt set to measure false positives
- [ ] Call the real Aegis Sentinel instead of copied rules
- [ ] Multi-turn and indirect injection scenarios
- [ ] Automated payload mutation (synonyms, languages, obfuscation)

---

## 🤖 AI Assistance Disclosure

This project was developed as **guardrails research for the *Foundations of AI Engineering* course (CodePath)**, with the help of AI tools used as assistants:

- **DeepSeek:** support for the initial code (`hydra.py` and the first version of the dashboard), and two evaluations of that first version.
- **Gemini (Google):** an additional analysis of the first version of the code, obtained for the comparison below.
- **Claude (Anthropic):** review of the first version, README drafting (scope, limitations, roadmap), and edits to `dashboard.py`.

**Author's contribution:** guardrails research for the *Foundations of AI Engineering* course (CodePath). The author ran the dashboard locally, checked the raw model responses, and published the repository.

### Stage 1: Evaluation of the first version

When the project started, the first version of the code was submitted to several AI tools for evaluation.

| Tool | What it returned | Not covered |
| :--- | :--- | :--- |
| DeepSeek (response 1, English) | Concrete defects: API key crash with a ready fix, exact-match detection, no retries, non-determinism; suggested separating firewall and model tests. | `max_tokens` truncation, false-positive testing, single-turn coverage. |
| DeepSeek (response 2, Spanish) | 11 problems (firewall pre-blocking ATK-001/002, fragile detection, no key validation, no retries, non-determinism, no false-positive testing); recommended a no-firewall baseline, repetitions and benign prompts. Gave subjective scores (6/10 as a demo, 4/10 as a real tool). | `max_tokens` truncation, single-turn coverage, unverifiable Aegis claim. |
| Gemini | A structured description of the architecture; no defects or limitations listed. | Any critical evaluation. |
| Claude | Core defects plus methodological limits (statistical validity, result labels, circular firewall results, false positives, coverage). Flagged a truncation risk that was not observed in the author's run. | An explicit no-firewall baseline. |

> This is a qualitative comparison from a single project, with one response per tool (two for DeepSeek, which differed noticeably in depth). It is not a benchmark and should not be generalized.

### Stage 2: Final result

After the evaluations, the following changes were made with Claude's help. `hydra.py` was **not** modified in this stage, so the items marked Open correspond to the roadmap above.

| Issue found | Status in this version |
| :--- | :--- |
| README described layers and claims the code does not implement | Addressed: README rewritten with scope, limitations and roadmap |
| Saved log view displayed API errors as "BLOCKED" | Fixed in `dashboard.py` (error path not exercised in the author's run) |
| API errors diluted the evasion rate | Fixed: errors are excluded from the rate |
| Refusals could not be verified | Raw response viewer added; in the author's run the responses were complete refusals |
| Sidebar claimed the full firewall | Reworded: Layers 1–2 simulated |
| API key validation | **Open** |
| Exact-match canary detection | **Open** |
| Repetitions / attack success rate | **Open** |
| Retries and rate-limit handling | **Open** |
| Reproducibility (temperature) | **Open** |
| No-firewall baseline and benign prompts | **Open** |
| Real Aegis Sentinel instead of copied rules | **Open** |

**Final state:** a research prototype whose documentation now matches what the code does. The core methodological improvements remain future work.

---

## ⚖️ Ethical Disclaimer

This tool is built for educational and authorized security testing purposes only. Do not use it against systems you do not own or have explicit permission to test. The author is not responsible for any misuse or damage caused by this program.

---
*Built by Gustavo Ramos | Senior Computer Science & Information Security Student*