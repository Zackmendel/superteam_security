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

# :blue[Mango Markets Exploit Report (October 11, 2022)]

## :red[1. A Brief Description of the Protocol]

Mango Markets is a decentralized exchange (DEX) and lending protocol built on the Solana blockchain. It allowed users to trade spot and perpetual futures and to lend and borrow various cryptocurrency assets. A key component of Mango Markets was its reliance on price oracles, which provided external market data to the protocol's smart contracts for purposes such as determining asset values for collateral and liquidations.

The individual identified and later convicted for orchestrating this exploit is **Avraham Eisenberg**. While specific wallet addresses directly initiating the manipulative trades might be numerous and complex due to the nature of the attack across different platforms, addresses associated with receiving the stolen funds were tracked as part of the subsequent investigations and legal proceedings. Some addresses linked to the movement of funds during and after the exploit have been publicly discussed in post-mortem analyses and court documents.

#### Attacker address = :green[yUJw9a2PyoqKkH47i4yEGf4WXomSHMiK7Lp29Xs2NqM]
---

## :orange[2. Exploit Summary]

On October 11, 2022, Mango Markets became the target of a calculated manipulation scheme that resulted in the draining of over $116 million in assets. The individual behind the attack, Avraham Eisenberg, did not exploit a typical smart contract bug but rather manipulated the market price of Mango's native token, MNGO, to benefit his positions on the platform.

The narrative of the attack unfolds as a high-stakes financial maneuver. Eisenberg first established significant positions on Mango Markets related to the MNGO token's perpetual futures. Then, in a rapid series of transactions across various exchanges that fed into Mango's price oracle, he artificially inflated the spot price of the relatively low-liquidity MNGO token. As Mango's oracle updated its price based on this manipulated data, Eisenberg's futures positions on Mango became extraordinarily valuable. Leveraging this inflated, albeit artificial, collateral value, he was able to borrow and withdraw nearly all the available assets from the Mango Markets protocol, effectively draining its treasury and user deposits. Following the incident, Eisenberg engaged with the Mango DAO, proposing terms for the return of a portion of the funds.

---

""")
    
    st.markdown("""
# :blue[On-chain Activity Analysis]
                
---
                
From our analysis, we discovered that the exploiter made initial transfer of ~5M USDC to Mango to cause a price surge after which he was able to make several borrows which in-turn enable him accumulate large profits which were withdrawn back to his wallet.
                
---
                """)
    

    csva = pd.read_csv("csv_files/mango/wallet_summary.csv")
    csvb = pd.read_csv("csv_files/mango/token_amount.csv")
    csvc = pd.read_csv("csv_files/mango/transfers_in.csv")
    csvd = pd.read_csv("csv_files/mango/swaps.csv")
    csve = pd.read_csv("csv_files/mango/transfers.csv")
    csvf = pd.read_csv("csv_files/mango/net_transfer.csv")
    csvg = pd.read_csv("csv_files/mango/price.csv")

    col_1, col_2 = st.columns([2, 1], gap='large')
    with col_1:
        fig_1 = px.area(
        csvg,
        x="DATE1",
        y="OPEN",
        color="TIMEFRAME",
        title="$ANA Daily Token Price",
        height=500,
        )

        fig_1.update_layout(hovermode="x unified")

        st.plotly_chart(fig_1, use_container_width=True)

    with col_2:
        # --- Replace st.metric with custom HTML markdown ---
        label1 = "Net Transfers - USD"
        value1 = millify(csvf["AMOUNT_USD"][0], precision=2)  # Use the millify value
        render_metric_box(label1, value1)

        st.markdown("""
    ---
                    """)


        # --- Replace st.metric with custom HTML markdown ---
        label1 = "Total Amount Sent to Hacker's Wallet - USD"
        value1 = millify(csve["AMOUNT_USD"][0], precision=2)  # Use the millify value
        render_metric_box(label1, value1)


    st.subheader("Exploiter's Wallet On-chain Summary")
    st.dataframe(csva, use_container_width=True, hide_index=True)


    st.markdown("""
---
                
### :blue[Attacker's Wallet History Summary:]

- Primary haul:

~$114M in tokens drained from Mango Markets via price manipulation and overcollateralized borrowing; assets included MSOL, USDC, SOBTC, SRM, MNGO, SOETH, AVAX, BNB, FTT, and others.
Key conversions:

- Initial ~5M USDC → MNGO, triggering a price surge.
    - MNGO price spike → enabled borrowing of:
    - ~50M+ USDC, 798K MSOL, 281 SOBTC, 2.35M SRM, and more.
    - 3.26M USDT → swapped → 3.26M USDC post-exploit.
    - MNGO ⇄ USDC back-and-forth between key wallets (BFkxdUwW17..., 5Q544fKr...) used to manipulate price.
- Mixing and Movement Strategy:

    - Multi-wallet splitting: Funds dispersed across ~6–8 Solana wallets in timed sequences.
    - Stablecoin & asset cycling: USDT ⇄ USDC, MSOL/AVAX/SOBTC → centralized consolidator wallet (9mM6NfXa...).
    - Post-theft layering: Large tranches moved over days to obscure provenance and consolidate gains.
    - Custodial staging: USDC outflows and asset clusters suggest positioning for off-ramping or laundering.

