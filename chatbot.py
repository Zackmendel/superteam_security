import os
import streamlit as st

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
        st.session_state['messages'] = []

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
