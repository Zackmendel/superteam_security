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

    st.image("images/cypher.jpeg")  

    st.markdown("""
# :blue[Cypher Protocol Exploit Report - August 7, 2023]

## :red[1. Protocol Description]

The Cypher Protocol was a decentralized finance (DeFi) protocol operating on the Solana blockchain. It aimed to provide a range of services, including lending, borrowing, and trading of various digital assets. The protocol utilized smart contracts to manage user funds and execute operations automatically. At the time of the exploit, the protocol held significant user deposits across different markets.

The attacker's wallet address associated with the exploit is reportedly: **:orange[`9WzDxLzdtpx2pQ1WfS9P8VdJbLz7v9W2p1bX7pQ1bX7p`]** (Note: This is a placeholder address as the exact address might vary across reports; always verify with official sources or blockchain explorers).

## :orange[2. Exploit Summary]

The incident unfolded rapidly on the morning of August 7, 2023. It began when an attacker initiated a series of transactions targeting specific vulnerabilities within the Cypher Protocol's smart contracts. The attacker seemingly identified a flaw related to how the protocol handled certain market interactions or price updates.

Like a carefully orchestrated raid, the attacker executed a sequence of steps designed to manipulate the protocol's internal state. They appeared to exploit a window of opportunity, potentially involving flash loans or rapid trading actions, to drain assets from the protocol's liquidity pools. The attack was swift and precise, leaving the protocol's reserves significantly depleted in a matter of minutes. Users and the protocol team quickly noticed unusual activity as funds were siphoned away, leading to a frantic effort to understand and mitigate the damage. The exploit effectively halted the protocol's operations as the team moved to contain the situation and prevent further losses.

## :green[3. Technical Analysis]

The root cause of the exploit is believed to be a critical vulnerability within the Cypher Protocol's smart contract logic, specifically related to its handling of certain market operations or potentially an oracle integration issue. While the exact technical vector is complex, the core issue appears to stem from a flaw that allowed the attacker to interact with the protocol in an unintended way, leading to incorrect state updates or unauthorized fund withdrawals.

One likely scenario involves a logic error in how the protocol processed deposits, withdrawals, or liquidations under specific, manipulated conditions. The attacker could have potentially used a flash loan to acquire a large amount of a particular asset, interact with the vulnerable part of the protocol to trigger the exploit, and then repay the flash loan, keeping the illicitly gained funds. The vulnerability allowed the attacker to bypass intended checks or constraints, granting them the ability to withdraw more assets than they were legitimately entitled to. The impact was severe: a substantial amount of digital assets, including various tokens supported by the protocol, were drained from the protocol's reserves, causing significant financial loss to the protocol and its users.

## :blue[4. Protocol Response and Aftermath]

Upon detection of the exploit, the Cypher Protocol team immediately took action to halt the protocol's operations. This involved pausing the affected smart contracts to prevent any further siphoning of funds. The team initiated an urgent investigation to understand the full scope of the exploit, identify the vulnerability, and trace the flow of stolen assets. They engaged with security experts and blockchain analytics firms to assist in the investigation.

In the aftermath, communication with the community was a critical challenge. The team provided updates on the situation, confirming the exploit and the pause of operations. Efforts were focused on assessing the total loss and exploring potential avenues for recovery or compensation for affected users. The incident severely damaged trust in the protocol and highlighted the inherent risks in DeFi. Discussions around potential recovery plans, including seeking the return of funds or exploring compensation mechanisms, became the primary focus.

## :violet[5. Lessons Learnt]

The Cypher Protocol exploit serves as a stark reminder of the critical importance of rigorous security practices in the DeFi space. Key lessons include:

* **:green[Comprehensive Audits:]** Smart contracts must undergo multiple, thorough audits by reputable security firms before deployment and after any significant code changes.
* **:orange[Robust Testing:]** Extensive testing, including unit tests, integration tests, and fuzz testing, is crucial to uncover edge cases and vulnerabilities.
* **Continuous Monitoring:** Protocols need robust, real-time monitoring systems to detect unusual activity and potential exploits quickly.
* **Secure Oracle Usage:** If relying on external price oracles, ensure their security, reliability, and resistance to manipulation.
* **Incident Response Plan:** Having a well-defined incident response plan is essential for rapid and effective action during an exploit.
* **Defense in Depth:** Implementing multiple layers of security checks and safeguards can help prevent a single vulnerability from leading to catastrophic loss.

## :red[6. Conclusion]

The Cypher Protocol exploit on August 7, 2023, was a significant security incident in the DeFi ecosystem, resulting in substantial financial losses. The attack exploited a critical vulnerability within the protocol's smart contract logic, allowing an attacker to drain funds. The incident underscores the persistent security challenges faced by DeFi protocols and emphasizes the absolute necessity of prioritizing security throughout the development lifecycle, from design and coding to auditing, testing, and continuous monitoring. The recovery process for the Cypher Protocol and its users remains a key focus, highlighting the long-term consequences of such security breaches.
""")
