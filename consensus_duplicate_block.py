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

    st.image("images/duplicate.jpeg")

    st.markdown("""


# :blue[Solana Duplicate Block (Fork) Bug – September 2022]

## :red[1. A Brief Description of the Protocol]

Solana is a high-performance Layer 1 blockchain known for its fast and scalable architecture, underpinned by its Proof of History and Tower BFT consensus. In September 2022, Solana experienced a critical consensus failure caused by a bug in its fork choice rules, which led to a network-wide halt.

---

## :orange[2. Exploit Summary]

On **September 30, 2022**, Solana’s network came to a halt for over **eight and a half hours** following a chain split caused by duplicate block production from a faulty validator. 

The chain began to experience issues when both the **primary** and **fallback** nodes of a validator became active simultaneously, using the same node identity. This led to the validator producing **duplicate blocks** for the same slots—initially unnoticed, as Solana was capable of resolving these forks normally.

However, the situation escalated when a **bug in the fork selection logic** prevented validators from recognizing the correct chain once a **fork conflict** occurred. One validator (G) saw only one version of a duplicated block and continued to build normally. Another validator (D), which detected both duplicate blocks, discarded them and began building its own chain from an earlier slot.

Once the fork led by validator G gained the majority of stake votes, validator D attempted to switch forks. However, a bug prevented the transition because the **common ancestor** of both forks (slot 5) had duplicate blocks. This inconsistency made it impossible for validator D to switch to the heaviest chain, resulting in a stalled network.

The exploit narrative wasn’t a direct "funds stolen" attack through Serum’s existing contracts, but rather a critical loss of **trust and security** through potential control of Serum’s upgrade path.

---
""")
    


    csva = pd.read_csv("csv_files/duplicate/duration.csv")
    csvb = pd.read_csv("csv_files/duplicate/hourly.csv")

    col_1, col_2 = st.columns([1,2], gap='large')
    with col_1:
        # --- Replace st.metric with custom HTML markdown ---
        label1 = "DURATION (HOURS)"
        value1 = f"Over {millify(csva['DURATION'][0])} hrs"
        render_metric_box(label1, value1)

        st.markdown("""
                    #### These charts show the downtime, it is seen that Solana was down for over eight hours. 
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

### Root Issue:

- **:green[Duplicate block generation:]** A validator’s main node and its backup node became active simultaneously, producing conflicting blocks for the same slot using the same node identity.
  
- **:orange[Consensus failure caused by fork logic bug:]** While Solana's fork resolution usually handles such forks by following the "heaviest fork" (the one with most votes), a flaw in fork choice logic meant validators couldn’t switch if the last voted slot matched the slot they wanted to revert to.

- **:green[Unrecoverable fork:]** The network became unrecoverable when validators failed to agree on a canonical fork. This was due to their inability to discard their local state and adopt the fork with majority consensus.

### Visual Example (as described):

- Validator C produces duplicate blocks at slots 5 through 8.
- Validator G extends a fork from slot 5 (seeing only one duplicate).
- Validator D sees both duplicates, discards them, and builds on slot 4.
- G's fork gains votes and becomes canonical.
- D cannot switch to G’s fork due to the fork choice bug (shared ancestor is duplicated).

### Impact:

- **:green[No funds lost.]**
- **:orange[8.5 hours of complete network downtime.]**
- **:green[Validator operations stalled.]**
- **:orange[Reputation impact for Solana’s reliability and uptime guarantees.]**

---

## :blue[4. Protocol Response and Aftermath]

- **:green[Core developers reviewed logs and replicated the issue.]**
  
- **:orange[A client patch was created:]** Fixes to the fork choice rules were developed and pushed to GitHub.
  
- **:green[Backported to release branches:]** The fix was merged into the master branch and backported across Solana’s active release versions.

- **:orange[Network was restarted from a known safe slot.]**

- **:green[Outage resolved and block production resumed after 8.5 hours.]**

---

## :violet[5. Lessons Learnt]

- **:green[Validator node identity enforcement is critical:]** Both primary and fallback nodes should never be active simultaneously under the same identity.

- **:orange[Fork choice logic must handle all edge cases, including duplicates at common ancestor slots:]**

- **:green[Fast detection of conflicting validator behavior could prevent prolonged issues:]**

- **:orange[Thorough testing of consensus failure modes is essential for production resilience:]**

---
- **:green[Transparency:]** Protocols need to disclose upgrade authority models clearly to users.

---

## :red[6. Conclusion]

The **Duplicate Block Bug** in September 2022 was a critical failure in Solana’s consensus logic, not an exploit by a malicious actor. While **no assets were lost**, the incident exposed the fragility of the protocol’s fork reconciliation mechanisms. Solana’s response in deploying a swift patch demonstrated its developer agility, but the incident reinforced the importance of:

- **:green[More rigorous fail-safe logic in consensus code.]**
- **:orange[Stricter validator behavior enforcement.]**
- **:green[Clearer recovery paths for consensus divergence events.]**

Solana has continued to evolve with improvements in validator coordination, but this incident remains a key lesson in the challenges of building performant, yet resilient, Layer 1 blockchains.

""")