- Temporal Pattern:

    - T = 0–4 hrs (Oct 11): Initial exploit executed, MNGO inflated, protocol drained.
    - Intense swapping and asset drain between 22:26–23:30 UTC.
    - T + 12 hrs (Oct 12): Additional transfers (MNGO → new wallet).
    - T + 3 days (Oct 14): Asset consolidation to a new wallet (9mM6NfXa...) begins.
    - T + 4 days (Oct 15): Final bulk MSOL + MNGO routed into consolidator wallet.
A high-speed, capital-intensive manipulation exploit designed to inflate governance token price and extract liquidity from protocol reserves. Followed by deliberate post-exploit asset reshuffling, cross-token conversions, and wallet consolidation - all consistent with professional laundering tactics aimed at fragmenting, anonymizing, and securing the stolen funds for long-term concealment or exit.
                
""")

    


    st.markdown("""
## :green[3. Technical Analysis]

The Mango Markets exploit was a sophisticated price oracle manipulation attack, exploiting the protocol's reliance on external price feeds for a thinly traded asset.

**The Issue:** Mango Markets used a price oracle to determine the value of assets on its platform. This oracle aggregated price data from several external exchanges. The vulnerability lay not necessarily in the oracle mechanism itself being faulty in aggregating data, but in the fact that the MNGO token, being relatively illiquid compared to major cryptocurrencies, was susceptible to significant price swings if large buy orders were executed on the exchanges the oracle monitored. Mango's protocol then used this potentially manipulable price for critical functions like determining collateral value and borrowing power.

**The Exploit:** Avraham Eisenberg orchestrated the attack in several coordinated steps:

- **:green[1. Establishing Positions:]** Eisenberg opened large perpetual futures positions on Mango Markets betting on the price of MNGO.

- **:orange[2. Market Manipulation:]** Using significant capital (reportedly around $10 million in USDC), Eisenberg simultaneously executed a large volume of buy orders for the MNGO token on the external spot markets that fed into Mango's price oracle. Due to MNGO's low liquidity, these concentrated buy orders rapidly drove up its price on those exchanges.

- **:green[3. Oracle Update:]** Mango Markets' oracle, reflecting the sudden surge in MNGO's price on the external markets, updated the price feed on the protocol.

- **:orange[4. Inflating Collateral Value:]** This artificially inflated price was then used by Mango Markets to calculate the value of Eisenberg's MNGO-related perpetual futures positions on the platform. These positions, based on the manipulated price, now appeared vastly more valuable than their true market worth.

- **:green[5. Borrowing and Withdrawal:]** With his collateral value artificially inflated, Eisenberg was able to borrow and withdraw a massive amount of other assets (primarily stablecoins like USDC, as well as SOL, mSOL, etc.) from Mango Markets' lending pools. These borrowed assets effectively came from the deposits of other users and the protocol's treasury.

- **:orange[6. Net Profit:]** Eisenberg repaid his initial flash loan (if one was used to acquire the initial capital, though reports suggest he used his own funds to some extent) and was left with the large amount of borrowed assets, while leaving his highly valued but illiquid MNGO perpetual futures positions as collateral, which subsequently plummeted in value.

**Impact:** The exploit resulted in a loss of approximately $116 million worth of various cryptocurrencies from the Mango Markets protocol, effectively draining its available liquidity and leaving the protocol with significant "bad debt" in the form of the devalued MNGO collateral. This caused substantial losses for other users who had deposited funds into the lending pools.

---

                
""")
    

    # ---------------------------------------------------------------------------------------------------------------
    st.subheader("Exploiter Transfer Timeline")
    
    col_1, col_2 = st.columns([1, 1], gap='large')
    with col_1:
        csvc = csvc.dropna(subset=["AMOUNT_USD"])

        fig_1 = px.scatter(
        csvc,
        x="TIMESPAN",
        y="AMOUNT_USD",
        size="AMOUNT_USD",  # 🔥 Scale marker size
        # color="ROUTE",
        title="Transfer Amounts By Exploiter(USD)",
        height=500,
        )

        fig_1.update_layout(hovermode="x unified")

        st.plotly_chart(fig_1, use_container_width=True)

    with col_2:
        csve_grouped = csvb.groupby("SYMBOL", as_index=False).agg({
            "AMOUNT_USD": "sum"
        })
        # csve_sorted = csve.sort_values(by="AMOUNT_USD")
        fig_2 = px.bar(
        csve_grouped,
        x="SYMBOL",
        y="AMOUNT_USD",
        color="SYMBOL",
        title="Tokens Transferred by Exploiter",
        height=500,
        )

        fig_2.update_layout(hovermode="x unified")

        st.plotly_chart(fig_2, use_container_width=True)
    

    # ---------------------------------------------------------------------------------------------------------------

    st.subheader("Hacker's Swap Timeline")
    
    col_1, col_2 = st.columns([1, 0.5], gap='large')
    with col_1:
        fig_1 = px.scatter(
        csvd,
        x="BLOCK_TIMESTAMP",
        y="AMOUNT_USD",
        size="AMOUNT_USD",  # 🔥 Scale marker size
        color="ROUTE",
        title="Swap Amounts By Exploiter(USD)",
        height=500,
        size_max=40  # optional: max bubble size in pixels
        )

        fig_1.update_layout(hovermode="x unified")

        st.plotly_chart(fig_1, use_container_width=True)

    with col_2:
        fig_2 = px.bar(
        csvb,
        x="SYMBOL",
        y="AMOUNT_USD",
        color="SYMBOL",
        title="Top Tokens Transferred",
        height=500,
        )
        # fig_2.update_traces(marker_color="#B7e493")

        fig_2.update_layout(hovermode="x unified")

        st.plotly_chart(fig_2, use_container_width=True)

    st.write("The attacker performed a couple of swaps, out of which the most noticeable was from USDC-SOL of about $23M in total.")



    st.markdown("""                
