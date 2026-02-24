import streamlit as st
import logging
from io import StringIO
import sys

# Configure logging
log_stream = StringIO()
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    handlers=[logging.StreamHandler(log_stream), logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

# Page config
st.set_page_config(page_title="ANNA - AI Assistant", page_icon="🤖", layout="wide")

# Sidebar
with st.sidebar:
    st.title("🤖 ANNA")
    st.markdown("**Automated Network & Narrative Assistant**")
    st.markdown("---")
    st.markdown("### About Anna")
    st.markdown("""
    Hi! I'm Anna, your AI assistant for summarizing content.
    
    I can help you:
    - 📰 Summarize web articles from URLs
    - 📄 Extract and summarize PDF documents
    
    I'm professional, organized, and here to make your life easier.
    """)
    st.markdown("---")
    st.markdown("*Created by Anna*")

def get_llm():
    """Initialize LLM based on available API keys"""
    if "GEMINI_API_KEY" in st.secrets:
        logger.info("Anna is using Google Gemini for summarization")
        from langchain_google_genai import ChatGoogleGenerativeAI
        return ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=st.secrets["GEMINI_API_KEY"], temperature=0.3, convert_system_message_to_human=True)
    elif "OPENAI_API_KEY" in st.secrets:
        logger.info("Anna is using OpenAI for summarization")
        from langchain_openai import ChatOpenAI
        return ChatOpenAI(model="gpt-3.5-turbo", api_key=st.secrets["OPENAI_API_KEY"], temperature=0.3)
    else:
        st.error("I need an API key to summarize! Please add GEMINI_API_KEY or OPENAI_API_KEY to your Streamlit secrets.")
        logger.error("No API keys found in secrets")
        return None

# Main content
st.title("ANNA - Your Content Summarization Assistant")
st.markdown("Let me help you digest information quickly and efficiently.")

# Tabs
tab1, tab2 = st.tabs(["📰 Summarize Link", "📄 Summarize PDF"])

# Tab 1: URL Summarization
with tab1:
    st.header("Summarize a Web Article")
    url_input = st.text_input("Enter the URL of the article:", placeholder="https://example.com/article")
    
    if st.button("Summarize URL", key="url_btn"):
        if not url_input:
            st.warning("Please enter a URL first.")
        else:
            log_stream.truncate(0)
            log_stream.seek(0)
            
            with st.spinner("Anna is reading the article..."):
                try:
                    logger.info(f"Anna is fetching content from: {url_input}")
                    from newspaper import Article
                    article = Article(url_input)
                    article.download()
                    article.parse()
                    
                    if not article.text:
                        st.error("I couldn't extract any text from that URL. It might be behind a paywall or require JavaScript.")
                        logger.error("No text extracted from URL")
                    else:
                        logger.info(f"Anna extracted {len(article.text)} characters from the article")
                        llm = get_llm()
                        
                        if llm:
                            from langchain.prompts import ChatPromptTemplate
                            from langchain.schema.output_parser import StrOutputParser
                            
                            prompt = ChatPromptTemplate.from_messages([
                                ("system", """You are Anna, a professional AI assistant. Summarize the following article in a clear, organized manner. 
                                Provide:
                                - A brief overview (2-3 sentences)
                                - 3-5 key points as bullet points
                                - A concluding insight
                                
                                Keep your tone professional yet approachable."""),
                                ("user", "Article text:\n\n{text}")
                            ])
                            
                            chain = prompt | llm | StrOutputParser()
                            logger.info("Anna is generating the summary...")
                            summary = chain.invoke({"text": article.text[:8000]})
                            
                            st.success("✅ Summary complete!")
                            st.markdown("### 📋 Summary")
                            st.markdown(summary)
                            if article.title:
                                st.markdown(f"**Original Title:** {article.title}")
                            logger.info("Anna completed the summarization successfully")
                
                except ImportError as e:
                    st.error(f"I'm missing a required library: {str(e)}. Please check the requirements.txt file.")
                    logger.error(f"Import error: {str(e)}")
                except Exception as e:
                    st.error(f"I hit a snag while processing that URL. The site might be blocking me, or there could be a paywall. Error: {str(e)}")
                    logger.error(f"Error processing URL: {str(e)}")

# Tab 2: PDF Summarization
with tab2:
    st.header("Summarize a PDF Document")
    uploaded_file = st.file_uploader("Upload a PDF file:", type=["pdf"])
    
    if st.button("Summarize PDF", key="pdf_btn"):
        if not uploaded_file:
            st.warning("Please upload a PDF file first.")
        else:
            log_stream.truncate(0)
            log_stream.seek(0)
            
            with st.spinner("Anna is reading the PDF..."):
                try:
                    logger.info(f"Anna is processing PDF: {uploaded_file.name}")
                    import pdfplumber
                    
                    text = ""
                    with pdfplumber.open(uploaded_file) as pdf:
                        for page in pdf.pages:
                            text += page.extract_text() or ""
                    
                    if not text.strip():
                        st.error("I couldn't extract any text from that PDF. It might be an image-based PDF that needs OCR.")
                        logger.error("No text extracted from PDF")
                    else:
                        logger.info(f"Anna extracted {len(text)} characters from the PDF")
                        llm = get_llm()
                        
                        if llm:
                            from langchain.prompts import ChatPromptTemplate
                            from langchain.schema.output_parser import StrOutputParser
                            
                            prompt = ChatPromptTemplate.from_messages([
                                ("system", """You are Anna, a professional AI assistant. Summarize the following document in a clear, organized manner. 
                                Provide:
                                - A brief overview (2-3 sentences)
                                - 3-5 key points as bullet points
                                - A concluding insight
                                
                                Keep your tone professional yet approachable."""),
                                ("user", "Document text:\n\n{text}")
                            ])
                            
                            chain = prompt | llm | StrOutputParser()
                            logger.info("Anna is generating the summary...")
                            summary = chain.invoke({"text": text[:8000]})
                            
                            st.success("✅ Summary complete!")
                            st.markdown("### 📋 Summary")
                            st.markdown(summary)
                            st.markdown(f"**File:** {uploaded_file.name}")
                            logger.info("Anna completed the summarization successfully")
                
                except ImportError as e:
                    st.error(f"I'm missing a required library: {str(e)}. Please check the requirements.txt file.")
                    logger.error(f"Import error: {str(e)}")
                except Exception as e:
                    st.error(f"I encountered an error while processing that PDF: {str(e)}")
                    logger.error(f"Error processing PDF: {str(e)}")

# Technical Logs
with st.expander("🔧 Technical Logs"):
    st.text(log_stream.getvalue())

# Footer
st.markdown("---")
st.markdown("*Anna is here to help. If something goes wrong, check the Technical Logs above for details.*")
