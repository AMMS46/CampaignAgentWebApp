"""
AI Campaign Assistant - Simplified Version for Streamlit Cloud
No CrewAI dependency to avoid ChromaDB/SQLite issues
"""
import streamlit as st
import json
import os
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import pandas as pd
import requests

# Simple LLM setup without CrewAI
def setup_llm():
    """Simple LLM setup using direct API calls"""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        st.error("❌ GEMINI_API_KEY environment variable is required!")
        st.stop()
    return api_key

# Simple API call function
def call_gemini_api(prompt, api_key):
    """Make direct API call to Gemini"""
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
    headers = {
        "Content-Type": "application/json",
    }
    data = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }
    
    try:
        response = requests.post(
            f"{url}?key={api_key}",
            headers=headers,
            json=data,
            timeout=60
        )
        response.raise_for_status()
        result = response.json()
        return result["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        return f"Error: {str(e)}"

# Simple agent functions
def research_agent_simple(product, goal, api_key):
    """Simple research agent using direct API calls"""
    prompt = f"""
    Act as a Market Research Specialist. Analyze this product and marketing goal:
    
    Product: {product}
    Goal: {goal}
    
    Provide a concise market research analysis (under 300 words) including:
    1. Target audience analysis
    2. Key market trends
    3. Competitor insights
    4. Market opportunities
    
    Be realistic and actionable. Don't fabricate specific statistics.
    """
    return call_gemini_api(prompt, api_key)

def content_agent_simple(product, audience, api_key):
    """Simple content agent using direct API calls"""
    prompt = f"""
    Act as a Creative Content Strategist. Create marketing content for:
    
    Product: {product}
    Target Audience: {audience}
    
    Generate:
    1. 3 compelling headlines (benefit-focused, problem-solving, social proof)
    2. 3 ad copy variations (50-75 words each)
    3. Key messaging themes
    4. Call-to-action suggestions
    
    Make it conversion-focused and engaging.
    """
    return call_gemini_api(prompt, api_key)

def channel_agent_simple(product, budget, goal, api_key):
    """Simple channel agent using direct API calls"""
    prompt = f"""
    Act as a Digital Marketing Channel Expert. Recommend marketing channels for:
    
    Product: {product}
    Budget: {budget}
    Goal: {goal}
    
    Provide:
    1. Top 5 recommended channels ranked by priority
    2. Budget allocation suggestions (percentages)
    3. Rationale for each channel selection
    4. Expected performance metrics
    
    Focus on ROI and effectiveness.
    """
    return call_gemini_api(prompt, api_key)

def schedule_agent_simple(channels, duration, api_key):
    """Simple schedule agent using direct API calls"""
    prompt = f"""
    Act as a Campaign Timing & Schedule Expert. Create posting schedule for:
    
    Selected Channels: {channels}
    Campaign Duration: {duration}
    
    Provide:
    1. Weekly posting frequency for each channel
    2. Best days and times for each platform
    3. Content calendar structure
    4. Performance monitoring milestones
    
    Optimize for maximum engagement.
    """
    return call_gemini_api(prompt, api_key)

# Main campaign generation
def generate_campaign_plan_simple(product, goal, budget, duration):
    """Generate campaign plan using simple API calls"""
    api_key = setup_llm()
    
    with st.spinner("🔍 Researching market..."):
        research = research_agent_simple(product, goal, api_key)
    
    with st.spinner("✨ Creating content..."):
        content = content_agent_simple(product, "target audience", api_key)
    
    with st.spinner("📱 Selecting channels..."):
        channels = channel_agent_simple(product, budget, goal, api_key)
    
    with st.spinner("📅 Optimizing schedule..."):
        schedule = schedule_agent_simple("Google Ads, Meta, LinkedIn", duration, api_key)
    
    return {
        "success": True,
        "campaign_plan": {
            "campaign_overview": {
                "product": product,
                "goal": goal,
                "budget": budget,
                "duration": duration,
                "created_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            },
            "research_insights": research,
            "content_strategy": content,
            "channel_recommendations": channels,
            "posting_schedule": schedule,
            "next_steps": [
                "Review and approve content variations",
                "Set up accounts on recommended platforms",
                "Configure targeting and budgets",
                "Launch campaign according to schedule",
                "Monitor performance and optimize"
            ]
        }
    }

# Streamlit UI
def main():
    st.set_page_config(
        page_title="AI Campaign Assistant",
        page_icon="🚀",
        layout="wide"
    )
    
    st.title("🚀 AI Campaign Assistant")
    st.markdown("Generate comprehensive marketing campaigns with AI")
    
    # Check API key
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        st.error("❌ GEMINI_API_KEY not found! Please set it in Streamlit Cloud Secrets.")
        st.info("Go to your app settings → Secrets and add: GEMINI_API_KEY = 'your_key'")
        return
    
    st.success("✅ Gemini API connected!")
    
    # Campaign builder
    st.header("📋 Campaign Builder")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        product = st.text_area(
            "Product/Service Description",
            placeholder="Describe your product in detail...",
            height=120
        )
        
        goal = st.text_area(
            "Marketing Objectives", 
            placeholder="What do you want to achieve?",
            height=100
        )
        
        col_a, col_b = st.columns(2)
        with col_a:
            budget = st.selectbox(
                "Investment Level",
                ["Startup ($1K-5K)", "SMB ($5K-25K)", "Enterprise ($25K+)"],
                index=1
            )
        
        with col_b:
            duration = st.selectbox(
                "Campaign Duration",
                ["2 weeks", "4 weeks", "6 weeks", "8 weeks", "12 weeks"],
                index=1
            )
        
        if st.button("🚀 Generate AI Campaign", type="primary", use_container_width=True):
            if not product or not goal:
                st.error("❌ Please provide both product description and marketing objectives")
            else:
                result = generate_campaign_plan_simple(product, goal, budget, duration)
                
                if result["success"]:
                    plan = result["campaign_plan"]
                    
                    st.success("🎉 Campaign Plan Generated!")
                    
                    # Display results in tabs
                    tab1, tab2, tab3, tab4, tab5 = st.tabs([
                        "🔍 Research", "✨ Content", "📱 Channels", "📅 Schedule", "🎯 Action Plan"
                    ])
                    
                    with tab1:
                        st.markdown("### Market Research & Insights")
                        st.write(plan["research_insights"])
                    
                    with tab2:
                        st.markdown("### Content Strategy")
                        st.write(plan["content_strategy"])
                    
                    with tab3:
                        st.markdown("### Channel Recommendations")
                        st.write(plan["channel_recommendations"])
                    
                    with tab4:
                        st.markdown("### Posting Schedule")
                        st.write(plan["posting_schedule"])
                    
                    with tab5:
                        st.markdown("### Implementation Roadmap")
                        for i, step in enumerate(plan["next_steps"], 1):
                            st.markdown(f"**{i}.** {step}")
                    
                    # Export
                    st.markdown("### 💾 Export Campaign")
                    campaign_json = json.dumps(plan, indent=2)
                    st.download_button(
                        label="📄 Download Campaign Plan (JSON)",
                        data=campaign_json,
                        file_name=f"campaign_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                        mime="application/json"
                    )
                else:
                    st.error(f"❌ Error: {result.get('error', 'Unknown error')}")
    
    with col2:
        st.markdown("### 🤖 AI Agents")
        st.markdown("""
        - **🔍 Research Agent** - Market analysis
        - **✨ Content Agent** - Creative content
        - **📱 Channel Agent** - Platform selection
        - **📅 Schedule Agent** - Timing optimization
        """)
        
        st.markdown("### 📊 Sample Metrics")
        st.metric("Campaign Duration", duration)
        st.metric("Budget Range", budget)
        st.metric("AI Agents Used", "4")

if __name__ == "__main__":
    main() 
