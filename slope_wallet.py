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

    st.image("images/slope_wallet.jpeg")  

    st.markdown("""

# :blue[Slope Wallet Exploit Report (August 2, 2022)]

## :red[1. A Brief Description of the Protocol]

Slope Wallet is a non-custodial cryptocurrency wallet primarily focused on the Solana ecosystem, offering mobile apps for iOS and Android, as well as a browser extension. It allows users to manage SOL, SPL tokens, NFTs, and interact with dApps. As a non-custodial wallet, users are solely responsible for their private keys or seed phrases.

Hacker Wallet 1: **:orange[Htp9MGP8Tig923ZFY7Qf2zzbMUmYneFRAhSp7vSg4wxV]**

Hacker Wallet 2: **:orange[CEzN7mqP9xoxn2HdyW6fjEJ73t7qaX9Rp2zyS6hb3iEu]**

Hacker Wallet 3: **:orange[5WwBYgQG6BdErM2nNNyUmQXfcUnB68b6kesxBywh1J3n]**

Hacker Wallet 4: **:orange[GeEccGJ9BEzVbVor1njkBCCiqXJbXVeDHaXDCrBDbmuy]**

---

## :orange[2. Exploit Summary]

On August 2, 2022, users of Slope Wallet and other Solana wallets began reporting unauthorized fund drains. Panic quickly spread as thousands of wallets were compromised in real time. Initial suspicions of a Solana blockchain exploit were later dismissed. The incident was traced back to the Slope Wallet app, which had a critical vulnerability in how it managed users’ private keys.

The exploit was not a direct attack on the Solana network, but rather a failure within Slope’s wallet infrastructure, exposing a large number of users to asset theft. Approximately 9,200 wallets were affected, and an estimated $4.1 million was drained.

The exploit narrative wasn’t a direct "funds stolen" attack through Serum’s existing contracts, but rather a critical loss of **trust and security** through potential control of Serum’s upgrade path.
                
---

""")


    csva = pd.read_csv("csv_files/slope/wallet_summary.csv")
    csvb = pd.read_csv("csv_files/slope/net_transfer_hacker.csv")
    csvc = pd.read_csv("csv_files/slope/amount_victim.csv")
    csvd = pd.read_csv("csv_files/slope/transfers_out.csv")
    csve = pd.read_csv("csv_files/slope/transfers_in.csv")
    csvf = pd.read_csv("csv_files/slope/net_transfer.csv")
    csvg = pd.read_csv("csv_files/slope/token_amount.csv")
    csvh = pd.read_csv("csv_files/slope/token_victim.csv")

    col_1, col_2, col_3 = st.columns(3, gap='large')
    with col_1:
        # --- Replace st.metric with custom HTML markdown ---
        label1 = "Net Transfers - USD"
        value1 = millify(csvf["NET_FLOW"][0], precision=2)  # Use the millify value
        render_metric_box(label1, value1)

    with col_2:
        # --- Replace st.metric with custom HTML markdown ---
        label1 = "Total Amount Sent to Hacker's Addresses - USD"
        value1 = millify(csvc["AMOUNT_USD"][0], precision=2)  # Use the millify value
        render_metric_box(label1, value1)


    with col_3:
         # --- Replace st.metric with custom HTML markdown ---
        label1 = "Total Victims of Slope Hack"
        value1 = millify(csvc["VICTIMS"][0], precision=2) # Use the millify value
        render_metric_box(label1, value1)

    csve_sorted = csvb.sort_values(by="NET_FLOW")
    fig_2 = px.bar(
    csve_sorted,
    x="LABELS",
    y="NET_FLOW",
    color="LABELS",
    title="Net Transfers on Each Hacker's Address",
    height=500,
    )
    fig_2.update_traces(marker_color="#B7e493")

    fig_2.update_layout(hovermode="x unified")

    st.plotly_chart(fig_2, use_container_width=True)

    st.markdown("""
---
                """)

    st.subheader("Exploiter's Wallet On-chain Summary")
    st.dataframe(csva, use_container_width=True, hide_index=True)




    st.markdown("""                                

## :green[3. Technical Analysis]

The vulnerability stemmed from Slope Wallet’s integration with a third-party error monitoring service—believed to be Sentry—which inadvertently captured and stored users’ private keys or seed phrases in plaintext.

- **:green[Private Key Exposure:]** When users generated or imported wallets in the Slope mobile app, their sensitive keys were transmitted as error logs to an external server.

- **:orange[Unauthorized Access:]** Attackers somehow accessed this server (method not definitively known), retrieving unencrypted private key data.

- **:green[Wallet Draining:]** Using the private keys, attackers signed transactions to systematically drain wallets of SOL, SPL tokens, and NFTs.

- **:orange[Impact:]** Roughly 9,200 wallets were affected with over $4.1M in assets stolen. Though the main attack vector was Slope’s misconfigured logging, not every affected wallet could be linked to that flaw alone.

---

""")
    

    st.markdown("""
# :blue[On-chain Analysis:]
                
From our analysis, we found that the amounts were transferred to the four wallets labeled above and wallet 1 received the most amount ~3.8M USD from 709 wallets, followed by address 2 with ~2.17M USD from 2,656 wallets, then wallet 3 with ~1.45M USD from 5,611 wallets and lastly wallet 4 with 294k USD from 6,960 wallets, giving a total of ~$7.71M from 10,687 wallets.
As at the time of writing this article, a total of 2.18M USD net transfers(balance) has been made in all the hacker's wallet with the most value stored in Hacker 1 wallet address.

---
    """)
    # ---------------------------------------------------------------------------------------------------------------
    st.subheader("TOP TOKENS TRANSFERRED TO HACKER'S ADDRESS")
    
    col_1, col_2 = st.columns(2, gap='large')
    with col_1:
        fig_2 = px.bar(
        csvg,
        x="SYMBOL",
        y="AMOUNT_USD",
        color="SYMBOL",
        title="Top Tokens Transferred by Amount - USD",
        height=500,
        )
        # fig_2.update_traces(marker_color="#B7e493")

        fig_2.update_layout(hovermode="x unified")

        st.plotly_chart(fig_2, use_container_width=True)

    with col_2:
        fig_2 = px.bar(
        csvh,
        x="SYMBOL",
        y="VICTIMS",
        color="SYMBOL",
        title="Top Tokens Transferred by Victims",
        height=500,
        )
        # fig_2.update_traces(marker_color="#B7e493")

        fig_2.update_layout(hovermode="x unified")

        st.plotly_chart(fig_2, use_container_width=True)

    st.markdown("""
---
                
USDC is seen to the most sent token from victim's wallets in terms of amount and in terms of victim count sending the tokens to the hacker's addresses, SOL is seen to be the most sent token.

--- 
                """)               


        # ---------------------------------------------------------------------------------------------------------------

    st.subheader("TRANSFERS INTO HACKER'S WALLETS")
    
    col_1, col_2 = st.columns([1, 0.8], gap='large')
    with col_1:
        fig_1 = px.scatter(
        csve,
        x="TIMESPAN",
        y="AMOUNT_USD",
        size="AMOUNT_USD",  # 🔥 Scale marker size
        color="LABELS",
        title="Hourly Amount Sent to Hacker's Wallets - USD",
        height=500,
        size_max=40  # optional: max bubble size in pixels
        )

        fig_1.update_layout(hovermode="x unified")

        st.plotly_chart(fig_1, use_container_width=True)

    with col_2:
        csve_grouped = csve.groupby("LABELS", as_index=False).agg({
            "AMOUNT_USD": "sum",
            "VICTIMS": "sum"
        })
        # # csve_sorted = csve.sort_values(by="AMOUNT_USD")
    
        fig_2 = go.Figure()

        # Bar chart (USD value on left axis)
        fig_2.add_trace(go.Bar(
            x=csve_grouped["LABELS"],
            y=csve_grouped["AMOUNT_USD"],
            name="AMOUNT_USD",
            marker_color="lightskyblue",
            yaxis="y1"
        ))

        # Line chart (Raw token amount on right axis)
        fig_2.add_trace(go.Scatter(
            x=csve_grouped["LABELS"],
            y=csve_grouped["VICTIMS"],
            name="VICTIMS",
            mode="lines+markers",
            line=dict(color="gold"),
            yaxis="y2"
        ))

        # Layout with updated y-axis formatting
        fig_2.update_layout(
            title="Amount Sent into Hacker's Wallets VS Victims",
            height=500,
            hovermode="x unified",
            xaxis=dict(title="LABELS"),
            yaxis=dict(
                title=dict(text="USD Value", font=dict(color="lightskyblue")),
                tickfont=dict(color="lightskyblue")
            ),
            yaxis2=dict(
                title=dict(text="Victims", font=dict(color="gold")),
                tickfont=dict(color="gold"),
                overlaying="y",
                side="right"
            )
        )

        st.plotly_chart(fig_2, use_container_width=True)



