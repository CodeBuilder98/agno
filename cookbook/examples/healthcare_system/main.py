"""
Main orchestrator for the healthcare agentic system.
Runs the complete 32-week simulation with all agents and interactions.

Usage:
    python cookbook/examples/healthcare_system/main.py
"""

import os
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional, List

# Add the libs directory to the path so we can import agno
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "libs"))

from database import HealthcareDatabase
from actionables import ActionablesManager
from scheduler import SchedulingManager
from simulation import ConversationSimulator
from agents import create_healthcare_agents


class HealthcareSystem:
    """Main healthcare agentic system orchestrator."""
    
    def __init__(self, db_path: str = "tmp/healthcare_system.db"):
        """Initialize the healthcare system."""
        # Ensure tmp directory exists
        os.makedirs("tmp", exist_ok=True)
        
        self.db = HealthcareDatabase(db_path)
        self.actionables_manager = ActionablesManager(self.db)
        self.scheduling_manager = SchedulingManager(self.db, self.actionables_manager)
        self.simulator = ConversationSimulator(self.db, self.actionables_manager, self.scheduling_manager)
        self.agents = create_healthcare_agents(self.db)
        
        print("🏥 Healthcare Agentic System Initialized")
        print(f"📊 Database: {db_path}")
        print(f"👥 Agents: {len(self.agents)} healthcare professionals")
    
    def setup_system(self):
        """Set up the complete healthcare system for 32-week simulation."""
        print("\n🔧 Setting up healthcare system...")
        
        # Initialize actionables for all 32 weeks
        print("📋 Initializing actionables...")
        self.actionables_manager.initialize_all_actionables()
        
        # Initialize schedule slots for all weeks
        print("📅 Initializing schedule slots...")
        self.scheduling_manager.initialize_schedule_slots()
        
        # Schedule actionables for all weeks
        print("⏰ Scheduling actionables...")
        total_scheduled = 0
        total_failed = 0
        
        for week in range(1, 33):
            result = self.scheduling_manager.schedule_week_actionables(week)
            total_scheduled += result["scheduled"]
            total_failed += result["failed"]
            
            if week <= 5 or week % 8 == 0:  # Show progress for early weeks and every 8th week
                print(f"  Week {week}: {result['scheduled']} scheduled, {result['failed']} failed")
        
        print(f"✅ Scheduling complete: {total_scheduled} scheduled, {total_failed} failed")
        print("🚀 Healthcare system ready for simulation!")
    
    def run_simulation(self, member_id: str = "patient_001") -> Dict[str, Any]:
        """Run the complete 32-week healthcare simulation."""
        print(f"\n🎬 Starting 32-week simulation for member: {member_id}")
        print("=" * 80)
        
        # Run the full simulation
        results = self.simulator.simulate_32_week_program(member_id)
        
        return results
    
    def run_single_week(self, week: int, member_id: str = "patient_001") -> Dict[str, Any]:
        """Run simulation for a single week."""
        print(f"\n📅 Running week {week} simulation for member: {member_id}")
        
        # Schedule actionables for this week if not already done
        scheduling_result = self.scheduling_manager.schedule_week_actionables(week)
        print(f"📋 Week {week} scheduling: {scheduling_result['scheduled']} items scheduled")
        
        # Run week simulation
        week_result = self.simulator.simulate_week(week, member_id)
        
        # Print week summary
        print(f"✅ Week {week} completed:")
        print(f"  💬 Conversations: {week_result['conversations_count']}")
        print(f"  ✓ Actionables completed: {week_result['actionables_completed']}")
        print(f"  🔄 Handoffs: {week_result['handoffs']}")
        
        return week_result
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get current system status and statistics."""
        # Get actionables overview
        actionables_overview = self.actionables_manager.get_program_overview()
        
        # Get agent information
        agent_info = {
            agent_id: {
                "name": agent.name,
                "role": agent.role,
                "agent_id": agent.agent_id
            }
            for agent_id, agent in self.agents.items()
        }
        
        status = {
            "system_initialized": True,
            "database_path": self.db.db_path,
            "total_agents": len(self.agents),
            "agent_details": agent_info,
            "actionables_overview": actionables_overview,
            "current_time": datetime.now().isoformat()
        }
        
        return status
    
    def demonstrate_agent_interaction(self, agent_id: str, member_input: str) -> str:
        """Demonstrate a single agent interaction."""
        if agent_id not in self.agents:
            return f"Error: Agent '{agent_id}' not found"
        
        agent = self.agents[agent_id]
        
        # This is a simplified demonstration - in a full implementation,
        # you would use the agent's run method with proper session management
        response = f"""
**Demonstration of {agent.name} ({agent_id})**

**Member Input:** {member_input}

**Agent Response:** 
Hello! As your {agent.role}, I understand you're asking about: "{member_input}"

Based on my specialized training and role, I would provide personalized guidance 
tailored to your specific needs. In a real interaction, I would:

1. Review your medical history and current status
2. Provide evidence-based recommendations
3. Coordinate with other team members as needed
4. Schedule any necessary follow-up actions
5. Document our interaction for continuity of care

**Agent Characteristics:**
- Role: {agent.role}
- Specialization: {agent.description}
- Handoff capabilities: Can coordinate with other specialists as needed

