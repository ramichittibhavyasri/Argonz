
import streamlit as st
import requests
from datetime import datetime
import json
import time

# Page config
st.set_page_config(
    page_title="Construction AI Assistant",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Enhanced CSS with glassmorphism and modern design
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

:root {
    --primary-gradient: linear-gradient(135deg, #12232E 0%, #007CC7 100%);
    --secondary-gradient: linear-gradient(135deg, #007CC7 0%, #4DA8DA 100%);
    --accent-gradient: linear-gradient(135deg, #4DA8DA 0%, #EEFBFB 100%);
    --success-color: #10b981;
    --text-dark: #12232E;
    --text-light: #4DA8DA;
    --bg-glass: rgba(238, 251, 251, 0.25); /* based on off-white */
    --bg-card: rgba(238, 251, 251, 0.95);  /* based on off-white */
}


/* Hide Streamlit branding and menu */
#MainMenu, footer, header {visibility: hidden;}
.stDeployButton {display: none;}

/* Global styles */
.stApp {
    background: var(--primary-gradient) !important;
    font-family: 'Inter', sans-serif !important;
}

/* Animated background particles */
.bg-particles {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    pointer-events: none;
    z-index: -1;
}

.particle {
    position: absolute;
    background: rgba(255, 255, 255, 0.1);
    border-radius: 50%;
    animation: float 20s infinite linear;
}

@keyframes float {
    0% { transform: translateY(100vh) rotate(0deg); opacity: 0; }
    10% { opacity: 1; }
    90% { opacity: 1; }
    100% { transform: translateY(-100px) rotate(360deg); opacity: 0; }
}

/* Main container */
.main-container {
    max-width: 900px;
    margin: 20px auto;
    background: var(--bg-glass);
    backdrop-filter: blur(20px);
    border-radius: 30px;
    border: 1px solid rgba(255, 255, 255, 0.2);
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
    overflow: hidden;
    animation: slideInUp 0.8s ease-out;
}

@keyframes slideInUp {
    from { opacity: 0; transform: translateY(50px); }
    to { opacity: 1; transform: translateY(0); }
}

/* Header styling */
.chat-header {
    background: var(--secondary-gradient);
    color: white;
    padding: 30px;
    text-align: center;
    position: relative;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
}

.header-title {
    font-size: 2.5rem;
    font-weight: 700;
    margin-bottom: 10px;
    text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
    animation: titleGlow 3s ease-in-out infinite alternate;
}

@keyframes titleGlow {
    from { text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3); }
    to { text-shadow: 2px 2px 20px rgba(255, 255, 255, 0.5); }
}

.header-desc {
    font-size: 1.1rem;
    opacity: 0.9;
    font-weight: 400;
}

.status-indicator {
    position: absolute;
    top: 30px;
    right: 30px;
    display: flex;
    align-items: center;
    gap: 12px;
    background: rgba(255, 255, 255, 0.2);
    padding: 8px 16px;
    border-radius: 20px;
    backdrop-filter: blur(10px);
}

.status-dot {
    width: 12px;
    height: 12px;
    background: var(--success-color);
    border-radius: 50%;
    animation: pulse 2s ease-in-out infinite;
    box-shadow: 0 0 10px var(--success-color);
}

@keyframes pulse {
    0%, 100% { transform: scale(1); opacity: 1; }
    50% { transform: scale(1.2); opacity: 0.7; }
}

/* Welcome card */
.welcome-card {
    background: var(--bg-card);
    border-radius: 25px;
    border: 1px solid rgba(255, 255, 255, 0.2);
    box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
    backdrop-filter: blur(20px);
    padding: 30px;
    margin: 20px;
    text-align: center;
    position: relative;
    overflow: hidden;
    animation: welcomeFadeIn 1s ease-out;
}

.welcome-card::before {
    content: "";
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
    animation: shimmer 3s infinite;
}

@keyframes shimmer {
    0% { left: -100%; }
    100% { left: 100%; }
}

@keyframes welcomeFadeIn {
    from { opacity: 0; transform: scale(0.9); }
    to { opacity: 1; transform: scale(1); }
}

.welcome-title {
    font-size: 2rem;
    font-weight: 700;
    margin-bottom: 15px;
    background: var(--secondary-gradient);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    display: inline-flex;
    align-items: center;
  
}

.welcome-title .sticker {
    -webkit-text-fill-color: initial; /* reset so emoji keeps its color */

}


.welcome-desc {
    font-size: 1.1rem;
    color: var(--text-dark);
    line-height: 1.7;
    margin-bottom: 25px;
}

/* Example queries */
.example-queries {
    display: flex;
    flex-wrap: wrap;
    gap: 15px;
    justify-content: center;
    margin-bottom: 20px;
}

/* Message styling */
.message-container {
    padding: 20px;
    background: rgba(255, 255, 255, 0.05);
}

.message {
    display: flex;
    align-items: flex-start;
    gap: 15px;
    margin-bottom: 20px;
    max-width: 85%;
    animation: messageSlide 0.5s ease-out;
}

@keyframes messageSlide {
    from { opacity: 0; transform: translateX(-30px); }
    to { opacity: 1; transform: translateX(0); }
}

.message.user {
    flex-direction: row-reverse;
    margin-left: auto;
    animation: messageSlideUser 0.5s ease-out;
}

@keyframes messageSlideUser {
    from { opacity: 0; transform: translateX(30px); }
    to { opacity: 1; transform: translateX(0); }
}

.message-avatar {
    width: 50px;
    height: 50px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 600;
    color: white;
    flex-shrink: 0;
    font-size: 20px;
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
    position: relative;
    overflow: hidden;
}

.message-avatar.user {
    background: var(--secondary-gradient);
}

.message-avatar.bot {
    background: var(--accent-gradient);
}

.message-content {
    padding: 18px 24px;
    border-radius: 25px;
    word-wrap: break-word;
    line-height: 1.6;
    font-size: 15px;
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.2);
    transition: all 0.3s ease;
}

.message-content:hover {
    transform: translateY(-2px);
}

.message-content.user {
    background: var(--secondary-gradient);
    color: white;
    box-shadow: 0 10px 30px rgba(245, 87, 108, 0.3);
}

.message-content.bot {
    background: var(--bg-card);
    color: var(--text-dark);
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
}

/* Typing indicator */
.typing-indicator {
    display: flex;
    align-items: center;
    gap: 15px;
    padding: 20px;
    color: var(--text-light);
    font-style: italic;
    background: var(--bg-card);
    border-radius: 25px;
    margin: 0 20px 20px 20px;
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.2);
}

.typing-dots {
    display: flex;
    gap: 6px;
}

.typing-dot {
    width: 10px;
    height: 10px;
    background: var(--accent-gradient);
    border-radius: 50%;
    animation: typing 1.4s infinite ease-in-out;
}

.typing-dot:nth-child(2) { animation-delay: 0.2s; }
.typing-dot:nth-child(3) { animation-delay: 0.4s; }

@keyframes typing {
    0%, 60%, 100% { transform: scale(1) translateY(0); opacity: 0.5; }
    30% { transform: scale(1.3) translateY(-10px); opacity: 1; }
}

/* Input styling */
.input-container {
    padding: 20px;
    border-top: 1px solid rgba(255, 255, 255, 0.1);
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(20px);
}

/* Streamlit input override */
.stTextInput > div > div > input {
    background: rgba(255, 255, 255, 0.9) !important;
    border: 1px solid rgba(255, 255, 255, 0.2) !important;
    border-radius: 25px !important;
    padding: 15px 20px !important;
    font-size: 16px !important;
    color: var(--text-dark) !important;
    backdrop-filter: blur(10px);
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1) !important;
}

