# Healthcare Agentic System

A comprehensive 32-week healthcare platform simulation with 7 specialized agents providing coordinated care to a healthcare platform member.

## Overview

This system simulates realistic healthcare interactions between a platform member and 6 support staff agents over 32 weeks, including medical consultations, nutritional guidance, physical therapy, performance analysis, and relationship management.

## Agents

### Staff Agents
1. **Ruby Agent** (Concierge/Orchestrator) - Primary coordination, empathetic, organized
2. **Dr. Warren Agent** (Medical Strategist) - Clinical authority, authoritative, precise
3. **Advik Agent** (Performance Scientist) - Data analysis, analytical, experiment-driven
4. **Carla Agent** (Nutritionist) - Nutrition planning, educational, practical
5. **Rachel Agent** (Physical Therapist) - Movement training, direct, encouraging
6. **Neel Agent** (Relationship Manager) - Strategic oversight, reassuring, big-picture

### Member Agent
7. **Member Agent** - Healthcare platform user with various intents and needs

## Features

- **32-Week Simulation**: Complete conversation timeline with realistic healthcare scenarios
- **Actionables System**: Weekly tracking with status management (to_be_scheduled, scheduled, action_taken)
- **Intelligent Scheduling**: Automatic time slot management and appointment booking
- **Agent Handoffs**: Role-based transfers between agents (Ruby→Carla for meals, Ruby→Neel for escalations)
- **Database Integration**: SQLite storage for actionables, schedules, and conversation history
- **Realistic Medical Data**: Hypothetical patient data with proper healthcare workflows

## Installation

```bash
pip install agno openai sqlite3
```

## Usage

```bash
python cookbook/examples/healthcare_system/main.py
```

## Files

- `main.py` - Main simulation orchestrator
- `agents.py` - Agent definitions and configurations
- `database.py` - Database models and operations
- `scheduler.py` - Scheduling logic and intelligence
- `simulation.py` - 32-week conversation simulation
- `actionables.py` - Weekly actionables system