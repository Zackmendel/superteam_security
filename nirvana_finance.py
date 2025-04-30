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

    st.image("images/nirvana_finance.jpeg") 

    st.markdown("""
## Nirvana Finance Exploit Report (July 28, 2022)

### 1. A brief description of the protocol

Nirvana Finance was a decentralized finance protocol on the Solana blockchain that featured a dual-token model: NIRV, a U.S. dollar stablecoin, and ANA, a yield-bearing asset designed with an algorithmically rising floor price. The protocol aimed to provide a stable store of wealth and sustainable yield through its unique mechanism.

The individual later identified and who pleaded guilty to executing this exploit is **Shakeeb Ahmed**. Specific wallet addresses used in the execution and movement of funds during the exploit have been tracked by investigators, but a single primary attacker wallet address initiating the exploit transaction is not as widely publicized as the perpetrator's identity. The exploit involved complex transactions across several addresses to facilitate the flash loan, interaction with Nirvana's contracts, and subsequent fund dispersal and laundering.

### 2. Exploit summary

The Nirvana Finance exploit occurred on July 28, 2022, and was a swift and devastating attack that drained the protocol's treasury. The attacker's strategy revolved around manipulating the reported price of the ANA token using a flash loan.

The event unfolded rapidly. The attacker first secured a large flash loan, a type of uncollateralized loan instantly borrowed and repaid within the same blockchain transaction. With this substantial capital, the attacker interacted with Nirvana's smart contracts, specifically targeting the mechanism responsible for pricing the ANA token. By exploiting a vulnerability in how the protocol calculated ANA's price based on recent trades and the amount being bought, the attacker was able to artificially inflate the price of ANA through a large, albeit temporary, purchase using the flash loan funds. Immediately after this price manipulation, the attacker sold the significantly revalued ANA tokens back to the protocol, realizing a massive profit in stablecoins. This entire sequence, from borrowing the flash loan to selling the manipulated ANA and repaying the loan, happened within a single transaction, leaving the Nirvana treasury severely depleted.

### 3. Technical analysis

The technical core of the Nirvana Finance exploit was a classic flash loan-assisted price oracle manipulation attack, targeting a flaw in the protocol's algorithmically determined price of the ANA token.

**The Issue:** The vulnerability lay in Nirvana's price oracle for the ANA token. The price of ANA was designed to increase with demand and the amount being purchased. However, the mechanism for updating this price based on trades was susceptible to manipulation if a sufficiently large purchase was made within a single transaction, especially when funded by a flash loan. The protocol's oracle did not adequately account for or validate sudden, large swings in purchase volume that did not reflect genuine market depth.

**The Exploit:** The attacker leveraged a flash loan to exploit this vulnerability:

1.  **Flash Loan:** The attacker borrowed a large sum of stablecoins (reported to be around $10 million USDC) from a lending protocol like Solend via a flash loan.
2.  **Price Manipulation Purchase:** Using the borrowed funds, the attacker executed a large purchase of ANA tokens from Nirvana Finance's liquidity pool. Due to the flawed price oracle, this massive purchase, occurring in a single transaction, caused the protocol to register a drastically inflated price for ANA.
3.  **Arbitrage/Exploitation:** With the ANA token's price artificially high according to Nirvana's oracle, the attacker immediately sold the acquired ANA tokens back to the protocol. Because the selling price was based on the manipulated, higher value, the attacker received a much larger amount of stablecoins than the initial flash loan amount.
4.  **Flash Loan Repayment:** The attacker used a portion of the stablecoins obtained from selling the overvalued ANA to repay the initial flash loan.
5.  **Profit Withdrawal:** The remaining stablecoins constituted the attacker's illicit profit.

**Impact:** The exploit directly drained Nirvana Finance's treasury of approximately $3.5 million. This sudden and significant loss of funds severely impacted the protocol's reserves, which were intended to back the value of NIRV and support the rising floor price of ANA. The ANA token's price plummeted by over 80% immediately after the attack, and the NIRV stablecoin lost its peg. The financial damage was so severe that it ultimately led to the demise of the Nirvana Finance protocol.

### 4. Protocol response and aftermath

In the immediate aftermath of the exploit, Nirvana Finance acknowledged the hack and temporarily halted protocol operations. They publicly appealed to the hacker, offering a white-hat bounty (initially reported as $300,000, later mentioned up to $600,000 in some reports) for the return of the stolen funds. However, the attacker reportedly demanded a higher amount ($1.4 million), and no agreement was reached at that time.

Despite efforts to recover the funds and explore options, the financial blow proved too significant for Nirvana Finance to overcome. The protocol effectively ceased operations shortly after the exploit, unable to recover from the drained treasury and the loss of user confidence.

Years later, in a significant development, the individual responsible, Shakeeb Ahmed, was identified and charged by U.S. authorities. He subsequently pleaded guilty to computer fraud in December 2023, admitting to the Nirvana Finance hack (among others). As part of his plea agreement, he agreed to forfeit a significant amount of cryptocurrency, including funds related to the Nirvana exploit. In June 2024, approximately $2.6 million in cryptocurrency stolen from Nirvana was reported to have been returned to the victim protocol as a result of these legal proceedings, a rare instance of substantial fund recovery in a DeFi hack.

### 5. Lessons learnt

The Nirvana Finance exploit provided several crucial lessons for the DeFi space:

* **The Perils of Flawed Price Oracles:** The exploit was a clear demonstration of how vulnerabilities in price oracles, especially those based on on-chain trading data without external validation or safeguards against manipulation, can be exploited with flash loans. Protocols must implement robust and decentralized oracle solutions that are resistant to manipulation by large, sudden trades.
* **Flash Loans as an Attack Vector:** This case further highlighted the risk posed by flash loans when combined with smart contract vulnerabilities. Protocols need to be designed to be resilient against attacks that utilize temporarily available large sums of capital.
* **Algorithmic Stability Mechanism Risks:** Protocols relying on complex algorithmic mechanisms for token pricing and stability must thoroughly stress-test these algorithms against various attack scenarios, including price manipulation.
* **The Importance of Security Audits and Bug bounties:** While audits are common, they are not foolproof. Continuous security review, formal verification, and substantial bug bounty programs can help identify vulnerabilities before they are exploited in the wild.
* **Law Enforcement's Growing Role:** The successful identification and prosecution of the attacker, leading to the return of a significant portion of funds years later, signals the increasing involvement and capability of law enforcement in the crypto space.
* **The Devastating Impact of Treasury Drain:** For many DeFi protocols, the treasury is critical for operations, development, and backing token value. A complete or near-complete drain can be an existential event.

### 6. Conclusion

The Nirvana Finance exploit of July 2022 was a damaging incident caused by a flash loan-assisted price manipulation attack that exploited a vulnerability in the protocol's ANA token pricing mechanism. The attack led to the loss of approximately $3.5 million, the collapse of the ANA token price, and ultimately the shutdown of the protocol. While initial attempts to negotiate with the attacker were unsuccessful, the later identification, prosecution, and guilty plea of Shakeeb Ahmed, resulting in the recovery of a significant portion of the stolen funds, underscore the evolving landscape of DeFi security and accountability. The exploit serves as a critical case study on the importance of secure oracle design, flash loan attack mitigation, and the potential for law enforcement to pursue perpetrators of DeFi crime.
""") 