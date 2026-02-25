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
        import google.generativeai as genai
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        model = genai.GenerativeModel('gemini-pro')
        return model
    else:
        st.error("I need an API key to summarize! Please add GEMINI_API_KEY to your Streamlit secrets.")
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
                    import requests
                    from bs4 import BeautifulSoup
                    
                    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
                    response = requests.get(url_input, headers=headers, timeout=10)
                    response.raise_for_status()
                    
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    # Remove script and style elements
                    for script in soup(["script", "style", "nav", "footer", "header"]):
                        script.decompose()
                    
                    # Get text
                    text = soup.get_text(separator='\n', strip=True)
                    # Clean up whitespace
                    lines = (line.strip() for line in text.splitlines())
                    text = '\n'.join(line for line in lines if line)
                    
                    if not text or len(text) < 100:
                        st.error("I couldn't extract enough text from that URL. The site might be blocking me or require JavaScript.")
                        logger.error("Insufficient text extracted from URL")
                    else:
                        logger.info(f"Anna extracted {len(text)} characters from the page")
                        llm = get_llm()
                        
                        if llm:
                            logger.info("Anna is generating the summary...")
                            prompt_text = f"""You are Anna, a professional AI assistant. Summarize the following content in a clear, organized manner.
Provide:
- A brief overview (2-3 sentences)
- 3-5 key points as bullet points
- A concluding insight

Keep your tone professional yet approachable.

Content:
{text[:15000]}"""
                            response = llm.generate_content(prompt_text)
                            summary = response.text
                            
                            st.success("✅ Summary complete!")
                            st.markdown("### 📋 Summary")
                            st.markdown(summary)
                            st.markdown(f"**Source:** {url_input}")
                            logger.info("Anna completed the summarization successfully")
                
                except requests.exceptions.RequestException as e:
                    st.error(f"I couldn't access that URL. The site might be blocking requests or the URL is invalid. Error: {str(e)}")
                    logger.error(f"Request error: {str(e)}")
                except ImportError as e:
                    st.error(f"I'm missing a required library: {str(e)}. Please check the requirements.txt file.")
                    logger.error(f"Import error: {str(e)}")
                except Exception as e:
                    st.error(f"I hit a snag while processing that URL. Error: {str(e)}")
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
                            logger.info("Anna is generating the summary...")
                            prompt_text = f"""You are Anna, a professional AI assistant. Summarize the following document in a clear, organized manner.
Provide:
- A brief overview (2-3 sentences)
- 3-5 key points as bullet points
- A concluding insight

Keep your tone professional yet approachable.

Document:
{text[:15000]}"""
                            response = llm.generate_content(prompt_text)
                            summary = response.text
                            
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
