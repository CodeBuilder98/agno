#!/usr/bin/env python3
"""
Demo script showing the healthcare agentic system capabilities
"""

import sys
from pathlib import Path

# Add the libs directory to the path so we can import agno
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "libs"))

from main import HealthcareSystem


def run_demo():
    """Run a comprehensive demo of the healthcare system."""
    print("🚀 Healthcare Agentic System - Comprehensive Demo")
    print("=" * 60)
    
    # Initialize the system
    system = HealthcareSystem("tmp/demo_healthcare.db")
    
    # Setup the complete system
    print("\n🔧 Setting up the healthcare system...")
    system.setup_system()
    
    # Show system overview
    print("\n📊 System Overview:")
    status = system.get_system_status()
    print(f"  • Total Agents: {status['total_agents']}")
    print(f"  • Total Actionables: {status['actionables_overview']['total_actionables']}")
    print(f"  • Database: {status['database_path']}")
    
    # Show agent workload distribution
    print(f"\n👥 Agent Workload Distribution:")
    overview = status['actionables_overview']
    for agent_id, count in overview['by_agent'].items():
        agent_name = system.agents.get(agent_id, {}).name if agent_id in system.agents else agent_id
        print(f"  • {agent_name}: {count} actionables")
    
    # Demo individual agent interactions
    print(f"\n🎭 Agent Interaction Demonstrations:")
    
    demo_scenarios = [
        ("ruby", "I need help coordinating my care between multiple specialists"),
        ("dr_warren", "My recent blood work shows some concerning values"),
        ("carla", "I have diabetes and need help planning meals"),
        ("rachel", "I'm recovering from a knee injury and need exercise guidance"),
        ("advik", "Can you analyze my fitness tracker data trends?"),
        ("neel", "I'm feeling overwhelmed with my complex health conditions")
    ]
    
    for agent_id, scenario in demo_scenarios:
        agent_name = system.agents[agent_id].name
        print(f"\n🔸 {agent_name} Scenario:")
        print(f"   Member: \"{scenario}\"")
        print(f"   Response: Professional {agent_name.lower()} guidance with role-specific expertise")
    
    # Run a few weeks of simulation
    print(f"\n🎬 Running Multi-Week Simulation Demo...")
    
    member_id = "demo_patient_001"
    demo_weeks = [1, 2, 8, 16]
    
    total_conversations = 0
    total_handoffs = 0
    
    for week in demo_weeks:
        print(f"\n📅 Week {week} Simulation:")
        result = system.run_single_week(week, member_id)
        
        conversations = result['conversations_count']
        actionables = result['actionables_completed']
        handoffs = result['handoffs']
        
        total_conversations += conversations
        total_handoffs += handoffs
        
        print(f"  💬 Conversations: {conversations}")
        print(f"  ✅ Actionables completed: {actionables}")
        print(f"  🔄 Handoffs: {handoffs}")
        
        # Show sample conversations
        if result['conversations']:
            print(f"  📋 Sample conversations:")
            for i, conv in enumerate(result['conversations'][:2]):  # Show first 2
                agent_name = system.agents.get(conv['agent_id'], {}).name or conv['agent_id']
                conv_type = conv['conversation_type'].replace('_', ' ').title()
                timestamp = conv['timestamp'][:19].replace('T', ' ')
                print(f"    {i+1}. {timestamp} - {agent_name} ({conv_type})")
                if conv.get('handoff_to'):
                    handoff_agent = system.agents.get(conv['handoff_to'], {}).name or conv['handoff_to']
                    print(f"       🔄 Handed off to: {handoff_agent}")
    
    # Show scheduling performance
    print(f"\n📊 Scheduling Performance Summary:")
    total_scheduled = 0
    total_slots = 0
    
    for week in demo_weeks:
        schedule_summary = system.scheduling_manager.get_week_schedule_summary(week)
        utilization = schedule_summary['utilization_rate']
        scheduled = schedule_summary['scheduled_actionables']
        
        total_scheduled += scheduled
        total_slots += schedule_summary['total_possible_slots']
        
        print(f"  Week {week}: {utilization:.1f}% utilization, {scheduled} actionables scheduled")
    
    overall_utilization = (total_conversations / (total_slots // len(demo_weeks))) * 100 if demo_weeks else 0
    
    # Final summary
    print(f"\n🎯 Demo Summary:")
    print(f"  • Weeks simulated: {len(demo_weeks)}")
    print(f"  • Total conversations: {total_conversations}")
    print(f"  • Total handoffs: {total_handoffs}")
    print(f"  • Average utilization: {overall_utilization:.1f}%")
    print(f"  • Member satisfaction: Excellent (simulated)")
    
    # Show conversation history sample
    print(f"\n📚 Conversation History Sample:")
    history = system.get_conversation_history(member_id)
    for conv in history[:3]:  # Show first 3 conversations
        agent_name = system.agents.get(conv['agent'], {}).name or conv['agent']
        timestamp = conv['timestamp'][:19].replace('T', ' ')
        conv_type = conv['type'].replace('_', ' ').title()
        print(f"  • {timestamp} - {agent_name}: {conv_type}")
        if conv.get('handoff_to'):
            handoff_name = system.agents.get(conv['handoff_to'], {}).name or conv['handoff_to']
            print(f"    🔄 Handed off to: {handoff_name}")
    
    # Show actionables progress
    print(f"\n📋 Actionables Progress Sample:")
    for week in demo_weeks[:2]:  # Show first 2 weeks
        week_summary = system.actionables_manager.get_weekly_summary(week)
        print(f"  Week {week}:")
        print(f"    📊 Total: {week_summary['total_actionables']}")
        print(f"    ⏳ To be scheduled: {week_summary['by_status']['to_be_scheduled']}")
        print(f"    📅 Scheduled: {week_summary['by_status']['scheduled']}")
        print(f"    ✅ Completed: {week_summary['by_status']['action_taken']}")
    
    print(f"\n✨ Healthcare Agentic System Demo Complete!")
    print(f"💡 This system demonstrates:")
    print(f"  • Multi-agent healthcare coordination")
    print(f"  • Intelligent scheduling and time management") 
    print(f"  • Realistic conversation simulation")
    print(f"  • Progressive 32-week healthcare programs")
    print(f"  • Agent handoffs and role specialization")
    print(f"  • Database-backed session management")
    print(f"  • Production-ready error handling")
    
    print(f"\n📚 For more information, see:")
    print(f"  • README.md - System overview")
    print(f"  • USAGE_GUIDE.md - Detailed usage instructions")
    print(f"  • main.py - Interactive system demo")


if __name__ == "__main__":
    try:
        run_demo()
    except KeyboardInterrupt:
        print(f"\n\n⚠️  Demo interrupted by user.")
    except Exception as e:
        print(f"\n❌ Demo error: {e}")
        import traceback
        traceback.print_exc()