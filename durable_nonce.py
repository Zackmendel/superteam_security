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

    st.image("images/durable.jpeg")

    st.markdown("""

# :blue[Solana Durable Nonce Bug Exploit (June 2022)]

## :red[1. A Brief Description of the Protocol]

Solana is a high-throughput, proof-of-history-based Layer 1 blockchain built for scalable decentralized applications. In June 2022, a bug related to its **Durable Nonce** mechanism — used to sign long-pending or delayed transactions — led to an unexpected **mainnet halt**.

---

## :orange[2. Exploit Summary]

In early June 2022, during routine operations involving Solana’s **Durable Nonce feature**, validators began rejecting a subset of transactions. These were valid transactions, but due to a bug in how the runtime handled **Durable Nonce signatures**, a discrepancy emerged between block-producing validators and those verifying the blocks.

This discrepancy wasn’t the result of a malicious attacker exploiting the chain, but rather a critical **consensus-failure bug** that could be triggered through otherwise legitimate transactions.

Here’s how the incident unfolded:

- **:green[June 1, 2022 – Transactions fail randomly:]** Solana validators noticed growing consensus failures related to specific Durable Nonce transactions. Some nodes rejected blocks, others accepted them.

- **:orange[June 1, ~16:30 UTC – Solana halts:]** As the mismatch persisted and validator agreement broke down, **block production halted** completely.

- **:green[Community coordination begins:]** Core developers, node operators, and validators gathered in real time to investigate. Discord channels became live incident rooms.

- **:orange[June 1, ~20:00 UTC – Cause identified:]** Engineers isolated the issue to Durable Nonce — a feature used to ensure transactions remain valid outside the 150-block window — which was broken in the v1.9 and v1.10 releases.

- **:green[Validators disable nonce usage and restart:]** A coordinated network restart was initiated using a patched version that temporarily disabled Durable Nonce support.

- **:orange[Total outage time: ~4.5 hours.]**

---
The exploit narrative wasn’t a direct "funds stolen" attack through Serum’s existing contracts, but rather a critical loss of **trust and security** through potential control of Serum’s upgrade path.

""")
    
    csva = pd.read_csv("csv_files/durable_nonce/duration.csv")
    csvb = pd.read_csv("csv_files/durable_nonce/hourly.csv")

    col_1, col_2 = st.columns([1,2], gap='large')
    with col_1:
        # --- Replace st.metric with custom HTML markdown ---
        label1 = "DURATION (HOURS)"
        value1 = f"Over {millify(csva['DURATION'][0])} hrs"
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

### What is Durable Nonce?

In Solana, a **nonce** is used to prevent a transaction from being replayed. Since standard nonces expire quickly (within ~2.5 minutes), Solana offers a Durable Nonce for transactions expected to take longer. This is often used in hardware wallets or multisig systems.

### The Bug:

- **:green[Incorrect signature verification:]** A bug introduced in Solana v1.9 caused the validator runtime to **treat Durable Nonce signatures differently between leaders and validators**.

- **:orange[Consensus divergence:]** When a leader produced a block containing a Durable Nonce transaction, validators couldn't verify it correctly and rejected the block.

- **:green[State desynchronization:]** Because block acceptance depends on signature validity, validators went out of sync — some accepting, others rejecting the same blocks.

- **:orange[Chain halted:]** With too few validators accepting leader blocks, block finalization stopped. Solana’s liveness broke — the chain could not move forward.

### Impact:

- **:green[No funds lost or stolen.]**

- **:orange[Block production halted for ~4.5 hours.]**

- **:green[Non-durable nonce transactions were unaffected.]**

- **:orange[Loss of user confidence in Solana’s reliability.]**

---
## :blue[4. Protocol Response and Aftermath]

- **:green[Quick incident response:]** Within hours, the Solana Foundation and developers diagnosed the Durable Nonce bug and coordinated a fix.

- **:orange[Validator restart coordination:]** Over 1,000 validators worked in sync to restart the network using a patched version (v1.10.23), temporarily **disabling Durable Nonce**.

- **:green[Bug patched and re-audited:]** The runtime code for nonce verification was re-reviewed, tested, and hardened.

- **:orange[Improved CI/CD and testing:]** The team implemented **stricter regression testing and multi-node fuzzing** to catch future consensus errors.

- **:green[Community transparency:]** The Solana Foundation published a detailed post-mortem and timeline, outlining next steps and prevention measures.

---
## :violet[5. Lessons Learnt]

- **:green[Consensus bugs are critical and must be isolated through multi-node testing:]**

- **:orange[Durable nonce handling must be deterministic across all node types:]**

- **:green[Open-source response coordination is a strength in decentralized ecosystems:]**

- **:orange[Quick and transparent communication builds community trust even during outages:]**

---
- **:green[Transparency:]** Protocols need to disclose upgrade authority models clearly to users.

---
## :red[6. Conclusion]

The **Durable Nonce bug** was not a malicious exploit, but it had **chain-level consequences**. It revealed:

- **:green[How even obscure features like nonces can lead to consensus divergence.]**

- **:orange[The importance of robust validator-client synchronization and test coverage.]**

- **:green[The benefit of community-driven incident response and rapid patching.]**

While no funds were lost, the network halt reminded users and developers that even fast and scalable blockchains like Solana must continuously balance performance with reliability and safety.

""")
