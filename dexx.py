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

    st.image("images/dexx.jpeg")


    st.markdown("""
## :blue[DEXX Memecoin Trading Terminal Hack Analysis]

## :red[1. A Brief Description of the Protocol]

DEXX is a Solana-based on-chain memecoin trading terminal that aggregates meme token trades and wallets via a centralized custody private key system.

---

## :orange[2. Exploit Summary]
On November 16, 2024, attackers exploited a private key vulnerability in DEXX’s centralized custody system, gaining unrestricted access to user wallets.  
They used the leaked private keys to transfer user funds—including various memecoins and SOL—into attacker-controlled addresses.  
Within minutes, over $21 million worth of assets were drained from at least 900 unique user accounts, triggering a massive sell-off and widespread panic.  
DEXX detected the abnormal withdrawals and immediately issued an emergency pause on trading services while initiating an internal investigation.

---
The exploit narrative wasn’t a direct "funds stolen" attack through Serum’s existing contracts, but rather a critical loss of **trust and security** through DEXX’s compromised custody model.

## :green[3. Technical Analysis]
The root cause was an insecure export_wallet function that exposed user private keys in plaintext when transmitted, enabling attackers to intercept them.  
With direct access to user keys, the attacker bypassed on-chain permission checks and initiated unauthorized transfers from multiple wallets.  
No multi-signature or time-locked withdrawal safeguards existed, allowing immediate and irreversible asset transfers.  
The impact included the loss of over $30 million in memecoins and SOL, significant user asset losses, and reputational damage to the DEXX brand.

---
## :blue[4. Protocol Response and Aftermath]
DEXX responded by halting all trading and wallet withdrawals, advising users to transfer remaining funds to self-custody solutions.  
The team engaged forensic firms to trace stolen assets and liaised with Solana validators to attempt to blacklist attacker addresses.  
DEXX rolled out a new client-side encryption module and disabled the vulnerable export_wallet feature in an emergency patch.  
Affected users were offered token compensation and priority support for recovery steps, though full reimbursement remained contingent on asset recovery.

---
## :violet[5. Lessons Learnt]
- **:green[Client-Side Encryption:]** Protocols must encrypt private keys locally, never transmit them in plaintext.

- **:orange[Multi-Sig Protections:]** Implement multi-signature and time-lock mechanisms for all withdrawal functions.

- **:green[Secure Key Management:]** Avoid centralized private key custody; promote non-custodial or hardware wallet integrations.

- **:orange[Transparent Incident Communication:]** Maintain clear, timely updates and recovery plans to preserve user trust.

- **:green[Transparency:]** Protocols need to disclose custody and key management models clearly to users.

---
## :red[6. Conclusion]
The DEXX hack illustrates the dangers of centralizing private key control and insufficient client-side security. By exposing user keys in transit, DEXX enabled attackers to drain millions within minutes. The incident underscores the importance of non-custodial designs, robust key encryption, and multi-signature safeguards. Moving forward, on-chain applications must prioritize end-user key security and transparent incident response to maintain trust and resilience in the memecoin ecosystem.
""")
