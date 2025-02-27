from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.text_splitter import CharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from news_scraper import fetch_article

from langchain_community.vectorstores import FAISS
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv('GROQ_API_KEY')
if not API_KEY:
    raise ValueError("GROQ_API_KEY not found in environment variables")

# Initialize Groq LLM
try:
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0.6,
        api_key=API_KEY
    )
except Exception as e:
    raise Exception(f"Failed to initialize ChatGroq: {str(e)}")


def split_article_into_chunks(article_text, chunk_size=500):
    try:
        text_splitter = CharacterTextSplitter(
            chunk_size=chunk_size, chunk_overlap=50)
        return text_splitter.split_text(article_text)
    except Exception as e:
        print(f"Error splitting article: {str(e)}")
        return [article_text]


def create_embeddings_and_index(chunks):
    try:
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        return FAISS.from_texts(chunks, embeddings)
    except Exception as e:
        raise Exception(f"Failed to create embeddings/index: {str(e)}")


def retrieve_relevant_chunks(query, vector_store, k=3):
    try:
        docs = vector_store.similarity_search(query, k=k)
        return [doc.page_content for doc in docs]
    except Exception as e:
        print(f"Error retrieving chunks: {str(e)}")
        return []


def create_augmented_prompt(query, relevant_chunks):
    context = "\n".join(
        relevant_chunks) if relevant_chunks else "No relevant context found"
    return (
        "You are an AI model that reads and answers questions based on finance articles.\n\n"
        f"Context:\n{context}\n\n"
        f"User's Question: {query}\nAnswer:"
    )


def answer_query_with_rag(query, article_text):
    try:
        if not article_text:
            return "Error: No article text provided"

        chunks = split_article_into_chunks(article_text)
        if not chunks:
            return "Error: Failed to process article text"

        vector_store = create_embeddings_and_index(chunks)
        relevant_chunks = retrieve_relevant_chunks(query, vector_store)
        augmented_prompt = create_augmented_prompt(query, relevant_chunks)

        response = llm.invoke(augmented_prompt)
        return response

    except Exception as e:
        return f"Error processing query: {str(e)}"


# Main execution
# if __name__ == "__main__":
#     # Assuming this is your fetch_article module
#     url = 'https://www.moneycontrol.com/news/opinion/trump-s-dollar-dilemma-12949689.html#goog_rewarded'
#     article_text = fetch_article(url)
#     if article_text:
#         answer = answer_query_with_rag(
#             'What does trump say about current administration.', article_text)
#         print("Summary:")
#         print(answer)
#     else:
#         print("Failed to fetch article")
