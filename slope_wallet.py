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

    st.image("images/slope_wallet.jpeg")  

    st.markdown("""
## Slope Wallet Exploit Report (August 2, 2022)

### 1. A brief description of the protocol

Slope Wallet is a non-custodial cryptocurrency wallet primarily focused on the Solana ecosystem, offering mobile applications for iOS and Android, as well as a browser extension. It allows users to manage their Solana (SOL) tokens, SPL tokens, and NFTs, and interact with decentralized applications (dApps) on the Solana network. As a non-custodial wallet, users are responsible for managing their private keys or seed phrases, which grant access to their funds.

Investigations into the exploit identified several attacker-controlled addresses that received the drained funds. Some of the addresses publicly associated with receiving stolen assets during the exploit include:
* **5WwBYgDigJiecdbfcitepm4rzgS4AYpuraD4s9xXg4Gz**
* **GEsh2LhvKfrb4PareyaF3gReisnnWc5DrRfCjCymoKTB**
* **CEzN7mqP9xoxn2HdyW6fjprERkbvukzgHFRHorneyC5Z**
* **8YDBpLpkb2pE1bVdHpCjT2LAcb3e9x6xGjC7kG7H8rYn**

These addresses were observed receiving assets from numerous compromised user wallets.

### 2. Exploit summary

On August 2, 2022, users of Slope Wallet and some other Solana wallets began reporting that their funds were being drained without their authorization. Panic spread quickly throughout the Solana community as the number of affected wallets grew rapidly. Users watched in real-time as their SOL tokens and other assets were transferred out of their wallets to unknown addresses.

Initial speculation pointed towards a potential vulnerability within the Solana blockchain itself, but investigations quickly shifted focus to wallet software. The trail of drained wallets eventually led security researchers and the Solana Foundation to identify a specific vulnerability within the Slope Wallet application as the likely source of the compromise. The exploit was not a direct attack on the Solana blockchain but rather a critical flaw in how some wallet providers, primarily Slope, handled users' sensitive private keys. Over several hours, the attacker systematically drained assets from thousands of affected wallets, highlighting a significant supply chain security issue within the ecosystem.

### 3. Technical analysis

The technical analysis points strongly to a critical security lapse in Slope Wallet's handling of users' private keys as the root cause of the widespread draining of wallets.

**The Issue:** The core vulnerability is believed to stem from Slope Wallet's integration with a third-party error monitoring and logging service, commonly identified as Sentry. According to incident reports and analyses, the mobile version of the Slope Wallet application was configured in a way that it inadvertently transmitted users' generated seed phrases or private keys in plaintext to this logging service's servers. This sensitive data was reportedly stored unencrypted on these servers.

**The Exploit:** The attacker(s) are believed to have gained unauthorized access to Slope's logging server or the data collected by the Sentry instance used by Slope.

1.  **Private Key Exposure:** When users created new wallets or imported existing ones using the vulnerable versions of the Slope mobile app, their seed phrases or private keys were sent to Slope's configured Sentry server as part of error reporting or logging.
2.  **Unauthorized Access:** The attacker(s) somehow gained access to the data stored on this logging server. The exact method of access (e.g., a vulnerability in the logging service itself, compromised credentials for Slope's account, etc.) was not definitively confirmed across all investigations, but the outcome was access to a database containing unencrypted private keys.
3.  **Wallet Draining:** With access to these private keys, the attacker(s) had full control over the corresponding user wallets. They then systematically signed transactions to transfer assets (SOL, other tokens, NFTs) from the compromised wallets to their own addresses. This process was automated and carried out across thousands of wallets that had their keys exposed through the vulnerable logging mechanism.

**Impact:** The exploit directly impacted approximately 9,200 wallets, resulting in the theft of assets valued at around $4.1 million at the time. While the investigation strongly linked the Slope logging vulnerability to a significant number of these compromised wallets, initial reports indicated a discrepancy, suggesting that this specific vulnerability might not have accounted for *all* affected wallets. However, the consensus among security researchers is that the private key leakage from Slope's service was the primary vector for the vast majority of the losses. The incident also caused significant panic and eroded trust in hot wallets within the Solana ecosystem.

### 4. Protocol response and aftermath

Upon discovering the ongoing exploit, the Slope Finance team, in collaboration with the Solana Foundation and other security firms in the ecosystem, immediately launched an investigation to identify the root cause. They communicated with users via social media and other channels, urging all Slope users to migrate their assets to a new wallet with a completely fresh seed phrase that had never been exposed or used in Slope.

Slope released an incident report acknowledging the vulnerability in their Sentry integration that led to the logging of private keys. They emphasized that they had removed the vulnerable code and were working to enhance their security practices. However, their report also noted the aforementioned discrepancy between the number of wallets with exposed keys in the logs and the total number of compromised wallets, indicating that other potential factors or vectors were still being investigated.

The aftermath saw a significant push for users to move their assets off Slope Wallet and into hardware wallets or other hot wallets perceived as more secure. The incident served as a wake-up call for wallet providers regarding the critical importance of secure private key management and careful consideration of third-party service integrations. While Slope took steps to address the vulnerability and communicate with users, the exploit severely damaged their reputation and highlighted the potential risks associated with software wallets if not developed and maintained with the highest security standards. There were no widespread reports of fund recovery directly facilitated by Slope following the exploit.

### 5. Lessons learnt

The Slope Wallet exploit provided crucial lessons for both wallet providers and users in the cryptocurrency space:

* **Private Key Security is Paramount:** The incident underscored that the security of a non-custodial wallet is directly tied to the security of the user's private key or seed phrase. Any compromise of this information, regardless of how it occurs (e.g., phishing, malware, or, in this case, a software vulnerability), grants an attacker full control.
* **Supply Chain Risks are Real:** Relying on third-party services (like logging platforms) without thoroughly vetting their security practices and ensuring sensitive data is never transmitted or stored insecurely introduces significant supply chain risks. Developers must exercise extreme caution when integrating external services, especially in applications handling financial assets.
* **Secure Development Lifecycle is Crucial:** The vulnerability in Slope's logging suggests a lapse in their secure development lifecycle. Thorough code reviews, security testing, and careful configuration management are essential to prevent such critical flaws.
* **User Education is Vital:** While the vulnerability was in the software, users must also be educated on best practices, such as the importance of keeping their seed phrases offline and never sharing them, and being aware of the risks associated with different wallet types.
* **The Importance of Independent Security Audits:** Regular and comprehensive security audits by reputable third parties are critical for identifying vulnerabilities before they are exploited.
* **Hardware Wallets Offer Enhanced Security:** The exploit reinforced the recommendation for users holding significant amounts of cryptocurrency to use hardware wallets, as private keys are stored offline and are not susceptible to software-based vulnerabilities of hot wallets.

### 6. Conclusion

The Slope Wallet exploit of August 2022 was a significant security incident that resulted in the loss of millions of dollars worth of cryptocurrency from thousands of user wallets on the Solana network. The exploit was primarily attributed to a critical vulnerability in the Slope mobile application that caused users' private keys to be inadvertently leaked to a third-party logging service. This incident served as a stark reminder of the paramount importance of secure private key management by wallet providers and the potential risks introduced by integrating external services without stringent security measures. The exploit led to a loss of user trust in affected hot wallets and reinforced the need for the highest security standards in the development and maintenance of cryptocurrency wallets to protect user assets from compromise.
""")