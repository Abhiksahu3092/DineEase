# app.py
import streamlit as st
from backend.agent import run_agent_step

# Page config
st.set_page_config(
    page_title="DineEase - Restaurant Reservations",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Custom CSS - Dark Mode UI
st.markdown(
    """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Main container styling - Dark background */
    .main {
        background-color: #0f172a;
        padding: 2rem 1rem;
    }
    
    .block-container {
        padding: 2rem 1rem;
        max-width: 800px;
    }
    
    /* Main container - Dark theme */
    .chat-container {
        background: #1e293b;
        border-radius: 16px;
        padding: 2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        max-width: 800px;
        margin: 0 auto;
        border: 1px solid #334155;
    }
    
    /* Header styling - Light text on dark */
    .main-header {
        text-align: center;
        color: #f1f5f9;
        font-size: 2rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    
    .sub-header {
        text-align: center;
        color: #94a3b8;
        font-size: 0.95rem;
        font-weight: 400;
        margin-bottom: 2rem;
    }
    
    /* Chat messages container */
    .chat-messages {
        max-height: 450px;
        overflow-y: auto;
        padding: 0.5rem;
        margin-bottom: 1.5rem;
    }
    
    .chat-messages::-webkit-scrollbar {
        width: 6px;
    }
    
    .chat-messages::-webkit-scrollbar-track {
        background: #0f172a;
        border-radius: 4px;
    }
    
    .chat-messages::-webkit-scrollbar-thumb {
        background: #475569;
        border-radius: 4px;
    }
    
    .chat-messages::-webkit-scrollbar-thumb:hover {
        background: #64748b;
    }
    
    /* User message bubble - Accent color */
    .user-message {
        background: #3b82f6;
        color: #ffffff;
        padding: 0.875rem 1.125rem;
        border-radius: 16px;
        margin: 0.75rem 0;
        margin-left: auto;
        max-width: 70%;
        font-size: 0.95rem;
        line-height: 1.5;
        box-shadow: 0 2px 4px rgba(59, 130, 246, 0.3);
    }
    
    /* Assistant message bubble - Dark gray */
    .assistant-message {
        background: #334155;
        color: #e2e8f0;
        padding: 0.875rem 1.125rem;
        border-radius: 16px;
        margin: 0.75rem 0;
        margin-right: auto;
        max-width: 70%;
        font-size: 0.95rem;
        line-height: 1.5;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
    }
    
    /* Message labels */
    .message-label {
        font-size: 0.7rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 0.4rem;
        opacity: 0.7;
    }
    
    /* Input styling - Dark theme */
    .stTextInput > div > div > input {
        background-color: #0f172a !important;
        border: 1px solid #475569 !important;
        border-radius: 12px !important;
        padding: 0.875rem 1rem !important;
        font-size: 0.95rem !important;
        color: #e2e8f0 !important;
        transition: all 0.2s ease !important;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: #64748b !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #3b82f6 !important;
        outline: none !important;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.2) !important;
        background-color: #1e293b !important;
    }
    
    /* Button styling - Accent color */
    .stButton > button {
        background: #3b82f6;
        color: white;
        border-radius: 12px;
        padding: 0.875rem 1.5rem;
        font-weight: 500;
        font-size: 0.95rem;
        border: none;
        transition: all 0.2s ease;
        width: 100%;
        box-shadow: 0 2px 4px rgba(59, 130, 246, 0.3);
    }
    
    .stButton > button:hover {
        background: #2563eb;
        box-shadow: 0 4px 8px rgba(59, 130, 246, 0.4);
        transform: translateY(-1px);
    }
    
    /* Empty state - Dark theme */
    .empty-state {
        text-align: center;
        padding: 3rem 1rem;
        color: #64748b;
    }
    
    .empty-state-text {
        font-size: 0.95rem;
        color: #94a3b8;
        margin-top: 0.5rem;
    }
    
    /* Spinner color */
    .stSpinner > div {
        border-top-color: #3b82f6 !important;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""",
    unsafe_allow_html=True,
)

# Initialize session state
if "history" not in st.session_state:
    st.session_state.history = []

# Main container
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">DineEase</h1>', unsafe_allow_html=True)
st.markdown(
    '<p class="sub-header">Find and book restaurants</p>',
    unsafe_allow_html=True,
)

# Chat messages area
st.markdown('<div class="chat-messages">', unsafe_allow_html=True)

if not st.session_state.history:
    # Empty state
    st.markdown(
        """
        <div class="empty-state">
            <div style="font-size: 3rem; margin-bottom: 0.5rem;">💬</div>
            <div class="empty-state-text">How can I help you today?</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
else:
    # Render chat history
    for m in st.session_state.history:
        if m["role"] == "user":
            st.markdown(
                f"""
            <div style="display: flex; justify-content: flex-end; margin-bottom: 0.75rem;">
                <div class="user-message">
                    <div class="message-label">You</div>
                    {m['content']}
                </div>
            </div>
            """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f"""
            <div style="display: flex; justify-content: flex-start; margin-bottom: 0.75rem;">
                <div class="assistant-message">
                    <div class="message-label">Assistant</div>
                    {m['content']}
                </div>
            </div>
            """,
                unsafe_allow_html=True,
            )

st.markdown("</div>", unsafe_allow_html=True)  # Close chat-messages

# Input area
col1, col2 = st.columns([5, 1])

with col1:
    user_input = st.text_input(
        "Message",
        placeholder="Type a message...",
        key="user_input",
        label_visibility="collapsed",
    )

with col2:
    send_button = st.button("Send")

st.markdown("</div>", unsafe_allow_html=True)  # Close chat-container

# Handle send
if send_button and user_input:
    user_msg = user_input
    with st.spinner("Thinking..."):
        assistant_text, tool_res = run_agent_step(
            user_msg, st.session_state.history.copy()
        )
    st.session_state.history.append({"role": "user", "content": user_msg})
    st.session_state.history.append({"role": "assistant", "content": assistant_text})
    st.rerun()
