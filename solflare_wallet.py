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

    st.image("images/solflare.jpeg")  

    st.markdown("""
# :blue[Solflare Wallet Security Incident Report - November 2, 2023]

## :red[1. Protocol Description]

Solflare is a popular non-custodial digital wallet designed for the Solana blockchain. It provides users with a secure way to manage their SOL tokens, NFTs, and interact with decentralized applications (dApps) within the Solana ecosystem. As a non-custodial wallet, Solflare gives users full control over their private keys and assets, placing the responsibility for security primarily on the user.

Regarding the events around November 2, 2023, there isn't a widely reported specific attacker's wallet address directly linked to a core vulnerability exploit within the Solflare wallet software itself on this date. Incidents affecting users around this time were more commonly associated with broader scam campaigns targeting individual wallet users through phishing, malware, or malicious smart contract interactions. Therefore, a single attacker address for a Solflare protocol exploit on this specific date is not applicable based on available information.

## :orange[2. Exploit Summary]

The period around November 2, 2023, saw a continuation of various security threats targeting users within the Solana ecosystem, including those using Solflare Wallet. While not a direct exploit of Solflare's core code, the incidents involved malicious actors employing sophisticated social engineering and technical tricks to compromise individual users' wallets.

The narrative of these incidents often began with users encountering deceptive links or advertisements, frequently disguised as legitimate airdrops, new token listings, or opportunities related to popular Solana projects. Upon clicking these links, users might be led to fake websites designed to mimic legitimate platforms or prompted to download malicious software. In other cases, users were tricked into approving malicious smart contract interactions that granted attackers sweeping permissions over their assets. These actions, often performed unknowingly by the user, resulted in the unauthorized draining of funds from their Solflare wallets. The attacks were often swift, leaving users with depleted balances before they fully understood what had happened.

## :green[3. Technical Analysis]

The technical vectors behind the incidents affecting Solflare users around November 2, 2023, primarily revolved around compromising user-side security rather than a flaw in Solflare's fundamental cryptography or smart contract implementation. The key technical issues exploited were:

* **Malicious Smart Contract Approvals:** Users were often socially engineered into signing transactions or granting token approvals to malicious smart contracts. These approvals could give attackers unlimited spending access to specific tokens in the user's wallet. The technical flaw here lies in the user's misunderstanding or the deceptive presentation of the approval request by the attacker's interface.
* **Phishing and Fake Websites:** Attackers created highly convincing fake websites that mimicked legitimate dApps or wallet interfaces. Users connecting their Solflare wallet to these sites might unknowingly expose their private keys or sign malicious transactions displayed deceptively in the wallet interface.
* **Malware and Drainers:** The proliferation of sophisticated wallet draining software (like the "Solana Drainer" mentioned in reports around this time) allowed attackers to automate the process of identifying and siphoning assets from compromised wallets. These drainers could be delivered via malicious downloads or scripts embedded in fake websites. The technical aspect involves the drainer code interacting with the wallet via the browser extension or application interface after the initial compromise (e.g., obtaining a signature or key).

The impact was direct financial loss for the affected individual users, with assets being transferred to attacker-controlled wallets.

## :blue[4. Protocol Response and Aftermath]

As a non-custodial wallet provider, Solflare's response to such widespread scam campaigns primarily focuses on educating users and implementing security features within the wallet to help prevent common attack vectors. While there wasn't a specific "fix" for a core protocol exploit on Nov 2, 2023, Solflare continuously works on enhancing user security.

Their response and ongoing efforts include:
* **User Education:** Publishing guides and warnings about common scams like phishing, malicious approvals, and the dangers of sharing seed phrases.
* **Security Features:** Implementing features like transaction simulations (allowing users to see the potential outcome of a transaction before signing), anti-phishing warnings for known malicious sites, and clear displays of smart contract approval details.
* **Collaboration:** Working with security researchers and other ecosystem participants to identify and flag malicious addresses and websites.
* **Support:** Providing support channels for users who believe their wallets have been compromised, offering guidance on steps to take (like revoking approvals).

The aftermath for affected users involved the loss of assets, and for Solflare and the broader ecosystem, it reinforced the ongoing challenge of user-level security and the need for continuous vigilance against evolving scam techniques.

## :violet[5. Lessons Learnt]

The security incidents affecting Solflare users around November 2, 2023, offer critical lessons for anyone interacting with DeFi and using non-custodial wallets:

* **:green[Guard Your Seed Phrase/Private Keys:]** Never share your seed phrase or private keys with anyone, ever. Do not enter them on any website or application unless you are absolutely certain of its legitimacy and necessity (which is rare).
* **:orange[Be Wary of Phishing:]** Always double-check URLs and the authenticity of websites and applications before connecting your wallet or entering any information. Bookmark legitimate sites.
* **:green[Review Smart Contract Permissions:]** Carefully examine the details of any transaction or approval request in your wallet before signing. Understand what permissions you are granting to a dApp or smart contract. Be cautious of unlimited spending approvals.
* **:orange[Use Transaction Simulations:]** Utilize wallet features like transaction simulations if available to understand the potential outcome of signing a transaction.
* **:green[Stay Informed:]** Keep up-to-date with common scam techniques and security threats in the crypto space. Follow official wallet and protocol channels for security announcements.
* **:orange[Consider Hardware Wallets:]** For storing significant amounts of crypto, consider using a hardware wallet, which keeps your private keys isolated offline.

## :red[6. Conclusion]

The security incidents affecting Solflare Wallet users around November 2, 2023, were not the result of a core protocol exploit but rather a series of successful scam and phishing attacks targeting individual users. Malicious actors exploited user-side vulnerabilities through deceptive websites, malware, and social engineering to gain unauthorized access to funds via compromised private keys or malicious smart contract approvals. This period highlighted the persistent threat of user-focused scams in the DeFi space and underscored the critical importance of individual user security practices, including safeguarding private keys, recognizing phishing attempts, and carefully reviewing smart contract interactions. Solflare and the broader Solana ecosystem continue to work on providing tools and education, but ultimate responsibility for non-custodial wallet security rests with the user.
""")
