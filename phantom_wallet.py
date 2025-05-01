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

    st.image("images/phantom_wallet.jpeg")  

    st.markdown("""

# :blue[Phantom Wallet Airdrop Phishing Scam]

## :red[1. A Brief Description of the Protocol]

Phantom is a non-custodial Solana wallet (browser extension and mobile app) enabling token and NFT management, dApp connectivity, and an in-app notification stream for newly received assets.

---

## :orange[2. Exploit Summary]

- **:green[April 15, 2022, ~10:00 UTC:]** Attackers airdropped custom-named tokens (e.g., “SOL Airdrop,” “Phantom Rewards”) into random Phantom wallets.  
- **:orange[Moments later:]** Clicking the token entry or its notification redirected victims to phishing sites mimicking popular Solana dApps.  
- **:green[Seed-phrase capture:]** On the fake sites, users were prompted to enter their 12- or 24-word seed phrase to “claim” the airdrop.  
- **:orange[Losses realized:]** Community reports estimate total losses under \\$1 million across dozens of users.

---

## :green[3. Technical Analysis]

- **:green[Unfiltered notifications:]** The wallet automatically surfaced every incoming token—legitimate or not—without provenance checks.  
- **:orange[Misleading labels:]** Attackers named scam tokens to imply legitimacy (e.g., “Phantom Rewards”), exploiting user trust in UI labels.  
- **:green[Phishing redirect:]** The click handler forwarded users directly to attacker-controlled URLs, bypassing any domain whitelist.

---

## :blue[4. Protocol Response and Aftermath]

- **:green[Endpoint lockdown:]** Within hours, Phantom disabled the auto-notification endpoints that surfaced new tokens in production.  
- **:orange[Spam filtering:]** A blacklist/deny-list for known malicious token contracts and a spam-scoring algorithm were added to the notification pipeline.  
- **:green[UI changes:]** Notifications for unverified tokens were hidden behind a secondary confirmation step.  
- **:orange[User advisories:]** Official blog posts and tweets reinforced “never enter your seed phrase on any website” and urged users to verify token origins.

---

## :violet[5. Lessons Learnt]

- **:green[Validate token provenance:]** Before auto-displaying in the UI—treat all incoming assets as untrusted by default.  
- **:orange[Domain allow-listing:]** For critical UI actions prevents redirection abuse.  
- **:green[Seed-phrase sanctity:]** Reserve seed-entry interfaces strictly for the local wallet context—never solicit seeds on external sites.  
- **:orange[Continuous monitoring:]** Regular endpoint scans and phishing drills help detect novel UI-based attacks early.
- **:green[Transparency:]** Wallets and dApps must clearly communicate how assets are detected and surfaced to users.

---

## :red[6. Conclusion]

The April 15, 2022 Phantom airdrop phishing incident demonstrated that even benign notification features can be weaponized for seed-phrase theft. Phantom’s swift remediation—combining technical filters, UI safeguards, and clear user education—effectively neutralized the threat and set a new standard for secure wallet UX design.

""")