## :blue[4. Protocol Response and Aftermath]

Immediately after detecting the large, suspicious withdrawals, Mango Markets halted all withdrawals and deposits on the platform to prevent further losses. They publicly acknowledged the incident, stating it was due to "an oracle price manipulation."

In a highly unusual move, Avraham Eisenberg engaged directly with the Mango DAO governance forum. He proposed a settlement agreement where he would return a portion of the stolen funds (around 67 million USD) in exchange for the DAO agreeing not to pursue criminal charges against him and allowing him to keep the remaining amount (around 47 million USD) as a "bug bounty" or profit from his trading strategy. This proposal was put to an on-chain governance vote. Controversially, Eisenberg himself used a significant portion of the MNGO tokens he had acquired or controlled through the exploit to vote in favor of his own proposal. Despite the ethical implications and concerns about governance under duress, the proposal passed, and Eisenberg returned approximately $67 million.

However, the situation did not end there. U.S. authorities launched investigations, leading to Avraham Eisenberg's arrest in Puerto Rico in December 2022. He was subsequently charged by the Department of Justice (DOJ), the Commodity Futures Trading Commission (CFTC), and the Securities and Exchange Commission (SEC) with various offenses, including market manipulation, commodities fraud, and wire fraud. In April 2024, Eisenberg was convicted on these charges after a jury trial, marking a significant case at the intersection of DeFi exploits and traditional legal systems. Mango Markets also initiated civil lawsuits against Eisenberg to recover the remaining funds. The protocol's operations were severely impacted by the exploit and the subsequent events.

---

## :violet[5. Lessons Learnt]

The Mango Markets exploit provided several critical lessons for the DeFi space:

- **:green[Oracle Security is Paramount:]** The exploit highlighted the extreme vulnerability of protocols that rely on price oracles, especially when those oracles are susceptible to manipulation through illiquid markets. Protocols must implement robust, decentralized, and manipulation-resistant oracle solutions, potentially incorporating mechanisms to detect and mitigate the impact of sudden, large price deviations or low trading volume.

- **:orange[Market Manipulation Risks in DeFi:]** This case demonstrated that even without a traditional smart contract bug, protocols can be exploited through market manipulation if their design allows for artificial price increases of assets used as collateral.

- **:green[Governance Under Duress is Problematic:]** The incident raised significant questions about the integrity and effectiveness of decentralized governance when a large portion of voting power is controlled by an exploiter who is dictating terms under duress. Mechanisms to prevent such scenarios or handle them more robustly are needed.

- **:orange[The Interplay of On-Chain and Off-Chain:]** The exploit and subsequent legal actions showed that on-chain activities have real-world legal consequences. While DeFi operates on blockchain, participants are still subject to traditional laws and regulations concerning fraud and market manipulation.

- **:green[Risk Management for Illiquid Assets:]** Protocols allowing the use of relatively illiquid assets as collateral need to implement stricter risk parameters, including higher collateralization ratios or limitations on borrowing against such assets, to mitigate the impact of price manipulation.

- **:orange[Incident Response and Communication:]** The immediate halting of operations and communication with users by Mango Markets were positive steps, but the handling of negotiations with the attacker through governance was highly controversial.

---

## :red[6. Conclusion]

The Mango Markets exploit on October 11, 2022, was a significant and complex incident of market manipulation orchestrated by Avraham Eisenberg. By exploiting the protocol's reliance on price oracles for the thinly traded MNGO token, Eisenberg artificially inflated its value and used this inflated collateral to drain approximately $116 million from the platform. The aftermath involved controversial on-chain governance negotiation and, notably, subsequent criminal and civil legal action against Eisenberg, resulting in his conviction. This exploit serves as a crucial case study illustrating the vulnerabilities at the intersection of decentralized finance protocols, external data feeds, market dynamics, and the increasing reach of traditional legal frameworks in addressing illicit activities in the crypto space. It underscored the urgent need for more robust oracle security, better risk management for illiquid assets, and more resilient governance mechanisms in DeFi protocols.

""")
