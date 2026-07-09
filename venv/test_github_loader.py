import os
from dotenv import load_dotenv
from llama_index.readers.github import GithubRepositoryReader, GithubClient

# Load the secret token from .env file
load_dotenv()
github_token = os.getenv("GITHUB_TOKEN")

if not github_token:
    print("ERROR: GITHUB_TOKEN not found in .env file")
    exit()

print("Token loaded successfully. Connecting to GitHub...")

# Create GitHub client
github_client = GithubClient(
    github_token=github_token,
    verbose=True
)

# Create the repository reader
reader = GithubRepositoryReader(
    github_client=github_client,
    owner="run-llama",
    repo="llama_index",
    use_parser=False,
    verbose=True,
    filter_file_extensions=(
        [".png", ".jpg", ".jpeg", ".gif", ".svg", ".ico", ".pdf", ".zip"],
        GithubRepositoryReader.FilterType.EXCLUDE,
    ),
)

print("Loading documents from GitHub repository...")

# Load the data
documents = reader.load_data(branch="main")

print(f"\nSUCCESS! Loaded {len(documents)} documents.")
print("=" * 60)

if documents:
    first_doc = documents[0]
    print("First document came from:")
    print(first_doc.metadata)
    print("\nFirst 500 characters of text:")
    print(first_doc.text[:500])
else:
    print("No documents were loaded.")