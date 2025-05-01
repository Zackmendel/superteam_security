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

    st.image("images/jit.jpeg")


    st.markdown("""

# :blue[Solana Infinite Recompile Loop Incident – February 2024]

## :red[1. A Brief Description of the Protocol]

Solana is a high-performance blockchain platform built for scalable decentralized applications. It uses a novel consensus mechanism—Proof of History (PoH)—and parallel smart contract execution powered by a Just-In-Time (JIT) compilation engine. Agave is the name for the validator client software that handles Solana’s transaction execution and state updates.

---

## :orange[2. Exploit Summary]

In February 2024, the Solana network experienced nearly **five hours of downtime** caused not by a malicious actor but by a **critical software bug** in the Agave validator's JIT caching system.

The incident unfolded as follows:

- The Agave validator introduced a new JIT caching layer called **ExecutorsCache** in v1.16, replacing the older **LoadedPrograms** system to improve performance.
- A validator processed a block containing a transaction that triggered a subtle bug in the **legacy loader logic**, causing a program to be infinitely recompiled on every slot iteration.
- Since over **95% of validators** were running Agave v1.17 (with the bug still active), the same buggy block propagated and caused **every validator** to enter an infinite loop.
- The network came to a halt as all nodes were caught in the same cycle of recompiling the same program without progressing.
- A fix had already been identified during a **Devnet outage investigation** the week prior, and a patch was scheduled.
- Following the mainnet halt, core developers executed a manual restart, **disabling the legacy loader** and applying a hotfix to stop the recompile loop.

---
                
                """)
    


    csva = pd.read_csv("csv_files/jit/duration.csv")
    csvb = pd.read_csv("csv_files/jit/hourly.csv")

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

The outage stemmed from a low-level failure in Agave’s program caching logic, introduced with ExecutorsCache in v1.16. Here’s how it occurred in detail:

- Solana’s JIT engine compiles on-chain programs for faster execution, caching their output to avoid redundant compilation.
- The legacy system, **LoadedPrograms**, tracked a program’s **effective slot height**—the slot at which the program becomes active—for cache validation.
- However, **legacy loader programs** lacked on-chain deployment slot data, so LoadedPrograms assigned them a sentinel height of **0**.
- When a legacy program was redeployed, LoadedPrograms inserted a temporary cache entry with a correct slot height. But since no transaction directly referenced it, the cache entry was soon evicted.
- Later, if a transaction invoked the same program, it was recompiled and cached again—but now with an effective height of **0**, lower than the previous unloaded entry.
- This tricked the system into **thinking the program wasn’t loaded**, causing it to **recompile it every time** it was accessed.
- Because Agave v1.16 did **not support cooperative loading**, the faulty transaction was allowed into a block and broadcasted to the cluster.
- The result: all validators replaying the block entered the same **infinite recompilation loop**, rendering the network inoperable.

---

## :blue[4. Protocol Response and Aftermath]

Solana core contributors responded rapidly to mitigate the incident:

- The network was halted and then **manually restarted** with a patched validator version.
- A previously planned patch—identified during a **Devnet postmortem**—was backported to **Agave v1.17**.
- A feature gate for the **legacy loader was removed**, completely disabling the deprecated loader and blocking any future triggers.
- Post-restart, the network resumed normal operations, and the incident accelerated internal efforts to **sunset legacy features** prone to state tracking inconsistencies.

---

## :violet[5. Lessons Learnt]

- **:green[Legacy Code Risk:]** Legacy features must be carefully isolated or deprecated as architectural changes are introduced.

- **:orange[Cooperative Loading Needed:]** Lack of cooperative program loading allowed a flawed transaction to propagate and halt the cluster.

- **:green[Testing on Devnet Isn’t Enough:]** Bugs previously seen in Devnet should be prioritized urgently for mainnet fixes, even if impact appears minimal.

- **:orange[Upgrade Synchronization Matters:]** Over 95% of validators ran the same version, reducing diversity and resilience to software faults.

---

- **:green[Transparency:]** Protocols need to disclose upgrade authority models clearly to users.

---

## :red[6. Conclusion]

The February 2024 Infinite Recompile Loop highlighted the fragility of low-level caching mechanisms when interacting with legacy systems. Although the incident was not due to a malicious exploit, it paralyzed the entire network for several hours due to a logic flaw in the Agave validator. Solana’s swift identification of the bug, rollback of legacy loaders, and deployment of fixes prevented recurrence. The event underscores the need for rigorous compatibility testing and layered fail-safes in blockchain execution engines to preserve liveness and security.

""")
