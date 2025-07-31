
from crewai import Agent, Task, Crew
import os


try:
    from crewai_tools import SerperDevTool, WebsiteSearchTool, ScrapeWebsiteTool
    has_research_tools = True
except ImportError:
    has_research_tools = False

# Global agent variables
research_agent = None
content_agent = None
channel_agent = None  
schedule_agent = None

def initialize_agents(llm):
    """Simple agent initialization"""
    global research_agent, content_agent, channel_agent, schedule_agent
    
    # Setup research tools if available
    research_tools = []
    serper_api_key = os.getenv("SERPER_API_KEY")
    
    if has_research_tools and serper_api_key:
        research_tools = [SerperDevTool(), WebsiteSearchTool(), ScrapeWebsiteTool()]
        print("🔍 Enhanced research agent with live tools")
    
    # Create agents directly
    research_agent = Agent(
        llm=llm,
        role="Market Research Specialist",
        goal="Analyze target markets and provide actionable insights",
        backstory="Expert market researcher with deep knowledge of consumer behavior and market trends.",
        tools=research_tools,
        memory=True,
        verbose=False
    )
    
    content_agent = Agent(
        llm=llm,
        role="Creative Content Strategist", 
        goal="Create compelling, conversion-focused marketing content",
        backstory="Creative marketing expert who crafts compelling content that drives engagement and conversions.",
        tools=[],
        memory=True,
        verbose=False
    )
    
    channel_agent = Agent(
        llm=llm,
        role="Digital Marketing Channel Expert",
        goal="Recommend effective marketing channels and platforms",
        backstory="Digital marketing strategist with expertise in platform selection and audience targeting.",
        tools=[],
        memory=True,
        verbose=False
    )
    
    schedule_agent = Agent(
        llm=llm,
        role="Campaign Timing & Schedule Optimizer",
        goal="Create optimal posting schedules and timing strategies",
        backstory="Scheduling specialist who understands audience behavior patterns and optimal timing.",
        tools=[],
        memory=True,
        verbose=False
    )

def create_tasks(product_description, marketing_goal, budget_range, campaign_duration):
    """Simple task creation"""
    
    # Research task
    research_task = Task(
        description=f"""
        Analyze the market for: {product_description}
        Marketing Goal: {marketing_goal}
        
        Provide:
        - Target audience analysis
        - Key market trends  
        - Competitor insights
        - Market opportunities
        
        Keep response focused and under 300 words.
        """,
        agent=research_agent,
        expected_output="Market research analysis with audience insights and trends."
    )
    
    # Content task
    content_task = Task(
        description=f"""
        Create marketing content for: {product_description}
        
        Generate:
        1. 3 compelling headlines
        2. 3 ad copy variations (50-75 words each)
        3. Key messaging themes
        4. Call-to-action suggestions
        
        Make it conversion-focused and engaging.
        """,
        agent=content_agent,
        expected_output="Multiple content variations optimized for conversions."
    )
    
    # Channel task  
    channel_task = Task(
        description=f"""
        Recommend marketing channels for: {product_description}
        Budget: {budget_range}
        Goal: {marketing_goal}
        Duration: {campaign_duration}
        
        Provide:
        - Top 5 recommended channels
        - Budget allocation suggestions
        - Platform-specific strategies
        
        Focus on ROI and effectiveness.
        """,
        agent=channel_agent,
        expected_output="Channel recommendations with budget allocation and strategies."
    )
    
    # Schedule task
    schedule_task = Task(
        description=f"""
        Create posting schedule for: {campaign_duration} campaign
        Goal: {marketing_goal}
        
        Provide:
        - Weekly posting frequency
        - Best days and times
        - Content calendar structure
        - Performance milestones
        
        Optimize for maximum engagement.
        """,
        agent=schedule_agent,
        expected_output="Posting schedule with optimal timing and frequency."
    )
    
    return research_task, content_task, channel_task, schedule_task

def get_agents():
    """Return all agents"""
    return research_agent, content_agent, channel_agent, schedule_agent



"""The below code is for Frontend Feature"""

# test functions
def test_research_agent(product_description, marketing_goal):
    """Test research agent"""
    task = Task(
        description=f"Analyze market for: {product_description}. Goal: {marketing_goal}. Provide audience analysis.",
        agent=research_agent,
        expected_output="Market research analysis."
    )
    crew = Crew(agents=[research_agent], tasks=[task], verbose=True)
    return crew.kickoff()

def test_content_agent(product_description, audience_info=""):
    """Test content agent"""
    task = Task(
        description=f"Create content for: {product_description}. Audience: {audience_info}. Generate headlines and ad copy.",
        agent=content_agent,
        expected_output="Content variations."
    )
    crew = Crew(agents=[content_agent], tasks=[task], verbose=True)
    return crew.kickoff()

def test_channel_agent(product_description, budget_range, marketing_goal):
    """Test channel agent"""
    task = Task(
        description=f"Recommend channels for: {product_description}. Budget: {budget_range}. Goal: {marketing_goal}.",
        agent=channel_agent,
        expected_output="Channel recommendations."
    )
    crew = Crew(agents=[channel_agent], tasks=[task], verbose=True)
    return crew.kickoff()

def test_schedule_agent(selected_channels, campaign_duration):
    """Test schedule agent"""
    task = Task(
        description=f"Create schedule for: {selected_channels}. Duration: {campaign_duration}. Provide timing.",
        agent=schedule_agent,
        expected_output="Posting schedule."
    )
    crew = Crew(agents=[schedule_agent], tasks=[task], verbose=True)
    return crew.kickoff()