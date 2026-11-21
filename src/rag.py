from dotenv import load_dotenv

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_groq import ChatGroq

from src.config import KNOWLEDGE_BASE_PATH, CHROMA_DB_PATH


# Load environment variables
load_dotenv()


# 1. Load Knowledge Base
def load_documents():

    documents = []

    for file_path in KNOWLEDGE_BASE_PATH.glob("*.txt"):
        with open(file_path, "r", encoding="utf-8") as file:
            text = file.read()
            documents.append({
                "source": file_path.name,
                "text": text
            })

    return documents


# 2. Split Documents into Chunks
def split_documents(documents):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    chunks = []

    for document in documents:
        document_chunks = splitter.split_text(document["text"])

        for chunk in document_chunks:
            chunks.append({
                "source": document["source"],
                "text": chunk
            })

    return chunks


# 3. Create Embeddings
def create_embeddings():

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-mpnet-base-v2"
    )

    return embeddings


# 4. Create Chroma Vector Database
def create_vector_store(chunks):

    embeddings = create_embeddings()
    texts = [chunk["text"] for chunk in chunks]
    metadatas = [{"source": chunk["source"]} for chunk in chunks]

    vectorstore = Chroma.from_texts(
        texts=texts,
        metadatas=metadatas,
        embedding=embeddings,
        persist_directory=str(CHROMA_DB_PATH)
    )

    return vectorstore


# 5. Load Existing Chroma Database
def load_vector_store():

    embeddings = create_embeddings()
    vectorstore = Chroma(
        persist_directory=str(CHROMA_DB_PATH),
        embedding_function=embeddings
    )

    return vectorstore


# 6. Create Retriever
def create_retriever(vectorstore):

    retriever = vectorstore.as_retriever(
        search_type="mmr",
        search_kwargs={
            "k": 4,
            "fetch_k": 10,
            "lambda_mult": 0.5
        }
    )

    return retriever


# 7. Search Relevant Documents
def search_documents(retriever, query):

    results = retriever.invoke(query)

    return results


# 8. Generate Career Answer
def ask_question(query):

    vectorstore = load_vector_store()

    retriever = create_retriever(
        vectorstore
    )

    documents = search_documents(
        retriever,
        query
    )

    if not documents:
        return ("I could not find relevant information in the career knowledge base.")

    # Combine retrieved chunks
    context = "\n\n".join(document.page_content for document in documents)

    # Create LLM
    llm = ChatGroq(model="openai/gpt-oss-120b")

    # Prompt
    prompt = f"""
You are an AI Student Career Assistant.

Help students with:

- Career guidance
- Placement preparation
- Learning roadmap
- Technical skills
- Interview preparation

Use ONLY the information provided
in the career knowledge below.

If the answer is not available
in the knowledge base, say:

"I could not find that information
in the career knowledge base."

Give the answer in simple and clear language.

Career Knowledge:

{context}

Student Question:

{query}

Answer:
"""

    # Generate answer
    response = llm.invoke(prompt)

    return response.content


# 9. Build Knowledge Base
def build_knowledge_base():

    documents = load_documents()
    print(f"\nDocuments loaded: {len(documents)}")

    chunks = split_documents(documents)
    print(f"Chunks created: {len(chunks)}")

    create_vector_store(chunks)
    print("\nChroma database created successfully!")


# 10. Testing
if __name__ == "__main__":

    # Build database first time
    build_knowledge_base()

    # Ask question
    question = input("\nAsk your career question: ")

    # Get answer
    answer = ask_question(question)
    print("\nAI Career Assistant Answer:")
    print(answer)