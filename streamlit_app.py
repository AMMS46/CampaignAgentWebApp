
import streamlit as st
import json
import os
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import pandas as pd
from campaign_assistant import generate_campaign_plan
from agents import test_research_agent, test_content_agent, test_channel_agent, test_schedule_agent


st.set_page_config(
    page_title="AI Campaign Assistant Pro",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': None
    }
)

def load_modern_css():
    """Load modern CSS design system inspired by React apps"""
    st.markdown("""
    <style>
    /* Import Modern Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600&display=swap');
    
    /* Reset and Base Styles */
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }
    
    /* Root Variables */
    :root {
        --primary-50: #eff6ff;
        --primary-100: #dbeafe;
        --primary-500: #3b82f6;
        --primary-600: #2563eb;
        --primary-700: #1d4ed8;
        --primary-900: #1e3a8a;
        
        --gray-50: #f9fafb;
        --gray-100: #f3f4f6;
        --gray-200: #e5e7eb;
        --gray-300: #d1d5db;
        --gray-400: #9ca3af;
        --gray-500: #6b7280;
        --gray-600: #4b5563;
        --gray-700: #374151;
        --gray-800: #1f2937;
        --gray-900: #111827;
        
        --success-50: #ecfdf5;
        --success-500: #10b981;
        --success-600: #059669;
        
        --warning-50: #fffbeb;
        --warning-500: #f59e0b;
        --warning-600: #d97706;
        
        --error-50: #fef2f2;
        --error-500: #ef4444;
        --error-600: #dc2626;
        
        --shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);
        --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);
        --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1);
        --shadow-xl: 0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1);
        
        --radius-sm: 0.375rem;
        --radius-md: 0.5rem;
        --radius-lg: 0.75rem;
        --radius-xl: 1rem;
    }
    
    /* Main App Layout */
    .main .block-container {
        padding: 0;
        max-width: none;
    }
    
    .main {
        background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 25%, #fef7ff 50%, #fff7ed 75%, #f0fdf4 100%);
        min-height: 100vh;
    }
    
    /* Hero Section */
    .hero-section {
        background: linear-gradient(135deg, var(--primary-600) 0%, var(--primary-700) 50%, var(--primary-900) 100%);
        padding: 4rem 2rem;
        text-align: center;
        position: relative;
        overflow: hidden;
    }
    
    .hero-section::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.05'%3E%3Ccircle cx='30' cy='30' r='2'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
        opacity: 0.3;
    }
    
    .hero-content {
        position: relative;
        z-index: 1;
        max-width: 800px;
        margin: 0 auto;
    }
    
    .hero-title {
        font-size: 3.5rem;
        font-weight: 800;
        color: white;
        margin-bottom: 1.5rem;
        line-height: 1.1;
        letter-spacing: -0.02em;
    }
    
    .hero-subtitle {
        font-size: 1.25rem;
        color: rgba(255, 255, 255, 0.9);
        margin-bottom: 2rem;
        font-weight: 400;
        line-height: 1.6;
    }
    
    .hero-stats {
        display: flex;
        justify-content: center;
        gap: 3rem;
        margin-top: 3rem;
        flex-wrap: wrap;
    }
    
    .stat-item {
        text-align: center;
        color: white;
    }
    
    .stat-number {
        font-size: 2rem;
        font-weight: 700;
        display: block;
    }
    
    .stat-label {
        font-size: 0.875rem;
        opacity: 0.8;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-top: 0.25rem;
    }
    
    /* Navigation */
    .nav-container {
        background: white;
        padding: 1rem 2rem;
        box-shadow: var(--shadow-sm);
        border-bottom: 1px solid var(--gray-200);
        position: sticky;
        top: 0;
        z-index: 50;
    }
    
    .nav-content {
        max-width: 1200px;
        margin: 0 auto;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    
    .nav-logo {
        font-size: 1.5rem;
        font-weight: 700;
        color: var(--primary-600);
        text-decoration: none;
    }
    
    .nav-menu {
        display: flex;
        gap: 2rem;
        list-style: none;
    }
    
    .nav-item {
        color: var(--gray-600);
        font-weight: 500;
        cursor: pointer;
        padding: 0.5rem 1rem;
        border-radius: var(--radius-md);
        transition: all 0.2s;
    }
    
    .nav-item:hover, .nav-item.active {
        color: var(--primary-600);
        background: var(--primary-50);
    }
    
    /* Section Container */
    .section {
        max-width: 1200px;
        margin: 0 auto;
        padding: 4rem 2rem;
    }
    
    .section-header {
        text-align: center;
        margin-bottom: 3rem;
    }
    
    .section-title {
        font-size: 2.5rem;
        font-weight: 700;
        color: var(--gray-900);
        margin-bottom: 1rem;
        line-height: 1.2;
    }
    
    .section-subtitle {
        font-size: 1.125rem;
        color: var(--gray-600);
        max-width: 600px;
        margin: 0 auto;
        line-height: 1.6;
    }
    
    /* Modern Cards */
    .card {
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
        border-radius: var(--radius-xl);
        padding: 2rem;
        box-shadow: var(--shadow-lg);
        border: 2px solid var(--primary-200);
        transition: all 0.3s ease;
        height: 100%;
    }
    
    .card:hover {
        transform: translateY(-4px);
        box-shadow: var(--shadow-xl);
        border-color: var(--primary-300);
        background: linear-gradient(135deg, #f1f5f9 0%, #ddd6fe 100%);
    }
    
    .card-header {
        margin-bottom: 1.5rem;
    }
    
    .card-title {
        font-size: 1.5rem;
        font-weight: 600;
        color: var(--gray-900);
        margin-bottom: 0.5rem;
    }
    
    .card-description {
        color: var(--gray-600);
        line-height: 1.5;
    }
    
    /* Feature Cards */
    .feature-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 2rem;
        margin-top: 3rem;
    }
    
    .feature-card {
        background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
        border-radius: var(--radius-lg);
        padding: 2rem;
        text-align: center;
        box-shadow: var(--shadow-md);
        border: 2px solid #93c5fd;
        transition: all 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-4px);
        box-shadow: var(--shadow-lg);
        border-color: #3b82f6;
        background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
    }
    
    .feature-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
        display: block;
    }
    
    .feature-title {
        font-size: 1.25rem;
        font-weight: 600;
        color: var(--gray-900);
        margin-bottom: 0.75rem;
    }
    
    .feature-description {
        color: var(--gray-600);
        line-height: 1.5;
    }
    
    /* Modern Buttons */
    .btn {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        padding: 0.75rem 1.5rem;
        font-size: 1rem;
        font-weight: 600;
        border-radius: var(--radius-md);
        border: none;
        cursor: pointer;
        transition: all 0.2s;
        text-decoration: none;
        line-height: 1;
    }
    
    .btn-primary {
        background: var(--primary-600);
        color: white;
    }
    
    .btn-primary:hover {
        background: var(--primary-700);
        transform: translateY(-1px);
        box-shadow: var(--shadow-lg);
    }
    
    .btn-secondary {
        background: white;
        color: var(--gray-700);
        border: 1px solid var(--gray-300);
    }
    
    .btn-secondary:hover {
        background: var(--gray-50);
        border-color: var(--gray-400);
    }
    
    .btn-lg {
        padding: 1rem 2rem;
        font-size: 1.125rem;
    }
    
    /* Form Styles */
    .form-group {
        margin-bottom: 1.5rem;
    }
    
    .form-label {
        display: block;
        font-size: 0.875rem;
        font-weight: 600;
        color: var(--gray-700);
        margin-bottom: 0.5rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Streamlit Override Styles */
    .stButton > button {
        background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: var(--radius-md) !important;
        padding: 0.85rem 2rem !important;
        font-weight: 700 !important;
        font-size: 1.05rem !important;
        transition: all 0.3s !important;
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.4) !important;
        width: 100%;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #1d4ed8 0%, #1e3a8a 100%) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(59, 130, 246, 0.5) !important;
    }
    
    .stTextInput > div > div > input {
        border: 2px solid #93c5fd !important;
        border-radius: var(--radius-md) !important;
        padding: 0.75rem !important;
        font-size: 1rem !important;
        background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%) !important;
        color: #1a202c !important;
        font-weight: 500 !important;
        box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1) !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: var(--primary-500) !important;
        box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.15) !important;
        background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%) !important;
    }
    
    .stTextArea > div > div > textarea {
        border: 2px solid #93c5fd !important;
        border-radius: var(--radius-md) !important;
        padding: 0.75rem !important;
        font-size: 1rem !important;
        background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%) !important;
        color: #1a202c !important;
        font-weight: 500 !important;
        box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1) !important;
    }
    
    .stTextArea > div > div > textarea:focus {
        border-color: var(--primary-500) !important;
        box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.15) !important;
        background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%) !important;
    }

    /* Fix placeholder text visibility */
    .stTextArea > div > div > textarea::placeholder {
        color: #6b7280 !important;
        opacity: 0.7 !important;
        font-weight: 400 !important;
    }

    .stTextInput > div > div > input::placeholder {
        color: #6b7280 !important;
        opacity: 0.7 !important;
        font-weight: 400 !important;
    }
    
    .stSelectbox > div > div {
        border: 2px solid #93c5fd !important;
        border-radius: var(--radius-md) !important;
        background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%) !important;
        box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1) !important;
    }

    /* Selectbox text and options visibility */
    .stSelectbox > div > div > div {
        color: #1a202c !important;
        font-weight: 500 !important;
    }

    .stSelectbox div[data-baseweb="select"] > div {
        color: #1a202c !important;
        font-weight: 500 !important;
    }

    /* Dropdown menu styling */
    .stSelectbox ul {
        background: #ffffff !important;
        border: 2px solid #93c5fd !important;
        border-radius: var(--radius-md) !important;
        box-shadow: 0 10px 15px -3px rgb(0 0 0 / 0.1) !important;
    }

    .stSelectbox ul li {
        color: #1a202c !important;
        font-weight: 500 !important;
        padding: 0.75rem !important;
    }

    .stSelectbox ul li:hover {
        background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%) !important;
        color: #1a202c !important;
    }
    
    .stSelectbox label {
        font-size: 0.875rem !important;
        font-weight: 600 !important;
        color: #ffffff !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .stTextInput label, .stTextArea label {
        font-size: 0.875rem !important;
        font-weight: 600 !important;
        color: #ffffff !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Progress Bar */
    .stProgress .st-bp {
        background: var(--primary-600) !important;
        border-radius: var(--radius-sm) !important;
    }
    
    .stProgress {
        background: var(--gray-200) !important;
        border-radius: var(--radius-sm) !important;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
        background: transparent;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: linear-gradient(135deg, #f1f5f9 0%, #e2e8f0 100%) !important;
        border: 2px solid #cbd5e0 !important;
        border-radius: var(--radius-md) !important;
        padding: 0.75rem 1.5rem !important;
        color: #374151 !important;
        font-weight: 600 !important;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, var(--primary-600) 0%, var(--primary-700) 100%) !important;
        color: white !important;
        border-color: var(--primary-600) !important;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3) !important;
    }
    
    /* Status Indicators */
    .status-badge {
        display: inline-flex;
        align-items: center;
        padding: 0.5rem 1rem;
        border-radius: var(--radius-md);
        font-size: 0.875rem;
        font-weight: 600;
        margin: 0.25rem;
    }
    
    .status-success {
        background: var(--success-50);
        color: var(--success-600);
        border: 1px solid var(--success-500);
    }
    
    .status-warning {
        background: var(--warning-50);
        color: var(--warning-600);
        border: 1px solid var(--warning-500);
    }
    
    .status-error {
        background: var(--error-50);
        color: var(--error-600);
        border: 1px solid var(--error-500);
    }
    
    /* Metrics Grid */
    .metrics-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1.5rem;
        margin: 2rem 0;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #ecfeff 0%, #cffafe 100%);
        border-radius: var(--radius-lg);
        padding: 1.5rem;
        text-align: center;
        box-shadow: var(--shadow-md);
        border: 2px solid #a7f3d0;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: var(--gray-900);
        display: block;
        margin-bottom: 0.5rem;
    }
    
    .metric-label {
        font-size: 0.875rem;
        color: var(--gray-600);
        text-transform: uppercase;
        letter-spacing: 0.5px;
        font-weight: 500;
    }
    
    /* Smart Text Visibility - Context-aware colors */
    
    /* Main content area - Dark text on light gradient background */
    .main .stMarkdown, .main .stMarkdown p, .main .stMarkdown div, .main .stMarkdown span {
        color: #1a202c !important;
        font-weight: 600 !important;
    }
    
    .main .stMarkdown h1, .main .stMarkdown h2, .main .stMarkdown h3, .main .stMarkdown h4 {
        color: #000000 !important;
        font-weight: 800 !important;
    }
    
    /* Section headers and content - dark text on light background */
    .section-title {
        color: #000000 !important;
        font-weight: 800 !important;
    }
    
    .section-subtitle {
        color: #374151 !important;
        font-weight: 600 !important;
    }
    
    /* Feature cards - dark text on light backgrounds */
    .feature-title {
        color: #1a202c !important;
        font-weight: 800 !important;
    }
    
    .feature-description {
        color: #4b5563 !important;
        font-weight: 600 !important;
    }
    
    /* Agent cards - dark text on light backgrounds */
    .agent-name {
        color: #1a202c !important;
        font-weight: 800 !important;
    }
    
    .agent-description {
        color: #4b5563 !important;
        font-weight: 600 !important;
    }
    
    /* Form elements - white labels for dark backgrounds */
    .stTextInput label, .stTextArea label, .stSelectbox label {
        color: #ffffff !important;
        font-weight: 700 !important;
    }
    
    /* Cards with light backgrounds - dark text */
    .card-title {
        color: #1a202c !important;
        font-weight: 800 !important;
    }
    
    .card-description {
        color: #4b5563 !important;
        font-weight: 600 !important;
    }
    
    /* Status and metrics - dark text */
    .metric-label {
        color: #374151 !important;
        font-weight: 700 !important;
    }
    
    /* General text improvements */
    .stMarkdown p {
        font-size: 1rem !important;
        line-height: 1.6 !important;
    }

    /* Agent Grid */
    .agent-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 1.5rem;
        margin: 2rem 0;
    }
    
    .agent-card {
        background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
        border-radius: var(--radius-lg);
        padding: 1.5rem;
        text-align: center;
        box-shadow: var(--shadow-md);
        border: 2px solid #fbbf24;
        transition: all 0.3s ease;
    }
    
    .agent-card:hover {
        transform: translateY(-3px);
        box-shadow: var(--shadow-lg);
        border-color: #f59e0b;
        background: linear-gradient(135deg, #fef3c7 0%, #fed7aa 100%);
    }
    
    .agent-icon {
        font-size: 2.5rem;
        margin-bottom: 1rem;
        display: block;
    }
    
    .agent-name {
        font-size: 1.125rem;
        font-weight: 600;
        color: var(--gray-900);
        margin-bottom: 0.5rem;
    }
    
    .agent-description {
        color: var(--gray-600);
        font-size: 0.875rem;
        line-height: 1.4;
    }
    
    /* Results Section */
    .results-container {
        background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
        border-radius: var(--radius-xl);
        padding: 2rem;
        margin: 2rem 0;
        box-shadow: var(--shadow-lg);
        border: 2px solid #7dd3fc;
    }
    
    /* Hide Streamlit Elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .hero-title {
            font-size: 2.5rem;
        }
        
        .hero-stats {
            gap: 1.5rem;
        }
        
        .section {
            padding: 2rem 1rem;
        }
        
        .section-title {
            font-size: 2rem;
        }
        
        .nav-content {
            flex-direction: column;
            gap: 1rem;
        }
        
        .feature-grid {
            grid-template-columns: 1fr;
        }
    }
    </style>
    """, unsafe_allow_html=True)

