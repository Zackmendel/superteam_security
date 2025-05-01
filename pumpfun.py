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

    st.image("images/pumpfun.jpeg")

    st.markdown("""
## :blue[Pump.fun Memecoin Flash Loan Exploit Analysis]

## :red[1. A Brief Description of the Protocol]

Pump.fun is a Solana-based memecoin launchpad that lets anyone create and trade tokens via bonding-curve mechanics, launching on Raydium once they hit market-cap thresholds.  
- Attacker's Wallet Address: **:orange[7ihN8QaTfNoDTRTQGULCzbUT3PHwPDTu5Brcu4iT2paP]**

---

## :orange[2. Exploit Summary]

On May 16, 2024 at approximately 15:21 UTC, the attacker used a Margin.fi flash loan to borrow large amounts of SOL and immediately purchased entire bonding curves of newly launched memecoins on Pump.fun.  
By driving each token’s price to the Raydium-listing threshold in one block, they triggered the bonding-curve payout function and drained over 12,300 SOL (~$2 million) before repaying the flash loan within minutes.  
Trading was halted seconds later, as Pump.fun announced an emergency pause to prevent further losses and began investigating the breach.

---

## :green[3. Technical Analysis]

The core vulnerability lay in Pump.fun’s bonding-curve contract, which lacked any mechanism to distinguish between flash-loan–funded purchases and genuine demand, allowing the attacker to exploit instant debt to drive prices up.  
Because purchases and liquidity withdrawals occurred in the same transaction without intermediate state checks, the attacker could buy the full curve, withdraw the bonded SOL, and still satisfy the loan repayment, resulting in a net siphon of protocol assets.  
Furthermore, the attacker’s prior employment granted them admin-level insights and a private key (“withdraw authority”), which they used to upgrade contracts mid-exploit—an insider move that compounded the damage to 12,300 SOL (~$1.9 million).

---

## :blue[4. Protocol Response and Aftermath]

Immediately upon confirmation, Pump.fun paused all trading and bonding-curve interactions, declaring TVL safe while contracts were audited and upgraded to add loan-detection and delayed withdrawal guards.  
The team publicly collaborated with law enforcement and blockchain forensics, identifying the exploiter as former employee “STACCoverflow” and tracing funds through on-chain analytics.  
Within 24 hours, Pump.fun redeployed audited contracts, resumed trading with 0 % fees for affected pools, and committed to fully reimbursing impacted users from treasury reserves.

---

## :violet[5. Lessons Learnt]

- **:green[Flash-Loan Awareness:]** Bonding-curve protocols must detect and restrict flash-loan–backed purchases, e.g., via time-locked withdrawals or loan-source oracles.  

- **:orange[Insider Risk Management:]** Admin keys and withdraw authority require robust multi-signature controls and frequent key rotation to prevent privilege misuse.  

- **:green[Atomicity Safeguards:]** Smart contracts should enforce intermediate state validations between buy and withdraw operations, breaking exploit chains within single transactions.  

- **:orange[Incident Response Protocols:]** Rapid pausing mechanisms, transparent communication, and emergency audits are vital to limit losses and restore user confidence.

---

## :red[6. Conclusion]

The Pump.fun exploit highlights the danger of unguarded bonding-curve mechanics combined with flash loans and insider privileges. While the attacker leveraged advanced DeFi tooling and privileged access to extract ~$2 million, Pump.fun’s swift pause, forensic collaboration, and contract overhauls helped safeguard remaining TVL and set new security standards for memecoin launchpads. Future protocols must integrate loan-source checks, tighten admin controls, and architect atomicity safeguards to prevent similar high-speed drains and maintain ecosystem trust.
""")
