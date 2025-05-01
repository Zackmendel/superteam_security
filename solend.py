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

    st.image("images/solend.jpeg")  

    st.markdown("""
# :blue[Solend Incident Report – November 2, 2022]

## :red[1. A Brief Description of the Protocol]

Solend is a decentralized lending and borrowing protocol on Solana. It enables users to deposit and earn yield or borrow against collateralized crypto assets. The protocol operates through a main pool and several isolated pools that handle assets of varying risk and liquidity profiles. Solend depends on price oracles like Switchboard and Pyth Network for asset valuation, liquidation, and lending logic.

---

## :orange[2. Exploit Summary]

On November 2, 2022, Solend suffered a market manipulation attack targeting its isolated lending pools. The attacker exploited a low-liquidity Saber pool used to price USDH (a stablecoin) via the Switchboard oracle. By manipulating the price of USDH and exploiting Solana’s transaction slot mechanics, they deposited inflated USDH as collateral and borrowed other tokens. When the price reverted, Solend was left with $1.26 million in bad debt.

The exploit narrative wasn’t a direct "funds stolen" attack via smart contract flaws, but rather a calculated abuse of oracle logic and liquidity conditions, leading to systemic bad debt.

---
## :green[3. Technical Analysis]

The core vulnerability was the oracle’s reliance on a low-liquidity Saber pool for USDH pricing. The attacker:

- Manipulated the USDH price upward in Saber’s thin pool.
- Used slot timing tactics to prevent arbitrage correction within the same Solana slot.
- Ensured the Switchboard oracle picked up the inflated USDH price.
- Deposited high-priced USDH into Solend’s isolated pools.
- Borrowed significant assets like SOL against the inflated collateral.
- Let the USDH price revert, leaving Solend with undercollateralized loans.

The technical sequence involved:
- **:green[Step 1:]** Acquire USDH and prepare capital.
- **:orange[Step 2:]** Pump USDH price in Saber’s pool.
- **:green[Step 3:]** Stuff Solana slots to prevent arbitrage.
- **:orange[Step 4:]** Oracle reads the inflated price.
- **:green[Step 5:]** Deposit USDH and borrow other tokens.
- **:orange[Step 6:]** Collateral value crashes → bad debt.

---

## :blue[4. Protocol Response and Aftermath]

Solend responded by:
- Disabling the affected isolated pools (Stable, Coin98, Kamino).
- Publicly disclosing the incident and classifying it as an oracle attack.
- Collaborating with exchanges and analytics firms to track the attacker’s wallets.
- Reevaluating its oracle sources and asset vetting within isolated pools.

---

## :violet[5. Lessons Learnt]

- **:green[Oracle Resilience is Paramount:]** Low-liquidity pools should not be primary sources for price feeds.
- **:orange[Isolated Pools Require Stronger Risk Controls:]** Asset oracles within these pools must be carefully vetted.
- **:green[Prevent Oracle Manipulation:]** Use TWAPs, liquidity filters, and multiple sources to guard against abuse.
- **:orange[Understand Blockchain Timing Risks:]** Slot-level exploits are real; architecture awareness is critical.
- **:green[Prepare for Bad Debt:]** Protocols should maintain insurance mechanisms for scenarios like this.
- **:green[Transparency:]** Protocols need to disclose oracle logic, asset vetting criteria, and incident reports in detail.

---

## :red[6. Conclusion]

Solend’s November 2 attack demonstrates how thin liquidity and oracle misconfiguration can lead to major lending losses without any smart contract exploit. By inflating USDH and manipulating oracle timing, the attacker induced ~$1.26M in bad debt. The event underscores the necessity for robust oracle systems, architectural awareness of blockchain mechanics, and clear risk frameworks for isolated lending pools.
""")
