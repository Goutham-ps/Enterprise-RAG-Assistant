import sys
import os
from pathlib import Path
from datetime import datetime

# Ensure the project directory is in sys.path
project_root = Path(__file__).parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

import streamlit as st
from html import escape

# Backend imports (UNCHANGED)
from utils.pipeline import (
    build_knowledge_base,
    load_knowledge_base,
    ask_question,
    get_statistics
)

# ========================================================
# PAGE CONFIG
# ========================================================

st.set_page_config(
    page_title="Enterprise AI Assistant",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ========================================================
# SESSION STATE INITIALIZATION
# ========================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "vector_store" not in st.session_state:
    st.session_state.vector_store = None

if "documents" not in st.session_state:
    st.session_state.documents = None

# ========================================================
# LOAD CUSTOM CSS
# ========================================================

def load_custom_css():
    try:
        with open("styles/styles.css", encoding="utf-8") as f:
            st.markdown(
                f"<style>{f.read()}</style>",
                unsafe_allow_html=True
            )
    except FileNotFoundError:
        pass

load_custom_css()

# ========================================================
# HELPER COMPONENTS
# ========================================================

def render_logo():
    """Render the sidebar logo and branding"""
    col1, col2 = st.columns([0.3, 0.7])
    with col1:
        st.markdown("# 📚")
    with col2:
        st.markdown("#### Enterprise AI\n*Knowledge Assistant*")

def render_upload_info():
    """Render the upload area info"""
    st.info("📄 **Supported:** PDF files only\n\n📦 **Limit:** 200MB per file")

def render_stats_cards(stats):
    """Render statistics in compact cards"""
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("📄 Documents", stats['documents'])
    
    with col2:
        st.metric("📑 Chunks", stats['chunks'])
    
    with col3:
        st.metric("🧠 Embeddings", stats['vectors'])

def render_status_badge(ready: bool):
    """Render knowledge base status badge"""
    if ready:
        st.success("✅ Knowledge Base Ready!")
    else:
        st.warning("⏳ Waiting for Documents...")

def render_message(message: dict):
    """Render a single chat message with avatar and timestamp"""
    role = message["role"]
    content = message["content"]
    timestamp = message.get("timestamp", "")
    
    with st.chat_message(role):
        st.markdown(content)
        if timestamp:
            st.caption(f"⏰ {timestamp}")

def render_sources(sources: list):
    """Render source citations in beautiful cards"""
    st.markdown("### 📚 Sources & Citations")
    
    for idx, source in enumerate(sources):
        source_name = source.get("source", "Unknown")
        page_num = source.get("page", "n/a")
        source_text = (source.get("text") or "")[:250]
        
        with st.expander(f"📄 {source_name} (Page {page_num})", expanded=False):
            st.markdown(f"**Document:** {source_name}")
            st.markdown(f"**Page:** {page_num}")
            st.markdown(f"**Preview:** {source_text}...")
            if len(source_text) > 250:
                st.caption("(Preview truncated)")

def render_thinking_animation():
    """Render AI thinking animation"""
    with st.spinner("🔍 Searching your documents..."):
        st.info("Processing your question and retrieving relevant information...")

def render_empty_state():
    """Render welcome empty state"""
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown(
            "<div style='text-align: center; padding: 2rem;'>",
            unsafe_allow_html=True,
        )
        st.markdown("# 👋 Welcome to Enterprise AI")
        st.markdown(
            "Powered by Retrieval-Augmented Generation. Analyze, summarize, and extract insights from your PDFs.",
            unsafe_allow_html=False,
        )
        
        st.markdown("---")
        
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            st.markdown("### 📄\n**Search Multiple PDFs**")
        with col_b:
            st.markdown("### 🔍\n**Semantic Search**")
        with col_c:
            st.markdown("### ✨\n**Instant Answers**")
        
        st.markdown("---")
        st.markdown("### 💡 Try asking:")
        
        col_s1, col_s2, col_s3 = st.columns(3)
        with col_s1:
            st.info("What are the main topics?")
        with col_s2:
            st.info("Summarize this document")
        with col_s3:
            st.info("What are key insights?")
        
        st.markdown("</div>", unsafe_allow_html=True)

def render_kb_not_ready():
    """Render knowledge base not ready state"""
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown(
            "<div style='text-align: center; padding: 3rem 2rem;'>",
            unsafe_allow_html=True,
        )
        st.markdown("# 🧠 No Knowledge Base Yet")
        st.markdown(
            "Upload PDFs and build your knowledge base to start chatting.",
            unsafe_allow_html=False,
        )
        
        st.markdown("---")
        st.markdown("### Getting Started in 3 Steps:")
        
        st.markdown("<div style='margin: 2rem 0;'>", unsafe_allow_html=True)
        st.markdown("**Step 1️⃣** - Upload PDF documents", unsafe_allow_html=False)
        st.info("Use the sidebar to upload one or more PDF files (up to 200MB each)")
        
        st.markdown("**Step 2️⃣** - Build Knowledge Base", unsafe_allow_html=False)
        st.info("Click the Build button to create embeddings and index your documents")
        
        st.markdown("**Step 3️⃣** - Start Chatting", unsafe_allow_html=False)
        st.info("Once ready, you can ask questions and get citations from your PDFs")
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)

