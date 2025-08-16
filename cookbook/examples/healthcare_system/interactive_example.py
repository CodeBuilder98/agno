"""
Interactive agent conversation example.
Shows how to use the healthcare agents for real conversations.

NOTE: This example is designed to work without OpenAI API keys for demonstration.
In production, you would set OPENAI_API_KEY environment variable.
"""

import sys
from pathlib import Path
import os

# Add the libs directory to the path so we can import agno
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "libs"))

from database import HealthcareDatabase
from agents import create_healthcare_agents


def mock_agent_conversation(agent, user_message: str) -> str:
    """
    Mock agent conversation for demonstration when API keys are not available.
    In production, you would use agent.run(user_message) or agent.cli_app()
    """
    agent_name = agent.name
    agent_role = agent.role
    
    # Create role-specific responses
    responses = {
        "Ruby": f"""
Hello! I'm {agent_name}, your healthcare concierge. I understand you're saying: "{user_message}"

As your care coordinator, I'm here to help you navigate your healthcare journey. Let me address your concern:

🩺 **My Assessment:**
Based on what you've shared, I can help coordinate the right care for you. I work closely with our entire healthcare team to ensure you get comprehensive support.

📋 **Next Steps:**
1. I'll review your current care plan
2. Connect you with the right specialist if needed
3. Schedule any necessary appointments
4. Follow up to ensure continuity of care

🤝 **Care Coordination:**
If your concern involves nutrition, I can connect you with Carla, our nutritionist. For physical therapy needs, Rachel is excellent. For complex medical questions, Dr. Warren is our medical authority.

Would you like me to schedule an appointment or connect you with a specific specialist?
""",
        
        "Dr. Warren": f"""
Good day. I'm Dr. Warren, your medical strategist. Regarding your concern: "{user_message}"

From a clinical perspective, let me provide evidence-based guidance:

🔬 **Medical Assessment:**
Your inquiry requires careful medical consideration. As a physician, I approach each case with systematic evaluation and evidence-based decision making.

📊 **Clinical Approach:**
1. Comprehensive history and symptom review
2. Physical examination if indicated
3. Appropriate diagnostic testing
4. Evidence-based treatment recommendations
5. Ongoing monitoring and follow-up

⚕️ **Recommendations:**
Based on current medical standards and best practices, I would recommend a thorough evaluation. Any treatment decisions should be made collaboratively, considering your medical history, current medications, and individual circumstances.

Please schedule a formal consultation for a comprehensive assessment. I can coordinate with other specialists as needed.
""",
        
        "Carla": f"""
Hi! I'm Carla, your nutritionist. Thanks for sharing: "{user_message}"

Let me help you with evidence-based nutrition guidance:

🥗 **Nutritional Assessment:**
Nutrition plays a crucial role in health outcomes. I focus on creating sustainable, personalized plans that fit your lifestyle and medical needs.

📚 **Educational Approach:**
1. Understanding your current dietary patterns
2. Identifying nutritional goals and challenges
3. Creating practical, achievable meal plans
4. Providing ongoing education and support
5. Adjusting plans based on progress and preferences

🍎 **Practical Guidance:**
I believe in making nutrition practical and enjoyable. We'll work together to develop habits you can maintain long-term, addressing any dietary restrictions or preferences you have.

Let's schedule a comprehensive nutrition assessment to create your personalized plan!
""",
        
        "Rachel": f"""
Hello! I'm Rachel, your physical therapist. You mentioned: "{user_message}"

Let me give you some movement and exercise guidance:

💪 **Physical Therapy Assessment:**
Movement is medicine! I specialize in helping people improve their physical function, manage pain, and prevent injuries through targeted exercise.

🏃‍♀️ **Movement Analysis:**
1. Current physical capabilities assessment
2. Movement pattern evaluation
3. Strength and flexibility testing
4. Functional goal identification
5. Progressive exercise program design

🎯 **Exercise Prescription:**
I'll create a safe, effective program tailored to your needs. We'll start where you are and progress gradually toward your goals, always prioritizing proper form and injury prevention.

Ready to get moving? Let's schedule an assessment to design your personalized exercise program!
""",
        
        "Advik": f"""
Greetings! I'm Advik, your performance scientist. Analyzing your input: "{user_message}"

Let me provide data-driven insights:

📊 **Performance Analysis:**
I specialize in analyzing health data to identify patterns, trends, and optimization opportunities. Data tells a story about your health journey.

🔬 **Analytical Approach:**
1. Comprehensive data collection and review
2. Statistical analysis and trend identification
3. Correlation analysis between variables
4. Evidence-based optimization recommendations
5. Progress tracking and measurement

📈 **Data Insights:**
Through careful analysis of your health metrics, I can identify what's working, what isn't, and where we can optimize. I use scientific methods to validate improvements and adjust strategies.

Let's set up a data review session to dive deep into your health metrics and create an optimization plan!
""",
        
        "Neel": f"""
Hello, I'm Neel, your relationship manager. I appreciate you sharing: "{user_message}"

From a strategic perspective, let me help coordinate your care:

🎯 **Strategic Overview:**
I focus on the big picture of your healthcare journey, ensuring all aspects of your care work together harmoniously for optimal outcomes.

🤝 **Relationship Management:**
1. Comprehensive care coordination
2. Communication facilitation between providers
3. Long-term goal alignment
4. Complex situation navigation
5. Advocacy and support

💭 **Holistic Approach:**
Healthcare can be complex, and I'm here to help you navigate it with confidence. I ensure your care team is working together effectively and that your voice is heard in all decisions.

Let's schedule a strategic planning session to review your overall care coordination and ensure everything is aligned with your goals.
"""
    }
    
    return responses.get(agent_name, f"Thank you for your message: '{user_message}'. As {agent_name}, I'm here to help with your healthcare needs.")


