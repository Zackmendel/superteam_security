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
## Solend Incident Report (November 2, 2022)

### 1. A brief description of the protocol

Solend is a decentralized lending and borrowing protocol operating on the Solana blockchain. It allows users to deposit cryptocurrency assets to earn yield and borrow assets by providing collateral. Solend utilizes different lending pools, including a main pool and isolated pools for assets with varying risk profiles and liquidity. The protocol relies on price oracles, such as Switchboard and Pyth Network, to determine the value of assets for lending, borrowing, and liquidation purposes.

Following the incident, the address(es) involved in the manipulation were identified, and Solend reportedly shared this information with exchanges to assist in tracing the stolen funds. While a single primary attacker wallet address is not consistently highlighted across public reports, the on-chain movements were tracked by investigators.

### 2. Exploit summary

On November 2, 2022, the Solend protocol experienced a market manipulation incident that resulted in bad debt within several of its isolated lending pools. This was not a traditional hack exploiting a smart contract vulnerability to directly steal deposited funds, but rather a calculated manipulation of asset prices to enable profitable borrowing against artificially inflated collateral.

The incident unfolded when an attacker targeted a specific stablecoin, USDH (Hubble Protocol Stablecoin), which was listed in some of Solend's isolated pools and whose price feed relied on a low-liquidity trading pool on the Saber DEX. The attacker artificially pumped the price of USDH in this low-liquidity pool through a series of transactions. Crucially, they also employed a technique to prevent arbitrage bots from quickly correcting the manipulated price within the same blockchain "slot" (a short time period on Solana). By timing their actions and effectively controlling the price seen by the oracle in the subsequent slot, the attacker was able to deposit the now artificially high-priced USDH as collateral into Solend's isolated pools and borrow other assets against it. When the price of USDH inevitably returned to its true market value, the value of the attacker's collateral plummeted, leaving their borrowed positions undercollateralized and resulting in bad debt for the protocol.

### 3. Technical analysis

The Solend incident on November 2, 2022, was a successful oracle manipulation attack leveraging the price feed's reliance on a low-liquidity market and employing transaction timing to control the price seen by the oracle.

**The Issue:** The vulnerability lay in the price oracle mechanism used for USDH in certain Solend isolated pools. The Switchboard oracle, in this case, was configured to source the price of USDH from a trading pool on the Saber DEX. The Saber USDH pool had low liquidity, making the USDH price within that pool susceptible to significant manipulation by relatively small trading volumes. Furthermore, the oracle's price updates, combined with Solana's transaction processing (specifically, how transactions are ordered and executed within slots), created a window for exploitation.

**The Attack:** The attacker executed a multi-step manipulation:

1.  **Acquiring USDH and Initial Capital:** The attacker likely acquired a significant amount of USDH and potentially other capital (though a large flash loan wasn't the primary mechanism as in some other exploits; the focus was on price impact).
2.  **Price Pumping in Low-Liquidity Pool:** The attacker executed buy orders for USDH in the low-liquidity Saber pool. This artificially inflated the price of USDH within that specific pool.
3.  **Preventing Arbitrage (Slot Stuffing/Timing):** To ensure the manipulated price persisted long enough for the oracle to pick it up, the attacker reportedly spammed transactions or otherwise manipulated the transaction flow to make it difficult or impossible for arbitrageurs to immediately correct the USDH price in the same slot on Saber.
4.  **Oracle Price Update:** The Switchboard oracle, reading the manipulated, high price of USDH from the Saber pool in the subsequent slot, reported this inflated price to the Solend protocol.
5.  **Depositing Inflated Collateral:** The attacker deposited the now artificially high-priced USDH into the affected Solend isolated lending pools as collateral.
6.  **Borrowing Assets:** Based on the inflated value of their USDH collateral, the attacker was able to borrow a larger amount of other assets (like SOL, etc.) from these pools than their USDH would have allowed at its true price.
7.  **Price Correction and Bad Debt:** After the attacker withdrew the borrowed assets, the manipulated price of USDH on Saber would inevitably revert to its true market value due to arbitrage or lack of continued buying pressure. This left the attacker's deposited USDH collateral on Solend significantly undercollateralized, creating bad debt for the protocol as the value of the borrowed assets exceeded the true value of the collateral.

**Impact:** The incident resulted in approximately $1.26 million in bad debt across the affected Solend isolated pools (Stable, Coin98, and Kamino). This loss impacted the liquidity providers in those specific pools.

### 4. Protocol response and aftermath

Upon detecting the price manipulation and the resulting bad debt, the Solend team took immediate action by disabling the affected isolated pools (Stable, Coin98, and Kamino) to prevent further borrowing against the manipulated asset and limit the increase of bad debt.

Solend publicly communicated the incident, identifying it as an oracle attack targeting USDH in low-liquidity pools. They acknowledged the resulting bad debt and stated they were working on a plan to address it. Solend also collaborated with exchanges and analytics firms to track the funds borrowed by the attacker. While the specific attacker was not named publicly by Solend initially, their address(es) were reportedly known to relevant parties for tracking purposes.

The aftermath involved Solend dealing with the bad debt in the affected pools and reassessing their oracle integrations and risk management for isolated pools, particularly concerning assets with low liquidity or price feeds reliant on easily manipulable markets.

### 5. Lessons learnt

The Solend incident on November 2, 2022, provided crucial lessons for DeFi lending protocols:

* **Oracle Resilience is Paramount:** Relying on price feeds from low-liquidity markets, even when aggregated, poses a significant risk. Oracles need to incorporate safeguards against manipulation, such as using time-weighted average prices (TWAPs), considering trading volume and depth, and potentially excluding illiquid markets as reliable price sources.
* **Isolated Pools Require Careful Risk Management:** While isolated pools are designed to contain risk, the incident showed that vulnerabilities in one aspect (like an oracle feed) can still lead to losses within those pools if not properly managed. Rigorous vetting of assets and their price feeds within isolated pools is essential.
* **The Importance of Preventing Oracle Manipulation:** Protocols must actively work to prevent the manipulation of the price feeds they rely on. This includes choosing robust oracle solutions and potentially implementing real-time monitoring for suspicious price movements.
* **Transaction Timing and Blockchain Architecture:** Attackers can leverage the specifics of blockchain architecture, such as transaction ordering within slots, to time their manipulations and ensure the oracle picks up the artificial price. Protocols need to consider these low-level attack vectors.
* **Bad Debt Management:** Lending protocols must have mechanisms or insurance funds in place to handle potential bad debt resulting from oracle failures, liquidations, or market manipulation.

### 6. Conclusion

The Solend incident on November 2, 2022, was a market manipulation attack that exploited the protocol's reliance on a susceptible price oracle for USDH in low-liquidity isolated pools. By artificially inflating the price of USDH and controlling the price seen by the oracle, the attacker was able to borrow assets against inflated collateral, resulting in approximately $1.26 million in bad debt for the protocol. This event underscored the critical importance of robust and manipulation-resistant oracle design, careful risk management within isolated lending pools, and the need for protocols to be resilient against sophisticated market manipulation techniques that leverage blockchain timing and liquidity characteristics.
""")