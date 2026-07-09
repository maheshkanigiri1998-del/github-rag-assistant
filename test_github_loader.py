import os
from dotenv import load_dotenv
from llama_index.readers.github import GithubRepositoryReader, GithubClient

from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.llms.ollama import Ollama
from llama_index.core import VectorStoreIndex, Settings

# ====================== LOAD TOKEN ======================
load_dotenv()
github_token = os.getenv("GITHUB_TOKEN")

if not github_token:
    print("ERROR: GITHUB_TOKEN not found in .env file")
    exit()

print("Token loaded successfully. Connecting to GitHub...")

# ====================== LOAD DOCUMENTS ======================
github_client = GithubClient(github_token=github_token, verbose=True)

reader = GithubRepositoryReader(
    github_client=github_client,
    owner="githubtraining",
    repo="hellogitworld",
    use_parser=False,
    verbose=True,
    filter_file_extensions=(
        [".png", ".jpg", ".jpeg", ".gif", ".svg", ".ico", ".pdf", ".zip"],
        GithubRepositoryReader.FilterType.EXCLUDE,
    ),
)

documents = reader.load_data(branch="master")
print(f"Loaded {len(documents)} documents from GitHub.")

# ====================== SETUP OLLAMA ======================
Settings.embed_model = OllamaEmbedding(model_name="nomic-embed-text")
Settings.llm = Ollama(model="llama3.2", temperature=0.1, request_timeout=120.0)

# ====================== CREATE INDEX ======================
print("Creating vector index...")
index = VectorStoreIndex.from_documents(documents)
query_engine = index.as_query_engine()
print("RAG system is ready!\n")

# ====================== INTERACTIVE QUESTION LOOP ======================
print("You can now ask questions about the repository.")
print("Type 'exit' to quit.\n")

while True:
    question = input("Ask a question: ")
    
    if question.lower() in ["exit", "quit", "q"]:
        print("Goodbye!")
        break
    
    if question.strip() == "":
        continue
    
    print("\nThinking...")
    response = query_engine.query(question)
    
    # Print Answer
    print(f"\nAnswer: {response}")
    
    # ====================== NEW: SOURCE CITATIONS ======================
    print("\nSources:")
    if response.source_nodes:
        for node in response.source_nodes:
            file_path = node.metadata.get("file_path", "Unknown file")
            print(f"  - {file_path}")
    else:
        print("  - No sources found")
    
    print("-" * 60)