# ----------------------------------------------------------------------------------------------------------------

    st.subheader("TRANSFERS OUT OF HACKER'S WALLETS")
    
    col_1, col_2 = st.columns([1, 0.8], gap='large')
    with col_1:
        fig_1 = px.scatter(
        csvd,
        x="TIMESPAN",
        y="AMOUNT_USD",
        size="AMOUNT_USD",  # 🔥 Scale marker size
        color="LABELS",
        title="Hourly Amount Sent out of Hacker's Wallets - USD",
        height=500,
        size_max=40  # optional: max bubble size in pixels
        )

        fig_1.update_layout(hovermode="x unified")

        st.plotly_chart(fig_1, use_container_width=True)

    with col_2:
        csve_grouped = csvd.groupby("LABELS", as_index=False).agg({
            "AMOUNT_USD": "sum",
            "VICTIMS": "sum"
        })
        # # csve_sorted = csve.sort_values(by="AMOUNT_USD")
    
        fig_2 = go.Figure()

        # Bar chart (USD value on left axis)
        fig_2.add_trace(go.Bar(
            x=csve_grouped["LABELS"],
            y=csve_grouped["AMOUNT_USD"],
            name="AMOUNT_USD",
            marker_color="lightskyblue",
            yaxis="y1"
        ))

        # Line chart (Raw token amount on right axis)
        fig_2.add_trace(go.Scatter(
            x=csve_grouped["LABELS"],
            y=csve_grouped["VICTIMS"],
            name="VICTIMS",
            mode="lines+markers",
            line=dict(color="gold"),
            yaxis="y2"
        ))

        # Layout with updated y-axis formatting
        fig_2.update_layout(
            title="Amount Sent out of Hacker's Wallets VS Victims",
            height=500,
            hovermode="x unified",
            xaxis=dict(title="LABELS"),
            yaxis=dict(
                title=dict(text="USD Value", font=dict(color="lightskyblue")),
                tickfont=dict(color="lightskyblue")
            ),
            yaxis2=dict(
                title=dict(text="Victims", font=dict(color="gold")),
                tickfont=dict(color="gold"),
                overlaying="y",
                side="right"
            )
        )

        st.plotly_chart(fig_2, use_container_width=True)




    st.markdown("""  
---              

## :blue[4. Protocol Response and Aftermath]

The Slope team collaborated with the Solana Foundation and ecosystem security firms to investigate. Users were urged to abandon old wallets and migrate to new ones with fresh seed phrases.

- Slope acknowledged the Sentry misconfiguration in an official report.
- They patched the issue, removed the vulnerable code, and began implementing stricter security measures.
- Despite these efforts, the damage to their reputation was extensive.
- No widespread fund recovery was reported, and user trust in hot wallets within the Solana ecosystem took a significant hit.

---

## :violet[5. Lessons Learnt]

- **:green[Private Key Security is Paramount:]** Any exposure of seed phrases grants attackers full control—wallet security begins and ends with key custody.

- **:orange[Supply Chain Risk Awareness:]** Integrating third-party services without strict security scrutiny exposes critical vulnerabilities.

- **:green[Secure Development Lifecycle:]** Rigorous security testing, code audits, and configuration management are essential.

- **:orange[User Education:]** Users must understand wallet types, private key safety, and recovery best practices.

- **:green[Security Audits are Non-Negotiable:]** Independent audits help detect flaws before they’re exploited.

- **:orange[Hardware Wallets Recommended:]** For large holdings, cold storage offers superior protection over hot wallets.

- **:green[Transparency:]** Protocols must clearly disclose what data is collected and how third-party services are integrated.

---

## :red[6. Conclusion]

The Slope Wallet exploit was one of the most significant Web3 security breaches of 2022. Caused by a critical lapse in private key handling through a logging service, the exploit led to over $4 million in losses and damaged confidence in software wallets. The incident highlights the absolute importance of secure key management, cautious third-party integrations, and transparent development practices to safeguard user assets in the DeFi ecosystem.

""")