.stTextInput > div > div > input:focus {
    border-color: var(--secondary-gradient) !important;
    box-shadow: 0 0 0 2px rgba(240, 147, 251, 0.2) !important;
}

/* Button styling */
.stButton > button {
    background: var(--secondary-gradient) !important;
    color: white !important;
    border: none !important;
    border-radius: 50px !important;
    padding: 12px 30px !important;
    font-weight: 600 !important;
    font-size: 16px !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 10px 25px rgba(245, 87, 108, 0.4) !important;
}

.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 15px 35px rgba(245, 87, 108, 0.6) !important;
}

/* Example button styling */
.example-btn {
    background: linear-gradient(135deg, rgba(79, 70, 229, 0.1), rgba(124, 58, 237, 0.1));
    color: #4f46e5;
    padding: 12px 20px;
    border-radius: 25px;
    cursor: pointer;
    font-size: 14px;
    font-weight: 500;
    border: 2px solid rgba(79, 70, 229, 0.2);
    text-decoration: none;
    display: inline-block;
    margin: 5px;
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
}

.example-btn::before {
    content: "";
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: var(--secondary-gradient);
    transition: all 0.3s ease;
    z-index: -1;
}

.example-btn:hover::before {
    left: 0;
}

.example-btn:hover {
    color: white;
    transform: translateY(-3px);
    box-shadow: 0 15px 35px rgba(79, 70, 229, 0.4);
    text-decoration: none;
}