# COMPONENT FUNCTIONS


def render_hero_section():
    """Render the hero section like a modern React component"""
    st.markdown("""
    <div class="hero-section">
        <div class="hero-content">
            <h1 class="hero-title">AI Campaign Assistant Pro</h1>
            <p class="hero-subtitle">
                Transform your marketing strategy with intelligent multi-agent AI. 
                Generate comprehensive campaigns in minutes, not days.
            </p>
            <div class="hero-stats">
                <div class="stat-item">
                    <span class="stat-number">4</span>
                    <span class="stat-label">AI Agents</span>
                </div>
                <div class="stat-item">
                    <span class="stat-number">10+</span>
                    <span class="stat-label">Channels</span>
                </div>
                <div class="stat-item">
                    <span class="stat-number">5min</span>
                    <span class="stat-label">Generation</span>
                </div>
                <div class="stat-item">
                    <span class="stat-number">99%</span>
                    <span class="stat-label">Success Rate</span>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_navigation():
    """Render navigation component"""
    st.markdown("""
    <div class="nav-container">
        <div class="nav-content">
            <div class="nav-logo">🚀 Campaign Assistant</div>
            <div class="nav-menu">
                <div class="nav-item active" onclick="scrollToSection('campaign')">Campaign Builder</div>
                <div class="nav-item" onclick="scrollToSection('agents')">AI Agents</div>
                <div class="nav-item" onclick="scrollToSection('features')">Features</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_features_section():
    """Render features section with Streamlit components"""
    
    # Section header
    st.markdown("""
    <div style="text-align: center; margin: 4rem 0 3rem 0;">
        <h2 style="font-size: 2.5rem; font-weight: 700; color: #ffffff; margin-bottom: 1rem; line-height: 1.2;">
            Powered by Advanced AI
        </h2>
        <p style="font-size: 1.125rem; color: #ffffff; max-width: 600px; margin: 0 auto; line-height: 1.6;">
            Our multi-agent system combines specialized AI experts to deliver 
            comprehensive marketing campaigns tailored to your needs.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Feature cards using Streamlit columns
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
                <div style="background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
                    border-radius: 0.75rem; padding: 2rem; text-align: center;
                    box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
                    border: 2px solid #93c5fd; transition: all 0.3s ease; height: 280px;
                    display: flex; flex-direction: column; justify-content: center;">
            <span style="font-size: 3rem; margin-bottom: 1rem; display: block;">🔍</span>
                                <h3 style="font-size: 1.25rem; font-weight: 800; color: #1a202c; margin-bottom: 0.75rem;">
                        Market Research
                    </h3>
                    <p style="color: #374151; line-height: 1.5; font-size: 0.95rem; font-weight: 600;">
                        Deep analysis of target audience, competitive landscape,
                        and market trends using advanced AI algorithms.
                    </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%); 
                    border-radius: 0.75rem; padding: 2rem; text-align: center; 
                    box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1); 
                    border: 2px solid #93c5fd; transition: all 0.3s ease; height: 280px;
                    display: flex; flex-direction: column; justify-content: center;">
            <span style="font-size: 3rem; margin-bottom: 1rem; display: block;">✨</span>
            <h3 style="font-size: 1.25rem; font-weight: 800; color: #1a202c; margin-bottom: 0.75rem;">
                Content Generation
            </h3>
            <p style="color: #374151; line-height: 1.5; font-size: 0.95rem; font-weight: 600;">
                Create compelling, conversion-focused content optimized 
                for different platforms and audience segments.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%); 
                    border-radius: 0.75rem; padding: 2rem; text-align: center; 
                    box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1); 
                    border: 2px solid #93c5fd; transition: all 0.3s ease; height: 280px;
                    display: flex; flex-direction: column; justify-content: center;">
            <span style="font-size: 3rem; margin-bottom: 1rem; display: block;">📱</span>
            <h3 style="font-size: 1.25rem; font-weight: 800; color: #1a202c; margin-bottom: 0.75rem;">
                Channel Selection
            </h3>
            <p style="color: #374151; line-height: 1.5; font-size: 0.95rem; font-weight: 600;">
                Intelligent platform recommendations based on your 
                audience, budget, and campaign objectives.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%); 
                    border-radius: 0.75rem; padding: 2rem; text-align: center; 
                    box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1); 
                    border: 2px solid #93c5fd; transition: all 0.3s ease; height: 280px;
                    display: flex; flex-direction: column; justify-content: center;">
            <span style="font-size: 3rem; margin-bottom: 1rem; display: block;">📅</span>
            <h3 style="font-size: 1.25rem; font-weight: 800; color: #1a202c; margin-bottom: 0.75rem;">
                Schedule Optimization
            </h3>
            <p style="color: #374151; line-height: 1.5; font-size: 0.95rem; font-weight: 600;">
                Data-driven timing strategies to maximize reach 
                and engagement across all channels.
            </p>
        </div>
        """, unsafe_allow_html=True)

def render_campaign_builder():
    """Render the main campaign builder component"""
    st.markdown("""
    <div class="section" id="campaign">
        <div class="section-header">
            <h2 style="font-size: 2.5rem; font-weight: 700; color: #ffffff; margin-bottom: 1rem; line-height: 1.2;">
            Build Your Campaign
        </h2>
             <p style="font-size: 1.125rem; color: #ffffff; max-width: 600px; margin: 0 auto; line-height: 1.6;">
             Describe your product and goals. Our AI agents will create a comprehensive 
             marketing strategy tailored to your specific needs.
        </p>
               
            
        
    </div>
    """, unsafe_allow_html=True)
    
    # Campaign Builder Form
    with st.container():
        col1, col2 = st.columns([2, 1])
        
        with col1:
            #st.markdown('<div class="card">', unsafe_allow_html=True)
            
            st.markdown("### 📝 Campaign Details")
            
            product = st.text_area(
                "Product/Service Description",
                placeholder="Describe your product in detail. Include features, benefits, and what makes it unique...",
                height=120,
                help="The more specific you are, the better our AI can tailor your campaign"
            )
            
            goal = st.text_area(
                "Marketing Objectives", 
                placeholder="What do you want to achieve? Include specific numbers and targets...",
                height=100,
                help="Be specific with metrics like user acquisition, sales targets, brand awareness goals"
            )
            
            col_a, col_b = st.columns(2)
            
            with col_a:
                budget = st.selectbox(
                    "Investment Level",
                    ["Startup ($1K-5K)", "SMB ($5K-25K)", "Enterprise ($25K+)"],
                    index=1,
                    help="This influences platform recommendations and strategy complexity"
                )
            
            with col_b:
                duration = st.selectbox(
                    "Campaign Duration",
                    ["Sprint (2 weeks)", "Standard (4 weeks)", "Extended (6 weeks)", "Long-term (8 weeks)", "Quarter (12 weeks)"],
                    index=1,
                    help="Duration affects content planning and budget pacing"
                )
            
            # Advanced options in expander
            with st.expander("🔧 Advanced Configuration"):
                col_x, col_y = st.columns(2)
                with col_x:
                    target_audience = st.text_input("Target Audience", placeholder="e.g., Tech professionals aged 25-45")
                    industry = st.selectbox("Industry", ["Technology", "Healthcare", "Finance", "E-commerce", "Education", "Other"])
                with col_y:
                    geo_target = st.text_input("Geographic Target", placeholder="e.g., North America, Global")
                    competition_level = st.slider("Competition Level", 1, 5, 3, help="How competitive is your market?")
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Generate button
            if st.button("🚀 Generate AI Campaign", type="primary", use_container_width=True):
                if not product or not goal:
                    st.error("❌ Please provide both product description and marketing objectives")
                else:
                    generate_campaign_with_ui(product, goal, budget, duration)
        
        with col2:
            render_agent_status_panel()

def render_agent_status_panel():
    """Render the agent status panel"""
    
    st.markdown("### 🤖 AI Agent Status")
    
    # Check API status
    gemini_key = os.getenv("GEMINI_API_KEY")
    
    if gemini_key:
        st.markdown('<div class="status-badge status-success">✅ Gemini Connected</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="status-badge status-error">❌ Gemini Offline</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Agent grid
    agents = [
        {"icon": "🔍", "name": "Research Agent", "desc": "Market analysis & insights"},
        {"icon": "✨", "name": "Content Agent", "desc": "Creative content generation"},  
        {"icon": "📱", "name": "Channel Agent", "desc": "Platform optimization"},
        {"icon": "📅", "name": "Schedule Agent", "desc": "Timing strategies"}
    ]
    
    # Different colors for each agent
    agent_colors = [
        {"bg": "linear-gradient(135deg, #fef2f2 0%, #fecaca 100%)", "border": "#f87171"},
        {"bg": "linear-gradient(135deg, #f0fdf4 0%, #bbf7d0 100%)", "border": "#4ade80"},
        {"bg": "linear-gradient(135deg, #fffbeb 0%, #fed7aa 100%)", "border": "#fb923c"},
        {"bg": "linear-gradient(135deg, #f3e8ff 0%, #d8b4fe 100%)", "border": "#a855f7"}
    ]
    
    for i, agent in enumerate(agents):
        color = agent_colors[i]
        st.markdown(f"""
        <div style="padding: 1rem; margin: 0.75rem 0; background: {color['bg']}; border-radius: var(--radius-md); border: 2px solid {color['border']}; transition: all 0.3s ease;">
            <div style="display: flex; align-items: center; gap: 0.75rem;">
                <span style="font-size: 1.75rem;">{agent['icon']}</span>
                <div>
                    <strong style="color: #1a202c; font-size: 0.95rem; font-weight: 700;">{agent['name']}</strong><br/>
                    <small style="color: #374151; font-weight: 500;">{agent['desc']}</small>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

def generate_campaign_with_ui(product, goal, budget, duration):
    """Generate campaign with beautiful UI feedback"""
    
    # Progress container
    progress_container = st.container()
    
    with progress_container:
        st.markdown("### 🤖 AI Agents Working...")
        
        # Create progress tracking
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Agent execution stages
        stages = [
            {"name": "🔍 Research Agent", "task": "Analyzing market and target audience", "progress": 25},
            {"name": "✨ Content Agent", "task": "Creating compelling content variations", "progress": 50},
            {"name": "📱 Channel Agent", "task": "Selecting optimal platforms", "progress": 75},
            {"name": "📅 Schedule Agent", "task": "Optimizing timing strategy", "progress": 100}
        ]
        
        # Visual progress feedback
        for i, stage in enumerate(stages):
            status_text.markdown(f"**{stage['name']}:** {stage['task']}")
            progress_bar.progress(stage['progress'])
        
       
        budget_clean = budget.split()[0]
        duration_clean = duration.split()[0] + " " + duration.split()[1]
        
       
        result = generate_campaign_plan(
            product_description=product,
            marketing_goal=goal,
            budget_range=budget_clean,
            campaign_duration=duration_clean
        )
        
        # Clear progress
        progress_bar.empty()
        status_text.empty()
        
        # Display results
        if result["success"]:
            render_campaign_results(result["campaign_plan"])
        else:
            render_error_message(result.get('error', 'Unknown error occurred'))

def render_campaign_results(plan):
    """Render campaign results with modern UI"""
    
    # Store campaign results in session state to prevent data loss
    st.session_state.campaign_plan = plan
    
    st.success("🎉 **Your AI-Generated Campaign Plan is Ready!**")
    
    # Campaign overview metrics
    overview = plan["campaign_overview"]
    
    st.markdown("""
    <div class="metrics-grid">
        <div class="metric-card">
            <span class="metric-value">💰</span>
            <span class="metric-label">Investment</span>
            <div style="margin-top: 0.5rem; font-weight: 600; color: var(--gray-900);">{}</div>
        </div>
        <div class="metric-card">
            <span class="metric-value">⏰</span>
            <span class="metric-label">Duration</span>
            <div style="margin-top: 0.5rem; font-weight: 600; color: var(--gray-900);">{}</div>
        </div>
        <div class="metric-card">
            <span class="metric-value">📅</span>
            <span class="metric-label">Created</span>
            <div style="margin-top: 0.5rem; font-weight: 600; color: var(--gray-900);">{}</div>
        </div>
        <div class="metric-card">
            <span class="metric-value">🤖</span>
            <span class="metric-label">AI Agents</span>
            <div style="margin-top: 0.5rem; font-weight: 600; color: var(--gray-900);">4 Experts</div>
        </div>
    </div>
    """.format(
        overview['budget'],
        overview['duration'], 
        overview['created_date'].split()[0],
    ), unsafe_allow_html=True)
    
    # Results in tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🔍 Research Insights", "✨ Content Strategy", "📱 Channel Plan", "📅 Schedule", "🎯 Action Plan"
    ])
    
    with tab1:
        st.markdown('<div class="results-container">', unsafe_allow_html=True)
        st.markdown("### 🔍 Market Research & Audience Analysis")
        # Use session state to prevent data loss on interactions
        current_plan = st.session_state.get('campaign_plan', plan)
        st.markdown(current_plan["research_insights"])
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab2:
        st.markdown('<div class="results-container">', unsafe_allow_html=True)
        st.markdown("### ✨ Content Strategy & Creative Direction")
        # Use session state to prevent data loss on interactions
        current_plan = st.session_state.get('campaign_plan', plan)
        st.markdown(current_plan["content_strategy"])
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab3:
        st.markdown('<div class="results-container">', unsafe_allow_html=True)
        st.markdown("### 📱 Recommended Marketing Channels")
        # Use session state to prevent data loss on checkbox interaction
        current_plan = st.session_state.get('campaign_plan', plan)
        st.markdown(current_plan["channel_recommendations"])
        
        # Add sample visualization
        if st.checkbox("📊 Show Channel Allocation Chart"):
            create_channel_chart()
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab4:
        st.markdown('<div class="results-container">', unsafe_allow_html=True)
        st.markdown("### 📅 Optimal Posting Schedule")
        # Use session state to prevent data loss on checkbox interaction
        current_plan = st.session_state.get('campaign_plan', plan)
        st.markdown(current_plan["posting_schedule"])
        
        # Add sample schedule visualization
        if st.checkbox("📊 Show Weekly Schedule"):
            create_schedule_chart()
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab5:
        st.markdown('<div class="results-container">', unsafe_allow_html=True)
        st.markdown("### 🎯 Implementation Roadmap")
        
        # Use session state to prevent data loss on interactions
        current_plan = st.session_state.get('campaign_plan', plan)
        for i, step in enumerate(current_plan["next_steps"], 1):
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%); padding: 1.5rem; margin: 1rem 0; border-radius: var(--radius-lg); border-left: 5px solid #16a34a; box-shadow: var(--shadow-md); border: 2px solid #86efac;">
                <h4 style="color: #1a202c; margin-bottom: 0.5rem; font-weight: 700;">Step {i}: {step}</h4>
                <div style="background: linear-gradient(135deg, #ecfdf5 0%, #d1fae5 100%); padding: 0.75rem; border-radius: var(--radius-md); margin-top: 0.75rem; border: 2px solid #22c55e;">
                    <small style="color: #15803d; font-weight: 600;">💡 Ready for implementation</small>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Export options
        st.markdown("### 💾 Export Your Campaign")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            campaign_json = json.dumps(current_plan, indent=2)
            st.download_button(
                label="📄 Complete Plan (JSON)",
                data=campaign_json,
                file_name=f"campaign_{current_plan['campaign_overview']['created_date'].replace(':', '-').replace(' ', '_')}.json",
                mime="application/json",
                use_container_width=True
            )
        
        with col2:
            summary = create_text_summary(current_plan)
            st.download_button(
                label="📝 Executive Summary",
                data=summary,
                file_name=f"campaign_summary_{current_plan['campaign_overview']['created_date'].replace(':', '-').replace(' ', '_')}.txt",
                mime="text/plain",
                use_container_width=True
            )
        
        with col3:
            if st.button("📧 Share Campaign", use_container_width=True):
                st.info("📧 Sharing functionality ready for integration")
        
        st.markdown('</div>', unsafe_allow_html=True)

def render_error_message(error_msg):
    """Render error message with helpful guidance"""
    st.error(f"❌ Campaign generation failed: {error_msg}")
    
    # Specific guidance for rate limits
    if "429" in error_msg or "quota" in error_msg or "exceeded" in error_msg or "rate limit" in error_msg.lower():
        st.markdown("""
        <div class="results-container">
            <h3>🚨 Rate Limit Detected</h3>
            <p><strong>Solutions:</strong></p>
            <ol>
                <li><strong>Wait a few minutes</strong> and try again</li>
                <li><strong>Check your Gemini API quota</strong> at <a href="https://makersuite.google.com/app/apikey" target="_blank">Google AI Studio</a></li>
                <li><strong>Ensure your API key is valid</strong> and has sufficient quota</li>
            </ol>
            <p><strong>Why this happened:</strong> Your Gemini API quota has been exceeded or rate limited.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="results-container">
            <h3>🔧 Troubleshooting Guide</h3>
            <ul>
                <li><strong>API Issues:</strong> Check if your API keys are valid and have credits</li>
                <li><strong>Network:</strong> Ensure stable internet connection</li>
                <li><strong>Configuration:</strong> Verify environment variables are set correctly</li>
                <li><strong>Retry:</strong> Try again in a few minutes if APIs are overloaded</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

def create_channel_chart():
    """Create sample channel allocation chart"""
    data = {
        'Channel': ['Google Ads', 'Meta', 'LinkedIn', 'YouTube', 'Email'],
        'Budget_%': [35, 30, 20, 10, 5],
        'Expected_Reach': [50000, 45000, 25000, 30000, 15000]
    }
    
    fig = px.bar(
        x=data['Channel'],
        y=data['Budget_%'],
        title="Recommended Budget Allocation by Channel",
        color=data['Budget_%'],
        color_continuous_scale=['#3b82f6', '#1d4ed8', '#1e3a8a']
    )
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#374151'),
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)

def create_schedule_chart():
    """Create sample weekly schedule chart"""
    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    posts = [3, 2, 4, 3, 5, 2, 1]
    
    fig = px.bar(
        x=days, 
        y=posts, 
        title="Recommended Posts Per Day",
        color=posts,
        color_continuous_scale=['#3b82f6', '#1d4ed8']
    )
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#374151'),
        height=300
    )
    
    st.plotly_chart(fig, use_container_width=True)

def create_text_summary(plan):
    """Create executive summary"""
    overview = plan["campaign_overview"]
    
    return f"""
AI CAMPAIGN PLAN - EXECUTIVE SUMMARY
{'='*50}

CAMPAIGN OVERVIEW
Product: {overview['product']}
Objective: {overview['goal']}
Investment: {overview['budget']}
Timeline: {overview['duration']}
Generated: {overview['created_date']}

RESEARCH INSIGHTS
{plan['research_insights'][:500]}...

CONTENT STRATEGY
{plan['content_strategy'][:500]}...

CHANNEL RECOMMENDATIONS
{plan['channel_recommendations'][:500]}...

IMPLEMENTATION ROADMAP
{chr(10).join([f"{i}. {step}" for i, step in enumerate(plan['next_steps'], 1)])}

Generated by AI Campaign Assistant Pro
{overview['created_date']}
    """

def render_agent_testing_section():
    """Render individual agent testing section"""
    
    st.markdown("""
    <div style="text-align: center; margin: 4rem 0 3rem 0;">
        <h2 style="font-size: 2.5rem; font-weight: 700; color: #ffffff; margin-bottom: 1rem; line-height: 1.2;">
            🔬 Test Individual AI Agents
        </h2>
        <p style="font-size: 1.125rem; color: #ffffff; max-width: 600px; margin: 0 auto; line-height: 1.6;">
            Test each AI agent separately to understand their specialized capabilities and see how they work.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Agent testing grid
    col1, col2 = st.columns(2)
    
    with col1:
        # Research Agent Testing
        st.markdown("""
        <div style="background: linear-gradient(135deg, #fef2f2 0%, #fecaca 100%); 
                    border-radius: 1rem; padding: 2rem; margin-bottom: 2rem;
                    border: 2px solid #f87171; box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);">
            <div style="text-align: center; margin-bottom: 1.5rem;">
                <span style="font-size: 3rem; display: block; margin-bottom: 1rem;">🔍</span>
                <h3 style="font-size: 1.5rem; font-weight: 700; color: #1a202c; margin-bottom: 0.5rem;">
                    Research Agent
                </h3>
                <p style="color: #4b5563; font-size: 0.9rem;">
                    Market analysis and audience research specialist
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        with st.expander("🔍 Test Research Agent", expanded=False):
            st.markdown("**Test market research and audience analysis capabilities**")
            
            research_product = st.text_input(
                "Product Description", 
                "AI-powered fitness tracker with heart rate monitoring",
                key="research_product"
            )
            research_goal = st.text_input(
                "Marketing Goal", 
                "Increase brand awareness by 50% in the fitness market",
                key="research_goal"
            )
            
            if st.button("🔍 Analyze Market & Audience", key="test_research", use_container_width=True):
                with st.spinner("🔍 Research agent analyzing..."):
                    try:
                        result = test_research_agent(research_product, research_goal)
                        st.markdown("### 📊 Research Results")
                        st.success("✅ Analysis Complete!")
                        st.markdown(result)
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
        
        # Channel Agent Testing  
        st.markdown("""
        <div style="background: linear-gradient(135deg, #fff7ed 0%, #fed7aa 100%); 
                    border-radius: 1rem; padding: 2rem; margin-bottom: 2rem;
                    border: 2px solid #fb923c; box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);">
            <div style="text-align: center; margin-bottom: 1.5rem;">
                <span style="font-size: 3rem; display: block; margin-bottom: 1rem;">📱</span>
                <h3 style="font-size: 1.5rem; font-weight: 700; color: #1a202c; margin-bottom: 0.5rem;">
                    Channel Agent
                </h3>
                <p style="color: #4b5563; font-size: 0.9rem;">
                    Platform selection and optimization expert
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        with st.expander("📱 Test Channel Agent", expanded=False):
            st.markdown("**Test platform selection and channel recommendations**")
            
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                channel_product = st.text_input("Product", "AI fitness app", key="channel_product")
            with col_b:
                channel_budget = st.selectbox("Budget", ["Low", "Medium", "High"], key="channel_budget")
            with col_c:
                channel_goal = st.text_input("Goal", "Get 10,000 users", key="channel_goal")
            
            if st.button("📱 Recommend Channels", key="test_channel", use_container_width=True):
                with st.spinner("📱 Channel agent analyzing platforms..."):
                    try:
                        result = test_channel_agent(channel_product, channel_budget, channel_goal)
                        st.markdown("### 📊 Channel Recommendations")
                        st.success("✅ Platforms Analyzed!")
                        st.markdown(result)
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
    
    with col2:
        # Content Agent Testing
        st.markdown("""
        <div style="background: linear-gradient(135deg, #f0fdf4 0%, #bbf7d0 100%); 
                    border-radius: 1rem; padding: 2rem; margin-bottom: 2rem;
                    border: 2px solid #4ade80; box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);">
            <div style="text-align: center; margin-bottom: 1.5rem;">
                <span style="font-size: 3rem; display: block; margin-bottom: 1rem;">✨</span>
                <h3 style="font-size: 1.5rem; font-weight: 700; color: #1a202c; margin-bottom: 0.5rem;">
                    Content Agent
                </h3>
                <p style="color: #4b5563; font-size: 0.9rem;">
                    Creative content generation specialist
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        with st.expander("✨ Test Content Agent", expanded=False):
            st.markdown("**Test creative content generation and copywriting**")
            
            content_product = st.text_area(
                "Product Description", 
                "Transform your fitness journey with our AI-powered health tracker",
                height=80,
                key="content_product"
            )
            content_audience = st.text_area(
                "Target Audience (optional)", 
                "Health-conscious professionals aged 25-45",
                height=60,
                key="content_audience"
            )
            
            if st.button("✨ Generate Content Variations", key="test_content", use_container_width=True):
                with st.spinner("✨ Content agent creating variations..."):
                    try:
                        result = test_content_agent(content_product, content_audience)
                        st.markdown("### 📝 Content Results")
                        st.success("✅ Content Created!")
                        st.markdown(result)
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
        
        # Schedule Agent Testing
        st.markdown("""
        <div style="background: linear-gradient(135deg, #f3e8ff 0%, #d8b4fe 100%); 
                    border-radius: 1rem; padding: 2rem; margin-bottom: 2rem;
                    border: 2px solid #a855f7; box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);">
            <div style="text-align: center; margin-bottom: 1.5rem;">
                <span style="font-size: 3rem; display: block; margin-bottom: 1rem;">📅</span>
                <h3 style="font-size: 1.5rem; font-weight: 700; color: #1a202c; margin-bottom: 0.5rem;">
                    Schedule Agent
                </h3>
                <p style="color: #4b5563; font-size: 0.9rem;">
                    Timing optimization and scheduling expert
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        with st.expander("📅 Test Schedule Agent", expanded=False):
            st.markdown("**Test timing optimization and posting schedules**")
            
            col_x, col_y = st.columns(2)
            with col_x:
                schedule_channels = st.text_input(
                    "Selected Channels", 
                    "Google Ads, Meta, LinkedIn",
                    key="schedule_channels"
                )
            with col_y:
                schedule_duration = st.selectbox(
                    "Duration", 
                    ["2 weeks", "4 weeks", "6 weeks", "8 weeks"],
                    key="schedule_duration"
                )
            
            if st.button("📅 Create Optimal Schedule", key="test_schedule", use_container_width=True):
                with st.spinner("📅 Schedule agent optimizing timing..."):
                    try:
                        result = test_schedule_agent(schedule_channels, schedule_duration)
                        st.markdown("### 📋 Posting Schedule")
                        st.success("✅ Schedule Optimized!")
                        st.markdown(result)
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
    
    # Quick test all agents
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; margin: 2rem 0;">
        <h3 style="font-size: 1.5rem; font-weight: 600; color: #1a202c;">
            🚀 Quick Test All Agents
        </h3>
        <p style="color: #4b5563;">
            Test all four agents with sample data to see the complete workflow
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🚀 Test All Agents with Sample Data", type="primary", use_container_width=True):
        st.markdown("### 🤖 Testing All AI Agents...")
        
        # Test all agents with sample data
        sample_product = "AI-powered fitness tracker with personalized coaching"
        sample_goal = "Launch product and acquire 50,000 users in 6 months"
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("#### 🔍 Research Agent")
            with st.spinner("Analyzing..."):
                try:
                    research_result = test_research_agent(sample_product, sample_goal)
                    st.success("✅ Complete")
                    with st.expander("View Results"):
                        st.markdown(research_result[:300] + "...")
                except Exception as e:
                    st.error(f"❌ Failed: {str(e)[:50]}...")
        
        with col2:
            st.markdown("#### ✨ Content Agent")
            with st.spinner("Creating..."):
                try:
                    content_result = test_content_agent(sample_product, "Tech-savvy fitness enthusiasts")
                    st.success("✅ Complete")
                    with st.expander("View Results"):
                        st.markdown(content_result[:300] + "...")
                except Exception as e:
                    st.error(f"❌ Failed: {str(e)[:50]}...")
        
        with col3:
            st.markdown("#### 📱 Channel Agent")
            with st.spinner("Selecting..."):
                try:
                    channel_result = test_channel_agent(sample_product, "Medium", sample_goal)
                    st.success("✅ Complete")
                    with st.expander("View Results"):
                        st.markdown(channel_result[:300] + "...")
                except Exception as e:
                    st.error(f"❌ Failed: {str(e)[:50]}...")
        
        with col4:
            st.markdown("#### 📅 Schedule Agent")
            with st.spinner("Optimizing..."):
                try:
                    schedule_result = test_schedule_agent("Google Ads, Meta, LinkedIn", "6 weeks")
                    st.success("✅ Complete")
                    with st.expander("View Results"):
                        st.markdown(schedule_result[:300] + "...")
                except Exception as e:
                    st.error(f"❌ Failed: {str(e)[:50]}...")

# =============================================================================
# MAIN APPLICATION
# =============================================================================

def main():
    """Main application with modern React-like structure and tabbed interface"""
    
    # Load modern CSS
    load_modern_css()
    
    # Render hero section
    render_hero_section()
    
    # Check API configuration
    gemini_key = os.getenv("GEMINI_API_KEY")
    
    if not gemini_key:
        st.markdown("""
        <div class="section">
            <div class="card" style="text-align: center; max-width: 600px; margin: 0 auto;">
                <h3 style="color: var(--error-600); margin-bottom: 1rem;">🔑 API Configuration Required</h3>
                <p style="margin-bottom: 2rem;">Please configure your Gemini API key to get started:</p>
                
                <div style="text-align: left; margin: 2rem 0;">
                    <h4>Gemini AI Setup</h4>
                    <ol>
                        <li>Get API key: <a href="https://makersuite.google.com/app/apikey" target="_blank">https://makersuite.google.com/app/apikey</a></li>
                        <li>Set environment variable: <code>GEMINI_API_KEY=your_key</code></li>
                        <li>Restart the Streamlit app</li>
                    </ol>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        return
    
    # Main application tabs
    main_tab1, main_tab2 = st.tabs(["🚀 Campaign Builder", "🔬 Test AI Agents"])
    
    with main_tab1:
        # Render features section
        render_features_section()
        
        # Render main campaign builder
        render_campaign_builder()
    
    with main_tab2:
        # Render agent testing section  
        render_agent_testing_section()
    
    # Footer (outside tabs)
    st.markdown("""
    <div style="text-align: center; padding: 3rem 2rem; background: var(--gray-800); color: white; margin-top: 4rem;">
        <p style="font-size: 1.125rem; margin-bottom: 1rem;">🚀 <strong>AI Campaign Assistant Pro</strong></p>
        <p style="color: #ffffff; font-weight: 600;">Powered by advanced multi-agent AI technology</p>
    </div>
    """, unsafe_allow_html=True)

# =============================================================================
# RUN APPLICATION
# =============================================================================

if __name__ == "__main__":
    main() 