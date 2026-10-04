import os

import streamlit as st
from pipeline import generate_itinary

# ============================================================
# Page Configuration
# ============================================================
st.set_page_config(
    page_title="Wanderlust AI | Trip Planner",
    page_icon="🌴",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# Custom Styling: Warm Sunset Teal + Coral, friendly & bright
# ============================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Fraunces:ital,wght@0,500;0,700;0,900;1,500&family=Plus+Jakarta+Sans:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

    :root {
        --teal: #0f766e;
        --teal-deep: #0a4f4a;
        --coral: #ff6b5b;
        --coral-deep: #e8503f;
        --sand: #fff8f0;
        --ink: #163832;
        --muted: #6b7a78;
        --card: #ffffff;
        --border: #e7e2d6;
    }

    .stApp {
        background: var(--sand);
        color: var(--ink);
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    #MainMenu, footer, header {visibility: hidden;}

    h1, h2, h3 {
        font-family: 'Fraunces', Georgia, serif !important;
        color: var(--teal-deep) !important;
        letter-spacing: -0.3px;
    }

    /* ---------- Hero ---------- */
    .hero-container {
        text-align: center;
        padding: 2.6rem 1.5rem 2rem 1.5rem;
        background: radial-gradient(ellipse at top, rgba(255,107,91,0.14) 0%, rgba(15,118,110,0.08) 55%, transparent 100%);
        border: 1px solid var(--border);
        margin-bottom: 2rem;
        border-radius: 20px;
        position: relative;
        overflow: hidden;
    }

    .hero-tag {
        display: inline-block;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.75rem;
        letter-spacing: 2px;
        text-transform: uppercase;
        color: var(--coral-deep);
        background: rgba(255, 107, 91, 0.12);
        border: 1px solid rgba(255, 107, 91, 0.3);
        padding: 4px 14px;
        border-radius: 20px;
        margin-bottom: 1rem;
        font-weight: 500;
    }

    .hero-title {
        font-size: 3rem;
        font-weight: 900;
        margin-bottom: 0.4rem;
    }

    .hero-subtitle {
        color: var(--muted);
        font-size: 1.05rem;
        max-width: 600px;
        margin: 0 auto;
        font-weight: 400;
    }

    /* ---------- Section labels ---------- */
    .section-label {
        font-family: 'Fraunces', serif;
        font-weight: 700;
        font-size: 1.25rem;
        color: var(--teal-deep);
        margin-bottom: 0.2rem;
    }
    .section-hint {
        color: var(--muted);
        font-size: 0.85rem;
        margin-bottom: 1rem;
    }

    /* ---------- Input Fields ---------- */
    .stTextInput label, .stTextArea label {
        color: var(--teal-deep) !important;
        font-weight: 600;
        font-size: 0.9rem;
    }

    .stTextInput input, .stTextArea textarea {
        background-color: var(--card) !important;
        border: 1.5px solid var(--border) !important;
        color: var(--ink) !important;
        border-radius: 10px !important;
        font-size: 0.95rem;
        transition: all 0.2s ease-in-out;
    }

    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: var(--coral) !important;
        box-shadow: 0 0 0 4px rgba(255, 107, 91, 0.12) !important;
    }

    /* ---------- Action Button ---------- */
    .stButton > button {
        background: linear-gradient(135deg, var(--coral) 0%, var(--coral-deep) 100%) !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.7rem 2rem !important;
        width: 100%;
        transition: all 0.25s ease;
        letter-spacing: 0.3px;
    }

    .stButton > button:hover {
        box-shadow: 0 8px 22px rgba(255, 107, 91, 0.35) !important;
        transform: translateY(-1px);
    }

    /* ---------- Output Card ---------- */
    .output-card {
        background-color: var(--card);
        border: 1px solid var(--border);
        border-left: 5px solid var(--teal);
        border-radius: 14px;
        padding: 2rem;
        margin-top: 1.5rem;
        box-shadow: 0 12px 28px -10px rgba(15, 118, 110, 0.18);
    }

    /* ---------- Sidebar ---------- */
    section[data-testid="stSidebar"] {
        background: var(--teal-deep);
    }
    section[data-testid="stSidebar"] * {
        color: #eafaf6 !important;
    }
    section[data-testid="stSidebar"] .stTextInput input,
    section[data-testid="stSidebar"] .stSelectbox > div {
        background-color: rgba(255,255,255,0.08) !important;
        border: 1px solid rgba(255,255,255,0.18) !important;
        color: #ffffff !important;
        border-radius: 9px !important;
    }
    section[data-testid="stSidebar"] .stTextInput input::placeholder {
        color: rgba(234,250,246,0.45) !important;
    }
    .sidebar-brand {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        margin-bottom: 0.3rem;
    }
    .sidebar-brand-mark {
        font-size: 1.4rem;
    }
    .sidebar-brand-name {
        font-family: 'Fraunces', serif;
        font-weight: 700;
        font-size: 1.1rem;
        color: #ffffff !important;
    }
    .sidebar-note {
        font-size: 0.78rem;
        color: rgba(234,250,246,0.65) !important;
        line-height: 1.5;
        margin-top: 0.3rem;
    }
    .key-pill {
        display: inline-flex;
        align-items: center;
        gap: 0.35rem;
        font-size: 0.72rem;
        font-weight: 600;
        padding: 0.25rem 0.6rem;
        border-radius: 999px;
        margin-top: 0.5rem;
        background: rgba(255, 107, 91, 0.18);
        border: 1px solid rgba(255, 107, 91, 0.4);
        color: #ffb3a8 !important;
    }
    .key-pill.active {
        background: rgba(45, 212, 191, 0.18);
        border: 1px solid rgba(45, 212, 191, 0.45);
        color: #99f6e4 !important;
    }
    .key-dot {
        width: 6px; height: 6px; border-radius: 50%;
        background: currentColor;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# Sidebar — Bring Your Own API Key
# ============================================================
with st.sidebar:
    st.markdown(
        """
        <div class="sidebar-brand">
            <span class="sidebar-brand-mark">🌴</span>
            <span class="sidebar-brand-name">Wanderlust AI</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("<div class='sidebar-note'>Plan trips with the shared key, or drop in your own for unlimited, private runs.</div>", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("**🔑 Bring your own API key**")

    key_provider = st.selectbox(
        "Provider",
        ["OpenAI", "Anthropic (Claude)", "Google (Gemini)", "Groq"],
        label_visibility="collapsed",
    )

    user_api_key = st.text_input(
        "API Key",
        type="password",
        placeholder=f"Paste your {key_provider} key…",
        label_visibility="collapsed",
        key="byo_api_key",
    )

    if user_api_key:
        # Make the key available to the pipeline without logging it anywhere.
        env_var_map = {
            "OpenAI": "OPENAI_API_KEY",
            "Anthropic (Claude)": "ANTHROPIC_API_KEY",
            "Google (Gemini)": "GOOGLE_API_KEY",
            "Groq": "GROQ_API_KEY",
        }
        os.environ[env_var_map[key_provider]] = user_api_key
        st.session_state["using_own_key"] = True
        st.markdown(
            "<span class='key-pill active'><span class='key-dot'></span>Using your key</span>",
            unsafe_allow_html=True,
        )
    else:
        st.session_state["using_own_key"] = False
        st.markdown(
            "<span class='key-pill'><span class='key-dot'></span>Using shared key</span>",
            unsafe_allow_html=True,
        )

    st.markdown(
        "<div class='sidebar-note'>Your key stays in this session only — it's never stored or sent anywhere besides the model provider.</div>",
        unsafe_allow_html=True,
    )

    st.markdown("---")
    st.markdown(
        "<div class='sidebar-note'>Built for wanderers who'd rather be exploring than scrolling through blogs. ✈️</div>",
        unsafe_allow_html=True,
    )

# ============================================================
# Hero Header
# ============================================================
st.markdown("""
<div class="hero-container">
    <div class="hero-tag">Your Next Trip, Sorted in Minutes</div>
    <div class="hero-title">🌴 Wanderlust AI</div>
    <div class="hero-subtitle">Tell us where you're headed and we'll pull live, up-to-date info from the web to build a trip that actually fits your vibe — no 40-tab research rabbit hole required.</div>
</div>
""", unsafe_allow_html=True)

# ============================================================
# Layout Setup
# ============================================================
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.markdown("<div class='section-label'>📍 Where to?</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-hint'>Give us the basics — we'll handle the research.</div>", unsafe_allow_html=True)

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

    generate_btn = st.button("✨ Plan My Trip")

with col2:
    st.markdown("<div class='section-label'>🗺️ Your Itinerary</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-hint'>Your curated day-by-day plan shows up here.</div>", unsafe_allow_html=True)

    if generate_btn:
        if not destination or not duration or not preferences:
            st.warning("⚠️ Fill in all the trip details first so we know what to plan for.")
        else:
            with st.status("🧳 Packing your itinerary...", expanded=True) as status:
                st.write("🛰️ Scouting the web for fresh spots, eats & events...")

                try:
                    itinerary_result = generate_itinary(
                        destination=destination,
                        duration=duration,
                        preferences=preferences
                    )

                    status.update(label="✨ Your trip is ready!", state="complete", expanded=False)

                    st.markdown(f'<div class="output-card">', unsafe_allow_html=True)
                    st.markdown(itinerary_result)
                    st.markdown('</div>', unsafe_allow_html=True)

                except Exception as err:
                    status.update(label="❌ Something went sideways", state="error")
                    st.error(f"Couldn't generate your itinerary: {err}")
    else:
        st.info("Fill in your trip details on the left, hit 'Plan My Trip', and let the agents do the legwork. 🌊")