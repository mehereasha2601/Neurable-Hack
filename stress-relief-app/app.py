"""
Main Streamlit application for stress monitoring and relief.

Integrated with beautiful UI from mindful-monitor design system.
Connects: Neurable EEG, Age-aware detection, Groq AI, Supabase DB
"""

import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import asyncio
import threading
import time
import uuid
from datetime import datetime, timedelta
from typing import Optional, Dict, List
import logging

# Import utility modules
from utils.stress_detector import AgeAwareStressDetector
from utils.ai_helper import AIHelper
from utils.db_helper import DBHelper
from utils.neurable_stream import NeurableStream
from components.interventions import InterventionManager
from components.visualizations import VisualizationManager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title="🧠 Stress Relief Companion",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Complete UI CSS from mindful-monitor design system
st.markdown("""
<style>
    /* Root variables - HSL color system */
    :root {
        --background: 220 25% 97%;
        --foreground: 220 15% 20%;
        --card: 0 0% 100%;
        --primary: 220 95% 68%;
        --secondary: 250 85% 75%;
        --accent: 280 75% 80%;
        --calm: 142 70% 55%;
        --stressed: 28 95% 65%;
        --extreme: 0 85% 60%;
        --child-bg: 340 85% 92%;
        --child-accent: 340 75% 70%;
        --teen-bg: 210 85% 92%;
        --teen-accent: 210 75% 65%;
        --adult-bg: 270 65% 92%;
        --adult-accent: 270 55% 65%;
        --radius: 1rem;
    }
    
    /* Main container */
    .main-container {
        min-height: 100vh;
        background: hsl(var(--background));
    }
    
    /* Hero/Landing page */
    .hero-container {
        min-height: 100vh;
        background: linear-gradient(135deg, 
            hsl(220, 95%, 68%) 0%, 
            hsl(250, 85%, 75%) 50%, 
            hsl(280, 75%, 80%) 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 2rem;
    }
    
    .hero-card {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-radius: 1.5rem;
        padding: 3rem;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.1);
        max-width: 1200px;
        width: 100%;
        animation: fadeIn 0.5s ease-out;
    }
    
    .hero-header {
        text-align: center;
        margin-bottom: 3rem;
    }
    
    .hero-emoji {
        font-size: 5rem;
        margin-bottom: 1rem;
        animation: scaleIn 0.5s ease-out;
    }
    
    .hero-title {
        font-size: 3rem;
        font-weight: 700;
        color: hsl(var(--foreground));
        margin-bottom: 0.5rem;
    }
    
    .hero-subtitle {
        font-size: 1.25rem;
        color: hsl(var(--foreground) / 0.7);
    }
    
    /* Age group cards */
    .age-card {
        background: white;
        border-radius: 1rem;
        padding: 2rem;
        text-align: center;
        cursor: pointer;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        border: 2px solid transparent;
        height: 100%;
    }
    
    .age-card:hover {
        transform: scale(1.05);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
    }
    
    .age-card.child {
        background: hsl(var(--child-bg));
    }
    
    .age-card.child:hover {
        background: hsl(var(--child-accent));
        border-color: hsl(var(--child-accent));
    }
    
    .age-card.teen {
        background: hsl(var(--teen-bg));
    }
    
    .age-card.teen:hover {
        background: hsl(var(--teen-accent));
        border-color: hsl(var(--teen-accent));
    }
    
    .age-card.adult {
        background: hsl(var(--adult-bg));
    }
    
    .age-card.adult:hover {
        background: hsl(var(--adult-accent));
        border-color: hsl(var(--adult-accent));
    }
    
    .age-emoji {
        font-size: 4rem;
        margin-bottom: 1rem;
    }
    
    .age-title {
        font-size: 1.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    
    .age-range {
        font-size: 0.875rem;
        font-weight: 600;
        opacity: 0.7;
        margin-bottom: 0.75rem;
    }
    
    .age-description {
        font-size: 0.875rem;
        opacity: 0.8;
    }
    
    /* Dashboard header */
    .dashboard-header {
        background: hsl(var(--card));
        border-bottom: 1px solid hsl(var(--foreground) / 0.1);
        padding: 1rem 1.5rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    
    .dashboard-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: hsl(var(--foreground));
    }
    
    .age-badge {
        padding: 0.5rem 1rem;
        border-radius: 9999px;
        font-weight: 600;
        font-size: 0.875rem;
    }
    
    .age-badge.child {
        background: hsl(var(--child-accent));
        color: hsl(var(--foreground));
    }
    
    .age-badge.teen {
        background: hsl(var(--teen-accent));
        color: hsl(var(--foreground));
    }
    
    .age-badge.adult {
        background: hsl(var(--adult-accent));
        color: hsl(var(--foreground));
    }
    
    /* Status card */
    .status-card {
        background: hsl(var(--card));
        border-radius: var(--radius);
        padding: 2rem;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: transform 0.3s ease;
    }
    
    .status-card:hover {
        transform: translateY(-5px);
    }
    
    .status-card.extreme {
        animation: pulseSoft 2s ease-in-out infinite;
    }
    
    .status-emoji {
        font-size: 5rem;
        margin-bottom: 1rem;
    }
    
    .status-text {
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 1rem;
    }
    
    .status-progress {
        margin: 1rem 0;
    }
    
    .status-info {
        margin-top: 1rem;
        padding-top: 1rem;
        border-top: 1px solid hsl(var(--foreground) / 0.1);
        font-size: 0.875rem;
        color: hsl(var(--foreground) / 0.7);
    }
    
    .status-info-row {
        display: flex;
        justify-content: space-between;
        margin: 0.5rem 0;
    }
    
    /* Control card */
    .control-card {
        background: hsl(var(--card));
        border-radius: var(--radius);
        padding: 1.5rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .control-button {
        width: 100%;
        padding: 1rem;
        border-radius: 0.5rem;
        font-size: 1.125rem;
        font-weight: 600;
        border: none;
        cursor: pointer;
        transition: all 0.3s ease;
        margin-bottom: 0.75rem;
    }
    
    .control-button.primary {
        background: hsl(var(--calm));
        color: white;
    }
    
    .control-button.primary:hover {
        background: hsl(var(--calm) / 0.9);
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
    
    .control-button.destructive {
        background: hsl(var(--extreme));
        color: white;
    }
    
    .control-button.destructive:hover {
        background: hsl(var(--extreme) / 0.9);
    }
    
    .session-stats {
        background: hsl(var(--foreground) / 0.05);
        border-radius: 0.5rem;
        padding: 1rem;
        margin-top: 1rem;
    }
    
    .session-stats-title {
        font-weight: 600;
        margin-bottom: 0.75rem;
    }
    
    .session-stats-row {
        display: flex;
        justify-content: space-between;
        font-size: 0.875rem;
        margin: 0.5rem 0;
    }
    
    /* Intervention panel */
    .intervention-panel {
        background: hsl(var(--card));
        border-left: 4px solid;
        border-radius: var(--radius);
        padding: 2rem;
        margin: 1.5rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        animation: scaleIn 0.3s ease-out;
    }
    
    .intervention-panel.child {
        border-left-color: hsl(var(--child-accent));
    }
    
    .intervention-panel.teen {
        border-left-color: hsl(var(--teen-accent));
    }
    
    .intervention-panel.adult {
        border-left-color: hsl(var(--adult-accent));
    }
    
    .intervention-header {
        margin-bottom: 1.5rem;
    }
    
    .intervention-title {
        font-size: 1.5rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    
    .intervention-subtitle {
        color: hsl(var(--foreground) / 0.7);
    }
    
    /* Tabs */
    .tab-container {
        margin-top: 1.5rem;
    }
    
    .tab-buttons {
        display: flex;
        gap: 0.5rem;
        margin-bottom: 1.5rem;
        border-bottom: 2px solid hsl(var(--foreground) / 0.1);
    }
    
    .tab-button {
        padding: 0.75rem 1.5rem;
        background: none;
        border: none;
        border-bottom: 3px solid transparent;
        cursor: pointer;
        font-weight: 500;
        transition: all 0.3s ease;
        color: hsl(var(--foreground) / 0.7);
    }
    
    .tab-button:hover {
        color: hsl(var(--foreground));
        background: hsl(var(--foreground) / 0.05);
    }
    
    .tab-button.active {
        color: hsl(var(--primary));
        border-bottom-color: hsl(var(--primary));
    }
    
    /* Crisis modal */
    .crisis-modal {
        background: hsl(var(--card));
        border-radius: var(--radius);
        padding: 2rem;
        margin: 1.5rem 0;
        border: 2px solid hsl(var(--extreme));
        animation: pulseSoft 2s ease-in-out infinite;
    }
    
    .crisis-header {
        display: flex;
        align-items: center;
        gap: 1rem;
        margin-bottom: 1.5rem;
        border-top: 4px solid hsl(var(--extreme));
        padding-top: 1rem;
    }
    
    .crisis-emoji {
        font-size: 3rem;
    }
    
    .crisis-title {
        font-size: 1.5rem;
        font-weight: 700;
    }
    
    .crisis-resources {
        background: hsl(var(--extreme) / 0.1);
        border: 1px solid hsl(var(--extreme));
        border-radius: 0.5rem;
        padding: 1.5rem;
        margin: 1.5rem 0;
    }
    
    .crisis-resource-card {
        background: hsl(var(--card));
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 0.75rem 0;
        display: flex;
        align-items: center;
        gap: 1rem;
        transition: box-shadow 0.3s ease;
    }
    
    .crisis-resource-card:hover {
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
    
    .crisis-techniques {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 0.75rem;
        margin: 1.5rem 0;
    }
    
    .crisis-technique {
        background: hsl(var(--card));
        border: 1px solid hsl(var(--foreground) / 0.1);
        border-radius: 0.5rem;
        padding: 1.5rem;
        text-align: center;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .crisis-technique:hover {
        background: hsl(var(--primary) / 0.1);
        border-color: hsl(var(--primary));
    }
    
    /* Animations */
    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: translateY(10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes scaleIn {
        from {
            transform: scale(0.95);
            opacity: 0;
        }
        to {
            transform: scale(1);
            opacity: 1;
        }
    }
    
    @keyframes pulseSoft {
        0%, 100% {
            opacity: 1;
        }
        50% {
            opacity: 0.7;
        }
    }
    
    /* Button overrides */
    .stButton > button {
        transition: all 0.3s ease;
        border-radius: 0.5rem;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
    
    /* Hide Streamlit default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)


def initialize_session_state():
    """Initialize all session state variables."""
    defaults = {
        'session_id': str(uuid.uuid4()),
        'age_group': None,
        'detector': None,
        'monitoring': False,
        'stress_data': [],
        'intervention_active': False,
        'eeg_stream': None,
        'ai_helper': None,
        'db_helper': None,
        'intervention_manager': InterventionManager(),
        'viz_manager': VisualizationManager(),
        'last_update': time.time(),
        'baseline_calibrated': False,
        'use_mock_data': True,
        'connection_status': 'disconnected',
        'connection_retries': 0,
        'journal_entries': [],
        'ai_story_cache': None,
        'ai_prompts_cache': None,
        'last_db_save': None,
        'stream_initialized': False,
        'readings_count': 0,
        'session_start_time': None,
        'current_tab': 'body-scan',
        'body_scan_progress': 0,
        'body_scan_active': False,
        'show_crisis_modal': False
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value
    
    # Initialize helpers
    if st.session_state.ai_helper is None:
        try:
            st.session_state.ai_helper = AIHelper()
        except Exception as e:
            logger.warning(f"AI Helper not available: {e}")
            st.session_state.ai_helper = None
    
    if st.session_state.db_helper is None:
        try:
            st.session_state.db_helper = DBHelper()
        except Exception as e:
            logger.warning(f"Database not available: {e}")
            st.session_state.db_helper = None


def show_age_selection():
    """Landing page - exact match to Index.tsx from mindful-monitor."""
    
    # Add custom CSS for animations and styling
    st.markdown("""
    <style>
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    @keyframes scaleIn {
        from { transform: scale(0.8); opacity: 0; }
        to { transform: scale(1); opacity: 1; }
    }
    .landing-container {
        background: linear-gradient(135deg, hsl(220, 95%, 68%) 0%, hsl(250, 85%, 75%) 50%, hsl(280, 75%, 80%) 100%);
        padding: 3rem 1rem;
        margin: -5rem -5rem 2rem -5rem;
        min-height: 40vh;
    }
    .landing-card {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
        border-radius: 1.5rem;
        padding: 3rem;
        max-width: 72rem;
        margin: 0 auto;
        animation: fadeIn 0.5s ease-out;
    }
    .landing-header {
        text-align: center;
        margin-bottom: 3rem;
    }
    .landing-emoji {
        font-size: 4.5rem;
        margin-bottom: 1rem;
        animation: scaleIn 0.5s ease-out;
    }
    .landing-title {
        font-size: 3rem;
        font-weight: 700;
        color: #1a1a1a !important;
        margin-bottom: 0.75rem;
        line-height: 1.2;
    }
    .landing-subtitle {
        font-size: 1.25rem;
        color: #666666 !important;
        margin: 0;
    }
    </style>
    
    <div class="landing-container">
        <div class="landing-card">
            <div class="landing-header">
                <div class="landing-emoji">🧠</div>
                <h1 class="landing-title">Stress Relief Companion</h1>
                <p class="landing-subtitle">Real-time stress monitoring using EEG technology</p>
            </div>
    """, unsafe_allow_html=True)
    
    # Age selection cards in 3-column grid INSIDE the white card
    st.markdown('<div style="margin-bottom: 2rem;">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3, gap="large")
    
    age_groups = [
        {
            "key": "child",
            "emoji": "👶",
            "title": "Child",
            "range": "0-10 years",
            "description": "Fun stories and calming activities designed for young minds",
            "bg_color": "hsl(340, 85%, 92%)",
            "hover_bg": "hsl(340, 75%, 70%)"
        },
        {
            "key": "teen",
            "emoji": "🧒",
            "title": "Teen",
            "range": "10-18 years",
            "description": "Journaling, art therapy, and mindfulness for adolescents",
            "bg_color": "hsl(210, 85%, 92%)",
            "hover_bg": "hsl(210, 75%, 65%)"
        },
        {
            "key": "adult",
            "emoji": "👤",
            "title": "Adult",
            "range": "18+ years",
            "description": "Professional meditation and stress management techniques",
            "bg_color": "hsl(270, 65%, 92%)",
            "hover_bg": "hsl(270, 55%, 65%)"
        }
    ]
    
    cols = [col1, col2, col3]
    
    for idx, (col, group) in enumerate(zip(cols, age_groups)):
        with col:
            # Render card with exact styling from Index.tsx
            card_html = f"""
            <div class="age-selection-card" 
                 data-age="{group['key']}"
                 style="background: {group['bg_color']}; 
                        border: none;
                        border-radius: 0.5rem; 
                        padding: 1.5rem; 
                        text-align: center;
                        cursor: pointer;
                        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
                        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
                        min-height: 280px;
                        display: flex;
                        flex-direction: column;
                        justify-content: center;">
                <div style="font-size: 4rem; margin-bottom: 1rem;">{group['emoji']}</div>
                <h3 style="font-size: 1.5rem; 
                           font-weight: 700; 
                           margin-bottom: 0.5rem;
                           color: #1a1a1a;">
                    {group['title']}
                </h3>
                <p style="font-size: 0.875rem; 
                          font-weight: 600; 
                          opacity: 0.7;
                          margin-bottom: 0.75rem;
                          color: #1a1a1a;">
                    {group['range']}
                </p>
                <p style="font-size: 0.875rem; 
                          opacity: 0.8;
                          color: #1a1a1a;">
                    {group['description']}
                </p>
            </div>
            
            <style>
            .age-selection-card:hover {{
                transform: scale(1.05);
                box-shadow: 0 10px 30px rgba(0,0,0,0.15);
                background: {group['hover_bg']} !important;
            }}
            </style>
            """
            st.markdown(card_html, unsafe_allow_html=True)
            
            # Invisible button over the card for click detection
            if st.button(f"Select {group['title']}", 
                        key=f"age_{group['key']}", 
                        use_container_width=True,
                        type="primary"):
                st.session_state.age_group = group['key']
                st.session_state.detector = AgeAwareStressDetector(age_group=group['key'])
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)  # Close the age cards container
    
    # Footer inside the white card
    st.markdown("""
            <div style="text-align: center; 
                        color: hsl(220, 15%, 45%); 
                        font-size: 0.875rem; 
                        margin-top: 2rem;
                        padding-top: 1.5rem;
                        border-top: 1px solid rgba(0,0,0,0.1);">
                <p style="display: flex; 
                          align-items: center; 
                          justify-content: center; 
                          gap: 1rem;
                          margin: 0;">
                    <span>🔒 Your data is secure</span>
                    <span style="opacity: 0.5;">|</span>
                    <span>💚 Mental health matters</span>
                </p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def connect_eeg_stream(websocket_url: Optional[str] = None, use_mock: bool = True) -> bool:
    """Connect to EEG stream with reconnection logic."""
    try:
        if use_mock or websocket_url is None:
            st.session_state.eeg_stream = NeurableStream(test_mode=True, stress_level="calm")
            st.session_state.connection_status = 'connected'
            st.session_state.use_mock_data = True
            
            def connect_async():
                try:
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    loop.run_until_complete(st.session_state.eeg_stream.connect())
                    loop.close()
                except Exception as e:
                    logger.error(f"Error connecting mock stream: {e}")
            
            threading.Thread(target=connect_async, daemon=True).start()
            return True
        else:
            st.session_state.connection_status = 'connecting'
            stream = NeurableStream(websocket_url=websocket_url)
            
            def connect_real():
                try:
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    success = loop.run_until_complete(stream.connect())
                    loop.close()
                    
                    if success and stream.is_connected():
                        st.session_state.eeg_stream = stream
                        st.session_state.connection_status = 'connected'
                        st.session_state.use_mock_data = False
                        st.session_state.connection_retries = 0
                    else:
                        raise ConnectionError("Connection failed")
                except Exception as e:
                    logger.error(f"Connection error: {e}")
                    st.session_state.connection_status = 'disconnected'
                    st.session_state.connection_retries += 1
                    if st.session_state.connection_retries >= 3:
                        st.session_state.use_mock_data = True
            
            threading.Thread(target=connect_real, daemon=True).start()
            return True
    except Exception as e:
        logger.error(f"Error in connect_eeg_stream: {e}")
        st.session_state.connection_status = 'disconnected'
        return False


def get_eeg_data() -> Optional[Dict]:
    """Get EEG data from stream or generate mock data."""
    if st.session_state.use_mock_data or st.session_state.eeg_stream is None:
        base_time = time.time()
        stress_value = 0.4 + np.sin(time.time() / 10) * 0.2 + np.random.normal(0, 0.05)
        stress_value = np.clip(stress_value, 0.2, 0.9)
        
        return {
            'Left__b_ab': stress_value,
            'Right__b_ab': stress_value,
            'Left__alpha': max(0, 0.3 + np.random.normal(0, 0.1)),
            'Right__alpha': max(0, 0.3 + np.random.normal(0, 0.1)),
            'Left__beta': max(0, 0.4 + np.random.normal(0, 0.1)),
            'Right__beta': max(0, 0.4 + np.random.normal(0, 0.1)),
            'Left__theta': max(0, 0.2 + np.random.normal(0, 0.05)),
            'Right__theta': max(0, 0.2 + np.random.normal(0, 0.05)),
            'Left__p_bad': np.clip(0.1 + np.random.uniform(0, 0.2), 0, 1),
            'Right__p_bad': np.clip(0.1 + np.random.uniform(0, 0.2), 0, 1),
            'time': base_time
        }
    
    try:
        if st.session_state.eeg_stream and st.session_state.eeg_stream.is_connected():
            data = st.session_state.eeg_stream.get_latest_data()
            if data:
                return data
    except Exception as e:
        logger.error(f"Error getting EEG data: {e}")
        st.session_state.use_mock_data = True
    
    return get_eeg_data()


def update_monitoring():
    """Update monitoring loop."""
    if not st.session_state.monitoring:
        return
    
    try:
        eeg_data = get_eeg_data()
        if eeg_data is None:
            return
        
        if not st.session_state.baseline_calibrated:
            calibrated = st.session_state.detector.calibrate_baseline(eeg_data)
            if calibrated:
                st.session_state.baseline_calibrated = True
        
        result = st.session_state.detector.detect_stress_level(eeg_data)
        
        reading = {
            'timestamp': datetime.now(),
            'b_ab': result['value'],
            'level': result['level'],
            'quality': result['quality'],
            'emoji': result['emoji'],
            'color': result['color'],
            'message': result['message']
        }
        
        st.session_state.stress_data.append(reading)
        st.session_state.readings_count += 1
        
        if len(st.session_state.stress_data) > 120:
            st.session_state.stress_data = st.session_state.stress_data[-120:]
        
        if st.session_state.db_helper and len(st.session_state.stress_data) % 10 == 0:
            try:
                st.session_state.db_helper.save_stress_reading(
                    user_id=st.session_state.session_id,
                    stress_level=result['value'],
                    metadata={'level': result['level'], 'quality': result['quality']}
                )
            except Exception as e:
                logger.error(f"Error saving to database: {e}")
        
        if st.session_state.detector.should_intervene():
            if not st.session_state.intervention_active:
                st.session_state.intervention_active = True
                st.rerun()
        
        if st.session_state.detector.needs_crisis_intervention():
            if not st.session_state.intervention_active:
                st.session_state.intervention_active = True
                st.session_state.show_crisis_modal = True
                st.rerun()
        
    except Exception as e:
        logger.error(f"Error in monitoring loop: {e}")


def render_dashboard_header():
    """Render dashboard header - exact match to Dashboard.tsx"""
    age_group = st.session_state.age_group
    age_labels = {
        'child': 'Child (0-10)',
        'teen': 'Teen (10-18)',
        'adult': 'Adult (18+)'
    }
    age_colors = {
        'child': 'hsl(340, 75%, 70%)',
        'teen': 'hsl(210, 75%, 65%)',
        'adult': 'hsl(270, 55%, 65%)'
    }
    
    # Top bar header
    col1, col2 = st.columns([3, 1])
    
    with col1:
        if st.button("← Back", key="back_button", help="Return to age selection"):
            st.session_state.age_group = None
            st.session_state.monitoring = False
            st.rerun()
        st.markdown(f"""
        <h1 style="font-size: 1.5rem; font-weight: bold; margin: 0; display: inline-block; margin-left: 1rem;">
            Stress Relief Companion
        </h1>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style="text-align: right;">
            <span style="background: {age_colors.get(age_group, '#666')}; 
                         color: white; 
                         padding: 0.5rem 1rem; 
                         border-radius: 9999px; 
                         font-weight: 600; 
                         font-size: 0.875rem;
                         display: inline-block;">
                {age_labels.get(age_group, 'Unknown')}
            </span>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<hr style='margin: 1rem 0; border-color: hsl(220, 20%, 88%);'>", unsafe_allow_html=True)


def render_status_card(result: Dict):
    """Render status card - EXACT match to Dashboard.tsx Status Card"""
    level = result['level']
    emoji = result['emoji']
    value = result['value']
    
    # Progress bar colors matching Dashboard.tsx
    progress_color_map = {
        'calm': 'hsl(142, 70%, 55%)',  # --calm
        'stressed': 'hsl(28, 95%, 65%)',  # --stressed
        'extreme': 'hsl(0, 85%, 60%)'  # --extreme
    }
    
    pulse_animation = 'animate-pulse-soft' if level == 'extreme' else ''
    
    # Exact HTML structure from Dashboard.tsx Card component
    st.markdown(f"""
    <div style="background: hsl(0, 0%, 100%); 
                border-radius: 0.5rem; 
                padding: 1.5rem; 
                box-shadow: 0 1px 3px rgba(0,0,0,0.1);"
         class="{pulse_animation}">
        <div style="text-center: true; display: flex; flex-direction: column; gap: 1rem;">
            <div style="text-align: center;">
                <!-- Large emoji matching text-8xl -->
                <div style="font-size: 6rem; margin-bottom: 1rem;">{emoji}</div>
                
                <!-- Status text matching text-3xl font-bold -->
                <h2 style="font-size: 1.875rem; font-weight: 700; margin: 0 0 1rem 0;">
                    {level.upper()}
                </h2>
                
                <!-- Progress section -->
                <div style="margin-bottom: 1rem;">
                    <div style="display: flex; justify-content: space-between; font-size: 0.875rem; margin-bottom: 0.5rem;">
                        <span>Stress Level</span>
                        <span style="font-weight: 600;">{(value * 100):.0f}%</span>
                    </div>
                    <!-- Progress bar h-3 (0.75rem) -->
                    <div style="height: 0.75rem; 
                                background: hsl(220, 20%, 92%); 
                                border-radius: 9999px; 
                                overflow: hidden;">
                        <div style="height: 100%; 
                                    width: {(value * 100):.0f}%; 
                                    background: {progress_color_map.get(level, 'hsl(220, 20%, 50%)')}; 
                                    transition: width 0.3s ease;"></div>
                    </div>
                </div>
                
                <!-- Info section matching Dashboard.tsx -->
                <div style="padding-top: 1rem; 
                            display: flex; 
                            flex-direction: column; 
                            gap: 0.5rem; 
                            font-size: 0.875rem;
                            color: hsl(220, 15%, 45%);">
                    <div style="display: flex; justify-content: space-between;">
                        <span>Signal Quality</span>
                        <span style="color: hsl(220, 15%, 20%); font-weight: 500;">Good</span>
                    </div>
                    <div style="display: flex; justify-between;">
                        <span>Baseline</span>
                        <span style="color: hsl(220, 15%, 20%); font-weight: 500;">0.25</span>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <style>
    @keyframes pulse-soft {{
        0%, 100% {{ opacity: 1; }}
        50% {{ opacity: 0.7; }}
    }}
    .animate-pulse-soft {{
        animation: pulse-soft 2s ease-in-out infinite;
    }}
    </style>
    """, unsafe_allow_html=True)


def render_stress_graph():
    """Render graph card - EXACT match to Dashboard.tsx Graph Card"""
    # Exact card structure from Dashboard.tsx
    st.markdown("""
    <div style="background: hsl(0, 0%, 100%); 
                border-radius: 0.5rem; 
                padding: 1.5rem; 
                box-shadow: 0 1px 3px rgba(0,0,0,0.1);">
        <h3 style="font-size: 1.25rem; 
                   font-weight: 600; 
                   margin-bottom: 1rem;
                   color: hsl(220, 15%, 20%);">
            Stress Level Over Time
        </h3>
        <!-- Gradient placeholder h-64 -->
        <div style="height: 16rem; 
                    background: linear-gradient(135deg, 
                                                hsla(220, 95%, 68%, 0.1), 
                                                hsla(250, 85%, 75%, 0.1)); 
                    border-radius: 0.5rem; 
                    display: flex; 
                    align-items: center; 
                    justify-content: center;
                    color: hsl(220, 15%, 45%);">
            Real-time graph will appear here
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_controls():
    """Render controls card - EXACT match to Dashboard.tsx Controls Card"""
    
    # Card wrapper
    st.markdown("""
    <div style="background: hsl(0, 0%, 100%); 
                border-radius: 0.5rem; 
                padding: 1.5rem; 
                box-shadow: 0 1px 3px rgba(0,0,0,0.1);
                display: flex;
                flex-direction: column;
                gap: 1rem;">
    """, unsafe_allow_html=True)
    
    # Main button styling
    button_style = f"""
    <style>
    div[data-testid="column"]:last-child .stButton > button {{
        width: 100% !important;
        height: 4rem !important;
        font-size: 1.125rem !important;
        font-weight: 600 !important;
        border-radius: 0.375rem !important;
        transition: all 0.2s !important;
    }}
    </style>
    """
    st.markdown(button_style, unsafe_allow_html=True)
    
    if st.session_state.monitoring:
        # Stop button
        st.markdown("""
        <button style="width: 100%;
                       height: 4rem;
                       font-size: 1.125rem;
                       font-weight: 600;
                       background: hsl(0, 85%, 60%);
                       color: white;
                       border: none;
                       border-radius: 0.375rem;
                       cursor: pointer;
                       transition: background 0.2s;">
            ⏹️ Stop Monitoring
        </button>
        """, unsafe_allow_html=True)
        
        if st.button("stop_btn_hidden", key="stop_monitoring", use_container_width=True, label_visibility="hidden"):
            st.session_state.monitoring = False
            st.rerun()
    else:
        # Start button  
        st.markdown("""
        <button style="width: 100%;
                       height: 4rem;
                       font-size: 1.125rem;
                       font-weight: 600;
                       background: hsl(142, 70%, 55%);
                       color: white;
                       border: none;
                       border-radius: 0.375rem;
                       cursor: pointer;
                       transition: background 0.2s;">
            ▶️ Start Monitoring
        </button>
        """, unsafe_allow_html=True)
        
        if st.button("start_btn_hidden", key="start_monitoring", use_container_width=True, label_visibility="hidden"):
            st.session_state.monitoring = True
            st.session_state.session_start_time = datetime.now()
            if not st.session_state.stream_initialized:
                connect_eeg_stream(use_mock=st.session_state.use_mock_data)
                st.session_state.stream_initialized = True
            st.rerun()
    
    # Secondary buttons
    if st.button("🔄 New Session", key="new_session", use_container_width=True):
        st.session_state.monitoring = False
        st.session_state.stress_data = []
        st.session_state.baseline_calibrated = False
        st.session_state.intervention_active = False
        st.session_state.readings_count = 0
        st.session_state.session_id = str(uuid.uuid4())
        if st.session_state.detector:
            st.session_state.detector.reset_calibration()
        st.rerun()
    
    if st.button("📖 View Journal History", key="journal_history", use_container_width=True):
        st.session_state.show_journal_history = True
        st.rerun()
    
    # Session stats (when monitoring)
    if st.session_state.monitoring:
        st.markdown("""
        <div style="background: hsl(220, 20%, 92%); 
                    padding: 1rem;
                    border-radius: 0.375rem;">
            <h4 style="font-weight: 600; margin-bottom: 0.75rem;">Session Stats</h4>
            <div style="display: flex; flex-direction: column; gap: 0.5rem; font-size: 0.875rem;">
                <div style="display: flex; justify-content: space-between;">
                    <span>Readings</span>
                    <span style="font-weight: 500;">{}</span>
                </div>
                <div style="display: flex; justify-content: space-between;">
                    <span>Duration</span>
                    <span style="font-weight: 500;">{}</span>
                </div>
                <div style="display: flex; justify-content: space-between;">
                    <span>Avg Stress</span>
                    <span style="font-weight: 500;">{:.0f}%</span>
                </div>
            </div>
        </div>
        """.format(
            st.session_state.readings_count,
            format_duration(st.session_state.session_start_time),
            np.mean([r['b_ab'] for r in st.session_state.stress_data]) * 100 if st.session_state.stress_data else 0
        ), unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)


def format_duration(start_time: Optional[datetime]) -> str:
    """Format session duration."""
    if not start_time:
        return "0:00"
    delta = datetime.now() - start_time
    mins = int(delta.total_seconds() // 60)
    secs = int(delta.total_seconds() % 60)
    return f"{mins}:{secs:02d}"


def render_intervention_panel():
    """Render age-specific intervention panel matching mindful-monitor design."""
    if not st.session_state.intervention_active:
        return
    
    age_group = st.session_state.age_group
    latest = st.session_state.stress_data[-1] if st.session_state.stress_data else None
    
    if not latest:
        return
    
    # Use the new intervention manager with age-specific components
    def close_intervention():
        st.session_state.intervention_active = False
        st.rerun()
    
    st.session_state.intervention_manager.render_intervention(age_group, close_intervention)


def render_crisis_modal():
    """Render crisis intervention modal."""
    if not st.session_state.show_crisis_modal:
        return
    
    st.markdown("""
    <div class="crisis-modal">
        <div class="crisis-header">
            <div class="crisis-emoji">🚨</div>
            <div>
                <h2 class="crisis-title">Very High Stress Detected</h2>
                <p>Your wellbeing matters. Let's get you help.</p>
            </div>
        </div>
        
        <div class="crisis-resources">
            <h3 style="font-size: 1.25rem; font-weight: 600; margin-bottom: 1rem;">
                If you're in crisis, reach out now:
            </h3>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### Crisis Resources")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**988 Suicide & Crisis Lifeline**")
        st.caption("24/7 support in English and Spanish")
        st.button("Call 988", key="call_988", use_container_width=True)
    
    with col2:
        st.markdown("**Crisis Text Line**")
        st.caption("Text with a trained crisis counselor")
        st.button("Text HOME to 741741", key="text_crisis", use_container_width=True)
    
    st.markdown("### Quick Calming Techniques")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("**🌬️ Box Breathing**")
        st.caption("30 seconds")
        st.info("Breathe in 4 → Hold 4 → Out 4 → Hold 4")
    
    with col2:
        st.markdown("**💧 Cold Water**")
        st.caption("Face dunk")
        st.info("Dunk face in cold water for 15-30 seconds")
    
    with col3:
        st.markdown("**👣 Movement**")
        st.caption("Break")
        st.info("Stand up, shake hands, roll shoulders")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("I'm safe, continue monitoring", key="crisis_continue", use_container_width=True):
            st.session_state.show_crisis_modal = False
            st.rerun()
    
    with col2:
        if st.button("Stop session", key="crisis_stop", use_container_width=True):
            st.session_state.monitoring = False
            st.session_state.show_crisis_modal = False
            st.rerun()


def main():
    """Main application entry point."""
    initialize_session_state()
    
    # Age selection page
    if st.session_state.age_group is None:
        show_age_selection()
        return
    
    # Dashboard
    render_dashboard_header()
    
    # Sidebar
    with st.sidebar:
        st.markdown("### ⚙️ Settings")
        use_mock = st.checkbox("Use Mock Data", value=st.session_state.use_mock_data)
        if use_mock != st.session_state.use_mock_data:
            st.session_state.use_mock_data = use_mock
            st.session_state.stream_initialized = False
            st.rerun()
        
        if not use_mock:
            websocket_url = st.text_input(
                "WebSocket URL",
                value=st.session_state.get('ws_url', 'wss://stream2.mindfulmakers.xyz'),
                key="ws_url_input",
                help="Default: wss://stream2.mindfulmakers.xyz (Mindful Makers stream)"
            )
            if 'ws_url' not in st.session_state or st.session_state.ws_url != websocket_url:
                st.session_state.ws_url = websocket_url
        
        st.markdown("---")
        st.markdown("### 📊 Session Info")
        st.text(f"Session: {st.session_state.session_id[:8]}...")
        
        if st.session_state.detector:
            stats = st.session_state.detector.get_stress_statistics()
            st.metric("Readings", stats['total_readings'])
            st.metric("Calm %", f"{stats['calm_percentage']:.1f}%")
    
    # Main content
    if st.session_state.monitoring:
        update_monitoring()
        
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col1:
            if st.session_state.stress_data:
                latest = st.session_state.stress_data[-1]
                result = {
                    'level': latest['level'],
                    'value': latest['b_ab'],
                    'emoji': latest['emoji']
                }
                render_status_card(result)
            else:
                st.info("📊 Collecting baseline data...")
        
        with col2:
            render_stress_graph()
        
        with col3:
            render_controls()
        
        # Intervention panel
        if st.session_state.intervention_active:
            st.markdown("---")
            render_intervention_panel()
        
        # Crisis modal
        if st.session_state.show_crisis_modal:
            st.markdown("---")
            render_crisis_modal()
        
        # Auto-refresh
        if time.time() - st.session_state.last_update > 0.5:
            st.session_state.last_update = time.time()
            if st.session_state.body_scan_active:
                st.session_state.body_scan_progress += (100 / 12) / 2  # 12 parts, 2 seconds each
            st.rerun()
    
    else:
        st.markdown("### 👋 Welcome Back!")
        st.info("Click 'Start Monitoring' to begin tracking your stress levels.")
        
        if st.session_state.baseline_calibrated:
            st.success("✅ Your baseline is calibrated and ready!")


if __name__ == "__main__":
    main()