/* Responsive design */
@media (max-width: 768px) {
    .main-container {
        margin: 10px;
        border-radius: 20px;
    }
    
    .chat-header {
        padding: 20px;
    }
    
    .header-title {
        font-size: 1.8rem;
    }
    
    .message {
        max-width: 90%;
    }
    
    .message-avatar {
        width: 40px;
        height: 40px;
        font-size: 16px;
    }
    
    .welcome-title {
        font-size: 1.5rem;
    }
    
    .example-btn {
        padding: 8px 14px;
        font-size: 12px;
    }
}
</style>
""", unsafe_allow_html=True)

# Background particles
st.markdown("""
<div class="bg-particles">
    <div class="particle" style="left: 10%; width: 5px; height: 5px; animation-delay: 0s;"></div>
    <div class="particle" style="left: 20%; width: 8px; height: 8px; animation-delay: 2s;"></div>
    <div class="particle" style="left: 30%; width: 3px; height: 3px; animation-delay: 4s;"></div>
    <div class="particle" style="left: 40%; width: 6px; height: 6px; animation-delay: 6s;"></div>
    <div class="particle" style="left: 50%; width: 4px; height: 4px; animation-delay: 8s;"></div>
    <div class="particle" style="left: 60%; width: 7px; height: 7px; animation-delay: 10s;"></div>
    <div class="particle" style="left: 70%; width: 5px; height: 5px; animation-delay: 12s;"></div>
    <div class="particle" style="left: 80%; width: 3px; height: 3px; animation-delay: 14s;"></div>
    <div class="particle" style="left: 90%; width: 6px; height: 6px; animation-delay: 16s;"></div>
