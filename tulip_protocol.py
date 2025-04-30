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

    st.image("images/tulip.jpeg")  

    st.markdown("""
## Tulip Protocol Exploit Report (October 12, 2022)
                
**1. Brief description of the protocol**  
Tulip Protocol (formerly SolFarm) is a Solana-based yield aggregator offering auto-compounding vaults, leveraged farming (up to 3×), and low-risk lending services via tuAssets. The attacker’s main Mango account was `4ND8FVPjUGGjx9VuGFuJefDWpg3THb58c277hbVRnjNa`.  

**2. Exploit summary**  
- **Oct 11, 2022, 19:36 UTC**: Attacker created and funded Mango Account 1 with an initial 25 K USDC, then topped it up to ~5.525 M USDC across multiple transfers.  
- **Oct 11–12, 2022**: Using two Mango accounts, they placed outsized short and long positions on MNGO perpetual futures, driving the on-chain price from ~$0.038 to ~$0.91 within minutes.  
- **Oct 12, 2022**: Tulip’s auto-compounding vaults, which had deployed user funds into Mango’s liquidity pools, saw ~$2.5 M drained when the attacker withdrew collateral and assets.  

**3. Technical analysis**  
Tulip’s vaults relied directly on Mango’s cross-margin lending pools and on-chain price oracles without additional sanity checks. The exploit unfolded in three phases:  
1. **Oracle manipulation**: The attacker skewed Mango’s MNGO oracle price via perp order placement.  
2. **Collateral inflation**: Vault deposits reflected inflated MNGO values, allowing excessive borrowing.  
3. **Asset extraction**: Stolen collateral (USDC, SOL, SRM, etc.) was pulled from both Mango and Tulip-connected pools, resulting in ~$2.5 M of losses.  

**4. Protocol response and aftermath**  
- Vaults were immediately paused; deposits and withdrawals halted.  
- On Oct 26, Tulip announced recovery of the lost $2.5 M and re-enabled USDC and $RAY strategy vaults under tightened risk controls.  
- Tulip refactored its risk model: halted direct Mango integrations, adopted multi-source oracles (e.g., Pyth), and imposed position limits.  

**5. Lessons learnt**  
- **Cross-protocol risk management**: Composability amplifies external exploits—monitor and cap third-party interactions.  
- **Oracle resilience**: Implement multi-source feeds with sanity checks and circuit breakers.  
- **Diversification & insurance**: Spread yield across multiple protocols and maintain an insurance buffer for bad-debt coverage.  

**6. Conclusion**  
The Oct 12, 2022 incident underscores the perils of unchecked composability: a Mango Markets exploit cascaded into Tulip’s vaults, draining ~$2.5 M. Tulip’s subsequent risk overhaul now serves as a blueprint for secure cross-protocol DeFi integrations.
""")
