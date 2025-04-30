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

    st.image("images/optifi.jpeg")  

    st.markdown("""
## Optifi Incident Report (August 29, 2022)

### 1. A brief description of the protocol

Optifi was a decentralized derivatives protocol built on the Solana blockchain, aiming to provide users with the ability to trade options and other derivative instruments in a decentralized manner. The protocol utilized smart contracts (referred to as programs on Solana) to manage trading, collateral, and settlement.

It is important to clarify that the incident on August 29, 2022, was not a malicious exploit initiated by an external attacker exploiting a vulnerability to steal funds. Instead, it was a severe operational error made by the Optifi team during a program update. Therefore, there is no external attacker's wallet address associated with the removal of funds from the protocol in the context of a hack. The funds were inadvertently locked due to a mistaken command execution.

### 2. Exploit summary

The event on August 29, 2022, concerning Optifi was not a hack by a malicious third party but rather a costly accident during a standard procedure. The Optifi team was in the process of deploying an update to their program on the Solana mainnet. However, during this process, they encountered network issues or latency. In an attempt to manage the situation, a critical error was made.

Instead of safely handling the interrupted update, the deployer mistakenly executed a command intended to permanently close the program. This was akin to demolishing the building while people and assets were still inside. The command had the irreversible effect of archiving the program with its existing program ID, making the associated data and funds inaccessible through a new program deployment. This accidental closure locked the assets held within the program's associated accounts, causing a sudden and unintended loss of access to funds for both the protocol's treasury and some users.

### 3. Technical analysis

The incident's technical root cause was a critical misstep in executing Solana's command-line interface (CLI) tools during a program upgrade.

**The Issue:** On Solana, programs have a program ID, and accounts (including those holding funds like Program Derived Addresses or PDAs) are often associated with a specific program ID. When a program is upgraded, the intention is usually to replace the executable code while maintaining the same program ID and thus access to the associated accounts. However, Solana also provides a command to permanently *close* a program. Executing this command archives the program with its current ID, and crucially, prevents any new program from being deployed with that identical ID.

**The Incident:** During the planned program upgrade, the Optifi team's deployer accidentally executed the `solana program close` command targeting their live program on the mainnet.

1.  **Interrupted Update & Mistaken Command:** While attempting to deploy an update (possibly interrupted), the deployer issued the `solana program close` command instead of the correct procedure for handling the update or rollback.
2.  **Permanent Program Closure:** The Solana runtime processed the `solana program close` command, permanently marking the Optifi program's current ID as closed and non-redeployable for new code.
3.  **Funds Locked in PDAs:** The funds and open positions within Optifi were held in various accounts, including PDAs, which were programmatically derived based on the *original* program ID. Since the program ID was permanently closed and a new program with the same ID could not be deployed, the new deployed program (even if it contained the correct logic) could no longer access or control the accounts associated with the old, closed program ID. The assets effectively became locked and inaccessible.

**Impact:** The immediate impact was the permanent locking of approximately $661,000 USDC and other associated assets (representing user funds in margin accounts, option tokens, and AMM vaults) within the inaccessible accounts linked to the closed program ID. The majority of these locked funds belonged to the Optifi team's treasury, but a portion belonged to users who had active positions or funds deposited in the protocol. This operational error directly led to financial losses due to inaccessibility, not theft by an external party.

### 4. Protocol response and aftermath

Following the incident, the Optifi team publicly acknowledged their operational mistake, explaining that they had accidentally closed the program during an update attempt. They were transparent about the cause being an error on their part rather than a security exploit by an external entity.

Optifi announced that the locked funds were likely irrecoverable due to the nature of the `solana program close` command and Solana's program management architecture. Despite this, they committed to compensating all affected users for their losses. They undertook a process to manually calculate user balances based on data snapshots and Pyth oracle prices at the time of the incident and initiated a compensation plan, which they reportedly completed within about two weeks.

The aftermath for Optifi was significant. While they demonstrated integrity by compensating users, the incident highlighted the risks of administrative errors in managing live blockchain programs. They implemented new internal procedures, including a multi-peer surveillance mechanism for deployments and more meticulous record-keeping during updates, to prevent similar accidents in the future. The incident served as a cautionary tale within the Solana development community regarding the power and finality of certain CLI commands.

### 5. Lessons learnt

The Optifi incident, though not a hack, provided valuable lessons for blockchain development and protocol operation:

* **Extreme Caution with Administrative Commands:** The most critical lesson is the absolute necessity of extreme caution and multiple layers of verification before executing powerful administrative commands, especially those that can affect program state or accessibility on a live blockchain.
* **Understanding Blockchain Architecture Deeply:** Developers need a profound understanding of the underlying blockchain's architecture, including how programs, accounts, and upgrades are managed, and the irreversible consequences of certain operations.
* **Robust Deployment Procedures:** Implementing rigorous, multi-signatory, and peer-reviewed deployment procedures is essential to prevent single points of failure and accidental command execution errors.
* **Separation of Concerns:** Structuring smart contracts and associated accounts such that administrative functions (like upgrades) are clearly separated from user fund management can help mitigate the impact of administrative errors.
* **Importance of Testing in Production-Like Environments:** While testing is standard, simulating deployment and update procedures in environments that closely mirror the mainnet is crucial to catch potential operational pitfalls.
* **Transparency in Mishaps:** Optifi's transparency about the cause of the incident, despite it being an internal error, was important for maintaining trust with their user base.

### 6. Conclusion

The Optifi incident on August 29, 2022, was a costly operational error resulting from the accidental execution of the `solana program close` command during a program update. This mistake permanently locked approximately $661,000 in funds within the protocol's accounts, rendering them inaccessible. The incident was a stark reminder to blockchain developers and protocol operators about the critical importance of meticulous procedures, deep understanding of platform-specific commands, and robust security measures not only against external threats but also against potential human error in managing live decentralized applications. Despite the significant financial loss due to inaccessibility, Optifi's commitment to compensating affected users was a positive step in managing the aftermath of this unfortunate incident.
""")