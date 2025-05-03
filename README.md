# 🔐 Solana Security Explorer

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) <!-- Optional: Replace MIT with your chosen license -->

A Streamlit application designed to track, summarize, and answer questions about security incidents and core protocol events within the Solana ecosystem.

![image](https://github.com/user-attachments/assets/acc697fc-ba5d-4ae1-9a24-1ab02e9b25bc)

## 📜 Overview

The Solana blockchain, while powerful, has experienced various security incidents, exploits, and network events. This application provides a centralized place to:

1.  **View** a chronological table of notable security incidents and core protocol issues.
2.  **Filter** these incidents by relevant tags (e.g., DeFi, Oracle, Wallet, Core Protocol).
3.  **Explore** details for specific incidents (where available in separate modules).
4.  **Analyze** summary statistics and insights derived from the incident data.
5.  **Ask** questions about Solana security using an AI-powered chatbot backed by relevant documentation.

## ✨ Features

*   **Chronological Incident Table:** Displays incidents with date, project/service, approximate loss, type, severity score, and tags. Sorts incidents by date.
*   **Tag-Based Filtering:** Easily filter the main table using a multi-select dropdown in the sidebar.
*   **Dynamic Incident Detail Pages:** Clicking on a project name in the table navigates to a dedicated page showing more details (loads content dynamically from corresponding Python files if they exist).
*   **Summary Dashboard:** Provides aggregated statistics and visualizations (e.g., total losses, incident types, severity distribution - implemented in `summary.py`).
*   **Conversational Chatbot:** Powered by LangChain and OpenAI (GPT models), allows users to ask questions about Solana security. The chatbot uses a knowledge base (`superteam_security.md`) vectorized using FAISS for Retrieval-Augmented Generation (RAG).
*   **Secure API Key Handling:** Uses Streamlit Secrets (`secrets.toml`) for managing the OpenAI API key.
*   **Responsive UI:** Built with Streamlit for a clean web interface.
*   **Custom Styling:** Includes CSS enhancements for better table readability (zebra striping, tag badges) and potentially styled chat messages.

## 🛠️ Tech Stack

*   **Frontend/App Framework:** [Streamlit](https://streamlit.io/)
*   **AI/LLM Orchestration:** [LangChain](https://python.langchain.com/)
*   **LLM Provider:** [OpenAI](https://openai.com/) (GPT models like `gpt-4.1-nano-2025-04-14`)
*   **Embeddings:** OpenAI Embeddings
*   **Vector Store:** [FAISS](https://github.com/facebookresearch/faiss) (for local vector storage)
*   **Data Handling:** [Pandas](https://pandas.pydata.org/)
*   **Language:** Python 3.x

## ⚙️ Setup and Installation

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY_NAME.git
    cd YOUR_REPOSITORY_NAME
    ```

2.  **Create a Virtual Environment (Recommended):**
    ```bash
    # Using venv
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`

    # Or using Conda
    # conda create -n solana-sec python=3.9
    # conda activate solana-sec
    ```

3.  **Install Dependencies:**
    Make sure you have a `requirements.txt` file listing all necessary packages. If not, create one:
    ```
    # requirements.txt
    streamlit
    langchain
    langchain-openai
    openai
    faiss-cpu  # Or faiss-gpu if you have CUDA installed and want GPU support
    tiktoken # Required by langchain/openai for token counting
    pandas
    # Add any other specific libraries used (e.g., plotting libraries in summary.py)
    ```
    Then install:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set Up OpenAI API Key:**
    *   Create a file named `secrets.toml` inside a `.streamlit` directory in your project root: `.streamlit/secrets.toml`.
    *   Add your OpenAI API key to this file:
        ```toml
        # .streamlit/secrets.toml
        api_key = "YOUR_OPENAI_API_KEY_HERE"
        ```
    *   **Important:** Ensure this `.streamlit/secrets.toml` file is added to your `.gitignore` to prevent accidentally committing your secret key.

5.  **Prepare Chatbot Data:**
    *   Ensure the `superteam_security.md` file (or your chosen document) is present in the project root directory.
    *   The first time you run the chatbot, it will process this file, generate embeddings, create a FAISS vector index, and save it locally to a folder named `watt_docs_index`. Subsequent runs will load the pre-built index for faster startup (thanks to `@st.cache_resource`).

## ▶️ Running the Application

Navigate to the project's root directory in your terminal (where `home.py` is located) and run:

```bash
streamlit run home.py
