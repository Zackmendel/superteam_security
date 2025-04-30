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

    st.image("images/marinade.jpeg")  

    st.markdown("""
# :blue[Marinade Finance Security Incident Report - December 20, 2023]

## :red[1. Protocol Description]

Marinade Finance is a leading liquid staking protocol on the Solana blockchain. It allows users to stake their SOL tokens to earn rewards while maintaining liquidity through its liquid staking token, mSOL. Marinade also offers a "Native Staking" product, introduced in July 2023, which allows users to stake SOL directly to validators using Marinade's automated delegation strategy without interacting with a smart contract, leveraging Solana's native staking mechanisms. The incident on December 20, 2023, primarily affected users of the Marinade Native staking product.

The incident was linked to a vulnerability in the underlying Solana staking delegation program, not a direct exploit of Marinade's smart contracts. While specific attacker wallet addresses involved in exploiting the Solana program vulnerability exist on the blockchain, there isn't a single attacker address universally tied to a "Marinade Finance exploit" in the sense of compromising Marinade's core protocol or mSOL liquid staking contract. Addresses involved were those that interacted with the vulnerable Solana staking program to perform unauthorized withdrawals from affected native stake accounts.

## :orange[2. Exploit Summary]

On December 20, 2023, the Solana ecosystem experienced an incident related to a vulnerability within the Solana staking delegation program. This vulnerability allowed unauthorized withdrawals from certain native staking accounts managed by this program. Marinade Finance users who utilized the Marinade Native staking product were consequently impacted, as their stake accounts are built on this underlying Solana program.

The exploit unfolded when malicious actors discovered and leveraged the flaw in the Solana staking program. They were able to craft transactions that bypassed intended security checks, enabling them to withdraw SOL from vulnerable native stake accounts without proper authorization. Because Marinade Native users' stake accounts are instances of this Solana program, some of these accounts became targets. The attackers systematically drained SOL from affected accounts, causing unexpected losses for the users who had staked natively through Marinade. Marinade Finance quickly identified the issue impacting their native stakers and worked to understand the root cause and communicate with affected users, emphasizing that the vulnerability was external to Marinade's own smart contracts.

## :green[3. Technical Analysis]

The technical root cause of the December 20, 2023 incident was a vulnerability found within the **Solana staking delegation program** itself. This program is a fundamental part of the Solana blockchain that manages native staking accounts and delegations. The specific flaw allowed an attacker to perform unauthorized `withdraw` operations from certain stake accounts under specific conditions.

The exploit involved the attacker crafting a malicious transaction that targeted a vulnerable stake account. By exploiting the logic error in the Solana program's withdrawal function, the attacker could execute a withdrawal from the stake account even though they did not possess the correct authorization (the withdraw authority key). This effectively allowed them to steal the staked SOL. Marinade Native stake accounts, being instances of this standard Solana program, were susceptible if they met the conditions for the vulnerability. The impact was the unauthorized draining of staked SOL from affected Marinade Native user accounts, resulting in direct financial loss for those users. It's crucial to note that this was a vulnerability in the *Solana program*, not a bug in Marinade's specific smart contracts or delegation strategy logic.

## :blue[4. Protocol Response and Aftermath]

Upon becoming aware of the unauthorized withdrawals impacting their Native stakers, Marinade Finance acted swiftly to address the situation and support affected users. Their response included:

* **Immediate Investigation:** Working to understand the scope of the issue and confirm that the vulnerability was in the underlying Solana staking program.
* **Communication:** Alerting the community about the incident, clarifying that it affected Marinade Native stakers due to an external Solana program vulnerability, and providing information on the situation.
* **Collaboration:** Engaging with the Solana Foundation, validators, and security researchers to understand the vulnerability and contribute to mitigation efforts.
* **Support for Users:** Providing guidance to affected Native stakers and exploring potential avenues for support or recovery, although recovery of stolen funds in such blockchain exploits is often challenging.

The aftermath involved affected users dealing with the loss of their staked SOL. For Marinade, it reinforced the importance of monitoring underlying blockchain infrastructure and clearly communicating the risks associated with different staking methods (native vs. liquid staking) and their dependencies on core blockchain programs.

## :violet[5. Lessons Learnt]

The Marinade Finance incident on December 20, 2023 (caused by the Solana staking program vulnerability) provides important lessons for users and protocols alike:

* **:green[Understand Underlying Dependencies:]** Protocols built on top of blockchain infrastructure are dependent on the security of those underlying layers. Users should be aware of these dependencies.
* **:orange[Solana Program Risks:]** Even core blockchain programs can have vulnerabilities. Users interacting directly or indirectly with these programs (like native staking) are exposed to their risks.
* **:green[Due Diligence on Staking Methods:]** Users should understand the technical differences and associated risks between native staking (interacting directly with blockchain programs) and liquid staking (interacting with a protocol's smart contracts).
* **:orange[Importance of Blockchain Security Audits:]** Fundamental blockchain programs, like the staking delegation program, require continuous and rigorous security audits.
* **:green[Protocol Response to External Issues:]** Protocols affected by external vulnerabilities should have clear communication and support plans for their users.
* **:orange[Risk of Unauthorized Withdrawals:]** Vulnerabilities allowing unauthorized withdrawals from staking or other accounts are critical and highlight the need for robust access control logic.

## :red[6. Conclusion]

The incident on December 20, 2023, which impacted Marinade Finance Native stakers, was a result of an exploit targeting a vulnerability in the Solana staking delegation program. This allowed unauthorized withdrawals from affected native stake accounts. While Marinade's core liquid staking protocol (mSOL) was not directly compromised, the incident highlighted the risks associated with interacting with fundamental blockchain programs and their potential impact on protocols built upon them. The event underscores the continuous need for security vigilance at all layers of the blockchain stack and the importance of users understanding the specific risks associated with different staking methods and their underlying technologies.
""")
