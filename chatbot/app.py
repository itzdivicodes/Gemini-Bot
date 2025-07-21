"""
Streamlit Messenger UI for Gemini AI Chatbot
Beautiful messaging app interface with blue user messages and red bot responses.
Run with: streamlit run app.py
"""

import streamlit as st
import time
from datetime import datetime
from bot import generate_gemini_response
import os

# Page configuration
st.set_page_config(
    page_title="🤖 Gemini AI Messenger",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for messenger appearance
st.markdown("""
<style>
    /* Hide Streamlit default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {visibility: hidden;}
    
    /* Remove top padding */
    .main > div {
        padding-top: 0rem !important;
        padding-left: 1rem;
        padding-right: 1rem;
        padding-bottom: 1rem;
        max-width: 800px;
        margin: 0 auto;
    }
    
    /* Main heading styling - Black with colorful emoji */
    .main-heading {
        text-align: center;
        margin: 1rem 0 2rem 0;
        padding: 0;
    }
    
    .main-heading h1 {
        color: #000000 !important;
        font-size: 2.5rem;
        font-weight: bold;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    .main-heading p {
        color: #666666;
        font-size: 1rem;
        margin: 0.5rem 0 0 0;
        font-style: italic;
    }
    
    /* User message (Blue) */
    .user-message {
        background: linear-gradient(135deg, #007bff, #0056b3);
        color: white;
        padding: 12px 16px;
        border-radius: 18px 18px 5px 18px;
        margin: 8px 0 8px 60px;
        box-shadow: 0 2px 10px rgba(0,123,255,0.2);
        font-size: 14px;
        line-height: 1.4;
        word-wrap: break-word;
        animation: slideInRight 0.3s ease-out;
    }
    
    /* Bot message (Red) */
    .bot-message {
        background: linear-gradient(135deg, #dc3545, #c82333);
        color: white;
        padding: 12px 16px;
        border-radius: 18px 18px 18px 5px;
        margin: 8px 60px 8px 0;
        box-shadow: 0 2px 10px rgba(220,53,69,0.2);
        font-size: 14px;
        line-height: 1.4;
        word-wrap: break-word;
        animation: slideInLeft 0.3s ease-out;
    }
    
    /* Smooth animations */
    @keyframes slideInRight {
        from { transform: translateX(100px); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    @keyframes slideInLeft {
        from { transform: translateX(-100px); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    /* Message timestamp */
    .message-time {
        font-size: 10px;
        opacity: 0.7;
        margin-top: 4px;
        text-align: right;
    }
    
    /* Input area styling */
    .stTextInput > div > div > input {
        border-radius: 25px;
        border: 2px solid #007bff;
        padding: 12px 20px;
        font-size: 14px;
        background: white;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #0056b3;
        box-shadow: 0 0 10px rgba(0,123,255,0.2);
    }
    
    /* Send button */
    .stButton > button {
        background: linear-gradient(135deg, #28a745, #20c997);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 12px 30px;
        font-weight: bold;
        box-shadow: 0 4px 15px rgba(40,167,69,0.3);
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(40,167,69,0.4);
    }
    
    /* Typing indicator */
    .typing-indicator {
        background: #f8f9fa;
        color: #6c757d;
        padding: 8px 16px;
        border-radius: 18px;
        margin: 8px 60px 8px 0;
        font-style: italic;
        animation: pulse 1.5s infinite;
    }
    
    @keyframes pulse {
        0% { opacity: 0.6; }
        50% { opacity: 1; }
        100% { opacity: 0.6; }
    }
    
    /* Status styling */
    .status-success {
        background: #d4edda;
        color: #155724;
        padding: 8px 16px;
        border-radius: 10px;
        border: 1px solid #c3e6cb;
        margin-bottom: 1rem;
        text-align: center;
    }
    
    /* Sidebar improvements */
    .css-1d391kg {
        background-color: #f8f9fa;
    }
    
    /* Smooth scrolling */
    .chat-container {
        scroll-behavior: smooth;
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state variables"""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "api_status" not in st.session_state:
        st.session_state.api_status = check_api_key()

def check_api_key():
    """Check if API key is configured"""
    api_key = os.getenv("GEMINI_API_KEY")
    return api_key is not None and len(api_key) > 0

def display_message(message, is_user=True):
    """Display a chat message with styling"""
    timestamp = datetime.now().strftime("%H:%M")
    
    if is_user:
        st.markdown(f"""
        <div class="user-message">
            {message}
            <div class="message-time">{timestamp}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="bot-message">
            {message}
            <div class="message-time">{timestamp}</div>
        </div>
        """, unsafe_allow_html=True)

def show_typing_indicator():
    """Show typing indicator animation"""
    typing_placeholder = st.empty()
    typing_placeholder.markdown("""
    <div class="typing-indicator">
        🤖 Gemini is thinking...
    </div>
    """, unsafe_allow_html=True)
    return typing_placeholder

def main():
    """Main Streamlit app"""
    # Initialize session state
    initialize_session_state()
    
    # Clean header with black text and colorful emoji
    st.markdown("""
    <div class="main-heading">
        <h1>🤖 Gemini AI Messenger</h1>
        <p>Chat with Google's Gemini AI in a beautiful interface</p>
    </div>
    """, unsafe_allow_html=True)
    
    # API Status check - Clean styling
    if not st.session_state.api_status:
        st.error("⚠️ GEMINI_API_KEY not found! Please add your API key to the .env file.")
        st.stop()
    else:
        st.markdown("""
        <div class="status-success">
            🟢 Connected to Gemini AI
        </div>
        """, unsafe_allow_html=True)
    
    # Clean chat container
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    # Display chat history
    for message in st.session_state.messages:
        display_message(message["content"], message["role"] == "user")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Input area
    st.markdown("---")
    col1, col2 = st.columns([4, 1])
    
    with col1:
        user_input = st.text_input(
            "Type your message...",
            placeholder="Ask me anything! 💭",
            key="user_input",
            label_visibility="collapsed"
        )
    
    with col2:
        send_button = st.button("Send ", use_container_width=True)
    
    # Handle user input
    if send_button and user_input.strip():
        # Add user message to chat
        st.session_state.messages.append({
            "role": "user",
            "content": user_input
        })
        
        # Show typing indicator
        with st.container():
            typing_placeholder = show_typing_indicator()
            
            try:
                # Generate bot response
                bot_response = generate_gemini_response(user_input)
                
                # Remove typing indicator
                typing_placeholder.empty()
                
                # Add bot response to chat
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": bot_response
                })
                
            except Exception as e:
                typing_placeholder.empty()
                error_message = f"❌ Sorry, I encountered an error: {str(e)}"
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": error_message
                })
        
        # Rerun to update the chat
        st.rerun()
    
    # Enhanced sidebar
    with st.sidebar:
        st.markdown("### Chat Controls")
        
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
        
        st.markdown("### Chat Stats")
        st.metric("Total Messages", len(st.session_state.messages))
        
        if st.session_state.messages:
            user_msgs = len([m for m in st.session_state.messages if m["role"] == "user"])
            bot_msgs = len([m for m in st.session_state.messages if m["role"] == "assistant"])
            st.metric("Your Messages", user_msgs)
            st.metric("Bot Responses", bot_msgs)
        
        st.markdown("### About")
        st.info("🚀 Powered by Google Gemini AI with advanced web search capabilities.")

if __name__ == "__main__":
    main()
