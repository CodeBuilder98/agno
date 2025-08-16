# Healthcare Agentic System - User Guide

## Overview

This comprehensive healthcare agentic system simulates a 32-week interaction between a healthcare platform member and 6 support staff agents. It demonstrates advanced multi-agent coordination, intelligent scheduling, and realistic healthcare workflows using the Agno framework.

## Quick Start

```bash
# Install dependencies
pip install agno openai sqlalchemy

# Navigate to the healthcare system directory
cd cookbook/examples/healthcare_system

# Run the system
python main.py
```

## System Architecture

### 🏥 Healthcare Agents

1. **Ruby Agent** (Concierge/Orchestrator)
   - **Role**: Primary coordination, empathetic, organized
   - **Responsibilities**: Initial member contact, care coordination, appointment scheduling
   - **Handoffs**: Can delegate to all specialists

2. **Dr. Warren Agent** (Medical Strategist)
   - **Role**: Clinical authority, authoritative, precise
   - **Responsibilities**: Medical consultations, test interpretation, clinical decisions
   - **Specialties**: Lab results, diagnoses, treatment plans

3. **Advik Agent** (Performance Scientist)
   - **Role**: Data analysis, analytical, experiment-driven
   - **Responsibilities**: Health metrics analysis, trend identification, data insights
   - **Specialties**: Performance tracking, statistical analysis

4. **Carla Agent** (Nutritionist)
   - **Role**: Nutrition planning, educational, practical
   - **Responsibilities**: Meal planning, dietary guidance, nutritional assessments
   - **Specialties**: Diet restrictions, meal plans, supplements

5. **Rachel Agent** (Physical Therapist)
   - **Role**: Movement training, direct, encouraging
   - **Responsibilities**: Exercise programs, mobility assessments, injury prevention
   - **Specialties**: Physical therapy, exercise design, movement analysis

6. **Neel Agent** (Relationship Manager)
   - **Role**: Strategic oversight, reassuring, big-picture
   - **Responsibilities**: Complex care coordination, strategic planning, escalation handling
   - **Specialties**: Long-term care planning, relationship management

7. **Member Agent** (Healthcare Platform User)
   - **Role**: Healthcare platform user with various intents
   - **Capabilities**: Schedule appointments, ask questions, seek guidance

### 🗄️ Database Schema

The system uses SQLite with three main tables:

#### Actionables Table
- Tracks 76+ healthcare activities across 32 weeks
- Status tracking: `to_be_scheduled`, `scheduled`, `action_taken`
- Time constraints with `started_after` and `completed_before`

#### Schedule Slots Table
- Weekly time slot management (Monday-Friday, 9 AM-5 PM)
- Availability tracking and appointment booking
- Agent assignment and conversation type mapping

#### Conversations Table
- Complete conversation history with timestamps
- Agent-member interaction tracking
- Handoff documentation and reasoning

### 📅 32-Week Program Structure

#### Weeks 1-4: Onboarding & Assessment
- **Week 1**: Medical history, health priorities, dietary assessment, lab planning
- **Weeks 2-4**: Biological samples, physical exams, progress consultations

#### Weeks 5-32: Ongoing Care
- **Weekly**: Health checkups (rotating between Ruby, Dr. Warren, Neel)
- **Biweekly**: Exercise routine updates (Rachel)
- **Monthly**: Performance reviews (Advik), Nutrition reviews (Carla)
- **Quarterly**: Strategic relationship reviews (Neel)
- **Special**: Comprehensive assessments at weeks 8, 16, 24

## Usage Examples

### Running a Single Week Simulation

```python
from main import HealthcareSystem

# Initialize the system
system = HealthcareSystem()
system.setup_system()

# Run week 1 simulation
result = system.run_single_week(1, "patient_001")
print(f"Week 1: {result['conversations_count']} conversations")
```

### Running Full 32-Week Simulation

```python
# Run complete simulation (may take several minutes)
results = system.run_simulation("patient_001")

print(f"Total conversations: {results['total_conversations']}")
print(f"Total handoffs: {len(results['handoffs'])}")
```

### Demonstrating Agent Interactions

```python
# Test individual agent responses
response = system.demonstrate_agent_interaction(
    "ruby", 
    "I'd like to schedule my annual checkup"
)
print(response)
```

### Viewing Conversation History

```python
# Get conversation history for a member
history = system.get_conversation_history("patient_001", week=1)
for conv in history:
    print(f"{conv['timestamp']}: {conv['agent']} - {conv['type']}")
```

## Agent Handoff Examples

### Nutrition Handoff (Ruby → Carla)
```
Member: "I'm having trouble with my meal plan"
Ruby: "Let me connect you with Carla, our nutrition specialist"
→ Handoff to Carla for detailed nutrition consultation
```

