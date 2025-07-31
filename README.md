# Multi-Agent Campaign Assistant

A multi-agent system that automates digital campaign planning using **Gemini AI** and **CrewAI** agents.
click this link for demo :  https://campaignagentwebapp.onrender.com/
## 🎯 Overview

This system uses four specialized AI agents working together to create comprehensive digital marketing campaigns:

- **🔍 Research Agent**: Identifies target audience and analyzes market trends
- **✨ Content Agent**: Creates ad copy and creatives using advanced prompt chaining
- **📱 Channel Agent**: Selects optimal marketing platforms (Google, Meta, YouTube, etc.)
- **📅 Schedule Agent**: Recommends optimal posting schedules and campaign timing

## 🏗️ System Architecture

### Simple Structure
```
socialagent/
├── campaign_assistant.py  # Main system with 4 CrewAI agents
├── streamlit_app.py       # Web interface
├── requirements.txt       # Dependencies (only 5 packages!)
└── README.md              # Documentation
```

### LangGraph Workflow
The system uses LangGraph for sophisticated workflow orchestration:

1. **Input Validation** → Validate product description and goals
2. **Research Phase** → Parallel audience research and trend analysis
3. **Content Development** → Strategy creation with prompt chaining
4. **Channel Selection** → Platform analysis and recommendations
5. **Schedule Optimization** → Timing strategy and calendar creation
6. **Campaign Finalization** → Complete plan generation

### 🌐 Streamlit Web Interface
The web app provides an intuitive interface with:

- **📋 Campaign Planner**: Complete campaign generation with visual results
- **🔬 Individual Agent Testing**: Test each agent separately with custom inputs
- **📊 Interactive Visualizations**: Charts and graphs for campaign insights
- **💾 Export Functionality**: Download campaign plans as JSON files
- **🎯 Real-time Progress**: Live updates during campaign generation
- **📱 Responsive Design**: Works on desktop and mobile devices

## 🚀 Features

### Research Agent
- **Target Audience Analysis**: Demographics, psychographics, and behavior patterns
- **Market Trend Research**: Industry developments and opportunities
- **Competitive Intelligence**: Competitor strategy analysis
- **Smart Data Integration**: Web search when available, comprehensive knowledge base otherwise

### Content Agent (Advanced Prompt Chaining)
- **Multi-stage Content Creation**: Base strategy → Refinement → Platform optimization
- **Psychological Frameworks**: AIDA, PAS, Before-After-Bridge copywriting
- **Platform Optimization**: Character limits and format requirements
- **Creative Brief Generation**: Visual direction and brand guidelines
- **A/B Testing Variations**: Multiple content versions for testing

### Channel Agent
- **Platform Scoring**: Algorithm-based channel compatibility analysis
- **Budget Optimization**: ROI-focused channel mix recommendations
- **Audience Alignment**: Matching target demographics to platform strengths
- **Integration Strategy**: Cross-platform campaign coordination

### Schedule Agent
- **Optimal Timing**: Platform-specific best posting times
- **Campaign Sequencing**: Strategic launch phases
- **Global Coordination**: Multi-timezone scheduling
- **Performance-based Adaptation**: Data-driven schedule optimization

## 📋 Installation & Setup

### Prerequisites
- Python 3.8+
- Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
- Optional: SerperDev API key for web search

### Installation
```bash
# Clone the repository
git clone <repository-url>
cd socialagent

# Create virtual environment
python -m venv myenv
source myenv/bin/activate  # On Windows: myenv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
export GEMINI_API_KEY="your_gemini_api_key_here"
export SERPER_API_KEY="your_serper_api_key_here"  # Optional
```

## 🎮 Usage

### 🌐 Web Interface (Recommended)
```bash
streamlit run streamlit_app.py
```

### Command Line
```bash
python campaign_assistant.py
# Choose: 1. Quick Demo, 2. Interactive Mode
```
