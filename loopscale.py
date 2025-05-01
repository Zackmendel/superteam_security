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

    st.image("images/loopscale.jpeg")


    st.markdown("""
## :blue[Loopscale Lending Protocol Exploit Analysis]

## :red[1. A Brief Description of the Protocol]

Loopscale is a Solana-based decentralized lending protocol that launched its Genesis phase on April 10, 2025, offering an order-book model to directly match lenders and borrowers rather than pooling liquidity like traditional DeFi platforms.  
- **Solana exploiter #1:** :orange[4QsqugQcrCuSVzU9WjeLDoR6HaaSZtMEZr5JCyxwHgCV]  
- **Solana exploiter #2:** :orange[C1QyPYoWQiueqhtLeaG5Nhkv1LJ8oweBNCbfGJ3LprYT]  
- **EVM (Ethereum) wallet of the attacker:** :orange[0xc9d30E520Af584d0867FfC71DE162f1C09987Fe8]

---

## :orange[2. Exploit Summary]

On April 26, 2025, at approximately 15:28 UTC, the attacker observed a pricing discrepancy in Loopscale’s RateX PT token valuation and initiated a series of undercollateralized loans that drained the USDC and SOL vaults.  
The attacker first manipulated the on-chain price feed to dramatically lower the perceived value of RateX PT tokens, then deposited minimal collateral and borrowed large amounts of USDC and SOL against the mispriced tokens.  
Within minutes, the attacker had siphoned approximately 5.7 million USDC and 1,200 SOL—about 12% of Loopscale’s TVL—before pausing to assess the success of the exploit.  
After swapping assets, the attacker bridged the funds through Wormhole, triggering on-chain alerts that led Loopscale’s team to halt lending and withdrawals across the platform.

---

## :green[3. Technical Analysis]

The vulnerability originated in Loopscale’s RateX PT token pricing mechanism, which relied on a single oracle without sufficient time-weighted averaging or sanity checks.  
By submitting manipulated price data, the attacker caused the protocol to understate the collateral’s value, enabling undercollateralized borrowing far beyond safe limits.  
Once the mispricing was in place, the attacker executed a sequence of borrowing transactions that drained the Genesis USDC and SOL vaults, taking advantage of the protocol’s failure to enforce minimum collateral ratios in real time.  
As a result, Loopscale lost roughly $5.8 million in assets, representing a major hit to user deposits and trust in the fledgling protocol.

---

## :blue[4. Protocol Response and Aftermath]

Immediately upon detection, Loopscale paused all lending markets, vault withdrawals, and new loan openings while preserving the ability to repay and top up existing positions.  
On April 27, the team sent an on-chain message to the exploiter offering a 10% bounty—approximately 3,947 SOL—in exchange for returning 90% of the stolen funds and immunity from prosecution.  
By April 28 at 15:52 UTC, the hacker responded positively, and over the next 48 hours, roughly 19,463 WSOL (≈ $2.88 million) was returned in tranches.  
Meanwhile, Loopscale engaged security auditors to review the RateX pricing contracts, implemented multi‐oracle feeds, and accelerated a second audit by Sec3 to bolster defenses.

---

## :violet[5. Lessons Learnt]

- **:green[Oracle Redundancy:]** DeFi protocols must implement multi-source oracle architectures with time-weighted averaging to prevent single-point manipulation.  
- **:orange[Collateral Checks:]** Real-time enforcement of collateralization ratios is crucial; protocols should simulate worst-case oracle deviations during each loan action.  
- **:green[Incident Response:]** Rapid pausing mechanisms and clear communication channels help limit losses and rebuild trust under pressure.  
- **:orange[Bug Bounty Strategy:]** Proactive negotiation with white-hat attackers can recover funds and demonstrate commitment to user protection.

---

## :red[6. Conclusion]

The Loopscale exploit underscores the critical importance of robust oracle design and stringent collateral checks in DeFi lending protocols. While the attacker successfully drained a significant portion of Loopscale’s TVL through a price manipulation attack, the team’s swift response—including market halts, bounty negotiations, and architectural fixes—led to the recovery of a majority of stolen assets. Going forward, DeFi platforms must prioritize multi-layer security audits, resilient oracle infrastructures, and transparent incident‐response frameworks to safeguard user funds and maintain ecosystem integrity.
""")