# ========================================================
# SIDEBAR
# ========================================================

# ========================================================
# SIDEBAR
# ========================================================

def render_sidebar():
    with st.sidebar:
        render_logo()
        
        st.divider()
        
        # Workspace section
        st.markdown("<div class='sidebar-section-title'>📁 Workspace</div>", unsafe_allow_html=True)
        
        # Upload area
        st.markdown("<div class='upload-zone-label'>Upload PDF Documents</div>", unsafe_allow_html=True)
        render_upload_info()
        
        uploaded_files = st.file_uploader(
            "Choose PDF files",
            type=["pdf"],
            accept_multiple_files=True,
            label_visibility="collapsed",
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🚀 Build", use_container_width=True):
                if uploaded_files:
                    with st.spinner("Building knowledge base..."):
                        vector_store, documents = build_knowledge_base(uploaded_files)
                        st.session_state.vector_store = vector_store
                        st.session_state.documents = documents
                    st.success("Knowledge Base Ready!")
                    st.balloons()
                else:
                    st.warning("Please upload at least one PDF")
        
        with col2:
            if st.button("📂 Load", use_container_width=True):
                vector_store, documents = load_knowledge_base()
                if vector_store is not None:
                    st.session_state.vector_store = vector_store
                    st.session_state.documents = documents
                    st.success("Loaded!")
                else:
                    st.error("No saved KB found")
        
        st.divider()
        
        kb_ready = (
            st.session_state.vector_store is not None
            and st.session_state.documents is not None
        )
        
        if kb_ready:
            st.markdown("<div class='sidebar-section-title'>📊 Overview</div>", unsafe_allow_html=True)
            stats = get_statistics(
                st.session_state.vector_store,
                st.session_state.documents
            )
            render_stats_cards(stats)
            render_status_badge(True)
            
            st.divider()
            
            if st.button("🗑️ Clear Chat", use_container_width=True):
                st.session_state.messages = []
                st.rerun()
        
        st.divider()
        
        st.markdown("<div class='sidebar-section-title'>⚙️ Settings</div>", unsafe_allow_html=True)
        st.markdown(
            """
            <div class="settings-item">
                <span>📖 About</span>
                <div style="color: #9CA3AF; font-size: 0.85em; margin-top: 4px;">
                    Enterprise AI Knowledge Assistant v1.0
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

render_sidebar()

# ========================================================
# MAIN CONTENT AREA
# ========================================================

# Header
st.title("🚀 Enterprise AI Assistant")
st.markdown("Chat with your PDFs using Retrieval-Augmented Generation and get grounded, cited answers.")

st.divider()

kb_ready = (
    st.session_state.vector_store is not None
    and st.session_state.documents is not None
)

# ========================================================
# CHAT INTERFACE
# ========================================================

if kb_ready:
    # Display empty state or messages
    if len(st.session_state.messages) == 0:
        render_empty_state()
    else:
        # Display all messages
        for message in st.session_state.messages:
            timestamp = message.get("timestamp", datetime.now().strftime("%H:%M"))
            render_message(message)
    
    # Chat input
    st.markdown("<div class='chat-input-spacer'></div>", unsafe_allow_html=True)
    
    user_input = st.chat_input(
        "Ask anything about your PDFs...",
        key="chat_input",
    )
    
    if user_input:
        # Add user message
        user_message = {
            "role": "user",
            "content": user_input,
            "timestamp": datetime.now().strftime("%H:%M"),
        }
        st.session_state.messages.append(user_message)
        
        # Display thinking animation
        render_thinking_animation()
        
        # Generate answer
        answer, sources = ask_question(
            user_input,
            st.session_state.vector_store,
            st.session_state.documents,
        )
        
        # Add assistant message
        assistant_message = {
            "role": "assistant",
            "content": answer,
            "sources": sources,
            "timestamp": datetime.now().strftime("%H:%M"),
        }
        st.session_state.messages.append(assistant_message)
        
        st.rerun()
    
    # Display sources for last assistant message
    if len(st.session_state.messages) > 0:
        last_message = st.session_state.messages[-1]
        if (
            last_message["role"] == "assistant"
            and "sources" in last_message
            and last_message["sources"]
        ):
            render_sources(last_message["sources"])

else:
    render_kb_not_ready()

# ========================================================
# FOOTER
# ========================================================

st.divider()
st.caption("🤖 Enterprise AI Assistant • Powered by RAG & Google Gemini • © 2026")