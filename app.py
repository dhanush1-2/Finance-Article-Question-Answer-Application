import streamlit as st
from nlp_pipeline import answer_query_with_rag, fetch_article  # Import your functions

# Streamlit app configuration
st.set_page_config(page_title="Finance Article Q&A",
                   page_icon="📈", layout="wide")

# Title and description
st.title("Finance Article Question & Answer")
st.markdown("""
    Enter a finance article URL and a question to get an AI-generated answer based on the article content.
""")

# Input fields
with st.form(key="input_form"):
    article_url = st.text_input(
        "Article URL",
        value="",
        help="Enter the full URL of a finance article"
    )
    user_query = st.text_input(
        "Your Question",
        value="",
        help="Ask a question about the article"
    )
    submit_button = st.form_submit_button(label="Get Answer")

# Process and display results
if submit_button:
    if not article_url or not user_query:
        st.error("Please provide both an article URL and a question.")
    else:
        with st.spinner("Fetching article and generating answer..."):
            # Fetch article text
            article_text = fetch_article(article_url)

            if not article_text:
                st.error(
                    "Failed to fetch article. Please check the URL and try again.")
            else:
                # Get answer from NLP pipeline
                answer = answer_query_with_rag(user_query, article_text)

                # Display results
                st.subheader("Answer:")
                if isinstance(answer, str) and answer.startswith("Error"):
                    st.error(answer)
                else:
                    # Extract content if it's an AIMessage object
                    answer_content = answer.content if hasattr(
                        answer, 'content') else str(answer)
                    st.success("Answer generated successfully!")
                    st.write(answer_content)

                # Optional: Display article preview
                with st.expander("View Article Preview"):
                    st.text(
                        f"Article Text (first 500 characters):\n{article_text[:500]}...")

# Footer
st.markdown("Developed by D")
st.markdown("Powered by Grok (xAI) and Streamlit | Date: February 25, 2025")
