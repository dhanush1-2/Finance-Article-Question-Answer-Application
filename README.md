# Finance Article Question & Answer Application

This is a Streamlit-based web application that allows users to input a finance article URL and a question about the article. The application fetches the article content, processes it using a Retrieval-Augmented Generation (RAG) pipeline powered by Grok (xAI), and provides an AI-generated answer.

## Features
- **Article Fetching**: Retrieves text content from finance article URLs using web scraping.
- **Question Answering**: Uses a RAG pipeline with Grok LLM to answer user queries based on article content.
- **User Interface**: Built with Streamlit for an interactive, web-based experience.
- **Text Processing**: Splits articles into chunks, generates embeddings, and retrieves relevant context for accurate answers.
- **Error Handling**: Includes robust error checking for URL fetching, text processing, and API calls.

## Project Structure
- **`app.py`**: The main Streamlit application script that handles the UI and integrates the RAG pipeline.
- **`nlp_pipeline.py`**: Contains the RAG pipeline logic, including text splitting, embeddings, and Grok LLM integration.
- **`news_scraper.py`**: Handles article fetching and cleaning using `requests` and `BeautifulSoup`.

## Prerequisites
- Python 3.9 or higher
- A Grok API key from xAI (set as an environment variable `GROQ_API_KEY`)
- Internet connection for fetching articles and API calls

## Installation

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd <repository-folder>

2. **Create a Virual Environment**
    python -m venv venv
    source venv/bin/activate  
    On Windows: venv\Scripts\activate

3. **Install Dependencies**
    pip install -r requirements.txt

4. **Set Up Environment Variables**
    GROQ_API_KEY=<your-grok-api-key>

## Usage
1. **Run the Application**
    streamlit run app.py
    Open your browser and navigate to http://localhost:8501.

2. **Interact with the App**
   - Enter a finance article URL (e.g., from Moneycontrol).
   - Type a question related to the article.
   - Click "Get Answer" to receive an AI-generated response.

# How It Works

## Article Fetching (`news_scraper.py`):
- Uses `requests` and `BeautifulSoup` to scrape and clean article text from the provided URL.
- Removes unwanted HTML elements (scripts, styles, etc.) and extracts paragraph text.

## RAG Pipeline (`nlp_pipeline.py`):
- Splits the article into manageable chunks using `CharacterTextSplitter`.
- Creates embeddings with `HuggingFaceEmbeddings` and indexes them with `FAISS`.
- Retrieves relevant chunks based on the user query.
- Augments the prompt with context and queries the Grok LLM (`ChatGroq`) for an answer.

## Streamlit UI (`app.py`):
- Provides a simple interface for inputting URLs and questions.
- Displays the AI-generated answer and an optional article preview.

## Dependencies
The application relies on the following Python packages:

```
streamlit==1.31.0  # Web interface
requests==2.31.0  # Fetch articles
beautifulsoup4==4.12.3  # Parse HTML
langchain==0.1.9  # LLM framework
langchain-community==0.0.24  # LangChain extensions
langchain-groq==0.0.1  # Grok LLM integration
langchain-huggingface==0.0.1  # Hugging Face embeddings
faiss-cpu==1.7.4  # Vector storage and search
python-dotenv==1.0.1  # Environment variables
```

To install dependencies, ensure they are listed in `requirements.txt` and run:

```bash
pip install -r requirements.txt
```

## Troubleshooting
- **"Failed to fetch article"**: Check the URL validity or internet connection.
- **"GROQ_API_KEY not found"**: Ensure the environment variable is set correctly.
- **No answer generated**: Verify the article contains relevant content for the question.

## Development
- **Author:** D
- **Date:** February 25, 2025
- **Powered By:** Grok (xAI), Streamlit

## License
This project is for educational purposes and is not licensed for commercial use without proper attribution and compliance with xAI's terms of service.

## Future Improvements
- Add support for multiple article sources.
- Enhance error messaging with specific diagnostics.
- Implement caching for faster repeated queries.

This README consolidates all necessary information for your project in VS Code.
