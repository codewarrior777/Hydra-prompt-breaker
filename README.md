# 🐍 Hydra-Prompt-Breaker: Automated LLM Red Teaming

**Hydra-Prompt-Breaker** is an offensive security framework designed to automate adversarial testing against Large Language Model (LLM) applications. 

It was built specifically to stress-test **[Aegis Sentinel](https://github.com/codewarrior777/prompt-aegis)**, my 5-layer AI Firewall, to ensure it can withstand real-world Prompt Injections, Jailbreaks, and Obfuscation attempts.

## 🎯 Why "Hydra"?
In mythology, cutting off one of Hydra's heads causes two more to grow in its place. This perfectly mirrors the cat-and-mouse game of AI Security: block one prompt injection, and attackers will mutate the payload into two new variations. This tool simulates that relentless attack surface.

## 🚀 Features (In Development)
*   **Automated Payload Delivery:** Sends a suite of adversarial prompts (Base64, Roleplay, PII Exfiltration) to a target LLM.
*   **Defense Evaluation:** Analyzes whether the target firewall (like Aegis Sentinel) successfully blocked the attack.
*   **Automated Reporting:** Generates a JSON/PDF report detailing successful bypasses and recommendations.

## ⚠️ Ethical Disclaimer
This tool is built for **educational and authorized security testing purposes only**. Do not use it against systems you do not own or have explicit permission to test. The author is not responsible for any misuse or damage caused by this program.

---
*Built by Gustavo Ramos | AI Security Engineer*