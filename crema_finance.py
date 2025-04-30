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

    st.image("images/crema_finance.jpeg")  

    st.markdown("""
    # Crema Finance Exploit Report

    This report details the Crema Finance exploit that occurred on July 2, 2022, analyzing the attack, its technical underpinnings, the protocol's response, and the lessons learned.

    ## 1. Brief Description of the Protocol

    Crema Finance was a concentrated liquidity protocol built on the Solana blockchain. It aimed to provide efficient trading and yield farming opportunities by allowing liquidity providers to specify narrow price ranges for their liquidity. This approach, known as Concentrated Liquidity Market Making (CLMM), was presented as an improvement over traditional Automated Market Maker (AMM) models.

    The attacker's wallet addresses associated with the exploit include a Solana address, reported as `Esmx2Q...`, and an Ethereum address, reported as `0x8021...`, to which funds were bridged after the attack.

    ## 2. Exploit Summary

    The Crema Finance exploit in July 2022 was a sophisticated attack that leveraged flash loans and a vulnerability in the protocol's fee calculation mechanism, resulting in the theft of approximately $8.8 million.

    The attack began with the exploiter setting up a malicious on-chain program and creating a fake "tick account." In Crema's CLMM model, tick accounts stored crucial pricing information used, in part, to calculate transaction fees.

    The attacker then took out a large flash loan from another Solana lending protocol, Solend. Using this borrowed capital, they interacted with a Crema liquidity pool.

    The core of the exploit involved the attacker tricking the Crema protocol into using their fake tick account instead of the legitimate one for fee calculations. By manipulating the data in this fake account, the attacker was able to claim an excessively large amount of fees from the liquidity pool during their flash loan transaction.

    After successfully draining funds by claiming these inflated fees, the attacker repaid the flash loan to Solend within the same transaction. The remaining stolen assets, primarily SOL and stablecoins (USDCet), were then swapped and bridged to the Ethereum network to the attacker's address.

    Following the exploit, the Crema Finance team engaged in negotiations with the attacker, which unusually resulted in the return of most of the stolen funds in exchange for a "white hat" bounty.
        """)
    

    with st.expander("Summarizing Wallet Activity"):
        st.markdown("""

## Summarizing Exploiter Wallet Activity (Crema Finance)

Based on the table above, a detailed summary of the exploiter's wallet activity reveals a series of transactions involving various cryptocurrencies over a period starting on 2022-07-02. The exploiter engaged in transfers, swaps, and bridging activities with multiple wallet addresses.

### Initial Activity (Around 2022-07-02 00:14 - 00:46):

The exploiter's initial activity involved relatively small amounts of various tokens, potentially for testing or reconnaissance.

* Transferred 0.01 MSOL and 0.01 SOL to the address `HS5GnRmXkeC8j2a6wJVaNhKNEbdrgeQJ1d3JL2x82g8Q`. These transfers were worth $0.33 USD each and occurred at 00:14:25.000.
* Transferred 0.01 SOL and 0.01 STSOL to `6kDhKM8rDR4DXvwUpao4UA6JtCZfooAgMhicePmUNeJu`, also worth $0.33 USD each, at 00:14:33.000.
* Later, transferred 1 SOL worth $32.85 USD to `EqLZKF1bwUWUzU5F21jDQMoK4HRx8wQpLt57jhP8LbKm`. Subsequently, 33.1 USDC worth $33.15 USD was transferred from this address, and the exploiter also swapped 1 SOL to 33.102978 USDC worth $32.97 USD at 00:16:04.000. This suggests an immediate conversion of SOL to USDC.
* Small transfers of 1 USDC and 1 USDT worth $1 USD each occurred involving the address `HsYb453638e4ZwykZj4PHNwFiXHauV9UuNL3mCmFkZzh` around 00:23:27.000.
* The exploiter also interacted with the address `3m15qNJDM5zydsYNJzkFYXE7iGCVnkKz1mrmbawrDUAH`, transferring 1 USDCET and 1 USDC, and swapping 1 USDC to 1.000025 USDCET around 00:46:04.000.

### Later Activity with 0 Value Transfers (Around 2022-07-02 01:44 - 21:32):

A significant portion of the logs shows repeated transfers of 0 MSOL, 0 PAI, 0 USDH, and 0 STSOL to various addresses, notably `HS5GnRmXkeC8j2a6wJVaNhKNEbdrgeQJ1d3JL2x82g8Q` and `HRWwcA1VZnG9r2k9BHpR3PjbYuK9qUmcqrEWrhc9je5W`, as well as `6kDhKM8rDR4DXvwUpao4UA6JtCZfooAgMhicePmUNeJu`. The purpose of these zero-value transfers is not evident from the provided data.

### Significant Value Transfers and Swaps (Around 2022-07-02 20:08 onwards):

The exploiter then engaged in transactions involving substantial amounts:

* Large transfers of PAI tokens involving addresses `HRWwcA1VZnG9r2k9BHpR3PjbYuK9qUmcqrEWrhc9je5W` and `Ej4KxxUz73edQzjfsPVWvYxT5eyhQoWoXpo7BYm2Ejhj` occurred around 20:08:52.000. These transfers involved amounts like 840001 PAI (worth $838660.8 USD) and 842520 PAI (worth $841175.77 USD), suggesting a large-scale movement of this token. There were also smaller transfers of USDC from `HRWwcA1VZnG9r2k9BHpR3PjbYuK9qUmcqrEWrhc9je5W` during this time.
* Later, starting around 22:10:14.000, the exploiter was involved in transactions with MSOL and STSOL, interacting with addresses like `HS5GnRmXkeC8j2a6wJVaNhKNEbdrgeQJ1d3JL2x82g8Q`, `DdZR6zRFiUt4S5mg7AV1uKB2z1f1WzcNYCaTEEWPAuby`, and `6kDhKM8rDR4DXvwUpao4UA6JtCZfooAgMhicePmUNeJu`. These involved transfers of significant amounts of MSOL (e.g., 10500.01 MSOL worth $362894.68 USD) and STSOL (e.g., 57171 STSOL worth $1962179.65 USD), indicating a shift in focus to these tokens.
* Around 22:14:13.000, the exploiter interacted with `8eyi347MTDeH5F6eVv2qjPxVnU685FFZLDGcj5QWHZ6y`, transferring and swapping STSOL for SOL. A swap of 20651.17 STSOL to 21278.685402968 SOL worth $714012.94 USD was recorded.
* There was also significant activity involving USDT and ETH around 22:27:14.000, with a swap of 999999.92 USDT to 29354.399802781 SOL worth $1000501.63 USD and a transfer of 927.16 ETH worth $966265.86 USD. The exploiter interacted with addresses `5jmsB5Z1sfy2Fixy1TRRUXkrxtk5gmBGjuz16L1sQUZQ` and `GRiN6BiHeaa2wrFEpqzR397d6RqefCSRhnQVsVscwT3r` during these transactions.
* Further swaps and transfers involving USDC and SOL, and later USDCET, occurred around 22:28:23.000, involving addresses like `FG3z1H2BBsf5ekEAxSc1K6DERuAuiXpSdUGkYecQrP5v` and `GRiN6BiHeaa2wrFEpqzR397d6RqefCSRhnQVsVscwT3r`.
* Interactions with USDH started around 22:33:38.000, including swaps with MSOL involving addresses `H66xGa3c5wvg5ZGF7RCwskf52iH42C8u8v8TPwQXwc3m` and `AiMZS5U3JMvpdvsr1KeaMiS354Z1DeSg5XjA4yYRxtFf`.
* The exploiter also engaged in bridging activities involving USDCET. A notable outbound bridge of 997429.372578 USDCET worth $999201.52 USD occurred around 22:44:39.000, and another of 2367302.979352 USDCET worth $2371508.99 USD around 22:55:01.000. These indicate movement of assets to other chains or platforms.
* Further large swaps involving USDH and USDC were observed around 23:53:58.000.
* Towards the end of the logs, around 23:58:31.000 and continuing into the next day, the exploiter frequently swapped SOL to USDCET and interacted with addresses `F8Vyqk3unwxkXukZFQeYyGmFfTG3CAX4v24iyrjEYBJV` and `7XFMgfxhDURuaPwhUkXAy6uQJCoC3HPpjiZBqcot57Ge`. These transactions involved amounts around 10000 SOL being swapped for USDCET worth over $330,000 USD. More bridging of USDCET outbound is also recorded.

### In summary, the exploiter's wallet activity shows a pattern of:

* Initial small-scale testing or reconnaissance with various tokens.
* Large-scale manipulation or movement of specific tokens like PAI, MSOL, STSOL, USDT, ETH, and USDC.
* Active use of swaps to convert between different cryptocurrencies.
* Engagement in bridging activities, suggesting the movement of funds to other blockchain networks.
* Repeated zero-value transfers to certain addresses for an unknown purpose.
* Frequent interaction with a set of specific wallet addresses, likely involved in different stages of the exploitation or fund movement.
* A focus on SOL and its associated tokens (MSOL, STSOL) and stablecoins (USDC, USDT, USDCET, USDH) throughout the observed period.

The activity suggests a sophisticated operation involving the exploitation of vulnerabilities allowing for the acquisition of large amounts of various cryptocurrencies, followed by rapid conversion and movement of these funds across different platforms and potentially different blockchain ecosystems.
                    
""")

    st.markdown("""
    ## 3. Technical Analysis

    The technical vulnerability exploited in the Crema Finance hack resided in the protocol's handling and verification of "tick accounts," which were fundamental to its Concentrated Liquidity Market Maker (CLMM) model. These accounts stored tick data essential for calculating transaction fees within the liquidity pools.

    The specific flaw allowed an attacker to "spoof" or substitute a legitimate tick account with a fake one they controlled. While the protocol performed some basic owner checks on the tick account, it failed to implement sufficient validation to ensure that the provided tick account was the *correct* and *authentic* one associated with the specific liquidity pool being interacted with.

    The attacker's exploit sequence was as follows:
    1.  **Create Fake Tick Account:** The attacker created a new account on Solana and populated it with manipulated data designed to influence fee calculations.
    2.  **Obtain Flash Loan:** A large, uncollateralized flash loan was taken from Solend. This provided the attacker with significant capital to interact with the Crema liquidity pool.
    3.  **Interact with Crema Pool:** The attacker initiated a transaction with a Crema CLMM pool, depositing the flash-loaned tokens.
    4.  **Spoof Tick Account:** Crucially, during the transaction where fees were calculated and claimed, the attacker forced the Crema protocol to reference their fake tick account instead of the pool's real one.
    5.  **Claim Inflated Fees:** Because the fake tick account contained manipulated data, the fee calculation resulted in an artificially inflated amount. The attacker's transaction was structured to claim this enormous, illegitimate fee amount from the pool's reserves.
    6.  **Repay Flash Loan:** Within the atomic flash loan transaction, the attacker repaid the borrowed funds to Solend.
    7.  **Withdraw Remaining Funds:** The significant amount of assets claimed as inflated fees, minus the flash loan repayment, represented the attacker's profit. These funds were then moved and bridged.

    The impact of the exploit was the draining of approximately $8.8 million worth of assets from Crema Finance's liquidity pools. The vulnerability in tick account validation allowed the attacker to manipulate the protocol's internal logic for financial gain, demonstrating how insufficient input validation can be exploited, especially when combined with mechanisms like flash loans that provide large amounts of capital for rapid, complex transactions.

    ## 4. Protocol Response and Aftermath

    Upon discovering the exploit on July 2, 2022, Crema Finance immediately suspended its smart contracts and halted all activity on the protocol to prevent further losses. The team launched an investigation with the help of blockchain security experts.

    In a somewhat unusual turn for a major DeFi hack, the Crema Finance team managed to establish communication with the attacker. They publicly offered a "white hat" bounty of $800,000 for the return of the stolen funds.

    After a period of negotiation, the attacker agreed to return most of the stolen assets. The final agreement involved the attacker keeping 45,455 SOL (valued at approximately $1.68 million at the time) as a bounty, and returning the remaining funds, which amounted to roughly $8.3 million in ETH and SOL. The return of funds occurred in several transactions.

    Following the return of assets, Crema Finance focused on creating a compensation plan for affected users. The protocol remained suspended while the team worked on patching the vulnerability and undergoing further security audits.

    Later, in July 2023, a former security engineer named Shakeeb Ahmed was arrested and charged in the US in connection with the Crema Finance hack, indicating that law enforcement efforts continued even after the partial return of funds and the white hat agreement.

    ## 5. Lessons Learned

    The Crema Finance exploit offered valuable lessons for the Solana ecosystem and DeFi in general:

    * **Criticality of Input Validation:** The exploit highlighted, once again, that insufficient validation of input accounts and data (like the tick account) is a major vulnerability vector in smart contracts. Developers must assume malicious input and validate everything rigorously.
    * **Flash Loans as an Amplifier:** Flash loans themselves are not malicious, but they provide attackers with the capital needed to exploit logic vulnerabilities on a large scale within a single transaction. Protocols must be designed to be resilient against attacks using large amounts of capital.
    * **Audits are Essential, But Not Guarantees:** While the specifics of Crema's code were not public, the exploit underscores that even protocols with some level of review can have vulnerabilities. Continuous security practices, including multiple audits and bug bounties, are crucial.
    * **Complexity Increases Risk:** The CLMM model, while potentially efficient, added complexity that introduced unforeseen vulnerabilities. Simpler designs often have a smaller attack surface.
    * **Incident Response and Communication:** Crema's swift action to halt the protocol and engage in communication (even if unusual) helped manage the crisis. A prepared incident response is vital.
    * **Legal Consequences:** The later arrest of an individual linked to the attack serves as a reminder that even in the pseudonymous world of crypto, exploits can lead to real-world legal consequences.

    ## 6. Conclusion

    The Crema Finance exploit was a significant security incident on Solana, resulting in the loss of approximately $8.8 million through a flash loan attack that exploited a vulnerability in the protocol's tick account validation. The attacker was able to manipulate fee calculations to drain funds. While the unusual negotiation led to the return of most assets in exchange for a bounty, the incident underscored the critical importance of robust input validation, the risks amplified by flash loans, and the ongoing need for stringent security practices in DeFi protocols. The subsequent arrest also highlighted the potential for accountability in the aftermath of such attacks.
    """)
