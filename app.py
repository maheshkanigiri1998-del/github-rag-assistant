import streamlit as st
from dotenv import load_dotenv
import os

from llama_index.readers.github import (
    GithubRepositoryReader, 
    GithubClient, 
    GitHubIssuesClient, 
    GitHubRepositoryIssuesReader
)
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.llms.ollama import Ollama
from llama_index.core import (
    VectorStoreIndex, 
    Settings, 
    StorageContext, 
    load_index_from_storage,
    PromptTemplate
)

# ====================== PAGE CONFIG ======================
st.set_page_config(page_title="GitHub RAG Assistant", page_icon="🤖", layout="wide")

st.title("🤖 GitHub RAG Assistant")
st.caption("Chat with any GitHub repository using your local AI (Ollama)")

# ====================== SETUP OLLAMA ======================
@st.cache_resource
def setup_models():
    Settings.embed_model = OllamaEmbedding(model_name="nomic-embed-text")
    Settings.llm = Ollama(model="llama3.2", temperature=0.1, request_timeout=120.0)
    return True

setup_models()

# ====================== SESSION STATE ======================
if "messages" not in st.session_state:
    st.session_state.messages = []
if "query_engine" not in st.session_state:
    st.session_state.query_engine = None
if "current_repo" not in st.session_state:
    st.session_state.current_repo = None

# ====================== SIDEBAR ======================
with st.sidebar:
    st.header("📁 Repository Settings")
    
    owner = st.text_input("Owner / Organization", value="githubtraining")
    repo = st.text_input("Repository Name", value="hellogitworld")
    branch = st.text_input("Branch", value="master")
    
    if st.button("Load & Index Repository", type="primary", use_container_width=True):
        with st.spinner(f"Loading {owner}/{repo}..."):
            try:
                github_token = os.getenv("GITHUB_TOKEN")
                if not github_token:
                    st.error("❌ GITHUB_TOKEN not found in .env file")
                    st.stop()

                # Create folder to save index
                persist_dir = f"./storage/{owner}_{repo}"
                os.makedirs(persist_dir, exist_ok=True)

                github_client = GithubClient(github_token=github_token, verbose=False)

                # Check if saved index exists
                if os.path.exists(os.path.join(persist_dir, "docstore.json")):
                    storage_context = StorageContext.from_defaults(persist_dir=persist_dir)
                    index = load_index_from_storage(storage_context)
                    st.info("✅ Loaded index from saved data (faster)")

                else:
                    # Load repository files
                    repo_reader = GithubRepositoryReader(
                        github_client=github_client,
                        owner=owner,
                        repo=repo,
                        use_parser=False,
                        verbose=False,
                        filter_file_extensions=(
                            [".png", ".jpg", ".jpeg", ".gif", ".svg", ".ico", ".pdf", ".zip"],
                            GithubRepositoryReader.FilterType.EXCLUDE,
                        ),
                    )
                    repo_documents = repo_reader.load_data(branch=branch)

                    # Load Issues & Pull Requests
                    issues_client = GitHubIssuesClient(github_token=github_token, verbose=False)
                    issues_reader = GitHubRepositoryIssuesReader(
                        github_client=issues_client,
                        owner=owner,
                        repo=repo,
                        verbose=False
                    )
                    issues_documents = issues_reader.load_data()

                    documents = repo_documents + issues_documents

                    if not documents:
                        st.error("❌ No documents found.")
                        st.stop()

                    # Create new index
                    index = VectorStoreIndex.from_documents(documents)

                    # Save index to disk
                    index.storage_context.persist(persist_dir=persist_dir)
                    st.success(f"✅ Index created and saved! ({len(documents)} documents)")

                # ====================== STRICT PROMPT (Anti-Hallucination) ======================
                qa_prompt = PromptTemplate(
                    "You are a helpful assistant that answers questions **only** using the provided context from the GitHub repository.\n"
                    "If the answer cannot be found in the context, clearly say: 'I don't have enough information in the repository to answer this question.'\n\n"
                    "Context:\n{context_str}\n\n"
                    "Question: {query_str}\n"
                    "Answer: "
                )

                st.session_state.query_engine = index.as_query_engine(text_qa_template=qa_prompt)
                st.session_state.current_repo = f"{owner}/{repo}"
                st.session_state.messages = []

            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

    # Show currently loaded repository
    if st.session_state.current_repo:
        st.info(f"📌 Currently chatting with: **{st.session_state.current_repo}**")

    # Clear Chat Button
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# ====================== MAIN CHAT ======================
st.subheader("💬 Chat with the Repository")

if not st.session_state.query_engine:
    st.info("👈 Please load a repository from the sidebar to start chatting.")
else:
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if "sources" in message and message["sources"]:
                with st.expander("📄 Sources"):
                    for source in message["sources"]:
                        st.write(f"- `{source}`")
    # Chat input
    if prompt := st.chat_input("Ask something about the repository..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Get AI response with error handling
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    # Safety check
                    if st.session_state.query_engine is None:
                        response_text = "⚠️ Please load a repository first before asking questions."
                        sources = []
                    else:
                        response = st.session_state.query_engine.query(prompt)
                        
                        # Extract sources
                        sources = [node.metadata.get("file_path", "Unknown") 
                                  for node in response.source_nodes]
                        
                        response_text = str(response)

                except Exception as e:
                    response_text = f"❌ Sorry, something went wrong while answering: {str(e)}"
                    sources = []

                st.markdown(response_text)
                
                if sources:
                    with st.expander("📄 Sources"):
                        for source in sources:
                            st.write(f"- `{source}`")

        # Save to history
        st.session_state.messages.append({
            "role": "assistant",
            "content": response_text,
            "sources": sources
        })