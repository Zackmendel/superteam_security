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

    st.image("images/wormhole_bridge.jpeg")  

    st.markdown("""
# Wormhole Bridge Exploit Report

This report details the Wormhole bridge exploit that occurred in February 2022, analyzing the attack, its technical underpinnings, the protocol's response, and the lessons learned.

### Exploiter wallet address: `CxegPrfn2ge5dNiQberUrQJkHCcimeR4VXkeawcFBBka`

## 1. Brief Description of the Protocol

Wormhole is a decentralized cross-chain bridge protocol that allows users to transfer tokens and data between different blockchain networks. It facilitates interoperability by locking assets on one chain and minting corresponding "wrapped" assets on another, or by relaying messages and data between chains. The protocol relies on a network of validators, known as "Guardians," to observe events on one chain and sign messages that attest to those events, allowing actions to be taken on another chain.

The attacker's wallet address involved in the exploit, based on the activity log provided, is associated with a series of transactions including large transfers, swaps, and bridging activities. Some of the initial large transfers of CASH and USDC, followed by bridging ETH and UST, and then numerous smaller USDC transfers, paint a picture of the attacker's movements post-exploit.

## 2. Exploit Summary

The Wormhole exploit unfolded like a high-stakes digital heist in early February 2022. It began when an attacker identified a critical vulnerability in the protocol's VAA (Validator Action Approval) verification process on the Solana side.

Acting swiftly, the exploiter initiated a series of transactions designed to trick the Wormhole protocol into releasing a massive amount of wrapped Ether (wETH) on the Solana network without the corresponding Ether being locked on the Ethereum network. The core of the attack involved forging a VAA message that falsely claimed a large deposit of ETH had been made on Ethereum, which the Solana side of the bridge then processed.

Once the forged VAA was accepted, the Wormhole contract on Solana minted 120,000 wETH for the attacker. This sudden influx of wETH, worth over $320 million at the time, was the primary target of the exploit.

Following the successful minting, the attacker's onchain activity, as detailed in the provided log, shows the subsequent steps taken to move and potentially launder the stolen funds. Initially, there were large transfers and swaps, including converting significant amounts of CASH to USDC. This was followed by bridging activities, moving assets like ETH and UST off the Solana network, likely to other chains to further obfuscate the trail. A notable phase involved numerous smaller transfers of USDC to a large number of different wallet addresses, often in rapid succession, potentially distributing funds or preparing them for further movement across the crypto ecosystem. These actions highlight the attacker's efforts to disperse the illicitly gained assets and make them harder to trace and recover.

The entire sequence, from the initial exploit to the subsequent movement of funds, occurred relatively quickly, demonstrating the attacker's preparedness and efficiency in executing the post-exploit strategy.

""")

    csva = pd.read_csv("csv_files/wormhole/wallet_summary.csv")
    csvb = pd.read_csv("csv_files/wormhole/timediff.csv")
    csvc = pd.read_csv("csv_files/wormhole/bridge.csv")
    csvd = pd.read_csv("csv_files/wormhole/swaps.csv")
    csve = pd.read_csv("csv_files/wormhole/transfers.csv")

    col_1, col_2 = st.columns(2, gap='large')
    with col_1:
        # --- Replace st.metric with custom HTML markdown ---
        label1 = "Token Stolen (WORMHOLE) - USD"
        value1 = millify(csvb["AMOUNT_USD"][0], precision=2)  # Use the millify value
        render_metric_box(label1, value1)


    with col_2:
         # --- Replace st.metric with custom HTML markdown ---
        label1 = "Amount Sent Out To Ethereum(WORMHOLE) - USD"
        value1 = millify(csvb["AMOUNT_USD"][1], precision=2) # Use the millify value
        render_metric_box(label1, value1)

    st.subheader("Exploiter's Wallet On-chain Summary")
    st.dataframe(csva, use_container_width=True, hide_index=True)

    with st.expander("Summarizing Wallet Activity"):
        st.markdown("""

Here’s a high‑level, phase‑by‑phase breakdown of the exploiter’s on‑chain movements following the Wormhole bridge hack:

### 1. Initial Bridge Activity on Ethereum (Minutes 0–181)

**Inflow:**
* **0 min:** Bridged in 0.1 ETH (~ $273)
* **181 min later:** Bridged in 120 000 ETH (≈ $328 M)

**Outflow:**
* **1 min after large inbound:** Bridged out 10 000 ETH (≈ $27 M)
* **2 min later:** Bridged out 80 000 ETH (≈ $219 M)
* **3 min later:** Bridged out 3 750 ETH (≈ $10.3 M)

⇒ **Net position on Ethereum after ~3 hrs:** Virtually entire 120 000 ETH siphoned out to Solana.

### 2. First Consolidation on Solana (Minutes 4–5)

* **From Solana gateway account GRiN6…VscwT3r:**
    * Received 9 370.72 ETH (~ $25.6 M) and 269 356.67 SOL (~ $28.9 M).
    * Sent back 26 250.1 ETH (~ $71.8 M) to itself (likely internal shuffling).
* **From second gateway FG3z1…QrP5v:**
    * Received 1 866.84 ETH (~ $5.1 M) and 18 044 852.11 USDC (~ $18.07 M).
    * Sent out 9 370.72 ETH (~ $25.6 M) back to the first gateway.

### 3. Stablecoin Swaps & SOL Conversion (Minutes 0–1 following consolidation)

**USDC → SOL swaps:**
* 18 044 852 USDC → 122 049 SOL (~ $18.1 M)
* 4 981 312 USDC → 41 254 SOL (~ $4.997 M)

These two swaps converted the bulk of stablecoins into over 163 000 SOL.

### 4. Long‑Term SOL Transfers and On‑Chain Layering

* **~346 days later:** Transferred 150 000 SOL (~ $3.32 M) to mixer‑style address BxnUi…C1my.
* **Same day:** From that address, splintered funds across USDC, USDT, USDCe, USDT e t al., and DAI—gradually converting SOL proceeds back into stablecoins and diversifying holdings.

### 5. Ongoing Micro‑Transfers & Mixing (Within 0–17 days after major SOL outflow)

* Repeated small transfers of SOL (e.g. 26 100 to 50 000 SOL) to multiple Solana addresses, each immediately swapped back into USDC.
* Cycling stablecoins between USDC, USDT, USDCe, USDT e t, and DAI across at least half a dozen recipient addresses (5Q544…, HJPjo…, 3m15q…, AuZrsp…, 7XFMgf… etc.).
* Final micro‑transfers of single‑digit ETH, STSOL, FRONK, etc., into controlled accounts—likely obfuscating any residual trace.
* **Last recorded move:** 213.58 USDT sent to EAUwik… 17 days later.

## Overall Takeaways

* **Primary haul:** 120 000 ETH ($328 M) bridged out, almost entirely routed to Solana.
* **Key conversions:**
    * ~18 M USDC & ~5 M USDC → ~163 000 SOL.
    * SOL proceeds (150 000 SOL initial tranche + numerous smaller chunks) converted back into dozens of stablecoin tranches.
* **Mixing strategy:** Large‑scale transfers into multiple custodial addresses, frequent small‑batch swaps, and cross‑asset fragmentation (ETH ⇄ SOL ⇄ USDC/USDT/DAI/USDCe/USDT e t).
* **Temporal pattern:**
    * **T = 0–4 min:** Rapid bridging and wallet‑to‑wallet shuffles.
    * **T = 4–181 min:** Bulk transfers and swaps.
    * **T = 346 days & T = 9–17 days:** Long‑term cash‑out and micro‑mixing transactions.

This pattern reflects a classic “smash‑and‑grab” exploit followed by aggressive layering and mixing to launder proceeds across chains.
""")


    st.markdown("""            
## 3. Technical Analysis

The root cause of the Wormhole exploit lay in a vulnerability within the logic that verified VAA messages on the Solana side of the bridge. VAAs are essentially signed messages from the Wormhole Guardians confirming an event on one chain (like a deposit). These VAAs are then used by the Wormhole contract on another chain to trigger a corresponding action (like minting wrapped tokens).

Specifically, the vulnerability was related to how the Solana core bridge contract handled the verification of guardian signatures on a VAA. The attacker found a way to bypass the signature verification check for a specific type of VAA, allowing them to craft and submit a malicious VAA that appeared legitimate to the Solana contract, even though it hadn't been signed by the required number of Guardians and no corresponding ETH deposit had occurred on Ethereum.

The malicious VAA claimed that 120,000 ETH had been deposited on the Ethereum side. Because the signature verification was bypassed, the Wormhole contract on Solana accepted this false claim as true. The contract then proceeded to execute the standard logic for a verified deposit: it minted 120,000 wrapped Ether (wETH) tokens and sent them to the attacker's specified Solana wallet address.

The impact was immediate and severe. The exploit resulted in the unauthorized minting of 120,000 wETH on Solana, valued at approximately $326 million at the time. This represented a significant loss for the Wormhole protocol and a major blow to confidence in cross-chain bridge security. The attacker gained control of a substantial amount of value without having locked any equivalent assets on the source chain, effectively draining the protocol's Solana wETH liquidity.
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
    
    col_1, col_2, col_3 = st.columns([1, 1, 1], gap='large')
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
        # csve_sorted = csve.sort_values(by="AMOUNT_USD")
        fig_2 = px.bar(
        csve_grouped,
        x="SYMBOL",
        y="AMOUNT_USD",
        color="SYMBOL",
        title="Tokens Transferred by Exploiter",
        height=500,
        )

        # Add Scatter plot
        fig_2.add_scatter(x=csve_grouped['SYMBOL'], y=csve_grouped['AMOUNT'], name="AMOUNT", line_color="yellow")

        fig_2.update_layout(hovermode="x unified")

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

The Wormhole team and community reacted swiftly upon discovering the exploit. Recognizing the severity of the situation and the need to prevent further damage and restore confidence, they took immediate steps:

* **Halting the Bridge:** The Wormhole team quickly took the bridge offline to prevent the attacker from exploiting the vulnerability further and to assess the full scope of the damage.

* **Investigation:** A rapid investigation was launched to understand the technical details of the exploit and identify the vulnerability.

* **Communication:** The team communicated openly with the community about the incident, providing updates on the situation and the steps being taken.

* **Vulnerability Patch:** The identified vulnerability was patched promptly to secure the protocol against similar attacks in the future.

* **Restoring Liquidity:** In a crucial move to maintain the peg of wETH on Solana and ensure users were not negatively impacted by the attacker's actions, Jump Crypto, a major contributor to the Wormhole project, stepped in and provided 120,000 ETH (worth approximately $325 million) to replenish the lost funds and back the wETH on Solana 1:1. This significant bailout was critical in stabilizing the situation and demonstrating commitment to the protocol's users.

* **Law Enforcement and Recovery Efforts:** Efforts were initiated to work with law enforcement and blockchain analytics firms to trace the stolen funds and explore potential recovery options.

The aftermath saw the Wormhole bridge successfully brought back online after the vulnerability was fixed and the liquidity was restored. While the incident was a major setback, the swift response and the substantial bailout by Jump Crypto helped to mitigate the long-term damage to the protocol's reputation and functionality, though it highlighted the inherent risks in cross-chain bridging.

## 5. Lessons Learned

The Wormhole exploit provided several critical lessons for the development and operation of cross-chain bridges and the broader DeFi ecosystem:

* **Security is Paramount:** The exploit underscored the absolute necessity of rigorous security audits, formal verification, and continuous monitoring for cross-chain protocols, which present a larger attack surface than single-chain applications.

* **VAA Verification is Critical:** The vulnerability highlighted the importance of robust and foolproof verification mechanisms for cross-chain messages (like VAAs). Any weakness in this process can be exploited to mint unauthorized assets.

* **Complexity Increases Risk:** Cross-chain bridges are inherently complex systems involving multiple blockchains and communication layers. This complexity increases the potential for vulnerabilities, emphasizing the need for simplicity and modularity where possible.

* **Centralization Risks in Decentralized Systems:** While Wormhole aims for decentralization, the role of Guardians and the potential for a vulnerability in their collective security or the verification process demonstrated that even seemingly decentralized systems can have centralized points of failure.

* **Importance of Incident Response:** The swift and decisive response from the Wormhole team and Jump Crypto was crucial in limiting the damage and restoring confidence. Having a well-defined incident response plan is vital for any critical infrastructure in the blockchain space.

* **The Cost of Interoperability:** The exploit served as a stark reminder of the significant financial risks associated with achieving interoperability between blockchains through bridging mechanisms. The large bailout highlighted the potential costs when security fails.

## 6. Conclusion

The Wormhole bridge exploit was one of the largest in DeFi history, resulting in the loss of over $320 million worth of wETH. The attack exploited a critical vulnerability in the VAA verification process on the Solana side of the bridge, allowing the attacker to mint unauthorized assets. The incident highlighted the significant security challenges inherent in cross-chain interoperability protocols. While the protocol team and a key contributor responded rapidly to patch the vulnerability and restore liquidity, the exploit served as a crucial, albeit costly, lesson for the entire blockchain ecosystem on the paramount importance of security, rigorous auditing, and robust incident response in the complex world of cross-chain bridges. The event continues to influence how cross-chain solutions are designed and secured.
""")

    # You could add charts, images, or other Streamlit components here
    # st.image("path/to/mango_chart.png")
    # st.code("Example exploit code snippet (if relevant and safe to show)")

    st.write("---")  # Optional separator for end of custom content
    st.info("This is content loaded from the `wormhole_bridge.py` file.")