
import os
import json
from datetime import datetime
from crewai import Agent, Task, Crew
from agents import initialize_agents, create_tasks, get_agents
from agents import test_research_agent, test_content_agent, test_channel_agent, test_schedule_agent
from crewai import LLM


api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("❌ GEMINI_API_KEY environment variable is required!")


serper_api_key = os.getenv("SERPER_API_KEY")
if serper_api_key:
    print("🔍 SerperDev API key found - enhanced market research enabled!")
else:
    print("💡 Set SERPER_API_KEY for live market research with real Google search")


os.environ["GOOGLE_API_KEY"] = api_key
os.environ["LITELLM_REQUEST_TIMEOUT"] = "120"
os.environ["LITELLM_DROP_PARAMS"] = "true"

model_options = ["gemini/gemini-2.5-flash"]

print("🔄 Setting up Gemini models...")
llm = None


try:
    print("🔄 Trying simple configuration...")
    llm = LLM(model="gemini/gemini-1.5-flash")
    print("✅ Successfully configured gemini-1.5-flash (simple config)")
except Exception as e:
    print(f"⚠️ Simple config failed: {str(e)[:100]}...")
    
    # Try with explicit parameters
    for model in model_options:
        try:
            print(f"🔄 Trying {model} with explicit params...")
            llm = LLM(model=model, temperature=0.7)
            print(f"✅ Successfully configured {model}")
            break
        except Exception as e:
            print(f"⚠️ {model} failed: {str(e)[:100]}...")
            continue

# Final fallback
if llm is None:
    print("⚠️ Using string fallback...")
    llm = "gemini/gemini-1.5-flash"

# Initialize agents
initialize_agents(llm)

def generate_campaign_plan(product_description: str, marketing_goal: str, 
                         budget_range: str = "Medium", campaign_duration: str = "4 weeks"):
    """
    Generate complete campaign plan using CrewAI agents
    This is the main function that orchestrates everything
    """
    
    print("🚀 Starting AI Campaign Planning...")
    print("=" * 50)
    
    try:
        # Step 1: Verify agents are initialized
        print("🔍 Checking agent initialization...")
        research_agent, content_agent, channel_agent, schedule_agent = get_agents()
        
        if not all([research_agent, content_agent, channel_agent, schedule_agent]):
            raise ValueError("❌ One or more agents are not properly initialized. Please check your API configuration.")
        
        print("✅ All agents are properly initialized")
        
        # Step 2: Create all tasks
        print("📋 Creating agent tasks...")
        research_task, content_task, channel_task, schedule_task = create_tasks(
            product_description, marketing_goal, budget_range, campaign_duration
        )
        
        # Step 2: Execute all agents in sequence
        print("🔍 Research agent analyzing market...")
        research_crew = Crew(
            agents=[research_agent],
            tasks=[research_task],
            verbose=True
        )
        research_results = research_crew.kickoff()
        
        print("✨ Content agent creating variations...")
        content_crew = Crew(
            agents=[content_agent],
            tasks=[content_task],
            verbose=True
        )
        content_results = content_crew.kickoff()
        
        print("📱 Channel agent selecting platforms...")
        channel_crew = Crew(
            agents=[channel_agent],
            tasks=[channel_task],
            verbose=True
        )
        channel_results = channel_crew.kickoff()
        
        print("📅 Schedule agent optimizing timing...")
        schedule_crew = Crew(
            agents=[schedule_agent],
            tasks=[schedule_task],
            verbose=True
        )
        schedule_results = schedule_crew.kickoff()
        
        # Step 6: Compile final campaign plan
        campaign_plan = {
            "campaign_overview": {
                "product": product_description,
                "goal": marketing_goal,
                "budget": budget_range,
                "duration": campaign_duration,
                "created_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            },
            "research_insights": str(research_results),
            "content_strategy": str(content_results),
            "channel_recommendations": str(channel_results),
            "posting_schedule": str(schedule_results),
            "next_steps": [
                "Review and approve content variations",
                "Set up accounts on recommended platforms",
                "Configure targeting and budgets",
                "Launch campaign according to schedule",
                "Monitor performance and optimize"
            ]
        }
        
        print("✅ Campaign Plan Generated Successfully!")
        return {
            "success": True,
            "campaign_plan": campaign_plan
        }
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }



