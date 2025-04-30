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

    st.image("images/uxd.jpeg")  

    st.markdown("""
**1. A brief description of the protocol**  
UXD Protocol is an algorithmic stablecoin on Solana that mints $UXD by allocating collateral across yield strategies—including lending protocols and liquidity pools such as Mango Markets—via its asset-liability management module. The attacker’s wallets were  
`CQvKSNnYtPTZfQRQ5jkHq8q2swJyRsdQLcFcj3EmKFfX` and `4ND8FVPjUGGjx9VuGFuJefDWpg3THb58c277hbVRnjNa`.  

**2. Exploit summary**  
- **Oct 11, 2022 (evening UTC)**: Attacker funds two Mango accounts and opens outsized positions on MNGO perpetual futures, driving the on-chain price from ~$0.03 to $0.91 within minutes.  
- **Oct 12, 2022 (early UTC)**: Inflated MNGO collateral allows the attacker to borrow the entire USDC, SOL, SRM, and other pools—draining Mango Markets of ~$116 million and triggering large unrealized losses for UXD.  
- **Immediate impact**: UXD’s vaults, with ~$19.97 million deployed into Mango, see their collateral valuations collapse, forcing a pause on minting and redemptions.  

**3. Technical analysis**  
The core vulnerability was UXD’s reliance on Mango’s single-source price oracle without sanity checks, paired with instant reuse of unrealized perp profits as collateral. Oracle manipulation inflated UXD collateral by over 20×, creating bad debt that overwhelmed its insurance buffer.  

**4. Protocol response and aftermath**  
- **Oct 12**: UXD paused all mint and redeem functions to halt further exposure.  
- **Oct 20**: Mango Markets opened the claims process for affected partners.  
- **Oct 26**: UXD recovered 1,601,017.23 USDC, 125,637.9371 SOL, 4,953.65348 SRM, and 10,000.34093 MNGO (≈19,965,020.91 USDC) and replenished its insurance fund.  
- **Risk overhaul**: UXD integrated multi-source oracles, added circuit breakers, enforced position limits, and increased insurance reserves.  

**5. Lessons learnt**  
- Integrate decentralized, multi-source oracles with sanity checks and circuit breakers.  
- Enforce strict position-size limits relative to market liquidity.  
- Maintain over-collateralization buffers and fee-funded insurance pools.  
- Embed pre-approved pause and recovery governance mechanisms.  

**6. Conclusion**  
The Oct 12, 2022 UXD Protocol exploit highlights how single-source oracle risks and rapid reuse of unrealized gains can cascade across composable DeFi. UXD’s swift suspension, full recovery of ~$19.97 million, and comprehensive risk-parameter overhaul now serve as a blueprint for resilient algorithmic stablecoin design.
""")

