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

    st.image("images/serum.jpeg")  

    st.markdown("""

# :blue[Serum DEX Exploit Report]

## :red[1. A Brief Description of the Protocol]

Serum was a decentralized exchange (DEX) built on Solana, offering a fully on-chain order book model, unlike typical AMM (automated market maker) DEXs. It enabled fast, cheap, and fully permissionless trading with a matching engine at its core, providing a "central limit order book" (CLOB) experience on-chain. Serum was widely integrated into other Solana DeFi apps and played a critical role in the ecosystem.

However, during a broader Solana ecosystem security crisis tied to FTX’s collapse in November 2022, Serum’s security was compromised. The attacker gained control of Serum's upgrade authority, allowing them to potentially inject malicious code into the protocol.

- Attacker's Wallet Address: **:orange[0x5f5c7ed0aee62f2ea41b1a08674ef3202afcf1f4]**

## :orange[2. Exploit Summary]

In November 2022, as the FTX empire collapsed, alarms were raised across Solana DeFi platforms integrated with Serum. 

- **November 12, 2022**: The community discovered that the Serum program upgrade key — effectively, the admin control over the contract — was not controlled by a multisig or decentralized party. It was held by a single private key, which was compromised during FTX’s downfall.
  
- **November 12, 2022 (later that day)**: Fears spread that the attacker could use the compromised key to upgrade Serum’s smart contracts to malicious versions that could drain users’ funds without their knowledge.

- **November 13, 2022**: Major Solana protocols like Jupiter, Raydium, and others announced emergency measures. They rapidly disabled Serum trading integrations and switched to Serum forks with known-safe, community-controlled upgrade authorities.

- **November 14, 2022**: The original Serum program was deemed "dead" by the community. Users were advised not to interact with it anymore, and a Serum community fork named "OpenBook" was launched to replace it.

The exploit narrative wasn’t a direct "funds stolen" attack through Serum’s existing contracts, but rather a critical loss of **trust and security** through potential control of Serum’s upgrade path.

## :green[3. Technical Analysis]

The technical vulnerability lay in **Serum’s upgrade authority design**:

- **Original Design Flaw**: Serum’s upgrade key was not transferred to a multisig wallet or DAO governance model. Instead, it was retained by a trusted entity (allegedly controlled by FTX/Alameda).

- **Compromise**: When FTX/Alameda's internal security collapsed, the Serum upgrade authority's private key was compromised. This meant an attacker could submit a new version of Serum's contract, approve malicious code, and inject it live into the Serum program.

- **Potential Exploit Steps**:
  1. Submit a new program upgrade for Serum (e.g., adding code to steal funds).
  2. Approve the upgrade using the compromised upgrade authority.
  3. As users interacted with Serum, malicious logic could reroute or steal funds.

- **Impact**:
  - Immediate shutdown of Serum integrations across the Solana DeFi stack.
  - Creation of a new fork (OpenBook) to rescue liquidity and rebuild trust.
  - Loss of a key DeFi building block and reputational damage to Solana DeFi.

**No mass funds theft occurred directly via Serum**, but the potential was large enough to warrant instant abandonment.

## :blue[4. Protocol Response and Aftermath]

- **Emergency Decentralization**: Developers and protocols moved swiftly to shut down Serum dependencies.
  
- **Forking Serum**: A "clean room" community fork called **OpenBook** was created. OpenBook had a new program address, controlled via a secure, decentralized multisig structure.

- **User Communications**: Teams like Jupiter and Raydium issued immediate warnings, recommending users stop interacting with Serum.

- **OpenBook Adoption**: Within days, OpenBook was adopted by major aggregators and protocols as the new source of liquidity and trading.

- **Ecosystem Recovery**: Although the Serum brand was deeply tarnished, Solana DeFi’s resilience was displayed through rapid recovery and the rise of OpenBook.

## :violet[5. Lessons Learnt]

- **:green[Comprehensive Audits:]** Having regular security reviews isn’t enough. The authority model must be thoroughly audited, not just code safety.

- **:orange[Robust Testing:]** Stress testing the assumptions around upgrade authorities and operational keys is vital.

- **:green[Decentralized Governance:]** Upgrade authorities must be in multisig or fully decentralized DAOs to mitigate single points of failure.

- **:orange[Incident Response Planning:]** Immediate action plans and communication channels helped save billions in liquidity during the crisis.

- **:green[Transparency:]** Protocols need to disclose upgrade authority models clearly to users.

## :red[6. Conclusion]

The Serum incident was less about a direct smart contract bug and more a profound governance and operational security failure. Trust, not code alone, underpins DeFi protocols. The compromised upgrade authority exposed how centralization risks can ripple through an entire ecosystem. 

However, the Solana community’s rapid pivot to OpenBook showcased the power of decentralized development and the importance of proactive, transparent leadership. Future protocols must not just build "secure" code — they must also decentralize **every vector of control** to survive crises.

""")