</div>
""", unsafe_allow_html=True)

# Main container
st.markdown('<div class="main-container">', unsafe_allow_html=True)

# Header
st.markdown('''
<div class="chat-header">
    <div class="header-title"> 🏠 Smart Construction AI 🏗️</div>
    <div class="header-desc">Your Trusted Guide to Structural Engineering & Modern Construction Practices</div>
    <div class="status-indicator">
        <div class="status-dot"></div>
        <span style="font-size: 14px; font-weight: 500;">Online</span>
    </div>
</div>
''', unsafe_allow_html=True)

# Gemini API Configuration
GEMINI_API_KEY = "AIzaSyBZYb0TpTwyPwcxQhL60G56CLo00tg1AE8"
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

# Construction keywords for filtering
CONSTRUCTION_KEYWORDS = [
    "concrete", "cement", "brick", "steel", "construction", "masonry", "plaster",
    "foundation", "reinforcement", "aggregate", "mortar", "beam", "column", "slab",
    "wall", "roof", "excavation", "compaction", "curing", "mix", "grade", "strength",
    "load", "structural", "building", "architecture", "engineering", "materials",
    "tools", "equipment", "safety", "site", "project", "design", "blueprint",
    "scaffold", "formwork", "rebar", "welding", "paint", "tiles", "flooring",
    "plumbing", "electrical", "hvac", "insulation", "waterproof", "contractor",
    "supervisor", "worker", "labor", "cost", "estimate", "measurement", "quantity",
    "surveying", "soil", "geotechnical"
]

def is_construction_query(query):
    """Check if the query is construction-related"""
    query_lower = query.lower()
    return any(keyword in query_lower for keyword in CONSTRUCTION_KEYWORDS)

def gemini_generate_response(query):
    """Generate response using Gemini API"""
    headers = {
        "Content-Type": "application/json",
        "X-goog-api-key": GEMINI_API_KEY
    }
    
    system_prompt = (
        "You are a veteran architect and civil engineering consultant with 80 years of practical and academic experience. "
    "Provide only detailed, professional answers to queries about construction, structural design, materials, and project execution. "
    "Reject all unrelated questions politely and remain focused on construction engineering."
    )
    
    payload = {
        "contents": [
            {"parts": [{"text": system_prompt + "\n\nUser question: " + query}]}
        ]
    }
    
    try:
        response = requests.post(GEMINI_API_URL, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        result = response.json()
        text = result.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "")
        return text if text else "No response generated. Please try again."
    except requests.exceptions.RequestException as e:
        return f"🔧 Connection error. Please check your internet connection and try again. Details: {str(e)}"
    except Exception as e:
        return f"🔧 An unexpected error occurred. Please try again. Details: {str(e)}"

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "typing" not in st.session_state:
    st.session_state.typing = False

# Welcome message and example queries
if not st.session_state.messages:
    st.markdown('''
    <div class="welcome-card">
        <div class="welcome-title"> Welcome aboard! Get expert insights on concrete, steel, materials, designs, and project execution.</div>
        <div class="welcome-desc">
            I’m your dedicated AI partner, here to provide expert guidance in construction technology, structural engineering, materials science, modern methodologies, and advanced civil engineering practices.
        </div>
        <div class="example-queries">
            <a href="#" class="example-btn" onclick="return false;">🧱 Concrete Curing</a>
            <a href="#" class="example-btn" onclick="return false;">⚖️ Mix Design</a>
            <a href="#" class="example-btn" onclick="return false;">🔩 Steel Properties</a>
            <a href="#" class="example-btn" onclick="return false;">🏭 Cement Types</a>
            <a href="#" class="example-btn" onclick="return false;">🏗️ Foundation Design</a>
        </div>
    </div>
    ''', unsafe_allow_html=True)
    
    # Example query buttons
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        if st.button("🧱 Concrete Curing", key="btn1"):
            st.session_state.pending_query = "What is the standard curing period for concrete?"
    
    with col2:
        if st.button("⚖️ Mix Design", key="btn2"):
            st.session_state.pending_query = "How to calculate concrete mix ratio?"
    
    with col3:
        if st.button("🔩 Steel Properties", key="btn3"):
            st.session_state.pending_query = "Properties of steel reinforcement"
    
    with col4:
        if st.button("🏭 Cement Types", key="btn4"):
            st.session_state.pending_query = "Different types of cement"
    
    with col5:
        if st.button("🏗️ Foundation Design", key="btn5"):
            st.session_state.pending_query = "Foundation design principles"

# Message container
st.markdown('<div class="message-container">', unsafe_allow_html=True)

# Display chat messages
for message in st.session_state.messages:
    role_class = "user" if message["role"] == "user" else "bot"
    avatar = "👤" if message["role"] == "user" else "🤖"
    
    st.markdown(f'''
    <div class="message {role_class}">
        <div class="message-avatar {role_class}">{avatar}</div>
        <div class="message-content {role_class}">{message["content"]}</div>
    </div>
    ''', unsafe_allow_html=True)

# Typing indicator
if st.session_state.typing:
    st.markdown('''
    <div class="typing-indicator">
        <div class="message-avatar bot">🤖</div>
        <span>AI Assistant is analyzing your query</span>
        <div class="typing-dots">
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
        </div>
    </div>
    ''', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)  # Close message container

# Input area
st.markdown('<div class="input-container">', unsafe_allow_html=True)

# Create input form
with st.form("chat_form", clear_on_submit=True):
    col1, col2 = st.columns([4, 1])
    
    with col1:
        user_input = st.text_input(
            "Your Query",
            placeholder="Ask me about construction techniques, materials, engineering principles...",
            key="user_input",
            label_visibility="hidden"
        )
    
    with col2:
        submit_button = st.form_submit_button("Send 📤", use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)  # Close input container

# Handle pending query from example buttons
if hasattr(st.session_state, 'pending_query'):
    user_input = st.session_state.pending_query
    submit_button = True
    delattr(st.session_state, 'pending_query')

# Process user input
if submit_button and user_input:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Show typing indicator
    st.session_state.typing = True
    st.rerun()

# Generate AI response
if st.session_state.typing and st.session_state.messages:
    last_message = st.session_state.messages[-1]
    
    if last_message["role"] == "user":
        # Check if construction-related
        if is_construction_query(last_message["content"]):
            # Generate response using Gemini
            with st.spinner("AI Assistant is analyzing your query..."):
                response = gemini_generate_response(last_message["content"])
        else:
            # Non-construction query response
            response = """🏗️ I specialize in **construction and civil engineering** questions only.

Please ask about topics such as:
• **Concrete technology** - mixing, curing, testing
• **Steel engineering** - properties, design, fabrication  
• **Building materials** - cement, aggregates, additives
• **Construction processes** - methods, equipment, safety
• **Structural engineering** - design principles, analysis
• **Foundation systems** - types, design, construction

Feel free to ask any **construction-related** question!"""
        
        # Add AI response
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.session_state.typing = False
        st.rerun()

st.markdown('</div>', unsafe_allow_html=True)  # Close main containe
st.markdown('</div>', unsafe_allow_html=True)  

st.markdown("""
<script>
function scrollToBottom() {
    window.scrollTo(0, document.body.scrollHeight);
}
setTimeout(scrollToBottom, 100);
</script>
""", unsafe_allow_html=True)