Would you like to schedule a follow-up or connect with another specialist?
"""
        return response
    
    def get_conversation_history(self, member_id: str = "patient_001", 
                               week: Optional[int] = None) -> List[Dict[str, Any]]:
        """Get conversation history for a member."""
        return self.simulator.get_conversation_history(member_id, week=week)
    
    def print_system_overview(self):
        """Print a comprehensive system overview."""
        status = self.get_system_status()
        
        print("\n" + "=" * 80)
        print("🏥 HEALTHCARE AGENTIC SYSTEM OVERVIEW")
        print("=" * 80)
        
        print(f"🕒 System Status: {'✅ Active' if status['system_initialized'] else '❌ Not initialized'}")
        print(f"🗄️  Database: {status['database_path']}")
        print(f"👥 Total Agents: {status['total_agents']}")
        
        print(f"\n👨‍⚕️ HEALTHCARE TEAM:")
        for agent_id, details in status['agent_details'].items():
            print(f"  • {details['name']} ({agent_id})")
            print(f"    Role: {details['role']}")
        
        actionables = status['actionables_overview']
        print(f"\n📋 ACTIONABLES OVERVIEW:")
        print(f"  • Total weeks: {actionables['total_weeks']}")
        print(f"  • Total actionables: {actionables['total_actionables']}")
        print(f"  • Average per week: {actionables['total_actionables'] / actionables['total_weeks']:.1f}")
        
        print(f"\n📊 BY AGENT:")
        for agent_id, count in actionables['by_agent'].items():
            agent_name = self.agents.get(agent_id, {}).name if agent_id in self.agents else agent_id
            print(f"  • {agent_name}: {count} actionables")
        
        print("\n🚀 Ready for simulation!")
        print("=" * 80)


def main():
    """Main function to run the healthcare agentic system."""
    print("🏥 Healthcare Agentic System - 32 Week Simulation")
    print("=" * 60)
    
    # Initialize the system
    healthcare_system = HealthcareSystem()
    
    # Print system overview
    healthcare_system.print_system_overview()
    
    # Setup the system
    healthcare_system.setup_system()
    
    # Run a demonstration
    print("\n🎭 DEMONSTRATION MODE")
    print("-" * 40)
    
    # Demonstrate single agent interactions
    demo_interactions = [
        ("ruby", "I'd like to schedule my annual checkup and discuss my family's health."),
        ("dr_warren", "Can you help me understand my recent blood test results?"),
        ("carla", "I'm struggling with meal planning for my dietary restrictions."),
        ("rachel", "My knee has been bothering me during exercise. Can you help?"),
        ("advik", "What do my fitness metrics tell us about my progress?"),
        ("neel", "I'm feeling overwhelmed with all my health appointments.")
    ]
    
    for agent_id, member_input in demo_interactions:
        print(f"\n🗣️  Demonstrating interaction with {healthcare_system.agents[agent_id].name}:")
        response = healthcare_system.demonstrate_agent_interaction(agent_id, member_input)
        print(response)
        print("-" * 60)
    
    # Option to run full simulation
    print("\n🎬 SIMULATION OPTIONS")
    print("-" * 40)
    print("1. Run single week simulation (Week 1)")
    print("2. Run full 32-week simulation (may take a few minutes)")
    print("3. Show system status only")
    
    try:
        choice = input("\nEnter your choice (1, 2, or 3): ").strip()
        
        if choice == "1":
            print("\n🚀 Running Week 1 simulation...")
            result = healthcare_system.run_single_week(1)
            
            print(f"\n📋 Week 1 Conversations:")
            for conv in result['conversations']:
                print(f"  • {conv['timestamp'][:19]} - {conv['agent_id']} ({conv['conversation_type']})")
                if conv.get('handoff_to'):
                    print(f"    🔄 Handed off to: {conv['handoff_to']}")
        
        elif choice == "2":
            print("\n🚀 Running full 32-week simulation...")
            print("⚠️  This may take a few minutes...")
            
            results = healthcare_system.run_simulation()
            
            print(f"\n📊 Final Results:")
            print(f"  Total conversations: {results['total_conversations']}")
            print(f"  Total handoffs: {len(results['handoffs'])}")
            
            # Show sample conversations from different weeks
            sample_weeks = [1, 8, 16, 24, 32]
            for week in sample_weeks:
                if week in results['weekly_summaries']:
                    week_data = results['weekly_summaries'][week]
                    print(f"\n  Week {week}: {week_data['conversations_count']} conversations")
        
        elif choice == "3":
            print("\n📊 System Status:")
            status = healthcare_system.get_system_status()
            print(f"  Agents: {status['total_agents']}")
            print(f"  Actionables: {status['actionables_overview']['total_actionables']}")
            print(f"  Database: {status['database_path']}")
        
        else:
            print("Invalid choice. Showing system status only.")
    
    except KeyboardInterrupt:
        print("\n\n⚠️  Simulation interrupted by user.")
    except Exception as e:
        print(f"\n❌ Error: {e}")
    
    print("\n✅ Healthcare Agentic System demonstration complete!")
    print("📚 Check the README.md for more information about the system.")


if __name__ == "__main__":
    main()