def display_campaign_summary(result):
    """Display campaign plan in readable format"""
    if not result["success"]:
        print(f"❌ Campaign generation failed: {result.get('error')}")
        return
    
    plan = result["campaign_plan"]
    overview = plan["campaign_overview"]
    
    print("\n" + "=" * 60)
    print("📋 CAMPAIGN PLAN SUMMARY")
    print("=" * 60)
    
    print(f"🎯 Product: {overview['product']}")
    print(f"🎪 Goal: {overview['goal']}")
    print(f"💰 Budget: {overview['budget']}")
    print(f"⏰ Duration: {overview['duration']}")
    
    print(f"\n🔍 RESEARCH INSIGHTS:")
    print(f"{plan['research_insights'][:200]}...")
    
    print(f"\n✨ CONTENT STRATEGY:")
    print(f"{plan['content_strategy'][:200]}...")
    
    print(f"\n📱 CHANNEL RECOMMENDATIONS:")
    print(f"{plan['channel_recommendations'][:200]}...")
    
    print(f"\n📅 POSTING SCHEDULE:")
    print(f"{plan['posting_schedule'][:200]}...")
    
    print(f"\n🎯 NEXT STEPS:")
    for i, step in enumerate(plan['next_steps'], 1):
        print(f"   {i}. {step}")
    
    print(f"\n💾 Generated: {overview['created_date']}")
    print("=" * 60)

def quick_demo():
    """Quick demo with sample data"""
    print("🎬 QUICK DEMO - CrewAI Campaign Assistant")  
    print("=" * 50)
    
    result = generate_campaign_plan(
        product_description="AI-powered fitness app with personalized workout plans and nutrition tracking",
        marketing_goal="Acquire 50,000 new users and achieve 10,000 premium subscriptions",
        budget_range="Medium",
        campaign_duration="8 weeks"
    )
    
    display_campaign_summary(result)

def interactive_mode():
    """Interactive campaign planning"""
    print("🎯 INTERACTIVE CAMPAIGN PLANNER")
    print("=" * 40)
    
    try:
        product = input("📦 Describe your product/service: ").strip()
        goal = input("🎯 What's your marketing goal? ").strip()
        budget = input("💰 Budget range (Low/Medium/High) [Medium]: ").strip() or "Medium"
        duration = input("⏰ Campaign duration [4 weeks]: ").strip() or "4 weeks"
        
        print(f"\n🚀 Generating campaign with CrewAI agents...")
        
        result = generate_campaign_plan(product, goal, budget, duration)
        display_campaign_summary(result)
        
        # Save option
        save = input(f"\n💾 Save campaign plan? (y/n): ").strip().lower()
        if save == 'y':
            filename = f"campaign_plan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(filename, 'w') as f:
                json.dump(result, f, indent=2)
            print(f"✅ Saved to {filename}")
            
    except KeyboardInterrupt:
        print("\n👋 Campaign planning cancelled")



if __name__ == "__main__":
    print("🤖 Multi-Agent Campaign Assistant (CrewAI)")
    print("=" * 50)
    
    # Check API keys
    gemini_key = os.getenv("GEMINI_API_KEY")
    
    if not gemini_key:
        print("⚠️  Warning: No API key found!")
        print("Set: GEMINI_API_KEY='your_gemini_key'")
        print()
    else:
        print("✅ Gemini API key found")
        print()
    
    print("Choose an option:")
    print("1. Quick Demo")
    print("2. Interactive Mode") 
    print("3. Exit")
    
    choice = input("\nSelect option (1-3): ").strip()
    
    if choice == "1":
        quick_demo()
    elif choice == "2":
        interactive_mode()
    else:
        print("👋 Goodbye!") 
