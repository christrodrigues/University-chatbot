# University Chatbot

The University Chatbot is an AI-powered conversational agent designed to assist students and faculty with various inquiries related to university services, courses, and campus life. It aims to provide quick and accurate responses to frequently asked questions, enhancing the overall experience for users. The chatbot can handle a range of topics, including admissions, course schedules, campus events, and more, making it a valuable resource for the university community.

## Features

- **RAG-based Architecture**: Uses Retrieval-Augmented Generation for accurate, context-aware responses
- **Interactive Web Interface**: Clean Streamlit-based chat interface
- **Real-time Processing**: Instant responses with source attribution
- **Semantic Search**: ChromaDB vector database for efficient document retrieval
- **Customizable Knowledge Base**: Easy to update with new university information

## Debugging and Querying a Chroma Vector Database

This project demonstrates how to use the `langchain` library to interact with a Chroma vector database for document storage and retrieval. It includes functionality to load a database, retrieve collection information, and perform similarity searches.

## Prerequisites

1. **Python**: Ensure you have Python 3.8 or higher installed.
2. **OpenAI API Key**: Get your API key from [OpenAI Platform](https://platform.openai.com/api-keys)
3. **Dependencies**: Install the required Python packages listed below:

   - `langchain_openai`
   - `langchain_community`
   - `langchain_text_splitters`
   - `python-dotenv`
   - `chromadb`
   - `streamlit`

   You can install these dependencies using `pip`:

   ```bash
   pip install langchain_openai langchain_community langchain_text_splitters python-dotenv chromadb streamlit
   ```

## Installation

1. **Clone the repository**:

   ```bash
   git clone <repository-url>
   cd university-chatbot
   ```

2. **Create a virtual environment**:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   Create a `.env` file in the project root directory:
   ```bash
   OPENAI_API_KEY=your_openai_api_key_here
   ```

## Project Structure

```
university-chatbot/
├── app.py              # Main Streamlit application
├── ingest.py           # Data ingestion and processing script
├── debug_db.py         # Database debugging utility
├── .env                # Environment variables (create this)
├── db/                 # ChromaDB vector database (auto-generated)
├── venv/               # Virtual environment
├── requirements.txt    # Project dependencies
└── README.md          # This file
```

## Usage

### Step 1: Data Ingestion

First, run the data ingestion script to scrape university web pages and create the vector database:

```bash
python ingest.py
```

This script will:

- Scrape content from specified university URLs
- Split documents into manageable chunks
- Generate embeddings using OpenAI
- Store embeddings in ChromaDB vector database

Expected output:

```
Loading documents...
Loaded 3 documents
Splitting documents...
Created 45 chunks
Creating vector store...
Vector store created and persisted!
```

### Step 2: Launch the Chatbot

Start the Streamlit web application:

```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

### Step 3: Interact with the Chatbot

You can now ask questions about the university. Try these examples:

- "What is Northeastern University known for?"
- "How do I apply for graduate programs?"
- "Tell me about campus life"
- "What are the admission requirements?"

## Configuration

### Modifying Data Sources

To add or change university web pages, edit the `urls` list in `ingest.py`:

```python
urls = [
    "https://www.northeastern.edu/",
    "https://www.northeastern.edu/campuses/boston/",
    "https://graduate.northeastern.edu/admissions-aid/how-to-apply/",
    # Add more URLs here
]
```

### Adjusting Text Processing

Modify chunk size and overlap in `ingest.py` for different processing strategies:

```python
splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,      # Adjust based on content complexity
    chunk_overlap=200,    # Overlap for context continuity
    separators=["\n\n", "\n", " ", ""]
)
```

### Changing the Language Model

Update the model configuration in `app.py`:

```python
llm = ChatOpenAI(
    model="gpt-4",        # Use gpt-4 for better quality
    temperature=0         # Keep at 0 for consistent responses
)
```

## Debugging and Maintenance

### Database Debugging

Use the included debugging script to inspect your vector database:

```bash
python debug_db.py
```

This will show:

- Total number of documents in the database
- Sample document content and metadata
- Search functionality test

### Resetting the Database

If you need to reset the vector database:

```bash
rm -rf db/
python ingest.py
```

### Common Issues

**"I don't know" responses:**

- Verify the `db/` folder exists and contains data
- Check that your OpenAI API key is valid
- Run `python debug_db.py` to inspect database content

**Import errors:**

```bash
pip install --upgrade langchain-openai langchain-community
```

**API rate limits:**

- Check your OpenAI usage limits
- Consider using `gpt-3.5-turbo` instead of `gpt-4`

## Performance Optimization

- **Chunk Size**: Larger chunks (1000+ tokens) often provide better context
- **Retrieval Count**: Adjust `k` parameter in retriever (4-6 works well)
- **Embedding Model**: Consider using different embedding models for cost optimization
- **Caching**: Streamlit's `@st.cache_resource` is used for efficient resource loading

## Technical Details

### RAG Pipeline

1. **Document Loading**: Web scraping using LangChain WebBaseLoader
2. **Text Splitting**: Recursive character text splitter with configurable parameters
3. **Embedding Generation**: OpenAI embeddings for semantic representation
4. **Vector Storage**: ChromaDB for persistent storage and similarity search
5. **Retrieval**: Semantic similarity search for relevant context
6. **Generation**: OpenAI GPT model generates responses based on retrieved context

### Technologies Used

- **LangChain**: Framework for building AI applications
- **OpenAI**: Large language model and embeddings
- **ChromaDB**: Vector database for similarity search
- **Streamlit**: Web application framework
- **Python**: Primary programming language

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For questions or issues:

- Open an issue in the GitHub repository
- Check the troubleshooting section above
- Review the LangChain and Streamlit documentation

## Future Enhancements

- [ ] Add conversation memory
- [ ] Implement user authentication
- [ ] Add multi-language support
- [ ] Include file upload capability
- [ ] Deploy to cloud platforms
- [ ] Add analytics and usage tracking
- [ ] Implement feedback collection system

---

**Built with ❤️ using LangChain, OpenAI, and Streamlit**
