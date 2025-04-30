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

    st.image("images/mango_market.jpeg")  

    st.markdown("""
## Mango Markets Exploit Report (October 11, 2022)

### 1. A brief description of the protocol

Mango Markets is a decentralized exchange (DEX) and lending protocol built on the Solana blockchain. It allowed users to trade spot and perpetual futures and to lend and borrow various cryptocurrency assets. A key component of Mango Markets was its reliance on price oracles, which provided external market data to the protocol's smart contracts for purposes such as determining asset values for collateral and liquidations.

The individual identified and later convicted for orchestrating this exploit is **Avraham Eisenberg**. While specific wallet addresses directly initiating the manipulative trades might be numerous and complex due to the nature of the attack across different platforms, addresses associated with receiving the stolen funds were tracked as part of the subsequent investigations and legal proceedings. Some addresses linked to the movement of funds during and after the exploit have been publicly discussed in post-mortem analyses and court documents.

### 2. Exploit summary

On October 11, 2022, Mango Markets became the target of a calculated manipulation scheme that resulted in the draining of over $116 million in assets. The individual behind the attack, Avraham Eisenberg, did not exploit a typical smart contract bug but rather manipulated the market price of Mango's native token, MNGO, to benefit his positions on the platform.

The narrative of the attack unfolds as a high-stakes financial maneuver. Eisenberg first established significant positions on Mango Markets related to the MNGO token's perpetual futures. Then, in a rapid series of transactions across various exchanges that fed into Mango's price oracle, he artificially inflated the spot price of the relatively low-liquidity MNGO token. As Mango's oracle updated its price based on this manipulated data, Eisenberg's futures positions on Mango became extraordinarily valuable. Leveraging this inflated, albeit artificial, collateral value, he was able to borrow and withdraw nearly all the available assets from the Mango Markets protocol, effectively draining its treasury and user deposits. Following the incident, Eisenberg engaged with the Mango DAO, proposing terms for the return of a portion of the funds.

### 3. Technical analysis

The Mango Markets exploit was a sophisticated price oracle manipulation attack, exploiting the protocol's reliance on external price feeds for a thinly traded asset.

**The Issue:** Mango Markets used a price oracle to determine the value of assets on its platform. This oracle aggregated price data from several external exchanges. The vulnerability lay not necessarily in the oracle mechanism itself being faulty in aggregating data, but in the fact that the MNGO token, being relatively illiquid compared to major cryptocurrencies, was susceptible to significant price swings if large buy orders were executed on the exchanges the oracle monitored. Mango's protocol then used this potentially manipulable price for critical functions like determining collateral value and borrowing power.

**The Exploit:** Avraham Eisenberg orchestrated the attack in several coordinated steps:

1.  **Establishing Positions:** Eisenberg opened large perpetual futures positions on Mango Markets betting on the price of MNGO.
2.  **Market Manipulation:** Using significant capital (reportedly around $10 million in USDC), Eisenberg simultaneously executed a large volume of buy orders for the MNGO token on the external spot markets that fed into Mango's price oracle. Due to MNGO's low liquidity, these concentrated buy orders rapidly drove up its price on those exchanges.
3.  **Oracle Update:** Mango Markets' oracle, reflecting the sudden surge in MNGO's price on the external markets, updated the price feed on the protocol.
4.  **Inflating Collateral Value:** This artificially inflated price was then used by Mango Markets to calculate the value of Eisenberg's MNGO-related perpetual futures positions on the platform. These positions, based on the manipulated price, now appeared vastly more valuable than their true market worth.
5.  **Borrowing and Withdrawal:** With his collateral value artificially inflated, Eisenberg was able to borrow and withdraw a massive amount of other assets (primarily stablecoins like USDC, as well as SOL, mSOL, etc.) from Mango Markets' lending pools. These borrowed assets effectively came from the deposits of other users and the protocol's treasury.
6.  **Net Profit:** Eisenberg repaid his initial flash loan (if one was used to acquire the initial capital, though reports suggest he used his own funds to some extent) and was left with the large amount of borrowed assets, while leaving his highly valued but illiquid MNGO perpetual futures positions as collateral, which subsequently plummeted in value.

**Impact:** The exploit resulted in a loss of approximately $116 million worth of various cryptocurrencies from the Mango Markets protocol, effectively draining its available liquidity and leaving the protocol with significant "bad debt" in the form of the devalued MNGO collateral. This caused substantial losses for other users who had deposited funds into the lending pools.

### 4. Protocol response and aftermath

Immediately after detecting the large, suspicious withdrawals, Mango Markets halted all withdrawals and deposits on the platform to prevent further losses. They publicly acknowledged the incident, stating it was due to "an oracle price manipulation."

In a highly unusual move, Avraham Eisenberg engaged directly with the Mango DAO governance forum. He proposed a settlement agreement where he would return a portion of the stolen funds (around $67 million) in exchange for the DAO agreeing not to pursue criminal charges against him and allowing him to keep the remaining amount (around $47 million) as a "bug bounty" or profit from his trading strategy. This proposal was put to an on-chain governance vote. Controversially, Eisenberg himself used a significant portion of the MNGO tokens he had acquired or controlled through the exploit to vote in favor of his own proposal. Despite the ethical implications and concerns about governance under duress, the proposal passed, and Eisenberg returned approximately $67 million.

However, the situation did not end there. U.S. authorities launched investigations, leading to Avraham Eisenberg's arrest in Puerto Rico in December 2022. He was subsequently charged by the Department of Justice (DOJ), the Commodity Futures Trading Commission (CFTC), and the Securities and Exchange Commission (SEC) with various offenses, including market manipulation, commodities fraud, and wire fraud. In April 2024, Eisenberg was convicted on these charges after a jury trial, marking a significant case at the intersection of DeFi exploits and traditional legal systems. Mango Markets also initiated civil lawsuits against Eisenberg to recover the remaining funds. The protocol's operations were severely impacted by the exploit and the subsequent events.

### 5. Lessons learnt

The Mango Markets exploit provided several critical lessons for the DeFi space:

* **Oracle Security is Paramount:** The exploit highlighted the extreme vulnerability of protocols that rely on price oracles, especially when those oracles are susceptible to manipulation through illiquid markets. Protocols must implement robust, decentralized, and manipulation-resistant oracle solutions, potentially incorporating mechanisms to detect and mitigate the impact of sudden, large price deviations or low trading volume.
* **Market Manipulation Risks in DeFi:** This case demonstrated that even without a traditional smart contract bug, protocols can be exploited through market manipulation if their design allows for artificial price increases of assets used as collateral.
* **Governance Under Duress is Problematic:** The incident raised significant questions about the integrity and effectiveness of decentralized governance when a large portion of voting power is controlled by an exploiter who is dictating terms under duress. Mechanisms to prevent such scenarios or handle them more robustly are needed.
* **The Interplay of On-Chain and Off-Chain:** The exploit and subsequent legal actions showed that on-chain activities have real-world legal consequences. While DeFi operates on blockchain, participants are still subject to traditional laws and regulations concerning fraud and market manipulation.
* **Risk Management for Illiquid Assets:** Protocols allowing the use of relatively illiquid assets as collateral need to implement stricter risk parameters, including higher collateralization ratios or limitations on borrowing against such assets, to mitigate the impact of price manipulation.
* **Incident Response and Communication:** The immediate halting of operations and communication with users by Mango Markets were positive steps, but the handling of negotiations with the attacker through governance was highly controversial.

### 6. Conclusion

The Mango Markets exploit on October 11, 2022, was a significant and complex incident of market manipulation orchestrated by Avraham Eisenberg. By exploiting the protocol's reliance on price oracles for the thinly traded MNGO token, Eisenberg artificially inflated its value and used this inflated collateral to drain approximately $116 million from the platform. The aftermath involved controversial on-chain governance negotiation and, notably, subsequent criminal and civil legal action against Eisenberg, resulting in his conviction. This exploit serves as a crucial case study illustrating the vulnerabilities at the intersection of decentralized finance protocols, external data feeds, market dynamics, and the increasing reach of traditional legal frameworks in addressing illicit activities in the crypto space. It underscored the urgent need for more robust oracle security, better risk management for illiquid assets, and more resilient governance mechanisms in DeFi protocols.
""")