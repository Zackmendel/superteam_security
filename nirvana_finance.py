import streamlit as st
import pandas as pd
from millify import millify
import plotly.express as px
import plotly.graph_objects as go


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

# :blue[Nirvana Finance Exploit Report (July 28, 2022)]

## :red[1. A Brief Description of the Protocol]

Nirvana Finance was a decentralized finance protocol on the Solana blockchain that featured a dual-token model: NIRV, a U.S. dollar stablecoin, and ANA, a yield-bearing asset designed with an algorithmically rising floor price. The protocol aimed to provide a stable store of wealth and sustainable yield through its unique mechanism.

The individual who later pleaded guilty to executing this exploit is **Shakeeb Ahmed**. Specific wallet addresses used in the execution and movement of funds have been tracked by investigators, but no single widely publicized primary attacker address is publicly associated.

---

## :orange[2. Exploit Summary]

The Nirvana Finance exploit occurred on July 28, 2022. It was a swift and devastating flash loan-assisted attack that drained the protocol's treasury of around $3.5 million.

The attacker used a flash loan to manipulate the reported price of ANA tokens via Nirvana’s flawed pricing mechanism. By artificially inflating ANA’s price through a large one-time purchase using borrowed capital, the attacker was able to sell ANA back to the protocol at the manipulated high price, realize profits in stablecoins, repay the flash loan, and walk away with the difference—all within a single transaction.

The exploit narrative was a classic flash loan price manipulation scheme that relied on weaknesses in Nirvana’s price oracle design.
                
---
                    
""")
    

    csva = pd.read_csv("csv_files/nirvana/wallet_summary.csv")
    csvb = pd.read_csv("csv_files/nirvana/timediff.csv")
    csvc = pd.read_csv("csv_files/nirvana/bridge.csv")
    csvd = pd.read_csv("csv_files/nirvana/swaps.csv")
    csve = pd.read_csv("csv_files/nirvana/transfers.csv")
    csvf = pd.read_csv("csv_files/nirvana/net_transfer.csv")
    csvg = pd.read_csv("csv_files/nirvana/price.csv")

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
        label1 = "Amount Bridged out - USD"
        value1 = millify(csvb["AMOUNT_USD"][0], precision=2)  # Use the millify value
        render_metric_box(label1, value1)


    st.subheader("Exploiter's Wallet On-chain Summary")
    st.dataframe(csva, use_container_width=True, hide_index=True)




    st.markdown("""
---
                
## :green[3. Technical Analysis]

The technical flaw in Nirvana Finance centered on its price oracle mechanism, which determined ANA’s price based on trade size and recent purchases without sufficient safeguards against manipulation.

- **Flash Loan:** The attacker borrowed approximately $10 million USDC, likely from Solend.
- **Price Manipulation Purchase:** The attacker used the flash loan to make a large ANA purchase, inflating ANA’s price in the protocol’s internal oracle.
- **Sell Back at Inflated Price:** The inflated ANA was sold back to the protocol for a large amount of stablecoins.
- **Loan Repayment:** A portion of the profit was used to repay the flash loan.
- **Profit Realization:** The attacker kept the remainder, draining $3.5 million from Nirvana’s treasury.

This exploit collapsed the ANA token’s price by over 80%, caused NIRV to lose its peg, and led to a total loss of trust in the protocol.

