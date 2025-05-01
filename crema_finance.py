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

    st.image("images/crema_finance.jpeg")  

    st.markdown("""
  
# :blue[Crema Finance Exploit Report]

## :red[1. A Brief Description of the Protocol]

Crema Finance was a concentrated liquidity protocol built on the Solana blockchain. It aimed to improve capital efficiency for liquidity providers by allowing them to define narrow price ranges for their positions—a model known as Concentrated Liquidity Market Making (CLMM), which was seen as an evolution beyond traditional AMM mechanisms.

- Attacker's Wallet Address: **:orange[`Esmx2Q...` (Solana)]**, **:orange[`0x8021...` (Ethereum)]**

---

## :orange[2. Exploit Summary]

On July 2, 2022, Crema Finance suffered an exploit that resulted in a loss of approximately 8.8 million USD. The attacker used a flash loan from Solend and took advantage of a vulnerability in Crema's tick account fee calculation system. By introducing a fake tick account that bypassed proper validation checks, the exploiter manipulated the fee calculation mechanism to withdraw exaggerated fees from the protocol.

The attacker returned a majority of the funds in exchange for a $1.68 million white hat bounty after negotiation with the Crema team.

---
The exploit narrative wasn’t a direct "funds stolen" attack through Serum’s existing contracts, but rather a critical loss of **trust and security** through potential control of Serum’s upgrade path.
 
                """)
    

    csva = pd.read_csv("csv_files/crema_finance/wallet_summary.csv")
    csvb = pd.read_csv("csv_files/crema_finance/timediff.csv")
    csvc = pd.read_csv("csv_files/crema_finance/bridge.csv")
    csvd = pd.read_csv("csv_files/crema_finance/swaps.csv")
    csve = pd.read_csv("csv_files/crema_finance/transfers.csv")
    csvf = pd.read_csv("csv_files/crema_finance/net_transfer.csv")

    col_1, col_2, col_3 = st.columns(3, gap='large')
    with col_1:
        # --- Replace st.metric with custom HTML markdown ---
        label1 = "Token Stolen - USD"
        value1 = millify(csvf["AMOUNT_USD"][0], precision=2)  # Use the millify value
        render_metric_box(label1, value1)

    with col_2:
        # --- Replace st.metric with custom HTML markdown ---
        label1 = "Amount Bridged out - USD"
        value1 = millify(csvb["AMOUNT_USD"][0], precision=2)  # Use the millify value
        render_metric_box(label1, value1)


    with col_3:
         # --- Replace st.metric with custom HTML markdown ---
        label1 = "Time Diff Between Outbound Bridges"
        value1 = millify(csvb["TIME_DIFF"][0], precision=2) # Use the millify value
        render_metric_box(label1, value1)

    st.subheader("Exploiter's Wallet On-chain Summary")
    st.dataframe(csva, use_container_width=True, hide_index=True)
    

    with st.expander("Summarizing Wallet Activity"):
        st.markdown("""

## Summarizing Exploiter Wallet Activity (Crema Finance)

Based on the table above, a detailed summary of the exploiter's wallet activity reveals a series of transactions involving various cryptocurrencies over a period starting on 2022-07-02. The exploiter engaged in transfers, swaps, and bridging activities with multiple wallet addresses.

### Initial Activity (Around 2022-07-02 00:14 - 00:46):

The exploiter's initial activity involved relatively small amounts of various tokens, potentially for testing or reconnaissance.

* Transferred 0.01 MSOL and 0.01 SOL to the address `HS5GnRmXkeC8j2a6wJVaNhKNEbdrgeQJ1d3JL2x82g8Q`. These transfers were worth $0.33 USD each and occurred at 00:14:25.000.
* Transferred 0.01 SOL and 0.01 STSOL to `6kDhKM8rDR4DXvwUpao4UA6JtCZfooAgMhicePmUNeJu`, also worth $0.33 USD each, at 00:14:33.000.
* Later, transferred 1 SOL worth $32.85 USD to `EqLZKF1bwUWUzU5F21jDQMoK4HRx8wQpLt57jhP8LbKm`. Subsequently, 33.1 USDC worth $33.15 USD was transferred from this address, and the exploiter also swapped 1 SOL to 33.102978 USDC worth $32.97 USD at 00:16:04.000. This suggests an immediate conversion of SOL to USDC.
* Small transfers of 1 USDC and 1 USDT worth $1 USD each occurred involving the address `HsYb453638e4ZwykZj4PHNwFiXHauV9UuNL3mCmFkZzh` around 00:23:27.000.
* The exploiter also interacted with the address `3m15qNJDM5zydsYNJzkFYXE7iGCVnkKz1mrmbawrDUAH`, transferring 1 USDCET and 1 USDC, and swapping 1 USDC to 1.000025 USDCET around 00:46:04.000.

### Later Activity with 0 Value Transfers (Around 2022-07-02 01:44 - 21:32):

A significant portion of the logs shows repeated transfers of 0 MSOL, 0 PAI, 0 USDH, and 0 STSOL to various addresses, notably `HS5GnRmXkeC8j2a6wJVaNhKNEbdrgeQJ1d3JL2x82g8Q` and `HRWwcA1VZnG9r2k9BHpR3PjbYuK9qUmcqrEWrhc9je5W`, as well as `6kDhKM8rDR4DXvwUpao4UA6JtCZfooAgMhicePmUNeJu`. The purpose of these zero-value transfers is not evident from the provided data.

### Significant Value Transfers and Swaps (Around 2022-07-02 20:08 onwards):

The exploiter then engaged in transactions involving substantial amounts:

* Large transfers of PAI tokens involving addresses `HRWwcA1VZnG9r2k9BHpR3PjbYuK9qUmcqrEWrhc9je5W` and `Ej4KxxUz73edQzjfsPVWvYxT5eyhQoWoXpo7BYm2Ejhj` occurred around 20:08:52.000. These transfers involved amounts like 840001 PAI (worth $838660.8 USD) and 842520 PAI (worth $841175.77 USD), suggesting a large-scale movement of this token. There were also smaller transfers of USDC from `HRWwcA1VZnG9r2k9BHpR3PjbYuK9qUmcqrEWrhc9je5W` during this time.
* Later, starting around 22:10:14.000, the exploiter was involved in transactions with MSOL and STSOL, interacting with addresses like `HS5GnRmXkeC8j2a6wJVaNhKNEbdrgeQJ1d3JL2x82g8Q`, `DdZR6zRFiUt4S5mg7AV1uKB2z1f1WzcNYCaTEEWPAuby`, and `6kDhKM8rDR4DXvwUpao4UA6JtCZfooAgMhicePmUNeJu`. These involved transfers of significant amounts of MSOL (e.g., 10500.01 MSOL worth $362894.68 USD) and STSOL (e.g., 57171 STSOL worth $1962179.65 USD), indicating a shift in focus to these tokens.
* Around 22:14:13.000, the exploiter interacted with `8eyi347MTDeH5F6eVv2qjPxVnU685FFZLDGcj5QWHZ6y`, transferring and swapping STSOL for SOL. A swap of 20651.17 STSOL to 21278.685402968 SOL worth $714012.94 USD was recorded.
* There was also significant activity involving USDT and ETH around 22:27:14.000, with a swap of 999999.92 USDT to 29354.399802781 SOL worth $1000501.63 USD and a transfer of 927.16 ETH worth $966265.86 USD. The exploiter interacted with addresses `5jmsB5Z1sfy2Fixy1TRRUXkrxtk5gmBGjuz16L1sQUZQ` and `GRiN6BiHeaa2wrFEpqzR397d6RqefCSRhnQVsVscwT3r` during these transactions.
* Further swaps and transfers involving USDC and SOL, and later USDCET, occurred around 22:28:23.000, involving addresses like `FG3z1H2BBsf5ekEAxSc1K6DERuAuiXpSdUGkYecQrP5v` and `GRiN6BiHeaa2wrFEpqzR397d6RqefCSRhnQVsVscwT3r`.
* Interactions with USDH started around 22:33:38.000, including swaps with MSOL involving addresses `H66xGa3c5wvg5ZGF7RCwskf52iH42C8u8v8TPwQXwc3m` and `AiMZS5U3JMvpdvsr1KeaMiS354Z1DeSg5XjA4yYRxtFf`.
* The exploiter also engaged in bridging activities involving USDCET. A notable outbound bridge of 997429.372578 USDCET worth $999201.52 USD occurred around 22:44:39.000, and another of 2367302.979352 USDCET worth $2371508.99 USD around 22:55:01.000. These indicate movement of assets to other chains or platforms.
* Further large swaps involving USDH and USDC were observed around 23:53:58.000.
* Towards the end of the logs, around 23:58:31.000 and continuing into the next day, the exploiter frequently swapped SOL to USDCET and interacted with addresses `F8Vyqk3unwxkXukZFQeYyGmFfTG3CAX4v24iyrjEYBJV` and `7XFMgfxhDURuaPwhUkXAy6uQJCoC3HPpjiZBqcot57Ge`. These transactions involved amounts around 10000 SOL being swapped for USDCET worth over $330,000 USD. More bridging of USDCET outbound is also recorded.

### In summary, the exploiter's wallet activity shows a pattern of:

* Initial small-scale testing or reconnaissance with various tokens.
* Large-scale manipulation or movement of specific tokens like PAI, MSOL, STSOL, USDT, ETH, and USDC.
* Active use of swaps to convert between different cryptocurrencies.
* Engagement in bridging activities, suggesting the movement of funds to other blockchain networks.
* Repeated zero-value transfers to certain addresses for an unknown purpose.
* Frequent interaction with a set of specific wallet addresses, likely involved in different stages of the exploitation or fund movement.
* A focus on SOL and its associated tokens (MSOL, STSOL) and stablecoins (USDC, USDT, USDCET, USDH) throughout the observed period.

The activity suggests a sophisticated operation involving the exploitation of vulnerabilities allowing for the acquisition of large amounts of various cryptocurrencies, followed by rapid conversion and movement of these funds across different platforms and potentially different blockchain ecosystems.
                    
""")

    st.markdown("""

## :green[3. Technical Analysis]

The vulnerability centered on Crema’s tick accounts, which stored crucial pricing data used in fee computation. Crema's system failed to adequately verify that the tick account being referenced in a transaction was authentic and belonged to the correct pool.

The attack sequence included:

- **:green[1. Create Fake Tick Account:]** The attacker initialized a tick account with manipulated data on Solana.

- **:orange[2. Obtain Flash Loan:]** A large uncollateralized flash loan was taken from Solend.

- **:green[3. Interact with CLMM Pool:]** The attacker interacted with Crema’s pool using the borrowed assets.

- **:orange[4. Spoof Tick Account:]** Instead of using the genuine tick account, the attacker substituted their own manipulated version.

- **:green[5. Claim Inflated Fees:]** The fake data led the protocol to overpay transaction fees to the attacker.

- **:orange[6. Repay Flash Loan:]** The borrowed funds were returned within the same atomic transaction.

- **:green[7. Withdraw and Bridge Remaining Funds:]** The illicit profits were swapped and bridged to Ethereum.

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

Immediately after the exploit was detected, Crema Finance paused smart contract operations and began investigating with blockchain security experts.

A rare negotiation followed: the team offered the attacker an $800,000 white hat bounty. The attacker accepted, ultimately returning approximately $8.3 million and retaining 45,455 SOL as a bounty.

Crema then initiated a user compensation plan and security overhaul. In July 2023, the U.S. Department of Justice arrested a former security engineer, Shakeeb Ahmed, in connection with the exploit.

---

## :violet[5. Lessons Learnt]

- **:green[Input Validation is Critical:]** Protocols must validate all external accounts, especially those impacting core functions like pricing or fees.

- **:orange[Flash Loans Amplify Exploits:]** Although not inherently malicious, flash loans enable attackers to maximize the damage from logic vulnerabilities.

- **:green[Security Reviews Must Be Continuous:]** One-off audits are not enough. Ongoing review and bug bounty programs are essential.

- **:orange[Protocol Complexity Increases Attack Surface:]** The intricacy of CLMM models introduces more opportunities for logical errors.

- **:green[Effective Incident Response Matters:]** Crema's ability to negotiate and limit losses shows the value of crisis planning.

- **:orange[Accountability is Possible:]** Legal action in the aftermath reaffirms that pseudonymity does not guarantee impunity.

---
- **:green[Transparency:]** Protocols should clearly communicate technical authority and potential risks to users.

---

## :red[6. Conclusion]

The Crema Finance exploit exposed critical flaws in tick account validation, enabling an attacker to manipulate internal logic and extract inflated fees using flash loans. Despite the initial loss of $8.8 million, most funds were returned via an unprecedented white hat negotiation. This incident reinforced the importance of robust validation, defensive programming, and clear communication protocols during crises. It also signaled growing legal consequences for DeFi exploits, potentially deterring future attackers.

""")
