import streamlit as st
import pandas as pd
from millify import millify
import plotly.express as px

def render_metric_box(label: str, value: str):
    st.markdown(
        f"""
        <div style="
            background-color: #424b43;
            border: 2px solid #111212;
            border-radius: 30px;
            padding: 30px 20px;
            color: white;
            text-align: center;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            height: 100%;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
        ">
            <div style="
                font-size: 1.3em;
                color: #B7e493;
                margin-bottom: 10px;
                font-weight: 600;
                word-wrap: break-word;
            ">
                {label}
            </div>
            <div style="
                font-size: 3em;
                font-weight: 700;
                color: #ffffff;
                word-wrap: break-word;
            ">
                {value}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


def display_content():

    st.image("images/solana.jpeg")


    st.markdown("""
## :blue[Solana/web3.js Supply-Chain Backdoor Attack Analysis]

## :red[1. A Brief Description of the Protocol]

@solana/web3.js is the official JavaScript SDK for interacting with the Solana blockchain, downloaded hundreds of thousands of times weekly. It provides wallet management, transaction creation, and RPC communication functionalities.

---

## :orange[2. Exploit Summary]

On December 2, 2024, between 15:20 UTC and 20:25 UTC, attackers published two backdoored npm versions (1.95.6 and 1.95.7) after compromising a maintainer’s publish credentials.  
The malicious packages introduced an `addToQueue` function that silently captured private keys during signing operations and sent them to a malicious endpoint (`sol-rpc[.]xyz`) via Cloudflare headers.  
Developers and bots using these versions unknowingly exposed wallet keys, enabling the attacker to drain funds from vulnerable deployments in real time.  
Within hours, the attack was detected by security researchers and the official package maintainers.

---

## :green[3. Technical Analysis]

The vulnerability stemmed from a targeted spear-phishing campaign that stole the npm account credentials of a @solana/web3.js maintainer.  
Malicious code was injected into essential modules, placing exfiltration calls adjacent to legitimate private-key-accessing functions.  
Because many dApps load this library client-side or in unattended scripts, the backdoor ran undetected until post-deployment, compromising any system handling raw private keys.  
The attack leveraged trusted infrastructure (npm registry, Cloudflare) to evade detection, and lacked any intermediate integrity checks or signature verification.

---

## :blue[4. Protocol Response and Aftermath]

Upon confirmation, the maintainers removed versions 1.95.6 and 1.95.7 from the npm registry and immediately released version 1.95.8 containing the clean code.  
A security advisory was issued, urging all users to audit their dependencies, downgrade/upgrade accordingly, and rotate any exposed keys or credentials.  
The team implemented mandatory multi-factor authentication for npm publishes, stricter access controls, and signed future releases to prevent unauthorized modifications.

---

## :violet[5. Lessons Learnt]

- **:green[Supply-Chain Vigilance:]** Continuously monitor and audit critical dependencies for unauthorized changes.  
- **:orange[Strong Auth Controls:]** Enforce multi-factor authentication and least-privilege access for package maintainers.  
- **:green[Package Signing:]** Adopt cryptographic signing and reproducible builds to verify package integrity.  
- **:orange[Dependency Hygiene:]** Limit direct private-key handling in client libraries; prefer external signing services or hardware wallets.

---

## :red[6. Conclusion]

The Solana/web3.js backdoor attack demonstrates how a single compromised credential can undermine entire ecosystems through trusted supply chains. Rapid detection, decisive package remediation, and strengthened maintainer security practices were essential to containing the incident. Moving forward, Web3 projects must integrate comprehensive supply-chain security measures—authentication hardening, signature verification, and dependency monitoring—to safeguard users and maintain trust.
""")
