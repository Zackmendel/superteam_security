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

    st.image("images/candy_nft.jpeg")

    st.markdown("""

# :blue[Candy Machine NFT Minting Spam Exploit (April–May 2022)]

## :red[1. A Brief Description of the Protocol]

Candy Machine is a Solana-based open-source tool developed by Metaplex that standardizes and streamlines NFT minting. It’s widely used by creators and developers to facilitate fair and verifiable NFT launches, often powering high-demand drops from projects like DeGods and Okay Bears.

---

## :orange[2. Exploit Summary]

Between **late April and early May 2022**, the Solana network began experiencing intense congestion and intermittent outages. Investigations revealed that this disruption coincided with a **mass spam attack targeting the Candy Machine minting system**.

Here’s a story-style timeline of the attack:

- **:green[April 2022 – Growing NFT hype:]** Solana NFT launches using Candy Machine saw explosive growth. Popular mints drew massive attention and aggressive participation, with many users employing bots.

- **:orange[Late April – Attack escalation:]** Attackers deployed sophisticated bots to spam Candy Machine with **mint transactions**, rapidly submitting requests across multiple wallet addresses to flood the system.

- **:green[Network degradation:]** At the peak of the spam, Solana was handling over **4 million failed transactions per second**, the vast majority coming from Candy Machine mint attempts. Block producers couldn’t process genuine transactions fast enough.

- **:orange[April 30 – Network outage:]** The Solana mainnet-beta halted for **approximately 7 hours** due to validator failures. Bots were using **1–2 SOL per spam wallet**, and mint instructions lacked sufficient anti-spam controls.

- **:green[May 1 – Post-mortem reveals spam root:]** Metaplex identified Candy Machine as the vector and announced an immediate protocol-level update to harden its minting logic.

- **:orange[Over 1.5 million failed minting transactions were recorded, consuming vast compute and leading to economic and operational loss for users and the network.]**

The exploit narrative wasn’t a smart contract vulnerability in Candy Machine, but rather an **economic denial-of-service attack** where attackers used cheap spam transactions to cripple both the protocol and Solana itself.
                
---
                """)
    
    csva = pd.read_csv("csv_files/candy_machine/duration.csv")
    csvb = pd.read_csv("csv_files/candy_machine/hourly.csv")

    col_1, col_2 = st.columns([1,2], gap='large')
    with col_1:
        # --- Replace st.metric with custom HTML markdown ---
        label1 = "DURATION (HOURS)"
        value1 = f"Over {millify(csva['DURATION'][0])} hrs"
        render_metric_box(label1, value1)

        st.markdown("""
                    #### These charts show the downtime, it is seen that Solana was down for over two hours. 
                    ### :red[⚠️NOTE: chart is formatted on a hourly basis and minute discrepancies are not accounted for.]
""")

    with col_2:
        # csve_sorted = csve.sort_values(by="AMOUNT_USD")
        fig_2 = px.bar(
        csvb,
        x="TIMESPAN",
        y="TRANSACTION_COUNT",
        # color="SYMBOL",
        title="Hourly Transaction Count",
        height=500,
        )
        fig_2.update_traces(marker_color="#B7e493")

        fig_2.update_layout(hovermode="x unified")

        st.plotly_chart(fig_2, use_container_width=True)

    st.markdown("""
---
                """)
    




    
    st.markdown("""

## :green[3. Technical Analysis]

The Candy Machine spam exploit took advantage of **cheap and insufficiently restricted minting logic** that lacked protections against rapid, unauthenticated wallet access.

### Core technical issues:

- **:green[No rate limiting or wallet verification:]** Candy Machine allowed virtually unlimited mint attempts from any wallet without verification or signature throttling.

- **:orange[Bot-created wallets:]** Attackers deployed thousands of throwaway wallets to send mint instructions at high frequency.

- **:green[Low transaction costs:]** Solana’s low fees (a fraction of a cent) allowed economically viable spamming using just 1–2 SOL per wallet.

- **:orange[Lack of compute unit restrictions:]** Without enforced compute limits or fee prioritization, validators were swamped with low-quality transactions that filled blocks and delayed consensus.

### Impact:

- **:green[7-hour Solana outage on April 30–May 1.]**

- **:orange[User minting failures and NFT sale disruption.]**

- **:green[Credibility hit for Candy Machine and Solana’s reliability claims.]**

- **:orange[Increased user costs from failed or delayed transactions.]**

---
## :blue[4. Protocol Response and Aftermath]

Both Metaplex and Solana responded quickly after identifying Candy Machine as the source of transaction spam.

- **:green[Metaplex patched Candy Machine:]** A new feature called **“bot tax”** was implemented — failed mint transactions would be penalized by **burning a portion of the transaction SOL**, making spam economically unviable.

- **:orange[Core Solana upgrades:]** Developers proposed introducing **stake-weighted Quality-of-Service (QoS)**, **compute unit pricing**, and **fee markets** to help prioritize legitimate traffic.

- **:green[Validator coordination improved:]** Solana validator operators were updated on how to identify spam and coordinate restarts faster.

- **:orange[Transparency through post-mortems:]** Metaplex and Solana Foundation issued open technical retrospectives, rebuilding some community trust.

---
## :violet[5. Lessons Learnt]

- **:green[Rate-limiting is essential for high-demand dApps:]** Protocols must protect mint functions against bot swarms.

- **:orange[Low fees can enable economic exploits:]** Without cost to failure, attackers can overwhelm networks cheaply.

- **:green[Spam prevention must be built into core logic:]** Protocols need to embed circuit breakers and penalty systems from the start.

- **:orange[Community trust depends on rapid response and communication:]** Timely updates and fixes help retain user faith.

- **:green[Transparency:]** Protocols need to disclose upgrade authority models clearly to users.

---
## :red[6. Conclusion]

The Candy Machine minting spam attack didn’t exploit a contract bug or steal funds — instead, it used Solana’s **high throughput and low-cost model against itself**. 

It revealed that:
- **:green[Scalability without robust anti-spam mechanisms leads to fragility.]**

- **:orange[Open-access minting without economic deterrents invites bot abuse.]**

- **:green[Protocol-level changes like Metaplex’s bot tax are crucial.]**

- **:orange[Solana’s fee-less model needs smart incentives and limits to preserve network health.]**

In the end, the incident became a catalyst for serious protocol improvements across both Metaplex and Solana, strengthening the entire NFT and smart contract minting ecosystem.

""")
