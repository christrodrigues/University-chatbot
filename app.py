import streamlit as st
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import Chroma
from langchain.callbacks.base import BaseCallbackHandler
from dotenv import load_dotenv
import os

load_dotenv()

class StreamlitCallbackHandler(BaseCallbackHandler):
    """Simple callback handler for streaming responses"""
    
    def __init__(self, container):
        self.container = container
        self.text = ""
        
    def on_llm_new_token(self, token: str, **kwargs) -> None:
        """Called when a new token is generated"""
        self.text += token
        self.container.markdown(f"""
        <div class="answer-box">
            <div class="answer-title">🎓 Answer:</div>
            <div>{self.text}</div>
        </div>
        """, unsafe_allow_html=True)

# Simple but effective styling
st.markdown("""
<style>
    .main-header {
        background-color: #c8102e;
        padding: 30px;
        border-radius: 10px;
        margin-bottom: 30px;
        text-align: center;
    }
    
    .main-header h1 {
        color: white;
        font-size: 2.5rem;
        margin: 0;
    }
    
    .main-header p {
        color: white;
        font-size: 1.2rem;
        margin: 10px 0 0 0;
    }
    
    .answer-box {
        background-color: #f8f9fa;
        border-left: 5px solid #c8102e;
        padding: 20px;
        border-radius: 5px;
        margin: 20px 0;
        color: #c8102e;
    }
    
    .answer-title {
        color: #c8102e;
        font-weight: bold;
        font-size: 1.2rem;
        margin-bottom: 10px;
    }
    
    .stButton > button[kind="primary"] {
        background-color: #c8102e;
        color: white;
        border: none;
        border-radius: 5px;
        padding: 10px 20px;
        font-weight: bold;
        width: 100%;
        margin-top: 10px;
    }
    
    .stButton > button[kind="primary"]:hover {
        background-color: #a50e26;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>🐾 Northeastern University Knowledge Hub</h1>
    <p>Your AI-powered guide to everything Northeastern</p>
</div>
""", unsafe_allow_html=True)

# Check if vector store exists
if not os.path.exists("db"):
    st.error("❌ Vector database not found! Please run `python ingest.py` first.")
    st.info("💡 Make sure you have processed your university documents before using the chatbot.")
    st.stop()

try:
    # Load vector store with streaming capability
    @st.cache_resource
    def load_qa_chain():
        db = Chroma(persist_directory="db", embedding_function=OpenAIEmbeddings())
        # Enable streaming by setting streaming=True
        llm = ChatOpenAI(
            model="gpt-3.5-turbo", 
            temperature=0,
            streaming=True  # This is the key change for streaming
        )
        return RetrievalQA.from_chain_type(llm=llm, retriever=db.as_retriever())
    
    qa_chain = load_qa_chain()
    
    # Main interface
    st.write("## 💬 Ask me anything about Northeastern!")
    st.write("*Try questions like: 'What are the admission requirements?' or 'Tell me about campus life'*")
    
    # Input with submit button
    query = st.text_input(
        "Enter your question:",
        placeholder="What would you like to know about Northeastern University?",
        key="question_input",
        on_change=lambda: st.session_state.update({"submit_triggered": True})
    )
    
    # Submit button
    submit_button = st.button("🔍 Ask Question", type="primary")
    
    # Check if Enter was pressed or button was clicked
    enter_pressed = st.session_state.get("submit_triggered", False)
    if enter_pressed:
        st.session_state["submit_triggered"] = False  # Reset the flag
    
    if query and (submit_button or enter_pressed):
        # Create container for streaming response
        response_container = st.empty()
        
        with st.spinner("🔍 Searching through Northeastern's knowledge base..."):
            # Create streaming callback handler
            stream_handler = StreamlitCallbackHandler(response_container)
            
            # Run the query with streaming callback
            response = qa_chain.run(query, callbacks=[stream_handler])
        
        # The streaming response is already displayed through the callback
        # No need to display it again
       
    # Information section
    with st.expander("ℹ️ About this chatbot"):
        st.write("""
        **This AI-powered chatbot helps you find information about Northeastern University.**
        
        Features:
        - 🔍 Intelligent document search
        - 🎯 Context-aware responses  
        - 📚 Comprehensive knowledge base
        - ⚡ Fast streaming responses
        
        **Tips for better results:**
        - Be specific in your questions
        - Ask about one topic at a time
        - Use keywords related to your interest area
        """)
    
    # Footer
    st.write("---")
    
    st.write("*For official information, always consult the university website*")

except Exception as e:
    st.error(f"❌ Error: {e}")
    st.info("**Troubleshooting:**")
    st.write("- Make sure your OpenAI API key is set in the `.env` file")
    st.write("- Verify that the vector database exists (run `python ingest.py`)")
    st.write("- Check your internet connection")
    
    with st.expander("🔧 Debug Information"):
        st.write(f"**Current directory:** {os.getcwd()}")
        st.write(f"**Database exists:** {os.path.exists('db')}")
        st.write(f"**OpenAI API key set:** {'OPENAI_API_KEY' in os.environ}")