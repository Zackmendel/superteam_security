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

# :blue[Optifi Incident Report (August 29, 2022)]

## :red[1. A Brief Description of the Protocol]

Optifi was a decentralized derivatives protocol built on the Solana blockchain, aiming to provide users with the ability to trade options and other derivative instruments in a decentralized manner. The protocol utilized smart contracts (referred to as programs on Solana) to manage trading, collateral, and settlement.

There was no attacker or malicious exploit in this incident. The funds were inadvertently locked due to an internal operational error by the Optifi team.

---

## :orange[2. Exploit Summary]

The Optifi incident on August 29, 2022, was not a hack but a costly operational error. While deploying an update to their smart contract (program), the Optifi team encountered network issues. In the process of trying to manage the situation, the deployer mistakenly executed the `solana program close` command — a command meant to permanently archive a program.

This action irreversibly locked ~$661,000 worth of user and treasury funds in program-derived accounts (PDAs) tied to the now-closed program ID. Because Solana doesn’t allow redeployment to a closed program ID, the locked funds became inaccessible.

The exploit narrative wasn’t a direct "funds stolen" attack through Serum’s existing contracts, but rather a critical loss of **trust and security** through potential control of Serum’s upgrade path.

---                

## :green[3. Technical Analysis]

- **:green[The Issue:]** On Solana, accounts such as Program Derived Addresses (PDAs) are tied to specific program IDs. When upgrading a program, the ID usually remains unchanged, preserving access to those accounts.

- **:orange[The Mistake:]** Instead of properly upgrading, the deployer accidentally issued the `solana program close` command on the live mainnet program.

- **:green[The Consequence:]** The program ID was permanently closed. All accounts linked to it became inaccessible, including margin accounts, option token accounts, and AMM vaults.

- **:orange[The Impact:]** ~$661,000 in USDC and other tokens were locked. These included both treasury and user funds, now permanently inaccessible due to the closed ID being non-redeployable.

---

## :blue[4. Protocol Response and Aftermath]

- **:green[Admission and Transparency:]** The Optifi team publicly admitted the mistake, emphasizing that it was an operational accident — not an exploit or attack.

- **:orange[Compensation Plan:]** They committed to compensating affected users based on balance snapshots and oracle prices. This process was completed within about two weeks.

- **:green[Operational Improvements:]** Optifi adopted internal safeguards such as multi-peer deployment checks, peer review mechanisms, and stricter deployment record-keeping.

- **:orange[Developer Cautionary Tale:]** The event raised broader awareness in the Solana developer community about the irreversible nature of certain CLI operations.

---

## :violet[5. Lessons Learnt]

- **:green[Extreme Caution with Admin Commands:]** Teams must add multiple verification layers before executing irreversible blockchain actions.

- **:orange[Deep Understanding of Architecture:]** Protocol teams need to fully understand how programs and accounts interact on a blockchain like Solana.

- **:green[Robust Deployment Procedures:]** Peer-reviewed, multi-signatory deployment processes can mitigate critical errors.

- **:orange[Separation of Concerns:]** Administrative controls should be decoupled from fund management functions wherever possible.

- **:green[Test in Mainnet-like Environments:]** Realistic simulations of deployment scenarios should be part of the standard workflow.

- **:orange[Transparency:]** Optifi's honest disclosure helped preserve some user trust despite the mishap.

- **:green[Transparency:]** Protocols need to disclose upgrade authority models clearly to users.

---

## :red[6. Conclusion]

The Optifi incident was a stark reminder of the risks posed by human error in managing live blockchain infrastructure. A single mistaken command — `solana program close` — led to the permanent inaccessibility of ~$661,000 in funds. Although this was not a malicious attack, the financial consequences were severe. Optifi’s commitment to user reimbursement, transparency, and improved internal controls was commendable. Still, the event serves as a cautionary tale for all Solana and broader Web3 developers to treat administrative privileges with the utmost respect and diligence.

""")
