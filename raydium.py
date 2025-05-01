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

    st.image("images/raydium.jpeg")  

    st.markdown("""

# :blue[Raydium Exploit Report (December 16, 2022)]

## :red[1. A Brief Description of the Protocol]

Raydium is an Automated Market Maker (AMM) and liquidity provider built on the Solana blockchain. It is integrated with the Serum decentralized exchange (DEX) order book, enabling it to provide on-chain liquidity to a central limit order book. Raydium offers features such as token swapping, liquidity provision, yield farming, and launching new tokens via an IDO launchpad. It leverages Solana's high-speed and low-cost transactions for efficient DeFi operations.

- **Attacker's Wallet Address:** **:orange[0x70479...]**

---

## :orange[2. Exploit Summary]

On December 16, 2022, Raydium suffered a significant exploit caused by the compromise of a private key controlling privileged functions within its AMM and farm programs. The attacker used the compromised key to withdraw funds from multiple liquidity pools without returning corresponding LP tokens. This breach enabled them to siphon off assets directly from user-supplied liquidity.

The attacker quickly executed a series of malicious transactions, transferring stolen assets to various wallets and bridging a portion of the funds to Ethereum. This was not a smart contract vulnerability, but rather a direct result of inadequate key security practices.

---

## :green[3. Technical Analysis]

The exploit stemmed from the compromise of a private key with "owner authority" over certain Raydium programs. This key allowed the attacker to:

- **:green[1:]** Call privileged functions such as `withdraw_pnl` to withdraw funds from liquidity pools without LP token redemption.
  
- **:orange[2:]** Circumvent normal contract logic by directly issuing transactions signed with the compromised key.

- **:green[3:]** Drain assets from affected pools across various tokens in a short time frame.

- **:orange[4:]** Bridge stolen funds to Ethereum and send them to mixing services like Tornado Cash to obscure their trail.

The breach is suspected to have occurred via malware—possibly a trojan—infecting a device with access to the private key. This highlights an off-chain vector of attack rather than a flaw in on-chain contract logic.

---

## :blue[4. Protocol Response and Aftermath]

Upon discovering the exploit, the Raydium team immediately revoked the compromised owner authority and halted affected programs to stop further losses.

They published a detailed incident report and coordinated with security experts and the Solana Foundation to trace the stolen funds. To address user losses:

- **:green[1:]** Raydium pledged to compensate affected users using unlocked RAY tokens.

- **:orange[2:]** A governance proposal approved using DAO treasury funds to repurchase missing non-RAY assets from the market.

- **:green[3:]** A bounty was offered for voluntary return of stolen assets, but the attacker did not comply.

The response emphasized damage control and community engagement, aiming to restore trust.

---

## :violet[5. Lessons Learnt]

- **:green[Private Key Security is Paramount:]** Even the most secure smart contracts are vulnerable if admin keys are compromised.

- **:orange[Reduce Centralization Risks:]** Excessive control via single keys contradicts DeFi principles and increases protocol risk.

- **:green[Improve Operational Security:]** Protocols should implement hardened operational environments and avoid key exposure on internet-connected devices.

- **:orange[Malware Vigilance is Essential:]** Malware remains a high-risk threat vector in compromising private keys.

- **:green[Community Transparency Matters:]** Timely, honest communication and compensation efforts are crucial for preserving user trust post-incident.

- **:green[Transparency:]** Protocols must clearly disclose their key management and upgrade authority structure to users.

---

## :red[6. Conclusion]

The Raydium exploit was a critical reminder that off-chain weaknesses—like poor key management—can be as damaging as on-chain bugs. The attacker’s access to a privileged private key enabled them to drain $4.3–$5.5 million from liquidity pools, bypassing normal protocol safeguards. Though Raydium responded with swift action and a compensation plan, the incident exposed the risks of centralized control in DeFi and underscored the urgent need for multi-sig protections and robust operational security.

""")
