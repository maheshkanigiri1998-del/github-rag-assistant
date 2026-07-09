# 🤖 GitHub RAG Assistant

A powerful **Retrieval-Augmented Generation (RAG)** application that allows you to **chat with any GitHub repository** using your local AI models. It can understand code, README files, Issues, and Pull Requests from any public repository.

Built completely with **local AI** (no OpenAI or paid APIs required).

## ✨ Key Features

- Load any public GitHub repository (Files + README + Issues + Pull Requests)
- Create embeddings and vector index using **local Ollama models**
- Persistent index storage (loads faster on subsequent runs)
- Interactive chat interface with **source citations**
- Strict prompting to minimize hallucination
- Clean and user-friendly Streamlit interface
- Fully local and private

## 🛠 Tech Stack

| Component          | Technology                              |
|--------------------|-----------------------------------------|
| Frontend           | Streamlit                               |
| RAG Framework      | LlamaIndex                              |
| LLM & Embeddings   | Ollama (`llama3.2` + `nomic-embed-text`) |
| Data Source        | GitHub API                              |
| Language           | Python                                  |

## 🚀 How to Run the Project

### Prerequisites

- Python 3.10 or higher
- [Ollama](https://ollama.com/) installed and running
- GitHub Personal Access Token (even for public repositories)

### Installation (All Steps in One Go)

Copy and paste all the commands below one by one:

```bash
# Step 1: Clone the repository
git clone https://github.com/maheshkanigiri1998-del/github-rag-assistant.git
cd github-rag-assistant

# Step 2: Create virtual environment and install dependencies
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

# Step 3: Pull required Ollama models
ollama pull llama3.2
ollama pull nomic-embed-text

# Step 4: Create .env file and add your GitHub token
# Create a file named .env and paste this inside:
# GITHUB_TOKEN=ghp_your_token_here

# Step 5: Run the application
python -m streamlit run app.py
Note: After cloning, create a .env file in the root folder and add your GitHub token like this:envGITHUB_TOKEN=ghp_your_token_here
How to create a GitHub token?
Go to GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic) → Generate new token → Select only public_repo scope.
The app will open in your browser at http://localhost:8501.

Main chat interface
Sidebar with repository settings
Answers with sources


🧠 How It Works

The user enters a GitHub repository in the sidebar.
The app fetches files, README, Issues, and Pull Requests using the GitHub API.
Documents are converted into embeddings using nomic-embed-text.
A vector index is created and saved locally for faster future access.
The user can ask questions in natural language.
The system retrieves relevant context and generates answers using llama3.2.
Sources are displayed for every answer for transparency and verification.


📌 Current Limitations

Works best with small to medium-sized repositories
Requires Ollama to be running locally
Needs a GitHub Personal Access Token
Performance depends on the local machine’s hardware


🔮 Future Improvements

Support for multiple repositories at once
Chat history persistence
Better chunking and metadata handling
Advanced RAG techniques (reranking, hybrid search)
One-click deployment option
Dark mode support


👨‍💻 Author
Mahesh Kanigiri
This project was built to demonstrate skills in:

Building end-to-end RAG applications
Integrating LLMs with external data sources (GitHub API)
Creating clean and functional user interfaces using Streamlit
Working with local AI models using Ollama


🙏 Acknowledgements

LlamaIndex
Ollama
Streamlit


📄 License
This project is licensed under the MIT License.
text