def interactive_demo():
    """Run an interactive demonstration of agent conversations."""
    
    print("🏥 Healthcare Agents - Interactive Conversation Demo")
    print("=" * 60)
    print("NOTE: This demo uses simulated responses. In production with API keys,")
    print("      agents would provide real AI-powered conversations.")
    print()
    
    # Initialize database and agents
    db = HealthcareDatabase("tmp/interactive_demo.db")
    agents = create_healthcare_agents(db)
    
    # Show available agents
    print("👥 Available Healthcare Agents:")
    for agent_id, agent in agents.items():
        if agent_id != "member":  # Skip member agent for this demo
            print(f"  {agent_id}: {agent.name} - {agent.role}")
    
    print(f"\n💡 Example interactions:")
    print(f"  ruby: 'I need help coordinating my care'")
    print(f"  dr_warren: 'Can you explain my test results?'")
    print(f"  carla: 'I need help with meal planning'")
    print(f"  rachel: 'My back has been hurting'")
    print(f"  advik: 'Analyze my fitness data'")
    print(f"  neel: 'I'm overwhelmed with appointments'")
    
    print(f"\n" + "=" * 60)
    
    while True:
        try:
            print(f"\nEnter: <agent_id> <your message>")
            print(f"Example: ruby I need help with my appointment")
            print(f"Type 'quit' to exit")
            
            user_input = input(f"\n🗣️  Your input: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                break
            
            # Parse input
            parts = user_input.split(' ', 1)
            if len(parts) < 2:
                print(f"❌ Please format as: <agent_id> <message>")
                continue
            
            agent_id, message = parts
            
            if agent_id not in agents or agent_id == "member":
                print(f"❌ Unknown agent: {agent_id}")
                print(f"Available: {', '.join([k for k in agents.keys() if k != 'member'])}")
                continue
            
            # Get agent response
            agent = agents[agent_id]
            print(f"\n🤖 {agent.name} responds:")
            print(f"-" * 40)
            
            try:
                # In production with API keys, you would use:
                # response = agent.run(message)
                response = mock_agent_conversation(agent, message)
                print(response)
            except Exception as e:
                print(f"Using simulated response (API not available): {e}")
                response = mock_agent_conversation(agent, message)
                print(response)
            
            print(f"-" * 40)
            
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print(f"\n✅ Interactive demo complete!")
    print(f"💡 To enable real AI conversations:")
    print(f"   1. Set OPENAI_API_KEY environment variable")
    print(f"   2. Use agent.run(message) or agent.cli_app()")


def showcase_handoffs():
    """Demonstrate agent handoff scenarios."""
    
    print(f"\n🔄 Agent Handoff Scenarios Demo")
    print(f"=" * 50)
    
    scenarios = [
        {
            "scenario": "Nutrition Question",
            "member_input": "I'm having trouble sticking to my diet",
            "initial_agent": "ruby",
            "handoff_to": "carla",
            "reason": "Nutrition expertise required"
        },
        {
            "scenario": "Exercise Injury",
            "member_input": "I hurt my shoulder during exercise",
            "initial_agent": "ruby", 
            "handoff_to": "rachel",
            "reason": "Physical therapy assessment needed"
        },
        {
            "scenario": "Complex Medical Question",
            "member_input": "I'm confused about my medication interactions",
            "initial_agent": "ruby",
            "handoff_to": "dr_warren", 
            "reason": "Medical expertise required"
        },
        {
            "scenario": "Care Coordination",
            "member_input": "I'm struggling to manage all my appointments",
            "initial_agent": "ruby",
            "handoff_to": "neel",
            "reason": "Strategic coordination needed"
        }
    ]
    
    for scenario in scenarios:
        print(f"\n📋 Scenario: {scenario['scenario']}")
        print(f"👤 Member: \"{scenario['member_input']}\"")
        print(f"🤖 Ruby: \"I understand your concern. Let me connect you with the right specialist.\"")
        print(f"🔄 Handoff: Ruby → {scenario['handoff_to']} ({scenario['reason']})")
        print(f"✅ Specialized care provided by appropriate expert")


if __name__ == "__main__":
    print("🚀 Healthcare Agentic System - Agent Interaction Examples")
    print("=" * 60)
    
    # Check if OpenAI API key is available
    api_key_available = bool(os.getenv("OPENAI_API_KEY"))
    
    if api_key_available:
        print("✅ OpenAI API key detected - Real AI conversations available")
    else:
        print("⚠️  No OpenAI API key - Using simulated responses for demo")
    
    try:
        interactive_demo()
        showcase_handoffs()
        
    except KeyboardInterrupt:
        print(f"\n\n⚠️  Demo interrupted by user.")
    except Exception as e:
        print(f"\n❌ Demo error: {e}")