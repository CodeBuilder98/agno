"""
Scheduling intelligence system for the healthcare platform.
Manages automatic scheduling of actionables and time slot allocation.
"""

import random
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Tuple
from database import HealthcareDatabase, ScheduleSlot, ConversationType, Actionable, ActionableStatus
from actionables import ActionablesManager


class SchedulingManager:
    """Manages intelligent scheduling of healthcare appointments and actionables."""
    
    def __init__(self, db: HealthcareDatabase, actionables_manager: ActionablesManager):
        self.db = db
        self.actionables_manager = actionables_manager
        self.working_hours = list(range(9, 18))  # 9 AM to 5 PM
        self.working_days = list(range(1, 6))    # Monday to Friday
        
    def initialize_schedule_slots(self):
        """Initialize schedule slots for all 32 weeks."""
        for week in range(1, 33):
            self._create_week_schedule(week)
    
    def _create_week_schedule(self, week: int):
        """Create schedule slots for a specific week."""
        base_date = datetime.now() + timedelta(weeks=week-1)
        
        for day in self.working_days:
            for hour in self.working_hours:
                slot = ScheduleSlot(
                    id=None,
                    week=week,
                    day=day,
                    hour=hour,
                    is_available=True,
                    assigned_actionable_id=None,
                    conversation_type=None,
                    agent_id=None,
                    member_intent=None,
                    created_at=datetime.now()
                )
                self.db.create_schedule_slot(slot)
    
    def schedule_week_actionables(self, week: int) -> Dict[str, Any]:
        """Schedule all actionables for a specific week."""
        actionables = self.actionables_manager.get_week_actionables(week)
        available_slots = self.db.get_available_slots(week)
        
        scheduling_results = {
            "week": week,
            "total_actionables": len(actionables),
            "scheduled": 0,
            "failed": 0,
            "remaining_slots": len(available_slots),
            "scheduled_items": []
        }
        
        # Priority order for scheduling
        priority_order = [
            "Initial medical history collection",
            "Biological sample collection",
            "Physical examination component",
            "Weekly health checkup",
            "Comprehensive health assessment",
            "Exercise routine update",
            "Performance data analysis",
            "Nutrition plan review",
            "Strategic relationship review"
        ]
        
        # Sort actionables by priority
        sorted_actionables = self._sort_actionables_by_priority(actionables, priority_order)
        
        for actionable in sorted_actionables:
            if actionable.status == ActionableStatus.TO_BE_SCHEDULED:
                success, slot_info = self._schedule_single_actionable(actionable, available_slots, week)
                if success:
                    scheduling_results["scheduled"] += 1
                    scheduling_results["scheduled_items"].append({
                        "actionable": actionable.required_action,
                        "agent": actionable.assigned_agent,
                        "slot": slot_info
                    })
                    # Remove the used slot from available slots
                    available_slots = [s for s in available_slots if s.id != slot_info["slot_id"]]
                else:
                    scheduling_results["failed"] += 1
        
        scheduling_results["remaining_slots"] = len(available_slots)
        
        # Fill remaining slots with member queries
        self._fill_remaining_slots_with_member_queries(available_slots, week)
        
        return scheduling_results
    
    def _sort_actionables_by_priority(self, actionables: List[Actionable], 
                                    priority_order: List[str]) -> List[Actionable]:
        """Sort actionables by priority based on their required action."""
        def get_priority(actionable):
            for i, priority_action in enumerate(priority_order):
                if priority_action in actionable.required_action:
                    return i
            return len(priority_order)  # Lowest priority for unmatched items
        
        return sorted(actionables, key=get_priority)
    
    def _schedule_single_actionable(self, actionable: Actionable, 
                                  available_slots: List[ScheduleSlot], 
                                  week: int) -> Tuple[bool, Optional[Dict[str, Any]]]:
        """Schedule a single actionable to an available slot."""
        if not available_slots:
            return False, None
        
        # Find suitable slots based on actionable timing constraints
        suitable_slots = self._find_suitable_slots(actionable, available_slots, week)
        
        if not suitable_slots:
            return False, None
        
        # Select the best slot (earliest available)
        selected_slot = suitable_slots[0]
        
        # Determine conversation type based on actionable
        conversation_type = self._determine_conversation_type(actionable.required_action)
        
        # Book the slot
        self.db.book_schedule_slot(
            selected_slot.id,
            actionable.id,
            actionable.assigned_agent,
            conversation_type
        )
        
        # Update actionable status
        scheduled_time = self._calculate_slot_datetime(week, selected_slot.day, selected_slot.hour)
        self.actionables_manager.schedule_actionable(actionable.id, scheduled_time)
        
        return True, {
            "slot_id": selected_slot.id,
            "day": selected_slot.day,
            "hour": selected_slot.hour,
            "scheduled_time": scheduled_time.isoformat(),
            "conversation_type": conversation_type.value
        }
    
    def _find_suitable_slots(self, actionable: Actionable, 
                           available_slots: List[ScheduleSlot], 
                           week: int) -> List[ScheduleSlot]:
        """Find slots that are suitable for the actionable's timing constraints."""
        suitable_slots = []
        
        for slot in available_slots:
            slot_time = self._calculate_slot_datetime(week, slot.day, slot.hour)
            
            # Check if slot time is within actionable's time window
            # Relax the constraints if they're too restrictive
            if actionable.started_after and slot_time < (actionable.started_after - timedelta(days=1)):
                continue
            if actionable.completed_before and slot_time > (actionable.completed_before + timedelta(days=1)):
                continue
            
            suitable_slots.append(slot)
        
        # Sort by day and hour for earliest scheduling
        return sorted(suitable_slots, key=lambda x: (x.day, x.hour))
    
    def _calculate_slot_datetime(self, week: int, day: int, hour: int) -> datetime:
        """Calculate the actual datetime for a schedule slot."""
        base_date = datetime.now() + timedelta(weeks=week-1)
        # Adjust to the start of the week (Monday)
        days_since_monday = base_date.weekday()
        monday = base_date - timedelta(days=days_since_monday)
        # Add the specific day and hour
        slot_datetime = monday + timedelta(days=day-1, hours=hour)
        return slot_datetime
    
    def _determine_conversation_type(self, required_action: str) -> ConversationType:
        """Determine conversation type based on the required action."""
        action_lower = required_action.lower()
        
        if "medical history" in action_lower or "examination" in action_lower:
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
    
    def _fill_remaining_slots_with_member_queries(self, available_slots: List[ScheduleSlot], week: int):
        """Fill remaining available slots with member queries and general interactions."""
        member_intents = [
            "General health question",
            "Family member health concern",
            "Health article inquiry",
            "Medication question",
            "Symptom discussion",
            "Lifestyle advice request",
            "Appointment rescheduling",
            "Test result inquiry",
            "Wellness goal discussion",
            "Health education request"
        ]
        
        agents_for_queries = ["ruby", "dr_warren", "neel"]  # Agents that handle general queries
        
        for slot in available_slots[:min(len(available_slots), 10)]:  # Fill up to 10 slots
            # Randomly assign member intents to available slots
            intent = random.choice(member_intents)
            agent = random.choice(agents_for_queries)
            
            # Update the slot with member query information
            # Note: This is a simplified implementation - in practice, you'd update the database
            slot.conversation_type = ConversationType.MEMBER_QUERY
            slot.agent_id = agent
            slot.member_intent = intent
    
    def generate_weekly_intents(self, week: int) -> List[Dict[str, Any]]:
        """Generate weekly intents for all agents based on their roles and the week's context."""
        intents = []
        
        # Ruby (Concierge) - Always has coordination intents
        intents.append({
            "agent_id": "ruby",
            "week": week,
            "intent": "Coordinate weekly care activities",
            "description": f"Review week {week} schedule, ensure all appointments are confirmed, and follow up on any outstanding items",
            "priority": "high"
        })
        
        # Dr. Warren (Medical) - Medical review intents
        if week <= 4 or week % 4 == 0:  # Initial weeks or monthly
            intents.append({
                "agent_id": "dr_warren",
                "week": week,
                "intent": "Medical assessment and review",
                "description": f"Conduct comprehensive medical review for week {week}, review any test results, and update treatment plans",
                "priority": "high"
            })
        
        # Advik (Performance) - Data analysis intents
        if week % 4 == 0:  # Monthly performance reviews
            intents.append({
                "agent_id": "advik",
                "week": week,
                "intent": "Performance data analysis",
                "description": f"Analyze health metrics and trends from weeks {week-3} to {week}, identify patterns and recommendations",
                "priority": "medium"
            })
        
        # Carla (Nutrition) - Nutrition planning intents
        if week == 1 or (week - 2) % 4 == 0:  # Initial and monthly reviews
            intents.append({
                "agent_id": "carla",
                "week": week,
                "intent": "Nutrition plan review and adjustment",
                "description": f"Review nutrition goals and meal plans for week {week}, adjust based on progress and preferences",
                "priority": "medium"
            })
        
        # Rachel (Physical Therapy) - Exercise and movement intents
        if week % 2 == 0:  # Biweekly exercise updates
            intents.append({
                "agent_id": "rachel",
                "week": week,
                "intent": "Exercise routine update and assessment",
                "description": f"Assess physical progress for week {week}, update exercise plans, and address any movement concerns",
                "priority": "medium"
            })
        
        # Neel (Relationship Manager) - Strategic oversight intents
        if week % 8 == 0:  # Quarterly strategic reviews
            intents.append({
                "agent_id": "neel",
                "week": week,
                "intent": "Strategic care coordination review",
                "description": f"Comprehensive review of care coordination for weeks {week-7} to {week}, strategic planning for next phase",
                "priority": "high"
            })
        
        # Member - Always has potential intents
        member_weekly_intents = [
            "Schedule follow-up appointment",
            "Ask about recent test results",
            "Discuss family member health concern",
            "Inquire about health article recommendations",
            "Request appointment rescheduling",
            "Follow up on previous recommendations"
        ]
        
        intents.append({
            "agent_id": "member",
            "week": week,
            "intent": random.choice(member_weekly_intents),
            "description": f"Member-initiated interaction for week {week}",
            "priority": "variable"
        })
        
        return intents
    
    def get_week_schedule_summary(self, week: int) -> Dict[str, Any]:
        """Get a summary of the week's schedule."""
        available_slots = self.db.get_available_slots(week)
        scheduled_actionables = self.actionables_manager.get_week_actionables(week)
        
        # Count scheduled vs available
        total_possible_slots = len(self.working_days) * len(self.working_hours)
        booked_slots = total_possible_slots - len(available_slots)
        
        summary = {
            "week": week,
            "total_possible_slots": total_possible_slots,
            "available_slots": len(available_slots),
            "booked_slots": booked_slots,
            "utilization_rate": (booked_slots / total_possible_slots) * 100,
            "scheduled_actionables": len([a for a in scheduled_actionables if a.status == ActionableStatus.SCHEDULED]),
            "pending_actionables": len([a for a in scheduled_actionables if a.status == ActionableStatus.TO_BE_SCHEDULED]),
            "completed_actionables": len([a for a in scheduled_actionables if a.status == ActionableStatus.ACTION_TAKEN])
        }
        
        return summary
    
    def optimize_schedule(self, week: int) -> Dict[str, Any]:
        """Optimize the schedule for a specific week by attempting to reschedule items."""
        # This is a placeholder for more sophisticated scheduling optimization
        # Could include algorithms for:
        # - Minimizing agent travel time
        # - Balancing workload across agents
        # - Optimizing for member preferences
        # - Handling urgent vs routine appointments
        
        summary = self.get_week_schedule_summary(week)
        summary["optimization_applied"] = "Basic scheduling optimization"
        return summary