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

    st.image("images/grape.jpeg")  


    st.markdown("""

# :blue[Grape Protocol IDO DDoS Exploit (September 2021)]

## :red[1. A Brief Description of the Protocol]

Grape Protocol is a decentralized social networking infrastructure built on Solana. It offers tools for DAO management, gated community access, and decentralized identity. In September 2021, Grape Protocol launched its Initial DEX Offering (IDO) on the Solana-based launchpad **Raydium's AcceleRaytor** platform, aiming to raise funds by selling its native $GRAPE token to the public.

---

## :orange[2. Exploit Summary]

On **September 14, 2021**, Grape Protocol’s IDO was scheduled to go live on **Raydium’s AcceleRaytor**. Anticipation was high, and Solana users flooded the platform to participate. However, a **massive DDoS (Distributed Denial of Service)** attack overwhelmed the Solana network just minutes into the sale.

Here’s a time-series breakdown of events:

- **:green[Prior to IDO launch:]** Solana was handling a large volume of transactions with growing DeFi activity, but its mainnet-beta version lacked robustness against large-scale spam.

- **:orange[IDO launch time (Sep 14, 2021):]** A DDoS attack was launched using a swarm of bots submitting duplicate and spammed transactions to validator nodes.

- **:green[Validators overwhelmed:]** At peak, large TPS were submitted, far exceeding Solana’s real processing limit of ~65,000 TPS. Validators started falling out of consensus.

- **:orange[Network Halted:]** As the flood intensified, the chain became unstable and stopped producing blocks for **approximately 17 hours**.

- **:green[IDO disrupted:]** Many legitimate users couldn’t access Raydium to participate in the IDO. The token launch was effectively bottlenecked and disrupted.

- **:orange[Fallout:]** Grape’s fair token distribution was compromised, while Solana suffered a reputational hit as critics pointed out the failure of liveness during a high-demand period.

The exploit narrative wasn’t a direct "funds stolen" attack through Grape or Raydium’s contracts, but rather a critical blow to **network integrity and trust**, showcasing Solana’s vulnerability to spam-driven denial-of-service.

---
""")
    

    csva = pd.read_csv("csv_files/grape/duration.csv")
    csvb = pd.read_csv("csv_files/grape/hourly.csv")

    col_1, col_2 = st.columns([1,2], gap='large')
    with col_1:
        # --- Replace st.metric with custom HTML markdown ---
        label1 = "DURATION (HOURS)"
        value1 = f"Over {millify(csva['DURATION'][0])} hrs"
        render_metric_box(label1, value1)

        st.markdown("""
                    #### These charts show the downtime, it is seen that Solana was down for over ten hours. 
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

The root of the exploit was a combination of Solana’s **unoptimized transaction processing model** and the lack of robust DDoS protections.

- **:green[High-frequency bot spam:]** Attackers sent hundreds of thousands of duplicate transactions per second using bots that created meaningless arbitrage and transaction loops to saturate validator queues.

- **:orange[Turbine + Gulf Stream overloading:]** Solana’s block propagation (Turbine) and transaction forwarding system (Gulf Stream) broke down under the massive load, with unprocessed transactions filling validator memory buffers.

- **:green[Consensus stall:]** Validators began to desynchronize as they couldn’t vote on valid blocks, breaking Solana’s Tower BFT assumptions.

- **:orange[Manual intervention required:]** The chain had to be manually restarted by 80% of validators, a process that took over 17 hours.

**Impact:**

- **:green[IDO disruption:]** The $GRAPE token IDO failed to complete as intended, disadvantaging legitimate participants.

- **:orange[Solana halted:]** The chain was down for nearly a full day — one of the longest outages in its history.

- **:green[No smart contract breach:]** Neither Grape nor Raydium’s contracts were directly exploited.

- **:orange[Network liveness questioned:]** Solana’s claim of "censorship resistance and uptime" came under scrutiny.

---
## :blue[4. Protocol Response and Aftermath]

Solana and Grape responded swiftly following the disruption:

- **:green[Solana core devs coordinated reboot:]** Over 1,000 validators participated in manually restarting the chain from a safe block height.

- **:orange[Grape resumed token distribution later:]** Grape team ensured users who missed the IDO were still able to acquire $GRAPE via alternative methods, such as secondary markets.

- **:green[Network upgrade proposals initiated:]** Solana developers proposed improvements like priority fees, stake-weighted transaction prioritization, and better DDoS protections.

- **:orange[Community transparency:]** Solana Foundation and Grape issued public post-mortems outlining the root causes and corrective actions.

---
## :violet[5. Lessons Learnt]

- **:green[Scalability ≠ Resilience:]** Handling high TPS doesn't guarantee resistance to spam and denial-of-service attacks.

- **:orange[Validator load management:]** Validators need memory-efficient transaction buffers and backpressure mechanisms.

- **:green[Better transaction prioritization:]** Spam should be deprioritized in favor of economically meaningful transactions.

- **:orange[Emergency restart coordination:]** Decentralized networks must plan for fast, validator-led emergency recoveries.

- **:green[Transparency:]** Public communication during outages builds long-term community trust.

---
## :red[6. Conclusion]

The Grape Protocol IDO DDoS incident was a defining moment in Solana's early history. While not a contract-level exploit, it demonstrated how a poorly defended network layer can severely disrupt application-level performance.

Despite no financial losses or smart contract bugs, the attack:
- **:green[Shook trust in Solana’s reliability.]**
- **:orange[Highlighted the fragility of high-TPS chains without proper DDoS mitigation.]**
- **:green[Prompted valuable upgrades to Solana’s networking and mempool design.]**
- **:orange[Offered hard lessons in operational resilience for both dApps and L1 protocols.]**

The incident emphasized that network performance is as much about **resilience and recovery** as it is about **raw throughput**.

""")
