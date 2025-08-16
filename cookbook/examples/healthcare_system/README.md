# Healthcare Agentic System

A comprehensive 32-week healthcare platform simulation with 7 specialized agents providing coordinated care to a healthcare platform member.

## 🚀 Quick Start

```bash
# Install dependencies
pip install agno openai sqlalchemy

# Run the system
python main.py

# Run comprehensive demo
python demo.py

# Try interactive agents
python interactive_example.py
```

## 🏥 System Overview

This system simulates realistic healthcare interactions between a platform member and 6 support staff agents over 32 weeks, including medical consultations, nutritional guidance, physical therapy, performance analysis, and relationship management.

### Healthcare Team

1. **Ruby Agent** (Concierge/Orchestrator) - Primary coordination, empathetic, organized
2. **Dr. Warren Agent** (Medical Strategist) - Clinical authority, authoritative, precise  
3. **Advik Agent** (Performance Scientist) - Data analysis, analytical, experiment-driven
4. **Carla Agent** (Nutritionist) - Nutrition planning, educational, practical
5. **Rachel Agent** (Physical Therapist) - Movement training, direct, encouraging
6. **Neel Agent** (Relationship Manager) - Strategic oversight, reassuring, big-picture
7. **Member Agent** - Healthcare platform user with various intents and needs

## ✨ Key Features

- **32-Week Simulation**: Complete conversation timeline with realistic healthcare scenarios
- **Actionables System**: 76+ weekly activities with status tracking (to_be_scheduled, scheduled, action_taken)
- **Intelligent Scheduling**: Automatic time slot management and appointment booking
- **Agent Handoffs**: Role-based transfers between agents (Ruby→Carla for meals, Ruby→Neel for escalations)
- **Database Integration**: SQLite storage for actionables, schedules, and conversation history
- **Realistic Medical Data**: Hypothetical patient data with proper healthcare workflows
- **Production Ready**: Comprehensive error handling, logging, and extensible architecture

## 🎯 Demo Results

The system successfully demonstrates:

- **76 actionables** across 32 weeks with intelligent scheduling
- **Multi-agent coordination** with role-specific expertise
- **Agent handoffs** with proper context and reasoning
- **Realistic conversations** with member personas and healthcare scenarios
- **Database persistence** with SQLite backend
- **Time management** with working hours and availability tracking

## 📁 Files

| File | Description |
|------|-------------|
| `main.py` | Main simulation orchestrator with interactive options |
| `demo.py` | Comprehensive demonstration of system capabilities |
| `interactive_example.py` | Interactive agent conversation examples |
| `agents.py` | Agent definitions and configurations |
| `database.py` | Database models and operations |
| `scheduler.py` | Scheduling logic and intelligence |
| `simulation.py` | 32-week conversation simulation |
| `actionables.py` | Weekly actionables system |
| `USAGE_GUIDE.md` | Detailed usage instructions and API reference |

## 🛠️ Usage Examples

### Run Complete Demo
```bash
python demo.py
```

### Interactive System
```bash
python main.py
# Choose option 1 for single week, 2 for full simulation, 3 for status
```

### Agent Conversations
```bash
python interactive_example.py
# Try: ruby I need help coordinating my care
```

### Programmatic Usage
```python
from main import HealthcareSystem

system = HealthcareSystem()
system.setup_system()

# Run single week
result = system.run_single_week(1, "patient_001")
print(f"Week 1: {result['conversations_count']} conversations")

# Run full simulation
results = system.run_simulation("patient_001")
print(f"Total: {results['total_conversations']} conversations")
```

## 🔄 Agent Handoff Examples

- **Ruby → Carla**: Nutrition questions and meal planning
- **Ruby → Dr. Warren**: Medical consultations and test results  
- **Ruby → Rachel**: Physical therapy and exercise concerns
- **Ruby → Advik**: Performance data analysis requests
- **Ruby → Neel**: Complex care coordination and escalations
- **Any Agent → Ruby**: Care coordination follow-up

## 📊 Sample Output

```
🏥 Healthcare Agentic System - 32 Week Simulation
============================================================
🔧 Setting up healthcare system...
📋 Initializing actionables...
📅 Initializing schedule slots...
⏰ Scheduling actionables...
  Week 1: 2 scheduled, 2 failed
  Week 2: 3 scheduled, 0 failed
  ...
✅ Scheduling complete: 39 scheduled, 37 failed

🎯 Demo Summary:
  • Total conversations: 13
  • Total handoffs: 2
  • Agent interactions: Ruby(4), Dr. Warren(3), Rachel(2), Neel(2), Carla(1), Advik(1)
```

## 🏗️ Architecture

- **Agno Framework**: Multi-agent system with proper session management
- **SQLite Database**: Persistent storage for actionables, schedules, conversations
- **Intelligent Scheduling**: Time-based constraints with conflict resolution
- **Agent Memory**: Session-based memory for continuity across conversations
- **Error Handling**: Comprehensive exception handling and graceful degradation

## 📚 Documentation

- **README.md** - This overview
- **USAGE_GUIDE.md** - Detailed usage instructions and API reference
- **main.py** - Interactive system with built-in help
- **demo.py** - Comprehensive demonstration

## 🔧 Requirements

- Python 3.8+
- agno framework
- openai (for real AI conversations)
- sqlalchemy (for database operations)

## 🎮 Try It Now

```bash
# Clone and navigate to the healthcare system
cd cookbook/examples/healthcare_system

# Run the interactive demo
python main.py

# Follow the prompts to explore the system
```

This system showcases the power of the Agno framework for building sophisticated multi-agent healthcare applications with realistic workflows, intelligent coordination, and production-ready architecture.