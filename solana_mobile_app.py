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

    st.image("images/solana_mobile.jpeg")  

    st.markdown("""
## Report on Solana Mobile Security(January 12, 2023)

### 1. A brief description of the protocol

Solana Mobile refers to efforts by Solana Labs to integrate the Solana blockchain experience more deeply with mobile devices, notably through the development of the Solana Saga smartphone and the Solana Mobile Stack (SMS). The Saga phone includes a built-in secure element known as the "Seed Vault," designed to securely store users' private keys separately from the device's main operating system, aiming to enhance the security of on-chain transactions and asset management on mobile.

Based on available public information and security analyses, there was no direct malicious exploit of the Solana Mobile (Saga) software or its Seed Vault security feature that resulted in the draining of user funds specifically on January 12, 2023. Therefore, there is no attacker's wallet address associated with a direct exploit of the Solana Mobile hardware or software on this date.

### 2. Exploit summary

While there was no reported malicious exploit directly compromising the Solana Mobile hardware or its Seed Vault on January 12, 2023, a security incident relevant to the Solana ecosystem and potentially impacting mobile users did occur around this time. On January 14, 2023, the Solana Foundation disclosed a data breach involving their account with the email marketing service Mailchimp.

This incident meant that an unauthorized third party gained access to and exported certain user data from the Solana Foundation's Mailchimp lists. The exposed information included user names and email addresses, and in some cases, Telegram usernames, for individuals who had interacted with the Solana Foundation. While this was not an exploit of the blockchain or wallet security, the compromised personal information could potentially be used by malicious actors for targeted phishing attacks aimed at gaining access to users' wallets and funds, including those used on Solana Mobile or other platforms.

### 3. Technical analysis

As stated, there was no technical exploit of the Solana Mobile (Saga) device's security features, such as the Seed Vault, reported on January 12, 2023. The Seed Vault is designed to store private keys in a secure environment isolated from the Android operating system, mitigating risks associated with typical mobile malware.

The security incident that did occur around this date was a data breach of a third-party service used by the Solana Foundation (Mailchimp).

1.  **Third-Party Data Breach:** An unauthorized actor gained access to the Solana Foundation's Mailchimp account.
2.  **Data Export:** The attacker exported user data stored in the Mailchimp lists, including names, email addresses, and potentially Telegram usernames.
3.  **Potential for Phishing:** This exposed personal information could then be used by attackers to craft highly convincing and personalized phishing emails or messages targeting individuals in the Solana ecosystem. These phishing attempts could try to trick users into revealing their private keys, seed phrases, or other sensitive information, or to download malware that could compromise their devices and wallets (including mobile wallets).

This incident highlights a risk vector external to the Solana blockchain and wallet technology itself but relevant to the overall security of users in the ecosystem. While malware exists that targets Solana private keys on various devices (as seen in unrelated reports from other dates), the Mailchimp breach specifically increased the risk of targeted social engineering attacks.

### 4. Protocol response and aftermath

The Solana Foundation publicly disclosed the Mailchimp data breach on January 14, 2023, shortly after being notified by Mailchimp. They communicated the incident to affected users via email and other channels, informing them about the type of data that was exposed and warning them to be vigilant against potential phishing attempts.

The Foundation emphasized that the breach did not compromise blockchain addresses, private keys, or financial information directly held by users. Their response focused on alerting the community to the increased risk of targeted phishing and advising caution regarding unsolicited communications asking for sensitive information. The incident served as a reminder to the Solana community about the importance of practicing good security hygiene and being wary of phishing scams, regardless of the wallet platform being used.

### 5. Lessons learnt

The security incident involving the Solana Foundation's Mailchimp account, while not a direct exploit of Solana Mobile, provided valuable lessons for users and entities in the crypto ecosystem:

* **Third-Party Service Risks:** Relying on third-party service providers for data storage or communication introduces a potential attack surface. The security of these external services is critical, as a breach can expose sensitive user information that can be leveraged for targeted attacks.
* **Importance of Data Minimization:** Entities should strive to collect and retain only the minimum amount of user data necessary for their operations to limit the impact of potential data breaches.
* **User Vigilance Against Phishing:** The incident underscored the ongoing and evolving threat of phishing and social engineering attacks. Users must remain highly vigilant, verify the legitimacy of communications, and never share private keys or seed phrases. This is particularly relevant for mobile users who might interact with various apps and links.
* **Awareness of Attack Vectors:** Users should be aware that threats can come from various sources, not just direct exploits of blockchain or wallet software. Data breaches of associated services can lead to targeted attacks.
* **Secure Communication Channels:** Protocols and foundations should consider the security of their communication channels and the potential for data breaches to impact user safety.

### 6. Conclusion

There was no reported malicious exploit directly targeting the Solana Mobile (Saga) device or its Seed Vault on January 12, 2023. However, a related security incident involving a data breach of the Solana Foundation's Mailchimp account occurred around this time, exposing user contact information. While this breach did not directly compromise users' private keys or funds, it increased the risk of targeted phishing attacks against individuals in the Solana ecosystem, including those using Solana Mobile. This incident served as a crucial reminder of the broader security landscape in web3, highlighting the risks associated with third-party service compromises and the paramount importance of user vigilance against social engineering and phishing attempts across all platforms, including mobile.
""")