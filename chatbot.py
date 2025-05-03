import os
import streamlit as st


def display_chatbot():
    st.markdown("""
        <style>
            /* Target the chat container */
            /* Note: Selectors might change with Streamlit updates. Inspect element if needed. */
            .stChatInput, .stChatInput > div {
                /* background-color: #f0f2f6; */ /* Example: Light background for input */
            }

            /* Style message bubbles */
            [data-testid="stChatMessage"] {
                border-radius: 10px;
                padding: 12px;
                margin-bottom: 10px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                max-width: 85%; /* Prevent messages from taking full width */
            }

            /* Style user messages */
            /* Find the parent div of user messages (might need inspection) */
            /* This selector targets the container Streamlit usually wraps messages in */
            div[data-testid="stVerticalBlock"] div:has(> [data-testid="stChatMessage"]):has([data-testid="chatAvatarIcon-user"]) [data-testid="stChatMessage"] {
                background-color: #dcf8c6; /* Light green, similar to WhatsApp */
                margin-left: auto; /* Align to the right */
                border-bottom-right-radius: 0; /* 'Tail' effect */
            }
            /* Alternatively, if the above is too complex/brittle, target based on content alignment Streamlit might apply */
            /* This is less reliable */
             [data-testid="stChatMessage"]:has(div[style*="text-align: right"]) {
                 /* background-color: #dcf8c6; */
                 /* margin-left: auto; */
             }


            /* Style assistant messages */
            div[data-testid="stVerticalBlock"] div:has(> [data-testid="stChatMessage"]):has([data-testid="chatAvatarIcon-assistant"]) [data-testid="stChatMessage"] {
                 background-color: #ffffff; /* White background */
                 margin-right: auto; /* Align to the left */
                 border-bottom-left-radius: 0; /* 'Tail' effect */
            }
             /* Alternatively, if the above is too complex/brittle */
             [data-testid="stChatMessage"]:has(div[style*="text-align: left"]) {
                 /* background-color: #ffffff; */
                 /* margin-right: auto; */
             }

            /* Add Avatars (using emojis here, could use background-image with URLs/base64) */
            [data-testid="chatAvatarIcon-user"]::after {
                content: '👤';
                font-size: 1.5em;
                margin-right: 5px; /* Adjust spacing */
            }
            [data-testid="chatAvatarIcon-assistant"]::after {
                content: '🤖';
                font-size: 1.5em;
                 margin-right: 5px; /* Adjust spacing */
            }

             /* Style the chat input area */
            [data-testid="stChatInput"] {
                background-color: #f0f2f6; /* Light grey background */
                border-top: 1px solid #e0e0e0;
                padding: 10px 15px;
            }
             /* Target the actual text input field within stChatInput */
            [data-testid="stChatInput"] textarea {
                 border: 1px solid #ccc;
                 border-radius: 15px;
                 padding: 8px 12px;
            }
            /* Style the send button (if possible - selector might be tricky) */
            [data-testid="stChatInput"] button {
                border-radius: 50%; /* Make it round */
                /* Add other button styling */
            }

        </style>
    """, unsafe_allow_html=True)

# Load OpenAI API key securely from Streamlit secrets
os.environ["OPENAI_API_KEY"] = st.secrets["api_key"]



from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate

# Load or build the vectorstore from watt-docs.md
@st.cache_resource
def load_db():
    if os.path.exists("watt_docs_index"):
        return FAISS.load_local(
            "watt_docs_index",
            OpenAIEmbeddings(),
            allow_dangerous_deserialization=True
        )
    with open("superteam_security.md", "r", encoding="utf-8") as f:
        docs = f.read()
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    texts = splitter.split_text(docs)
    embeddings = OpenAIEmbeddings()
    db = FAISS.from_texts(texts, embeddings)
    db.save_local("watt_docs_index")
    return db


def main():
    # st.sidebar.image("logo.png", width=200)
    # Title as hyperlink
    # st.markdown("# :red[Solana Security Chatbot]")
    st.markdown("### Ask questions about Solana Security.")
    db = load_db()
    link_only_prompt = PromptTemplate(
        template="""You are a helpful assistant.
If the user specifically asks for a link or URL (e.g., "Discord link", "provide the URL"), return *only* the URL with no explanation.
If the user asks any other question, provide a full, descriptive answer using the context, and include URLs only if they are essential to the answer.

Question: {question}
Context:
{context}

Answer:""",
        input_variables=["question", "context"]
    )
    # Set up conversational retrieval with memory
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    conv_chain = ConversationalRetrievalChain.from_llm(
        llm=ChatOpenAI(model_name="gpt-4.1-nano-2025-04-14", temperature=0),
        retriever=db.as_retriever(search_kwargs={"k": 5}),
        memory=memory,
        combine_docs_chain_kwargs={"prompt": link_only_prompt}
    )

    # Initialize chat messages
    if 'messages' not in st.session_state:
        st.session_state['messages'] = [
        {"role": "assistant", "content": "Hi! Ask me anything about Solana security and I would answer based on my the knowledge on the contents of this App."}
    ]

    # Display chat messages
    for msg in st.session_state['messages']:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # Get user input
    query = st.chat_input("Enter your question:")
    if query:
        # Record user message
        st.session_state['messages'].append({"role": "user", "content": query})
        # Generate and display assistant response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                result = conv_chain({"question": query})
                answer = result["answer"]
                st.write(answer)
        # Record assistant message
        st.session_state['messages'].append({"role": "assistant", "content": answer})

    

# if __name__ == "__main__":
def display_chatbot():
    main()