---
""")
    

      # ---------------------------------------------------------------------------------------------------------------
    st.subheader("Exploiter Bridge Timeline")
    
    col_1, col_2 = st.columns([1, 0.5], gap='large')
    with col_1:
        fig_1 = px.scatter(
        csvc,
        x="TIMESPAN",
        y="AMOUNT_USD",
        size="AMOUNT_USD",  # 🔥 Scale marker size
        color="DIRECTION",
        title="Bridge Amounts By Exploiter (ETH)",
        height=500,
        size_max=40  # optional: max bubble size in pixels
        )

        fig_1.update_layout(hovermode="x unified")

        st.plotly_chart(fig_1, use_container_width=True)

    with col_2:
        fig_2 = px.pie(
        csvc,
        names = "DIRECTION",
        values = "AMOUNT_USD",
        # color="DIRECTION",
        title="Bridge Amounts By Exploiter (ETH)",
        height=500,
        )

        fig_2.update_layout(hovermode="x unified")

        st.plotly_chart(fig_2, use_container_width=True)




        # ---------------------------------------------------------------------------------------------------------------

    st.subheader("Exploiter Swap Timeline")
    
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
        fig_2 = px.pie(
        csvd,
        names = "ROUTE",
        values = "AMOUNT_USD",
        # color="DIRECTION",
        title="Total Swap Amounts By Exploiter(USD)",
        height=500,
        )

        fig_2.update_layout(hovermode="x unified")

        st.plotly_chart(fig_2, use_container_width=True)

        # ---------------------------------------------------------------------------------------------------------------
    st.subheader("Exploiter Transfer Timeline")
    
    col_1, col_2, col_3 = st.columns([1.5, 1.2, 1], gap='small')
    with col_1:
        fig_1 = px.scatter(
        csve,
        x="BLOCK_TIMESTAMP",
        y="AMOUNT_USD",
        size="AMOUNT_USD",  # 🔥 Scale marker size
        color="ROUTE",
        title="Transfer Amounts By Exploiter(USD)",
        height=500,
        size_max=40  # optional: max bubble size in pixels
        )

        fig_1.update_layout(hovermode="x unified")

        st.plotly_chart(fig_1, use_container_width=True)

    with col_2:
        csve_grouped = csve.groupby("SYMBOL", as_index=False).agg({
            "AMOUNT_USD": "sum",
            "AMOUNT": "sum"
        })
        # # csve_sorted = csve.sort_values(by="AMOUNT_USD")
    
        fig_2 = go.Figure()

        # Bar chart (USD value on left axis)
        fig_2.add_trace(go.Bar(
            x=csve_grouped["SYMBOL"],
            y=csve_grouped["AMOUNT_USD"],
            name="AMOUNT_USD",
            marker_color="lightskyblue",
            yaxis="y1"
        ))

        # Line chart (Raw token amount on right axis)
        fig_2.add_trace(go.Scatter(
            x=csve_grouped["SYMBOL"],
            y=csve_grouped["AMOUNT"],
            name="AMOUNT",
            mode="lines+markers",
            line=dict(color="gold"),
            yaxis="y2"
        ))

        # Layout with updated y-axis formatting
        fig_2.update_layout(
            title="Tokens Transferred by Exploiter",
            height=500,
            hovermode="x unified",
            xaxis=dict(title="Token Symbol"),
            yaxis=dict(
                title=dict(text="USD Value", font=dict(color="lightskyblue")),
                tickfont=dict(color="lightskyblue")
            ),
            yaxis2=dict(
                title=dict(text="Raw Amount", font=dict(color="gold")),
                tickfont=dict(color="gold"),
                overlaying="y",
                side="right"
            )
        )

        st.plotly_chart(fig_2, use_container_width=True)

    with col_3:
        fig_3 = px.pie(
        csve,
        names = "ROUTE",
        values = "AMOUNT_USD",
        title="Transfer Amount by Direction",
        height=500,
        )

        fig_3.update_layout(hovermode="x unified")

        st.plotly_chart(fig_3, use_container_width=True)




    st.markdown("""
## :blue[4. Protocol Response and Aftermath]

Nirvana Finance quickly acknowledged the attack and paused operations. They publicly appealed to the hacker, offering a white-hat bounty between $300,000 and $600,000. However, the attacker demanded $1.4 million, and no deal was reached.

The protocol could not recover from the treasury loss and permanently shut down. 

In December 2023, U.S. authorities charged Shakeeb Ahmed, who pleaded guilty to the exploit. In June 2024, $2.6 million in cryptocurrency tied to the hack was returned to Nirvana as part of the legal resolution—one of the rare cases of successful recovery in DeFi exploits.

---

## :violet[5. Lessons Learnt]

- **:green[The Danger of Fragile Price Oracles:]** Internal pricing models without manipulation resistance are highly vulnerable to flash loan abuse.

- **:orange[Flash Loans as a Vector:]** Flash loans remain one of the most potent weapons in exploiting DeFi logic flaws.

- **:green[Stress Test Algorithmic Designs:]** Complex algorithmic stability mechanisms need to be simulated and audited under various manipulation scenarios.

- **:orange[Audits & Bounties Aren’t Optional:]** Continuous security reviews and incentivized bug disclosures are critical.

- **:green[Law Enforcement is Catching Up:]** The eventual arrest and prosecution of the attacker shows increasing regulatory oversight and forensic capability.

- **:orange[Treasury Drain is Often Fatal:]** Protocols must design risk management systems to prevent total treasury depletion.

- **:green[Transparency:]** Protocols need to disclose design assumptions, oracle mechanisms, and upgrade authority models clearly to users.

---

## :red[6. Conclusion]

The Nirvana Finance exploit of July 2022 was a textbook flash loan-assisted oracle manipulation attack. A flawed pricing mechanism allowed the attacker to drain $3.5 million in a single transaction. The exploit not only devastated Nirvana’s treasury but also destroyed user trust, causing the protocol to shut down. However, the story ended with a rare outcome—law enforcement identified and prosecuted the attacker, and a substantial portion of funds was recovered. This incident underscores the importance of oracle security, flash loan mitigation, transparent design, and the rising role of regulatory bodies in DeFi accountability.

""")
