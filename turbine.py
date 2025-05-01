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

    st.image("images/turbine.jpeg")  

    st.markdown("""
# :blue[Solana’s Turbine Block-Propagation Bug (Dec 4, 2020)]

## :red[1. A Brief Description of the Protocol]

Solana is a high-performance, permissionless blockchain designed for scalable decentralized applications. It uses a unique Proof-of-History (PoH) consensus combined with a Tower BFT protocol to achieve high throughput. A key innovation in Solana is **Turbine**, a block propagation protocol that helps distribute data quickly across nodes by breaking blocks into smaller packets and transmitting them in a tree-like structure.

---
                
## :orange[2. Exploit Summary]

On **December 4, 2020**, Solana experienced a **network-wide outage** due to a critical bug in its Turbine block propagation protocol. 

The chain began producing invalid blocks, causing validators to stop progressing. Here's a breakdown of the sequence:

- **:green[Early Dec 4, 2020:]** Validators began reporting synchronization issues. Nodes could no longer agree on the correct block, and consensus stalled.

- **:orange[Shortly After:]** The core team identified that the **block propagation system (Turbine)** had malfunctioned, leading to the dissemination of malformed blocks.

- **:green[Emergency Coordination:]** Validators and Solana Labs engineers coordinated via private communication channels and public Discord to assess the damage.

- **:orange[Chain Halt:]** Solana halted block production for approximately 6 hours.

- **:green[Recovery:]** The core team released a patch to fix the bug and coordinated a **manual restart** of the network with validator participation.

While no funds were stolen or contracts exploited, the bug **undermined confidence in Solana’s ability to maintain liveness** under edge conditions.

The exploit narrative wasn’t a direct "funds stolen" attack, but rather a critical **network failure** stemming from a bug in Solana's core propagation mechanism.

---
""")
    


    csva = pd.read_csv("csv_files/turbine/duration.csv")
    csvb = pd.read_csv("csv_files/turbine/hourly.csv")

    col_1, col_2 = st.columns([1,2], gap='large')
    with col_1:
        # --- Replace st.metric with custom HTML markdown ---
        label1 = "DURATION (HOURS)"
        value1 = f"Over {millify(csva['NULL_HOUR_COUNT'][0])} hrs"
        render_metric_box(label1, value1)

        st.markdown("""
                    #### These charts show the downtime, it is seen that Solana was down for over four hours. 
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

Solana's Turbine protocol is inspired by BitTorrent and designed for fast, efficient block propagation. It breaks each block into small packets, disseminated across validator nodes in a hierarchical structure.

The **root cause** of the bug was related to **malformed packets** being sent during the propagation process. Specifically:

- **:green[Block shred creation logic contained a flaw:]** A bug in the Turbine block shred creation logic introduced **invalid shreds** (small parts of blocks).

- **:orange[Invalid or inconsistent shreds:]** These were seen as incomplete or malformed by validators, which led to failure in reconstructing full blocks.

- **:green[Consensus stalled due to disagreement:]** Validators could not agree on the validity of blocks, halting progress.

- **:orange[Tower BFT halted voting:]** The Tower BFT system froze to avoid pushing invalid state forward.

**Impact:**

- **:green[6-hour chain halt:]** No blocks were produced during this time.

- **:orange[Transaction freeze:]** All smart contract executions and token transfers were paused.

- **:green[Validator intervention was required:]** Manual coordination and restart steps were necessary to resume operations.

- **:orange[No loss of funds:]** Despite the downtime, user assets remained secure.
                
---

## :blue[4. Protocol Response and Aftermath]

Solana Labs responded rapidly with the following actions:

- **:green[Bug Patch Released:]** A fix was issued to correct the shred creation logic error.

- **:orange[Validator Coordination Enabled Restart:]** Solana Labs coordinated with validators for a safe and orderly network reboot.

- **:green[Post-Mortem Published:]** The team published a transparent breakdown of the event and fix.

- **:orange[Testing Infrastructure Improved:]** Updates were made to include more robust stress tests for Turbine and other consensus-critical components.

- **:green[Community Confidence Restored:]** The fast and transparent response helped maintain user and validator trust.
                
---

## :violet[5. Lessons Learnt]

- **:green[Robust Testing:]** Protocol components like Turbine need exhaustive testing under adversarial and edge-case scenarios.

- **:orange[Resilience Engineering:]** Critical systems should be designed to degrade gracefully rather than fail completely.

- **:green[Validator Communication:]** Strong coordination mechanisms are essential for handling outages in real-time.

- **:orange[Automated Recovery:]** Introducing systems for automated recovery or fallback consensus modes could reduce downtime.

- **:green[Transparency:]** Public post-mortems build trust and demonstrate accountability in Web3 protocols.
                
---

## :red[6. Conclusion]

The Turbine block-propagation bug was an early, critical test of Solana’s architecture. While no funds were lost, the incident halted network activity and exposed vulnerabilities in block dissemination logic. Solana Labs’ quick response, transparent communication, and rapid fix were commendable and contributed to the network’s growing maturity.

The incident served as a powerful reminder that:

- **:green[Core infrastructure must be rigorously tested.]**  
- **:orange[Failover and recovery systems should be embedded.]**  
- **:green[Validator coordination is critical in decentralized systems.]**  
- **:orange[Early-stage protocols must over-communicate with their communities.]**  
""")
