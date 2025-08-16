"""
Weekly actionables system for the healthcare platform.
Defines and manages the 32-week progression of healthcare activities.
"""

from datetime import datetime, timedelta
from typing import List, Dict, Any
from database import HealthcareDatabase, Actionable, ActionableStatus


class ActionablesManager:
    def __init__(self, db: HealthcareDatabase):
        self.db = db
        self.actionables_template = self._create_actionables_template()

    def _create_actionables_template(self) -> Dict[int, List[Dict[str, Any]]]:
        """Create the template for all 32 weeks of actionables."""
        template = {}
        
        # Week 1: Member onboarding
        template[1] = [
            {
                "required_action": "Initial medical history collection",
                "description": "Comprehensive review of member's medical background, current medications, allergies, and family history",
                "assigned_agent": "dr_warren",
                "started_after": datetime.now() + timedelta(weeks=0),
                "completed_before": datetime.now() + timedelta(weeks=1, days=5)
            },
            {
                "required_action": "Health priorities assessment",
                "description": "Understand member's primary health goals and concerns",
                "assigned_agent": "ruby",
                "started_after": datetime.now() + timedelta(weeks=0),
                "completed_before": datetime.now() + timedelta(weeks=1, days=5)
            },
            {
                "required_action": "Dietary preferences and restrictions evaluation",
                "description": "Complete nutritional assessment including food preferences, allergies, and current diet",
                "assigned_agent": "carla",
                "started_after": datetime.now() + timedelta(weeks=0, days=1),
                "completed_before": datetime.now() + timedelta(weeks=1, days=5)
            },
            {
                "required_action": "Laboratory test planning discussion",
                "description": "Review recommended lab tests and schedule collection",
                "assigned_agent": "dr_warren",
                "started_after": datetime.now() + timedelta(weeks=0, days=2),
                "completed_before": datetime.now() + timedelta(weeks=1, days=5)
            }
        ]
        
        # Week 2-4: Biological samples and physical exams
        for week in range(2, 5):
            template[week] = [
                {
                    "required_action": "Biological sample collection",
                    "description": f"Week {week} lab sample collection and processing",
                    "assigned_agent": "dr_warren",
                    "started_after": datetime.now() + timedelta(weeks=week-1),
                    "completed_before": datetime.now() + timedelta(weeks=week, days=5)
                },
                {
                    "required_action": "Physical examination component",
                    "description": f"Week {week} physical assessment including vitals and mobility evaluation",
                    "assigned_agent": "rachel" if week % 2 == 0 else "dr_warren",
                    "started_after": datetime.now() + timedelta(weeks=week-1),
                    "completed_before": datetime.now() + timedelta(weeks=week, days=5)
                },
                {
                    "required_action": "Progress consultation",
                    "description": f"Week {week} check-in on member experience and early observations",
                    "assigned_agent": "ruby",
                    "started_after": datetime.now() + timedelta(weeks=week-1),
                    "completed_before": datetime.now() + timedelta(weeks=week, days=5)
                }
            ]
        
        # Week 5+: Regular checkups and biweekly exercise updates
        for week in range(5, 33):
            actionables = []
            
            # Weekly checkup with rotating agents
            primary_agent = self._get_primary_agent_for_week(week)
            actionables.append({
                "required_action": "Weekly health checkup",
                "description": f"Week {week} comprehensive health review and progress assessment",
                "assigned_agent": primary_agent,
                "started_after": datetime.now() + timedelta(weeks=week-1),
                "completed_before": datetime.now() + timedelta(weeks=week, days=5)
            })
            
            # Biweekly exercise updates (even weeks)
            if week % 2 == 0:
                actionables.append({
                    "required_action": "Exercise routine update",
                    "description": f"Week {week} physical therapy assessment and exercise plan adjustment",
                    "assigned_agent": "rachel",
                    "started_after": datetime.now() + timedelta(weeks=week-1, days=1),
                    "completed_before": datetime.now() + timedelta(weeks=week-1, days=3)
                })
            
            # Monthly performance reviews (every 4 weeks)
            if week % 4 == 0:
                actionables.append({
                    "required_action": "Performance data analysis",
                    "description": f"Week {week} comprehensive data review and trend analysis",
                    "assigned_agent": "advik",
                    "started_after": datetime.now() + timedelta(weeks=week-1, days=2),
                    "completed_before": datetime.now() + timedelta(weeks=week-1, days=4)
                })
            
            # Monthly nutritional reviews (every 4 weeks, offset by 2)
            if (week - 2) % 4 == 0:
                actionables.append({
                    "required_action": "Nutrition plan review",
                    "description": f"Week {week} meal plan evaluation and dietary adjustments",
                    "assigned_agent": "carla",
                    "started_after": datetime.now() + timedelta(weeks=week-1, days=1),
                    "completed_before": datetime.now() + timedelta(weeks=week-1, days=3)
                })
            
            # Quarterly relationship management (every 8 weeks)
            if week % 8 == 0:
                actionables.append({
                    "required_action": "Strategic relationship review",
                    "description": f"Week {week} comprehensive care coordination and strategic planning",
                    "assigned_agent": "neel",
                    "started_after": datetime.now() + timedelta(weeks=week-1, days=3),
                    "completed_before": datetime.now() + timedelta(weeks=week-1, days=5)
                })
            
            # Special case handling for certain weeks
            if week in [8, 16, 24]:
                actionables.append({
                    "required_action": "Comprehensive health assessment",
                    "description": f"Week {week} comprehensive evaluation including lab review and care plan updates",
                    "assigned_agent": "dr_warren",
                    "started_after": datetime.now() + timedelta(weeks=week-1, days=2),
                    "completed_before": datetime.now() + timedelta(weeks=week-1, days=4)
                })
            
            template[week] = actionables
        
        return template

    def _get_primary_agent_for_week(self, week: int) -> str:
        """Determine the primary agent for weekly checkups based on rotation."""
        agents = ["ruby", "dr_warren", "neel"]
        return agents[(week - 5) % len(agents)]

    def initialize_all_actionables(self):
        """Initialize all actionables for the 32-week program."""
        for week, actionables_data in self.actionables_template.items():
            for actionable_data in actionables_data:
                actionable = Actionable(
                    id=None,
                    week=week,
                    required_action=actionable_data["required_action"],
                    description=actionable_data["description"],
                    assigned_agent=actionable_data["assigned_agent"],
                    status=ActionableStatus.TO_BE_SCHEDULED,
                    scheduled_time=None,
                    started_after=actionable_data["started_after"],
                    completed_before=actionable_data["completed_before"],
                    created_at=datetime.now(),
                    updated_at=None
                )
                self.db.create_actionable(actionable)

    def get_week_actionables(self, week: int) -> List[Actionable]:
        """Get all actionables for a specific week."""
        return self.db.get_actionables_by_week(week)

    def schedule_actionable(self, actionable_id: int, scheduled_time: datetime):
        """Schedule an actionable for a specific time."""
        self.db.update_actionable_status(
            actionable_id, 
            ActionableStatus.SCHEDULED, 
            scheduled_time
        )

    def complete_actionable(self, actionable_id: int):
        """Mark an actionable as completed."""
        self.db.update_actionable_status(
            actionable_id, 
            ActionableStatus.ACTION_TAKEN
        )

    def get_actionables_by_agent(self, agent_id: str, week: int = None) -> List[Actionable]:
        """Get actionables assigned to a specific agent, optionally filtered by week."""
        if week:
            actionables = self.db.get_actionables_by_week(week)
            return [a for a in actionables if a.assigned_agent == agent_id]
        else:
            # Get all actionables for agent across all weeks
            all_actionables = []
            for w in range(1, 33):
                week_actionables = self.db.get_actionables_by_week(w)
                all_actionables.extend([a for a in week_actionables if a.assigned_agent == agent_id])
            return all_actionables

    def get_overdue_actionables(self) -> List[Actionable]:
        """Get actionables that are past their completion deadline."""
        overdue = []
        current_time = datetime.now()
        
        for week in range(1, 33):
            actionables = self.db.get_actionables_by_week(week)
            for actionable in actionables:
                if (actionable.status != ActionableStatus.ACTION_TAKEN and 
                    actionable.completed_before and 
                    current_time > actionable.completed_before):
                    overdue.append(actionable)
        
        return overdue

    def get_weekly_summary(self, week: int) -> Dict[str, Any]:
        """Get a summary of actionables for a specific week."""
        actionables = self.get_week_actionables(week)
        
        summary = {
            "week": week,
            "total_actionables": len(actionables),
            "by_status": {
                "to_be_scheduled": len([a for a in actionables if a.status == ActionableStatus.TO_BE_SCHEDULED]),
                "scheduled": len([a for a in actionables if a.status == ActionableStatus.SCHEDULED]),
                "action_taken": len([a for a in actionables if a.status == ActionableStatus.ACTION_TAKEN])
            },
            "by_agent": {},
            "actionables": actionables
        }
        
        for actionable in actionables:
            agent = actionable.assigned_agent
            if agent not in summary["by_agent"]:
                summary["by_agent"][agent] = 0
            summary["by_agent"][agent] += 1
        
        return summary

    def get_program_overview(self) -> Dict[str, Any]:
        """Get an overview of the entire 32-week program."""
        overview = {
            "total_weeks": 32,
            "total_actionables": 0,
            "by_agent": {},
            "by_week": {}
        }
        
        for week in range(1, 33):
            week_actionables = self.get_week_actionables(week)
            overview["total_actionables"] += len(week_actionables)
            overview["by_week"][week] = len(week_actionables)
            
            for actionable in week_actionables:
                agent = actionable.assigned_agent
                if agent not in overview["by_agent"]:
                    overview["by_agent"][agent] = 0
                overview["by_agent"][agent] += 1
        
        return overview