### Medical Escalation (Ruby → Dr. Warren)
```
Member: "I'm concerned about my test results"
Ruby: "Let me have Dr. Warren review your results"
→ Handoff to Dr. Warren for medical interpretation
```

### Strategic Escalation (Any Agent → Neel)
```
Complex case requiring care coordination
→ Handoff to Neel for strategic oversight
```

## Conversation Types

The system supports 8 conversation types:

1. **Medical Consultation**: Clinical discussions, test reviews
2. **Weekly Checkup**: Regular health status reviews
3. **Nutrition Consult**: Dietary planning and guidance
4. **Physical Therapy**: Exercise and movement sessions
5. **Performance Review**: Data analysis and insights
6. **Relationship Management**: Strategic care coordination
7. **Member Query**: General questions and concerns
8. **Biweekly Exercise**: Exercise routine updates

## Member Intent Examples

The system handles various member intents:

- **Appointment Scheduling**: "I need to reschedule my appointment"
- **Health Questions**: "I read an article about a new supplement"
- **Family Health**: "My family member has a health concern"
- **Symptom Discussion**: "I've been experiencing some symptoms"
- **Test Results**: "Can you explain my lab results?"
- **Medication Questions**: "I have questions about my medication"

## Configuration Options

### Database Configuration
```python
# Custom database path
system = HealthcareSystem(db_path="custom/path/healthcare.db")
```

### Agent Customization
```python
# Modify agent instructions or tools
agents = create_healthcare_agents(db)
agents["ruby"].instructions.append("Custom instruction")
```

### Scheduling Parameters
```python
# Adjust working hours and days
scheduler.working_hours = list(range(8, 20))  # 8 AM to 8 PM
scheduler.working_days = list(range(1, 7))    # Monday to Saturday
```

## Monitoring and Analytics

### System Status
```python
status = system.get_system_status()
print(f"Total agents: {status['total_agents']}")
print(f"Total actionables: {status['actionables_overview']['total_actionables']}")
```

### Weekly Performance
```python
for week in range(1, 33):
    summary = system.scheduling_manager.get_week_schedule_summary(week)
    print(f"Week {week}: {summary['utilization_rate']:.1f}% utilization")
```

### Agent Workload
```python
overview = system.actionables_manager.get_program_overview()
for agent, count in overview['by_agent'].items():
    print(f"{agent}: {count} actionables")
```

## Error Handling

The system includes comprehensive error handling:

- **Database Connection**: Automatic retry and recovery
- **Scheduling Conflicts**: Intelligent rescheduling
- **Agent Errors**: Graceful degradation
- **Input Validation**: Comprehensive parameter checking

## Production Considerations

### Scalability
- SQLite suitable for development/small deployments
- PostgreSQL recommended for production
- Agent sessions can be distributed across servers

### Security
- No hardcoded API keys (environment variables recommended)
- Database connections use parameterized queries
- Session management with proper isolation

### Monitoring
- Built-in logging for all interactions
- Performance metrics collection
- Error tracking and alerting

## Extending the System

### Adding New Agents
```python
def create_custom_agent(db):
    return Agent(
        name="Custom Specialist",
        agent_id="custom",
        role="Custom Role",
        instructions=["Custom instructions"],
        tools=[custom_tools]
    )
```

### Custom Actionables
```python
def add_custom_actionable(manager, week, action, agent):
    actionable = Actionable(
        week=week,
        required_action=action,
        assigned_agent=agent,
        # ... other parameters
    )
    return manager.db.create_actionable(actionable)
```

### Integration with External Systems
```python
# Add custom tools for external integrations
class ExternalSystemTool:
    def __init__(self, api_endpoint):
        self.endpoint = api_endpoint
    
    def fetch_data(self, patient_id):
        # Integration logic
        pass
```

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure all dependencies are installed
   ```bash
   pip install agno openai sqlalchemy
   ```

2. **Database Errors**: Check database permissions and path
   ```python
   import os
   os.makedirs("tmp", exist_ok=True)
   ```

3. **Scheduling Failures**: Review time constraints in actionables
   ```python
   # Relax time constraints if needed
   actionable.completed_before += timedelta(days=1)
   ```

### Performance Optimization

1. **Database Indexing**: Add indexes for frequently queried columns
2. **Conversation Caching**: Cache frequent conversation patterns
3. **Batch Processing**: Process multiple actionables together

## API Reference

### Core Classes

- `HealthcareSystem`: Main orchestrator class
- `HealthcareDatabase`: Database operations and management
- `ActionablesManager`: Weekly actionables tracking
- `SchedulingManager`: Intelligent appointment scheduling
- `ConversationSimulator`: Realistic conversation generation

### Key Methods

- `system.setup_system()`: Initialize complete system
- `system.run_simulation(member_id)`: Run 32-week simulation
- `system.run_single_week(week, member_id)`: Simulate single week
- `system.get_system_status()`: Get current system status

For more detailed API documentation, see the inline docstrings in each module.