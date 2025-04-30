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

    st.image("images/cash.io.jpeg")  

    st.markdown("""
# Cashio (Saber Cash) Exploit Report

This report provides a detailed analysis of the Cashio (Saber Cash) exploit that occurred in March 2022 on the Solana blockchain.
                
### Exploiter wallet address: `6D7fgzpPZXtDB6Zqg3xRwfbohzerbytB2U5pFchnVuzw`

## 1. Brief Description of the Protocol

Cashio, also known as Saber Cash, was a decentralized stablecoin protocol built on the Solana network. Its native token, CASH, was designed to be fully backed by interest-bearing Saber USD liquidity provider (LP) tokens. Users could mint CASH by depositing approved collateral, primarily Saber LP tokens, into the protocol's smart contracts. The protocol consisted of different programs, notably "Bankman" for managing approved collateral and "Brrr" for handling the minting and burning of CASH tokens based on deposited collateral.

The attacker's primary wallet address on Solana associated with the exploit is reported as `6D7fgzpPZXtDB6Zqg3xRwfbohzerbytB2U5pFchnVuzw`. Funds were subsequently moved to other addresses, including on Ethereum.

## 2. Exploit Summary

The Cashio exploit, which resulted in a loss of approximately $52.8 million, was a classic "infinite mint" vulnerability executed in March 2022. The attacker identified a critical flaw in how the Cashio protocol verified the collateral used to mint CASH tokens.

The attack began with the exploiter creating a fake, valueless token and associated accounts on Solana. Leveraging the vulnerability, the attacker was able to trick the Cashio protocol's "Brrr" program into accepting this worthless token as valid collateral.

With the fake collateral accepted, the attacker proceeded to mint an enormous amount of CASH tokens – billions of them – without providing any real value as backing. This effectively created CASH tokens out of thin air.

Immediately after minting the unbacked CASH, the attacker moved swiftly to convert these worthless tokens into valuable assets. They swapped the newly minted CASH for legitimate stablecoins like USDC, USDT, and UST on the Saber decentralized exchange.

Following the swaps, the attacker began moving the stolen funds off the Solana network, with some assets being transferred to Ethereum via bridges like Wormhole and Paraswap, likely to further obscure the trail. In a peculiar turn, the attacker embedded a message in an Ethereum transaction, stating that accounts with less than $100k would have their funds returned and the rest would be donated to charity, though the extent of actual returns or donations remains unclear.
    
""")

    csva = pd.read_csv("csv_files/cash_io/wallet_summary.csv")
    csvb = pd.read_csv("csv_files/cash_io/timediff.csv")
    csvc = pd.read_csv("csv_files/cash_io/bridge.csv")
    csvd = pd.read_csv("csv_files/cash_io/swaps.csv")
    csve = pd.read_csv("csv_files/cash_io/transfers.csv")

    col_1, col_2 = st.columns(2, gap='large')
    with col_1:
        # --- Replace st.metric with custom HTML markdown ---
        label1 = "Token Stolen - USD"
        value1 = millify(csvb["AMOUNT_USD"][0], precision=2)  # Use the millify value
        render_metric_box(label1, value1)


    with col_2:
         # --- Replace st.metric with custom HTML markdown ---
        label1 = "Amount Sent Out To Ethereum - USD"
        value1 = millify(csvb["AMOUNT_USD"][1], precision=2) # Use the millify value
        render_metric_box(label1, value1)

    st.subheader("Exploiter's Wallet On-chain Summary")
    st.dataframe(csva, use_container_width=True, hide_index=True)

    with st.expander("Summarizing Wallet Activity"):
        st.markdown("""
## Detailed Exploiter Wallet Activity Log

The table provide a detailed log of the "Exploiter's" wallet activity, primarily consisting of transfers of various cryptocurrencies, along with some swaps and bridging events. The data includes the amount of cryptocurrency, its USD value at the time of the transaction, the source and destination wallets for transfers, the tokens involved in swaps, and the time elapsed since a previous recorded event.

Initially, the exploiter engaged in several high-value transfers and swaps. For instance, there are records of the exploiter transferring 16,405,366.67 USDC worth 16,404,909.84 USD and 17,041,006.5 USDC worth 17,040,531.98 USD. The exploiter also swapped 986,253,434.96 CASH to 17,041,006.502517 USDC worth 985,391,449.46 USD. Shortly after, a large amount of 986,253,434.96 CASH was transferred to multiple wallets, including `7K88AAbfSVHEZY87Ur3PrDhBYpwhKfTGxSWzMdh7XxUj` and `4ofEvMGQ87LFQ9aNw6pCDocFytWBH8BYqL7MwDKfQt1U`, each transfer worth 369,910,478.49 USD.

The exploiter also utilized bridging, moving assets across different blockchains. There are instances of the exploiter bridging 0.01 ETH outbound worth 28.35 USD, 1000 ETH outbound worth 2,975,880.74 USD, and 2618.3742 ETH outbound worth 7,791,969.35 USD. Additionally, the exploiter bridged 7,970,165.413595 USDCET outbound worth 7,974,109.58 USD and 29,196,154.704281 UST outbound worth 29,287,515.84 USD. Later, there are more ETH bridging activities, such as bridging 155.5995 ETH outbound worth 463,045.56 USD.

A significant portion of the logged activity involves numerous transfers of USDC to a large number of different wallet addresses. These transfers range in value from millions of USD down to less than a dollar. For example, the exploiter transferred 6,400,000 USDC worth 6,399,821.78 USD to `7XFMgfxhDURuaPwhUkXAy6uQJCoC3HPpjiZBqcot57Ge`, and also made many smaller transfers of USDC in the range of $100-$200 and even less. These smaller transfers are often separated by very short time intervals, frequently 0 minutes later.

Apart from USDC and ETH, the exploiter also engaged in transfers and swaps involving other cryptocurrencies like UST, SOL, and USDT. For example, there is a transfer of 0.1 SOL and swaps involving USDT for ETH. There are also transfers of CASH and USDCET.

The time gaps between recorded events vary significantly. Many transactions occur with 0 minutes later, indicating a rapid sequence of actions. However, there are also instances with longer delays, such as 1 day later, 12 minutes later, 3 minutes later, 5 minutes later, 8 minutes later, 17 minutes later, 7 minutes later, 4 minutes later, and 6 minutes later. One notable entry shows a transfer of 117.75 USDC to the same address 12 minutes later, suggesting a potential re-transfer or repeated action.

In summary, the exploiter's wallet activity began with high-value swaps and transfers of CASH and USDC, followed by bridging activities involving ETH and UST. A significant part of the activity then shifted to numerous USDC transfers of varying amounts to a large number of different addresses, often occurring in rapid succession. There were also transactions involving SOL, USDT, and USDCET. The time intervals between these activities ranged from immediate consecutive transactions to delays of several minutes or even a day.
""")


    st.markdown("""            
## 3. Technical Analysis

The root cause of the Cashio exploit was a critical missing validation check within the protocol's "Brrr" program, specifically in the logic designed to verify the deposited collateral. The "Brrr" program was responsible for ensuring that the tokens presented by a user as collateral were legitimate Saber LP tokens, which were the approved backing for CASH.

The vulnerability lay in the `validate` function for the `SaberSwapAccounts` structure used during the minting process. While the function performed several checks, it critically missed verifying that the `saber_swap.mint` account, which represented the collateral token being used, actually corresponded to a valid Saber Arrow (LP) token mint.

This oversight meant that the attacker could create *any* token with a valid Solana Program Library (SPL) token mint and present it to the Cashio protocol as if it were legitimate Saber LP collateral. The flawed validation logic would pass this fake token mint, allowing the attacker to proceed with the minting process.

The attacker exploited this by:
1.  Creating a new, worthless SPL token and associated accounts.
2.  Crafting a transaction that called the Cashio "Brrr" program's mint function.
3.  Providing their newly created worthless token as the "collateral" input.
4.  Due to the missing validation check, the "Brrr" program accepted the worthless token as valid collateral.
5.  The program then executed the minting logic, issuing billions of CASH tokens to the attacker's wallet without any real assets being locked.

The impact was devastating. The unbacked minting of CASH tokens devalued the stablecoin to near zero, causing significant losses for users holding CASH or providing liquidity in CASH pairs. The attacker was able to drain valuable assets from Saber's liquidity pools by swapping the fraudulently minted CASH, resulting in a total loss of approximately $52.8 million.
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

## 4. Protocol Response and Aftermath

In the immediate aftermath of the exploit, the value of the CASH stablecoin plummeted to virtually zero. The Cashio team acknowledged the hack and advised users to withdraw liquidity from any pools involving CASH.

The attacker's public message regarding potential partial returns for smaller holders and charity donations added a layer of unusual complexity to the situation. While some reports suggested limited returns might have occurred for small holders, a significant portion of the stolen funds remained unrecovered.

Efforts were made to trace the flow of the stolen assets, which were moved across different chains using bridges like Wormhole. However, tracing and recovering funds once dispersed and potentially sent through mixers is extremely challenging.

The Cashio project's activity significantly slowed down following the exploit. While there were discussions and announcements about plans for a new protocol to potentially help victims and rebuild, the long-term status and future of the Cashio project and these recovery plans remain largely unclear.

## 5. Lessons Learned

The Cashio exploit provided several critical lessons for the DeFi ecosystem, particularly on Solana:

* **The Absolute Necessity of Audits:** Cashio was reportedly never audited by a third party. This exploit is a stark reminder that unaudited or poorly audited smart contracts are high-risk and should be approached with extreme caution.
* **Robust Input Validation:** The core vulnerability stemmed from a simple but critical missing validation check. All inputs to a smart contract, especially those related to asset handling and minting, must be rigorously validated to prevent attackers from using malicious or fake data.
* **Complexity and Attack Surface:** Even seemingly simple operations like minting based on collateral can have complex underlying logic. Developers must be meticulous in accounting for all possible scenarios and external interactions.
* **Risks of New/Unaudited Protocols:** Users should be extremely cautious when interacting with new or unaudited DeFi protocols, especially those involving significant value. The promise of high yields often comes with higher, sometimes hidden, risks.
* **Importance of Community and Transparency:** While the attacker's message was unusual, the incident highlighted the importance of clear and timely communication from protocol teams during and after an exploit.

## 6. Conclusion

The Cashio exploit was a significant security breach on the Solana network, resulting in the loss of over $52 million due to an infinite mint vulnerability. The exploit was made possible by a fundamental flaw in the protocol's collateral validation logic, which failed to verify the legitimacy of the token used for minting CASH. The incident underscored the critical importance of rigorous smart contract security, comprehensive audits, and robust input validation in the rapidly evolving DeFi space. While the aftermath saw some unusual interactions from the attacker and efforts to trace funds, the majority of assets remained lost, serving as a potent reminder of the risks associated with unaudited and vulnerable protocols.
                
""")

    # You could add charts, images, or other Streamlit components here
    # st.image("path/to/mango_chart.png")
    # st.code("Example exploit code snippet (if relevant and safe to show)")

    st.write("---")  # Optional separator for end of custom content
    st.info("This is content loaded from the `wormhole_bridge.py` file.")