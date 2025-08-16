"""
32-week conversation simulation for the healthcare agentic system.
Generates realistic healthcare interactions between members and staff agents.
"""

import random
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from database import HealthcareDatabase, ConversationType, Conversation
from actionables import ActionablesManager
from scheduler import SchedulingManager
from agents import create_healthcare_agents, get_agent_handoff_rules


class ConversationSimulator:
    """Simulates realistic conversations between healthcare agents and members."""
    
    def __init__(self, db: HealthcareDatabase, actionables_manager: ActionablesManager, 
                 scheduling_manager: SchedulingManager):
        self.db = db
        self.actionables_manager = actionables_manager
        self.scheduling_manager = scheduling_manager
        self.agents = create_healthcare_agents(db)
        self.handoff_rules = get_agent_handoff_rules()
        self.member_personas = self._create_member_personas()
        self.conversation_templates = self._create_conversation_templates()
        
    def _create_member_personas(self) -> List[Dict[str, Any]]:
        """Create diverse member personas for realistic conversations."""
        return [
            {
                "name": "Sarah Johnson",
                "age": 34,
                "concerns": ["work stress", "family health", "preventive care"],
                "communication_style": "detailed questions, thorough",
                "health_goals": ["reduce stress", "improve sleep", "family wellness"]
            },
            {
                "name": "Michael Chen",
                "age": 42,
                "concerns": ["chronic condition management", "medication adherence"],
                "communication_style": "direct, focused on outcomes",
                "health_goals": ["manage diabetes", "weight loss", "cardiovascular health"]
            },
            {
                "name": "Emily Rodriguez",
                "age": 28,
                "concerns": ["nutrition", "fitness", "mental health"],
                "communication_style": "enthusiastic, detail-oriented",
                "health_goals": ["optimize nutrition", "build fitness routine", "stress management"]
            }
        ]
    
    def _create_conversation_templates(self) -> Dict[ConversationType, List[Dict[str, Any]]]:
        """Create conversation templates for different interaction types."""
        return {
            ConversationType.MEDICAL_CONSULTATION: [
                {
                    "member_input": "I've been experiencing some unusual symptoms lately and wanted to discuss them with you.",
                    "agent_response_type": "medical_assessment",
                    "duration_minutes": 45
                },
                {
                    "member_input": "Can you help me understand my recent test results?",
                    "agent_response_type": "test_interpretation",
                    "duration_minutes": 30
                },
                {
                    "member_input": "I'm concerned about some side effects from my current medication.",
                    "agent_response_type": "medication_review",
                    "duration_minutes": 25
                }
            ],
            ConversationType.WEEKLY_CHECKUP: [
                {
                    "member_input": "How am I progressing with my health goals this week?",
                    "agent_response_type": "progress_review",
                    "duration_minutes": 20
                },
                {
                    "member_input": "I have some updates on how I've been feeling lately.",
                    "agent_response_type": "status_update",
                    "duration_minutes": 15
                }
            ],
            ConversationType.NUTRITION_CONSULT: [
                {
                    "member_input": "I'm struggling to stick to my meal plan. Can we adjust it?",
                    "agent_response_type": "meal_plan_adjustment",
                    "duration_minutes": 30
                },
                {
                    "member_input": "I have questions about supplements and their interaction with my diet.",
                    "agent_response_type": "supplement_consultation",
                    "duration_minutes": 25
                }
            ],
            ConversationType.PHYSICAL_THERAPY: [
                {
                    "member_input": "My exercise routine feels too challenging. Can we modify it?",
                    "agent_response_type": "exercise_modification",
                    "duration_minutes": 35
                },
                {
                    "member_input": "I'm experiencing some discomfort during certain exercises.",
                    "agent_response_type": "movement_assessment",
                    "duration_minutes": 40
                }
            ],
            ConversationType.PERFORMANCE_REVIEW: [
                {
                    "member_input": "What do my health metrics tell us about my progress?",
                    "agent_response_type": "data_analysis",
                    "duration_minutes": 30
                }
            ],
            ConversationType.MEMBER_QUERY: [
                {
                    "member_input": "I read an article about a new health trend. What are your thoughts?",
                    "agent_response_type": "health_education",
                    "duration_minutes": 15
                },
                {
                    "member_input": "My family member has a health concern. Can you provide some guidance?",
                    "agent_response_type": "family_health_guidance",
                    "duration_minutes": 20
                },
                {
                    "member_input": "I need to reschedule my upcoming appointment.",
                    "agent_response_type": "appointment_management",
                    "duration_minutes": 5
                }
            ]
        }
    
    def simulate_32_week_program(self, member_id: str = "member_001") -> Dict[str, Any]:
        """Simulate the complete 32-week healthcare program."""
        print("🏥 Starting 32-Week Healthcare Simulation...")
        print("=" * 60)
        
        simulation_results = {
            "member_id": member_id,
            "start_date": datetime.now().isoformat(),
            "total_weeks": 32,
            "weekly_summaries": {},
            "total_conversations": 0,
            "agent_interactions": {},
            "handoffs": [],
            "completion_status": "in_progress"
        }
        
        # Initialize agent interaction counters
        for agent_id in self.agents.keys():
            simulation_results["agent_interactions"][agent_id] = 0
        
        # Simulate each week
        for week in range(1, 33):
            week_summary = self.simulate_week(week, member_id)
            simulation_results["weekly_summaries"][week] = week_summary
            simulation_results["total_conversations"] += week_summary["conversations_count"]
            
            # Update agent interaction counts
            for conversation in week_summary["conversations"]:
                agent_id = conversation["agent_id"]
                simulation_results["agent_interactions"][agent_id] += 1
                
                if conversation.get("handoff_to"):
                    simulation_results["handoffs"].append({
                        "week": week,
                        "from_agent": agent_id,
                        "to_agent": conversation["handoff_to"],
                        "reason": conversation.get("handoff_reason", "Care coordination")
                    })
            
            print(f"✅ Week {week} completed - {week_summary['conversations_count']} conversations")
            
            # Simulate time passage (optional - remove for faster execution)
            # time.sleep(0.1)
        
        simulation_results["completion_status"] = "completed"
        simulation_results["end_date"] = datetime.now().isoformat()
        
        print("\n" + "=" * 60)
        print("🎉 32-Week Healthcare Simulation Completed!")
        self._print_simulation_summary(simulation_results)
        
        return simulation_results
    
    def simulate_week(self, week: int, member_id: str) -> Dict[str, Any]:
        """Simulate all conversations and interactions for a specific week."""
        week_summary = {
            "week": week,
            "conversations": [],
            "conversations_count": 0,
            "actionables_completed": 0,
            "handoffs": 0
        }
        
        # Get scheduled actionables for the week
        actionables = self.actionables_manager.get_week_actionables(week)
        scheduled_actionables = [a for a in actionables if a.scheduled_time]
        
        # Generate conversations for scheduled actionables
        for actionable in scheduled_actionables:
            conversation = self._generate_actionable_conversation(actionable, member_id, week)
            if conversation:
                week_summary["conversations"].append(conversation)
                week_summary["conversations_count"] += 1
                
                # Mark actionable as completed
                self.actionables_manager.complete_actionable(actionable.id)
                week_summary["actionables_completed"] += 1
        
        # Generate additional member-initiated conversations
        member_conversations = self._generate_member_initiated_conversations(week, member_id)
        week_summary["conversations"].extend(member_conversations)
        week_summary["conversations_count"] += len(member_conversations)
        
        # Count handoffs
        week_summary["handoffs"] = len([c for c in week_summary["conversations"] if c.get("handoff_to")])
        
        return week_summary
    
    def _generate_actionable_conversation(self, actionable, member_id: str, week: int) -> Optional[Dict[str, Any]]:
        """Generate a conversation based on a scheduled actionable."""
        agent_id = actionable.assigned_agent
        conversation_type = self._determine_conversation_type_from_actionable(actionable.required_action)
        
        # Get conversation template
        templates = self.conversation_templates.get(conversation_type, [])
        if not templates:
            return None
        
        template = random.choice(templates)
        
        # Generate conversation content
        conversation_content = self._generate_conversation_content(
            agent_id, member_id, conversation_type, template, actionable.description
        )
        
        # Determine if handoff is needed
        handoff_info = self._determine_handoff(agent_id, conversation_type, actionable.required_action)
        
        conversation_data = {
            "timestamp": actionable.scheduled_time.isoformat(),
            "agent_id": agent_id,
            "member_id": member_id,
            "conversation_type": conversation_type.value,
            "actionable_id": actionable.id,
            "duration_minutes": template["duration_minutes"],
            "content": conversation_content,
            "handoff_to": handoff_info["to_agent"] if handoff_info else None,
            "handoff_reason": handoff_info["reason"] if handoff_info else None
        }
        
        # Store conversation in database
        conversation = Conversation(
            id=None,
            week=week,
            timestamp=actionable.scheduled_time,
            agent_id=agent_id,
            member_id=member_id,
            conversation_type=conversation_type,
            content=conversation_content,
            actionable_id=actionable.id,
            handoff_to=handoff_info["to_agent"] if handoff_info else None,
            created_at=datetime.now()
        )
        self.db.create_conversation(conversation)
        
        return conversation_data
    
    def _generate_member_initiated_conversations(self, week: int, member_id: str) -> List[Dict[str, Any]]:
        """Generate additional member-initiated conversations for the week."""
        conversations = []
        
        # Generate 1-3 additional conversations per week
        num_conversations = random.randint(1, 3)
        
        for _ in range(num_conversations):
            # Member always starts with Ruby (concierge)
            conversation = self._generate_member_query_conversation(week, member_id)
            if conversation:
                conversations.append(conversation)
        
        return conversations
    
    def _generate_member_query_conversation(self, week: int, member_id: str) -> Optional[Dict[str, Any]]:
        """Generate a member-initiated query conversation."""
        templates = self.conversation_templates[ConversationType.MEMBER_QUERY]
        template = random.choice(templates)
        
        # Member always starts with Ruby
        agent_id = "ruby"
        conversation_type = ConversationType.MEMBER_QUERY
        
        # Generate conversation content
        conversation_content = self._generate_conversation_content(
            agent_id, member_id, conversation_type, template, ""
        )
        
        # Ruby might hand off to specialists
        handoff_info = self._determine_handoff_for_member_query(template["member_input"])
        
        # Generate timestamp for this week
        week_start = datetime.now() + timedelta(weeks=week-1)
        conversation_time = week_start + timedelta(
            days=random.randint(0, 4),  # Monday to Friday
            hours=random.randint(9, 17)  # Business hours
        )
        
        conversation_data = {
            "timestamp": conversation_time.isoformat(),
            "agent_id": agent_id,
            "member_id": member_id,
            "conversation_type": conversation_type.value,
            "actionable_id": None,
            "duration_minutes": template["duration_minutes"],
            "content": conversation_content,
            "handoff_to": handoff_info["to_agent"] if handoff_info else None,
            "handoff_reason": handoff_info["reason"] if handoff_info else None
        }
        
        # Store conversation in database
        conversation = Conversation(
            id=None,
            week=week,
            timestamp=conversation_time,
            agent_id=agent_id,
            member_id=member_id,
            conversation_type=conversation_type,
            content=conversation_content,
            actionable_id=None,
            handoff_to=handoff_info["to_agent"] if handoff_info else None,
            created_at=datetime.now()
        )
        self.db.create_conversation(conversation)
        
        return conversation_data
    
    def _generate_conversation_content(self, agent_id: str, member_id: str, 
                                     conversation_type: ConversationType, template: Dict[str, Any],
                                     context: str) -> str:
        """Generate realistic conversation content."""
        member_persona = random.choice(self.member_personas)
        
        content_parts = [
            f"**Week Conversation - {conversation_type.value.replace('_', ' ').title()}**",
            f"**Participants:** {self.agents[agent_id].name} and {member_persona['name']}",
            f"**Duration:** {template['duration_minutes']} minutes",
            f"**Context:** {context}" if context else "",
            "",
            f"**Member ({member_persona['name']}):** {template['member_input']}",
            "",
            f"**{self.agents[agent_id].name}:** Based on your question, I'll provide comprehensive guidance tailored to your needs. "
        ]
        
        # Add role-specific responses
        if agent_id == "ruby":
            content_parts.append("As your care coordinator, I want to ensure we address all your concerns and coordinate with the right specialists as needed.")
        elif agent_id == "dr_warren":
            content_parts.append("From a medical perspective, let me review your current status and provide evidence-based recommendations.")
        elif agent_id == "carla":
            content_parts.append("Let's look at your nutritional needs and create a sustainable plan that fits your lifestyle and preferences.")
        elif agent_id == "rachel":
            content_parts.append("I'll assess your current physical capabilities and design a safe, effective exercise program for your goals.")
        elif agent_id == "advik":
            content_parts.append("Let me analyze your health data to identify patterns and provide data-driven insights for optimization.")
        elif agent_id == "neel":
            content_parts.append("From a strategic perspective, let's ensure all aspects of your care are well-coordinated and aligned with your long-term goals.")
        
        content_parts.extend([
            "",
            f"**Key Discussion Points:**",
            f"- Addressed member's primary concern: {template['member_input'][:50]}...",
            f"- Reviewed relevant health data and progress",
            f"- Provided personalized recommendations",
            f"- Scheduled appropriate follow-up actions",
            f"- Ensured member understanding and comfort with plan"
        ])
        
        return "\n".join(filter(None, content_parts))
    
    def _determine_conversation_type_from_actionable(self, required_action: str) -> ConversationType:
        """Determine conversation type from actionable description."""
        action_lower = required_action.lower()
        
        if "medical" in action_lower or "examination" in action_lower or "lab" in action_lower:
            return ConversationType.MEDICAL_CONSULTATION
        elif "checkup" in action_lower:
            return ConversationType.WEEKLY_CHECKUP
        elif "exercise" in action_lower or "physical" in action_lower:
            return ConversationType.PHYSICAL_THERAPY
        elif "nutrition" in action_lower or "diet" in action_lower:
            return ConversationType.NUTRITION_CONSULT
        elif "performance" in action_lower or "data" in action_lower:
            return ConversationType.PERFORMANCE_REVIEW
        elif "relationship" in action_lower or "strategic" in action_lower:
            return ConversationType.RELATIONSHIP_MANAGEMENT
        else:
            return ConversationType.MEMBER_QUERY
    
    def _determine_handoff(self, from_agent: str, conversation_type: ConversationType, 
                          required_action: str) -> Optional[Dict[str, str]]:
        """Determine if a handoff is needed based on conversation context."""
        handoff_probability = 0.15  # 15% chance of handoff
        
        if random.random() > handoff_probability:
            return None
        
        # Ruby hands off most frequently
        if from_agent == "ruby":
            if "nutrition" in required_action.lower():
                return {"to_agent": "carla", "reason": "Nutrition expertise needed"}
            elif "exercise" in required_action.lower():
                return {"to_agent": "rachel", "reason": "Physical therapy consultation"}
            elif "complex" in required_action.lower() or "strategic" in required_action.lower():
                return {"to_agent": "neel", "reason": "Strategic coordination required"}
            else:
                return {"to_agent": "dr_warren", "reason": "Medical consultation needed"}
        
        # Other agents might hand back to Ruby or escalate to Neel
        elif from_agent in ["carla", "rachel", "advik"]:
            if random.random() < 0.7:
                return {"to_agent": "ruby", "reason": "Care coordination follow-up"}
            else:
                return {"to_agent": "neel", "reason": "Strategic escalation"}
        
        return None
    
    def _determine_handoff_for_member_query(self, member_input: str) -> Optional[Dict[str, str]]:
        """Determine handoff for member-initiated queries."""
        input_lower = member_input.lower()
        
        if "nutrition" in input_lower or "diet" in input_lower or "meal" in input_lower:
            return {"to_agent": "carla", "reason": "Nutrition expertise required"}
        elif "exercise" in input_lower or "physical" in input_lower or "movement" in input_lower:
            return {"to_agent": "rachel", "reason": "Physical therapy consultation"}
        elif "medical" in input_lower or "symptom" in input_lower or "medication" in input_lower:
            return {"to_agent": "dr_warren", "reason": "Medical consultation needed"}
        elif "data" in input_lower or "progress" in input_lower or "metrics" in input_lower:
            return {"to_agent": "advik", "reason": "Performance analysis requested"}
        elif "complex" in input_lower or "concern" in input_lower:
            return {"to_agent": "neel", "reason": "Strategic support needed"}
        
        return None
    
    def _print_simulation_summary(self, results: Dict[str, Any]):
        """Print a summary of the simulation results."""
        print(f"📊 Total Conversations: {results['total_conversations']}")
        print(f"🤝 Total Handoffs: {len(results['handoffs'])}")
        print("\n📈 Agent Interaction Counts:")
        for agent_id, count in results['agent_interactions'].items():
            agent_name = self.agents[agent_id].name
            print(f"  {agent_name}: {count} conversations")
        
        print(f"\n🔄 Handoff Summary:")
        handoff_summary = {}
        for handoff in results['handoffs']:
            key = f"{handoff['from_agent']} → {handoff['to_agent']}"
            handoff_summary[key] = handoff_summary.get(key, 0) + 1
        
        for handoff_pair, count in handoff_summary.items():
            print(f"  {handoff_pair}: {count} handoffs")
        
        print(f"\n⏱️  Simulation Duration: {results['start_date']} to {results['end_date']}")
    
    def get_conversation_history(self, member_id: str, agent_id: str = None, 
                                week: int = None) -> List[Dict[str, Any]]:
        """Get conversation history with optional filtering."""
        if week:
            conversations = self.db.get_conversations_by_week(week)
        elif agent_id:
            conversations = self.db.get_conversation_history(agent_id)
        else:
            # Get all conversations for member
            all_conversations = []
            for w in range(1, 33):
                week_conversations = self.db.get_conversations_by_week(w)
                all_conversations.extend(week_conversations)
            conversations = [c for c in all_conversations if c.member_id == member_id]
        
        return [
            {
                "timestamp": conv.timestamp.isoformat(),
                "week": conv.week,
                "agent": conv.agent_id,
                "type": conv.conversation_type.value,
                "content": conv.content,
                "handoff_to": conv.handoff_to
            }
            for conv in conversations
        ]