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

    st.image("images/validator.jpeg")

    st.markdown("""

# :blue[Solana Large Block Turbine Incident – February 2023]

## :red[1. A Brief Description of the Protocol]

Solana is a high-performance blockchain platform designed for fast, low-cost decentralized applications. It employs a novel consensus mechanism known as Proof of History (PoH) in conjunction with a Turbine-based block propagation protocol that helps scale throughput. Turbine is Solana’s block propagation system that breaks blocks into smaller packets (shreds) and transmits them through a tree-like structure to validators.

- Attacker's Wallet Address: **:orange[Not applicable – incident caused by validator misconfiguration]**

---

## :orange[2. Exploit Summary]

On February 25, 2023, the Solana network experienced a major outage lasting nearly **19 hours** due to a malfunction in a validator's custom shred-forwarding service. Here's a high-level sequence of what unfolded:

- **An improperly configured validator** began producing an exceptionally large block—nearly 150,000 shreds, far exceeding normal sizes.
- This massive data payload overwhelmed the deduplication logic in Turbine’s shred-forwarding pipeline.
- The data began to loop within the Turbine tree, leading to widespread retransmission of redundant data.
- As more leaders came online and continued block production, the problem snowballed.
- Eventually, the network's normal transmission mechanism failed, forcing block data to be delivered via the slower fallback **Block Repair** protocol.
- During this degraded state, new block leaders automatically entered **vote-only mode**, excluding economic transactions to preserve minimal consensus functionality.
- After hours of network degradation and failed recovery attempts, a **manual restart** of the network was initiated using the last stable validator software.

---
                
""")
    


    csva = pd.read_csv("csv_files/large/duration.csv")
    csvb = pd.read_csv("csv_files/large/hourly.csv")

    col_1, col_2 = st.columns([1,2], gap='large')
    with col_1:
        # --- Replace st.metric with custom HTML markdown ---
        label1 = "DURATION (HOURS)"
        value1 = f"Over {millify(csva['DURATION'][0])} hrs"
        render_metric_box(label1, value1)

        st.markdown("""
                    #### These charts show the downtime, it is seen that Solana was down for over nineteen hours. 
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

At the core of the outage was a **failure in the deduplication logic** in the shred-forwarding services, which are responsible for relaying block data (shreds) across the validator network. Here's a detailed breakdown:

- A single validator, acting as a block producer during its slot, generated an **unusually large block** composed of roughly 150,000 shreds—several orders of magnitude larger than standard blocks.
- These shreds were forwarded through the network using a **custom shred-forwarding service**, bypassing normal safeguards.
- **Turbine’s deduplication filters**, meant to drop redundant shreds, became ineffective because they operate **downstream** of the shred-forwarding logic.
- As a result, the same shreds were continuously reforwarded, causing a **loop** within the propagation tree.
- The deduplication logic also lacked the necessary protections to prevent such internal looping, a weakness that had not been previously exploited or anticipated.
- As the network’s capacity became saturated, Turbine failed to propagate blocks effectively, and the network defaulted to the **Block Repair protocol**, a fallback method designed for limited emergency use.
- The chain continued in a degraded state until Solana core developers coordinated a **manual restart**, deploying validator versions with stronger deduplication logic and abort mechanisms for oversized blocks.

---

## :blue[4. Protocol Response and Aftermath]

Solana core developers responded with urgency:

- The network was **manually restarted** using a stable validator version, restoring normal operations.
- Two patched releases—**v1.13.7** and **v1.14.17**—were introduced to address the deduplication logic failure:
  - These updates included more **robust deduplication filters** to prevent shred looping and propagation saturation.
  - An additional patch forced **block producers to abort block production** if block sizes exceeded a threshold.
- The team conducted a **retrospective analysis** and began implementing a stricter filtering framework upstream in the shred-forwarding pipeline.
- The incident triggered renewed community debate around the **centralization of restart coordination** and transparency in validator misbehavior.

---

## :violet[5. Lessons Learnt]

- **:green[Validator Software Safety:]** Validators should avoid running custom or untested modifications, especially on critical systems like shred-forwarding.
  
- **:orange[Upstream Filtering Importance:]** Critical filters like deduplication should operate as early as possible in the data pipeline to prevent saturation before it spreads.
  
- **:green[Fail-Safes for Abnormal Behavior:]** The network must have abort mechanisms for anomalously large blocks or data floods.

- **:orange[Fallback Protocol Limits:]** Reliance on fallback protocols like Block Repair highlights the need for stronger default resilience.

- **:green[Transparent Communication:]** Real-time status and clear updates during outages help maintain trust with users and developers.

---

- **:green[Transparency:]** Protocols need to disclose upgrade authority models clearly to users.

---

## :red[6. Conclusion]

The February 2023 Large Block Turbine Incident was a **non-malicious but critical failure** rooted in misconfiguration and weaknesses in network-level data handling. While no funds were lost, the nearly 19-hour outage highlighted key fragilities in Solana’s block propagation logic. The swift protocol response, along with validator coordination and software patches, helped restore functionality and confidence. More importantly, the event has driven important changes in how Solana mitigates propagation failures, making the network more robust against similar future incidents.

""")
