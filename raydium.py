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
## Raydium Exploit Report (December 16, 2022)

### 1. A brief description of the protocol

Raydium is an Automated Market Maker (AMM) and liquidity provider built on the Solana blockchain. It is integrated with the Serum decentralized exchange (DEX) order book, allowing it to provide on-chain liquidity to a central limit order book. Raydium offers features such as token swapping, liquidity provision, yield farming, and launching new tokens (IDO launchpad). It aims to leverage Solana's speed and low transaction costs to provide efficient trading and yield opportunities.

The primary exploit associated with Raydium occurred on December 16, 2022, and was attributed to a private key compromise. Addresses associated with receiving the stolen funds in this exploit include:
* **AgJddDJ...**
* **5ndLnEY...**
* **0x70479...** (an Ethereum address where some funds were bridged)

These addresses were identified as controlled by the exploiter who drained funds from Raydium's liquidity pools.

### 2. Exploit summary

On December 16, 2022, the Raydium protocol suffered a significant exploit that resulted in the unauthorized draining of assets from several of its liquidity pools. Unlike many DeFi exploits that target smart contract vulnerabilities, this incident was primarily a consequence of a compromised private key associated with a privileged protocol account.

The attack unfolded when an attacker gained unauthorized access to a private key that held administrative control over certain functions within Raydium's programs, specifically related to managing liquidity pools. With this compromised key, the attacker was able to invoke functions that allowed them to withdraw assets from various liquidity pools without depositing the corresponding liquidity provider (LP) tokens. This effectively allowed the attacker to steal funds contributed by users to these pools. The malicious transactions were executed rapidly, transferring a mix of tokens out of the affected pools before the Raydium team could fully react.

### 3. Technical analysis

The technical analysis of the Raydium exploit on December 16, 2022, points to a critical compromise of a private key with elevated privileges, rather than a flaw in the core AMM smart contracts themselves.

**The Issue:** The root cause of the exploit is widely believed to be the compromise of a private key belonging to an account that had the "owner authority" or administrative control over certain Raydium programs, particularly those managing AMM and farm operations. Reports suggest this private key may have been compromised via malware, possibly a trojan virus, on a device used by a team member or someone with access to this key. The vulnerability wasn't in the smart contract logic for swapping or farming itself, but in the centralized control granted to this specific private key.

**The Exploit:** The attacker, having obtained the compromised private key, was able to directly interact with Raydium's on-chain programs using this key to sign malicious transactions:

1.  **Private Key Compromise:** The attacker gained unauthorized access to the private key of a privileged Raydium account. The exact method is speculated to be malware (trojan).
2.  **Invoking Privileged Functions:** Using the compromised key, the attacker called specific administrative functions within the Raydium programs that were intended for managing liquidity pools, such as functions related to withdrawing funds or managing protocol fees (`withdraw_pnl` was specifically mentioned in analyses).
3.  **Unauthorized Withdrawal:** By executing these functions with the compromised key, the attacker bypassed the normal requirements for withdrawing liquidity (which would typically involve burning LP tokens) and was able to directly drain assets from multiple liquidity pools controlled by the affected programs.
4.  **Asset Transfer and Laundering:** The stolen assets, a mix of various tokens from the drained pools, were then transferred to the attacker's wallet addresses. A portion of these funds was later bridged to other blockchains, such as Ethereum, and some were sent to coin mixing services like Tornado Cash in an attempt to obfuscate the trail.

**Impact:** The exploit resulted in the theft of approximately $4.3 million to $5.5 million worth of various cryptocurrency assets from Raydium's liquidity pools. This directly impacted users who had provided liquidity to the compromised pools, leading to significant financial losses for them. The incident also caused a temporary halt in certain Raydium operations and a drop in the price of the native RAY token.

### 4. Protocol response and aftermath

Immediately upon detecting the unauthorized activity, the Raydium team acted quickly to halt the affected AMM and farm programs by revoking the compromised owner authority. This prevented the attacker from draining further funds.

Raydium publicly acknowledged the incident, stating that their initial understanding was that the owner authority key had been overtaken. They communicated with their community about the situation and the steps they were taking. Raydium collaborated with security researchers and the Solana Foundation to investigate the root cause and trace the stolen funds.

In response to the losses, Raydium announced a plan to compensate users affected by the exploit. They committed to using a portion of their protocol's unlocked token allocation to help cover the losses. For assets other than RAY tokens that were stolen, Raydium proposed using the DAO treasury to buy back the missing tokens on the market to compensate affected users, which was subject to and passed a governance vote. While they offered a bounty to the exploiter for the return of funds, the attacker did not comply. The incident underscored the importance of robust key management and the risks associated with centralized control in a decentralized protocol.

### 5. Lessons learnt

The Raydium exploit in December 2022 provided critical lessons for DeFi protocols and users alike:

* **Paramount Importance of Private Key Security:** The incident served as a stark reminder that even with secure smart contracts, a compromised private key with administrative privileges can be a single point of failure leading to catastrophic losses. Protocols must employ the highest standards of security for managing sensitive keys, including multi-signature wallets, hardware security modules (HSMs), and stringent access controls.
* **Risks of Centralization in DeFi:** Granting excessive administrative power to a single or a few private keys, even for operational efficiency, introduces centralization risks that run counter to the decentralized ethos of DeFi. Protocols should strive for greater decentralization of control over critical functions.
* **Operational Security is Crucial:** The suspected role of malware in compromising the private key highlights the importance of robust operational security practices within development teams and for any individuals holding keys with elevated permissions. Secure environments and practices are essential.
* **Impact of Malware:** Users and protocol teams must be vigilant against malware, as it can be a direct vector for compromising private keys stored on affected devices.
* **Transparency and Response:** Raydium's relatively swift response in halting the affected programs and communicating with the community, along with their commitment to compensation (though partial initially for non-RAY tokens), were important steps in managing the crisis and maintaining some level of trust.

### 6. Conclusion

The Raydium exploit of December 16, 2022, was a significant security breach on the Solana ecosystem, resulting in the theft of millions of dollars from Raydium's liquidity pools. The incident was primarily caused by the compromise of a private key with administrative control, which the attacker used to bypass normal protocol operations and drain funds. This exploit underscored the critical vulnerability introduced by centralized control points in decentralized protocols and the paramount importance of implementing stringent security measures for private key management and operational security. While Raydium took steps to mitigate further losses and planned for user compensation, the incident served as a strong cautionary tale about the potential consequences of a single compromised key in the DeFi landscape.
""")