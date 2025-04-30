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

    st.image("images/jupiter.jpeg")  

    st.markdown("""
# :blue[Jupiter Aggregator Exploit Report - September 14, 2023]

## :red[1. Protocol Description]

Jupiter Aggregator is a key liquidity aggregator on the Solana blockchain, designed to find the best trading routes and prices across various decentralized exchanges (DEXs) and liquidity pools. It aims to provide users with optimal execution for their token swaps. The platform integrates with numerous protocols to offer a comprehensive trading experience.

Information regarding a specific attacker's wallet address directly tied *solely* to the September 14, 2023 incident is less publicly reported compared to some other exploits, as the incident was more related to a specific token listing and price anomaly rather than a direct smart contract hack draining core Jupiter funds. However, suspicious activities and associated wallets involved in manipulating the price of the affected token were noted. A specific attacker wallet address for this particular incident is not universally cited in the same way as in direct protocol hacks.

## :orange[2. Exploit Summary]

The incident on September 14, 2023, wasn't a traditional hack of Jupiter's core smart contracts, but rather an exploit related to the listing and initial trading of a new token, called "Soles," on a liquidity pool that Jupiter aggregated. The exploit began shortly after the token's launch.

It appears that malicious actors were able to manipulate the price of the Soles token in its initial liquidity pool. By executing rapid buy and sell orders, potentially combined with insufficient initial liquidity or a vulnerability in the token's mechanics or the pool's setup, they artificially inflated the token's price. Jupiter, acting as an aggregator, routed user trades through this manipulated pool, leading users to buy the Soles token at vastly inflated prices. The attackers then profited by selling their holdings of the token at these manipulated highs. The situation unfolded quickly, causing significant losses for users who traded the Soles token via Jupiter during the exploit window before the anomaly was detected and the token listing addressed.

## :green[3. Technical Analysis]

The technical issue was primarily centered around the liquidity pool mechanics and the specific characteristics of the newly launched "Soles" token, rather than a vulnerability in Jupiter's core aggregation logic itself. The exploit capitalized on the initial low liquidity and potentially flawed tokenomics or configuration of the Soles token's trading pair on a specific DEX pool that Jupiter was aggregating.

The attackers likely employed a "rug pull" or "pump and dump" style manipulation. They could have used bots or rapid manual trading to execute a series of transactions that significantly moved the price in the low-liquidity environment. Because Jupiter's role is to find the *best available price* across integrated DEXs, it directed user trades to this pool where the manipulated price was temporarily the "best" on paper. Users trading through Jupiter effectively became victims of buying into the artificially inflated price, while the manipulators offloaded their tokens for a profit before the price inevitably crashed. The impact was localized to users who traded the specific Soles token during the manipulation window, resulting in significant financial losses for those individuals.

## :blue[4. Protocol Response and Aftermath]

Jupiter's response focused on mitigating further harm to users. Upon identifying the suspicious trading activity and the price anomaly related to the Soles token, the team quickly delisted or paused aggregation for the affected token and liquidity pool. They communicated with the community, explaining that the issue was with the specific token and pool, not a compromise of Jupiter's core infrastructure.

In the aftermath, Jupiter emphasized the risks associated with trading newly launched, low-liquidity tokens and highlighted the importance for users to do their own research (DYOR) on tokens and liquidity pools, even when using an aggregator. The incident led to discussions about how aggregators can better identify and potentially flag or avoid routing trades through highly volatile or potentially manipulated low-liquidity pools, especially for new token listings.

## :violet[5. Lessons Learnt]

The Jupiter Aggregator incident with the Soles token highlights crucial lessons for both DeFi users and protocols:

* **:green[User Due Diligence:]** Users must exercise caution and conduct thorough research on new tokens, their liquidity, and the pools they trade in, regardless of using an aggregator. Aggregators find the best price, but that price can still be manipulated.
* **:orange[Liquidity Risk:]** Trading in low-liquidity pools is inherently risky and highly susceptible to price manipulation.
* **:green[Tokenomics and Pool Configuration:]** The design and configuration of new tokens and their initial liquidity pools are critical and can be vectors for exploits.
* **:orange[Aggregator Safeguards:]** While aggregators aim for the best price, they could explore implementing additional heuristics or warnings for users trading in extremely low-liquidity or suspicious pools.
* **:green[Rapid Response:]** Quick detection and delisting of problematic assets or pools are vital to limit user losses during an incident.
* **:orange[Communication:]** Clear and timely communication with the community during and after an incident is essential for maintaining trust.

## :red[6. Conclusion]

The Jupiter Aggregator incident on September 14, 2023, while not a direct hack of its core system, served as a significant event highlighting the risks associated with liquidity manipulation, particularly with new token listings on integrated DEXs. The exploit capitalized on the low liquidity and potentially problematic setup of a specific token's pool, leading to users buying at manipulated prices via the aggregator. The incident underscores the shared responsibility between DeFi protocols and users in ensuring a safer trading environment, emphasizing the need for user vigilance and potential enhancements in how aggregators handle risky, low-liquidity assets.
""")
