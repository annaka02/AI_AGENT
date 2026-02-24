# ANNA - Automated Network & Narrative Assistant

Hi! I'm Anna, your AI-powered content summarization assistant. I can help you quickly digest web articles and PDF documents using advanced AI models.

## Features

- 📰 **URL Summarization**: Paste any article URL and get a concise summary
- 📄 **PDF Summarization**: Upload PDF files and extract key insights
- 🤖 **AI-Powered**: Uses OpenAI GPT or Amazon Bedrock Claude 3 Sonnet
- 📊 **Technical Logs**: View detailed process logs for transparency
- 🎨 **Clean UI**: Professional Streamlit interface with tabs and organized layout

## Prerequisites

- Python 3.8 or higher
- An API key for either:
  - OpenAI (GPT-3.5 or GPT-4)
  - Amazon Bedrock (with AWS credentials)

## Local Installation & Setup

### 1. Clone or Download the Repository

```bash
git clone <your-repo-url>
cd AI_AGENT
```

### 2. Create a Virtual Environment (Recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Secrets

Create a `.streamlit` folder in your project directory and add a `secrets.toml` file:

```bash
mkdir .streamlit
```

Create `.streamlit/secrets.toml` with one of the following configurations:

**Option A: Using OpenAI**
```toml
OPENAI_API_KEY = "sk-your-openai-api-key-here"
```

**Option B: Using Amazon Bedrock**
```toml
AWS_ACCESS_KEY_ID = "your-aws-access-key-id"
AWS_SECRET_ACCESS_KEY = "your-aws-secret-access-key"
AWS_REGION = "us-east-1"
```

### 5. Run the Application

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## Deployment to Streamlit Community Cloud

### 1. Prepare Your GitHub Repository

1. Create a new repository on GitHub
2. Initialize git in your project folder (if not already done):
   ```bash
   git init
   git add .
   git commit -m "Initial commit - ANNA application"
   ```
3. Add your GitHub repository as remote:
   ```bash
   git remote add origin https://github.com/your-username/your-repo-name.git
   git branch -M main
   git push -u origin main
   ```

**Important**: Add `.streamlit/secrets.toml` to your `.gitignore` file to avoid committing secrets:
```bash
echo ".streamlit/secrets.toml" >> .gitignore
```

### 2. Deploy to Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with your GitHub account
3. Click "New app"
4. Select your repository, branch (main), and main file path (`app.py`)
5. Click "Deploy"

### 3. Configure Secrets in Streamlit Cloud

1. In your Streamlit Cloud dashboard, click on your deployed app
2. Click the "⋮" menu (three dots) and select "Settings"
3. Go to the "Secrets" section
4. Paste your secrets in TOML format:

**For OpenAI:**
```toml
OPENAI_API_KEY = "sk-your-openai-api-key-here"
```

**For Amazon Bedrock:**
```toml
AWS_ACCESS_KEY_ID = "your-aws-access-key-id"
AWS_SECRET_ACCESS_KEY = "your-aws-secret-access-key"
AWS_REGION = "us-east-1"
```

5. Click "Save"
6. Your app will automatically restart with the new secrets

## Usage Guide

### Summarizing a Web Article

1. Click on the "📰 Summarize Link" tab
2. Paste the URL of the article you want to summarize
3. Click "Summarize URL"
4. Wait for Anna to fetch and analyze the content
5. View your summary with key points and insights

### Summarizing a PDF

1. Click on the "📄 Summarize PDF" tab
2. Upload your PDF file using the file uploader
3. Click "Summarize PDF"
4. Wait for Anna to extract and analyze the text
5. View your summary with key points and insights

### Viewing Technical Logs

- Expand the "🔧 Technical Logs" section at the bottom of the page
- View detailed process information and any error messages
- Useful for troubleshooting issues

## Troubleshooting

### "I need an API key to summarize!"
- Make sure you've added your API key to `.streamlit/secrets.toml` (local) or Streamlit Cloud secrets
- Verify the key name matches exactly: `OPENAI_API_KEY` or `AWS_ACCESS_KEY_ID`/`AWS_SECRET_ACCESS_KEY`

### "I couldn't extract any text from that URL"
- The website might be behind a paywall
- The site might require JavaScript rendering (newspaper3k has limitations)
- Try a different URL or use the PDF upload feature

### "I couldn't extract any text from that PDF"
- The PDF might be image-based and require OCR
- Try converting the PDF to a text-based format first

### Import Errors
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Try upgrading pip: `pip install --upgrade pip`

## Project Structure

```
AI_AGENT/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── README.md             # This file
└── .streamlit/
    └── secrets.toml      # API keys (local only, not committed)
```

## Technologies Used

- **Streamlit**: Web application framework
- **LangChain**: LLM orchestration framework
- **OpenAI / Amazon Bedrock**: AI models for summarization
- **newspaper3k**: Web article scraping
- **PyMuPDF**: PDF text extraction
- **Python logging**: Process tracking and debugging

## Security Notes

- Never commit your `secrets.toml` file to GitHub
- Always use environment variables or Streamlit secrets for API keys
- Rotate your API keys regularly
- Monitor your API usage to avoid unexpected charges

## Support

If you encounter any issues or have questions, check the Technical Logs in the app for detailed error messages. Anna will do her best to explain what went wrong in plain language.

## License

This project is open source and available for personal and commercial use.

---

*Built with ❤️ by Anna*
