import streamlit as st
from pipeline import generate_itinary

# Page Configuration
st.set_page_config(
    page_title="Wanderlust AI | Vintage Travel Planner",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom Styling: Modern Deep Black + Vintage Amber/Orange Accents
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,600;0,800;1,400&family=Plus+Jakarta+Sans:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');

    /* Global Theme & Background */
    .stApp {
        background-color: #0b0b0d;
        color: #e5e5e5;
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    /* Headings with Vintage Serif Typography */
    h1, h2, h3 {
        font-family: 'Playfair Display', Georgia, serif !important;
        color: #ff9f43 !important;
        letter-spacing: -0.5px;
    }

    /* Header Container */
    .hero-container {
        text-align: center;
        padding: 2.5rem 1rem 1.5rem 1rem;
        background: linear-gradient(180deg, rgba(255, 138, 0, 0.07) 0%, rgba(11, 11, 13, 0) 100%);
        border-bottom: 1px solid #26262a;
        margin-bottom: 2rem;
        border-radius: 12px;
    }
    
    .hero-tag {
        display: inline-block;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.8rem;
        letter-spacing: 2px;
        text-transform: uppercase;
        color: #ff8a00;
        background: rgba(255, 138, 0, 0.12);
        border: 1px solid rgba(255, 138, 0, 0.3);
        padding: 4px 12px;
        border-radius: 20px;
        margin-bottom: 0.8rem;
    }

    .hero-title {
        font-size: 2.8rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
    }

    .hero-subtitle {
        color: #9e9ea7;
        font-size: 1.05rem;
        max-width: 600px;
        margin: 0 auto;
    }

    /* Input Field Overrides */
    .stTextInput label, .stTextArea label {
        color: #f1c40f !important;
        font-weight: 500;
        font-size: 0.95rem;
    }

    .stTextInput input, .stTextArea textarea {
        background-color: #141418 !important;
        border: 1px solid #2b2b32 !important;
        color: #f3f3f3 !important;
        border-radius: 8px !important;
        font-size: 0.95rem;
        transition: all 0.25s ease-in-out;
    }

    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: #ff8a00 !important;
        box-shadow: 0 0 10px rgba(255, 138, 0, 0.25) !important;
    }

    /* Action Button */
    .stButton > button {
        background: linear-gradient(135deg, #ff8a00 0%, #e65c00 100%) !important;
        color: #0b0b0d !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.65rem 2rem !important;
        width: 100%;
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .stButton > button:hover {
        background: linear-gradient(135deg, #ffa733 0%, #ff6f00 100%) !important;
        box-shadow: 0 4px 18px rgba(255, 138, 0, 0.35) !important;
        transform: translateY(-1px);
    }

    /* Output Card */
    .output-card {
        background-color: #121216;
        border: 1px solid #27272e;
        border-left: 4px solid #ff8a00;
        border-radius: 10px;
        padding: 2rem;
        margin-top: 1.5rem;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
    }
</style>
""", unsafe_allow_html=True)

# Hero Header
st.markdown("""
<div class="hero-container">
    <div class="hero-tag">Autonomous Multi-Agent Planner</div>
    <div class="hero-title">🧭 Vintage Voyager</div>
    <div class="hero-subtitle">Real-time live web extraction synthesized into tailored, curated travel itineraries.</div>
</div>
""", unsafe_allow_html=True)

# Layout Setup
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.markdown("### 📍 Journey Parameters")
    
    destination = st.text_input(
        "Destination",
        placeholder="e.g., Manali, Himachal Pradesh, India"
    )
    
    duration = st.text_input(
        "Trip Duration",
        placeholder="e.g., 4 Days 3 Nights"
    )
    
    preferences = st.text_area(
        "Preferences, Budget & Vibe",
        placeholder="e.g., Backpacking budget, scenic mountain treks, quiet cafe corners, local Himachali food",
        height=120
    )
    
    generate_btn = st.button("Generate Expedition Plan")

with col2:
    st.markdown("### 🗺️ Curated Expedition")
    
    if generate_btn:
        if not destination or not duration or not preferences:
            st.warning("⚠️ Please fill in all journey details to start planning.")
        else:
            with st.status("🔍 Deploying Agents...", expanded=True) as status:
                st.write("🛰️ Searching live web for up-to-date attractions & local events...")
                
                try:
                    # Executes the multi-agent pipeline
                    itinerary_result = generate_itinary(
                        destination=destination,
                        duration=duration,
                        preferences=preferences
                    )
                    
                    status.update(label="✨ Itinerary generated successfully!", state="complete", expanded=False)
                    
                    # Display the final output inside the stylized container
                    st.markdown(f'<div class="output-card">', unsafe_allow_html=True)
                    st.markdown(itinerary_result)
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                except Exception as err:
                    status.update(label="❌ Pipeline Error", state="error")
                    st.error(f"An error occurred while executing the itinerary pipeline: {err}")
    else:
        st.info("Fill out your journey parameters on the left and click generate to launch the search and extraction agents.")