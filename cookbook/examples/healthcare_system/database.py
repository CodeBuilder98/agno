"""
Database models and operations for the healthcare agentic system.
Handles actionables, scheduling, and conversation storage.
"""

import sqlite3
import time
from datetime import datetime, timedelta
from dataclasses import dataclass
from typing import List, Optional, Dict, Any
from enum import Enum


class ActionableStatus(Enum):
    TO_BE_SCHEDULED = "to_be_scheduled"
    SCHEDULED = "scheduled"
    ACTION_TAKEN = "action_taken"


class ConversationType(Enum):
    MEMBER_QUERY = "member_query"
    WEEKLY_CHECKUP = "weekly_checkup"
    BIWEEKLY_EXERCISE = "biweekly_exercise"
    MEDICAL_CONSULTATION = "medical_consultation"
    NUTRITION_CONSULT = "nutrition_consult"
    PHYSICAL_THERAPY = "physical_therapy"
    PERFORMANCE_REVIEW = "performance_review"
    RELATIONSHIP_MANAGEMENT = "relationship_management"


@dataclass
class Actionable:
    id: Optional[int]
    week: int
    required_action: str
    description: str
    assigned_agent: str
    status: ActionableStatus
    scheduled_time: Optional[datetime]
    started_after: Optional[datetime]
    completed_before: Optional[datetime]
    created_at: datetime
    updated_at: Optional[datetime]


@dataclass
class ScheduleSlot:
    id: Optional[int]
    week: int
    day: int  # 1-7 (Monday-Sunday)
    hour: int  # 0-23
    is_available: bool
    assigned_actionable_id: Optional[int]
    conversation_type: Optional[ConversationType]
    agent_id: Optional[str]
    member_intent: Optional[str]
    created_at: datetime


@dataclass
class Conversation:
    id: Optional[int]
    week: int
    timestamp: datetime
    agent_id: str
    member_id: str
    conversation_type: ConversationType
    content: str
    actionable_id: Optional[int]
    handoff_to: Optional[str]
    created_at: datetime


class HealthcareDatabase:
    def __init__(self, db_path: str = "tmp/healthcare.db"):
        self.db_path = db_path
        self.init_database()

    def init_database(self):
        """Initialize the database with required tables."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create actionables table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS actionables (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                week INTEGER NOT NULL,
                required_action TEXT NOT NULL,
                description TEXT NOT NULL,
                assigned_agent TEXT NOT NULL,
                status TEXT NOT NULL,
                scheduled_time TEXT,
                started_after TEXT,
                completed_before TEXT,
                created_at TEXT NOT NULL,
                updated_at TEXT
            )
        """)
        
        # Create schedule slots table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS schedule_slots (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                week INTEGER NOT NULL,
                day INTEGER NOT NULL,
                hour INTEGER NOT NULL,
                is_available BOOLEAN NOT NULL DEFAULT 1,
                assigned_actionable_id INTEGER,
                conversation_type TEXT,
                agent_id TEXT,
                member_intent TEXT,
                created_at TEXT NOT NULL,
                FOREIGN KEY (assigned_actionable_id) REFERENCES actionables (id),
                UNIQUE(week, day, hour)
            )
        """)
        
        # Create conversations table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                week INTEGER NOT NULL,
                timestamp TEXT NOT NULL,
                agent_id TEXT NOT NULL,
                member_id TEXT NOT NULL,
                conversation_type TEXT NOT NULL,
                content TEXT NOT NULL,
                actionable_id INTEGER,
                handoff_to TEXT,
                created_at TEXT NOT NULL,
                FOREIGN KEY (actionable_id) REFERENCES actionables (id)
            )
        """)
        
        conn.commit()
        conn.close()

    def create_actionable(self, actionable: Actionable) -> int:
        """Create a new actionable and return its ID."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO actionables (week, required_action, description, assigned_agent, 
                                   status, scheduled_time, started_after, completed_before, 
                                   created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            actionable.week,
            actionable.required_action,
            actionable.description,
            actionable.assigned_agent,
            actionable.status.value,
            actionable.scheduled_time.isoformat() if actionable.scheduled_time else None,
            actionable.started_after.isoformat() if actionable.started_after else None,
            actionable.completed_before.isoformat() if actionable.completed_before else None,
            actionable.created_at.isoformat(),
            actionable.updated_at.isoformat() if actionable.updated_at else None
        ))
        
        actionable_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return actionable_id

    def update_actionable_status(self, actionable_id: int, status: ActionableStatus, 
                                scheduled_time: Optional[datetime] = None):
        """Update actionable status and optionally set scheduled time."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE actionables 
            SET status = ?, scheduled_time = ?, updated_at = ?
            WHERE id = ?
        """, (
            status.value,
            scheduled_time.isoformat() if scheduled_time else None,
            datetime.now().isoformat(),
            actionable_id
        ))
        
        conn.commit()
        conn.close()

    def get_actionables_by_week(self, week: int) -> List[Actionable]:
        """Get all actionables for a specific week."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM actionables WHERE week = ?
        """, (week,))
        
        rows = cursor.fetchall()
        conn.close()
        
        actionables = []
        for row in rows:
            actionables.append(Actionable(
                id=row[0],
                week=row[1],
                required_action=row[2],
                description=row[3],
                assigned_agent=row[4],
                status=ActionableStatus(row[5]),
                scheduled_time=datetime.fromisoformat(row[6]) if row[6] else None,
                started_after=datetime.fromisoformat(row[7]) if row[7] else None,
                completed_before=datetime.fromisoformat(row[8]) if row[8] else None,
                created_at=datetime.fromisoformat(row[9]),
                updated_at=datetime.fromisoformat(row[10]) if row[10] else None
            ))
        
        return actionables

    def create_schedule_slot(self, slot: ScheduleSlot) -> int:
        """Create a new schedule slot and return its ID."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Check if slot already exists
        cursor.execute("""
            SELECT id FROM schedule_slots 
            WHERE week = ? AND day = ? AND hour = ?
        """, (slot.week, slot.day, slot.hour))
        
        existing = cursor.fetchone()
        if existing:
            conn.close()
            return existing[0]
        
        cursor.execute("""
            INSERT INTO schedule_slots (week, day, hour, is_available, assigned_actionable_id,
                                      conversation_type, agent_id, member_intent, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            slot.week,
            slot.day,
            slot.hour,
            slot.is_available,
            slot.assigned_actionable_id,
            slot.conversation_type.value if slot.conversation_type else None,
            slot.agent_id,
            slot.member_intent,
            slot.created_at.isoformat()
        ))
        
        slot_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return slot_id

    def get_available_slots(self, week: int) -> List[ScheduleSlot]:
        """Get all available schedule slots for a week."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM schedule_slots 
            WHERE week = ? AND is_available = 1
            ORDER BY day, hour
        """, (week,))
        
        rows = cursor.fetchall()
        conn.close()
        
        slots = []
        for row in rows:
            slots.append(ScheduleSlot(
                id=row[0],
                week=row[1],
                day=row[2],
                hour=row[3],
                is_available=bool(row[4]),
                assigned_actionable_id=row[5],
                conversation_type=ConversationType(row[6]) if row[6] else None,
                agent_id=row[7],
                member_intent=row[8],
                created_at=datetime.fromisoformat(row[9])
            ))
        
        return slots

    def book_schedule_slot(self, slot_id: int, actionable_id: int, agent_id: str, 
                          conversation_type: ConversationType):
        """Book a schedule slot for an actionable."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE schedule_slots 
            SET is_available = 0, assigned_actionable_id = ?, agent_id = ?, conversation_type = ?
            WHERE id = ?
        """, (actionable_id, agent_id, conversation_type.value, slot_id))
        
        conn.commit()
        conn.close()

    def create_conversation(self, conversation: Conversation) -> int:
        """Create a new conversation record and return its ID."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO conversations (week, timestamp, agent_id, member_id, conversation_type,
                                     content, actionable_id, handoff_to, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            conversation.week,
            conversation.timestamp.isoformat(),
            conversation.agent_id,
            conversation.member_id,
            conversation.conversation_type.value,
            conversation.content,
            conversation.actionable_id,
            conversation.handoff_to,
            conversation.created_at.isoformat()
        ))
        
        conversation_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return conversation_id

    def get_conversations_by_week(self, week: int) -> List[Conversation]:
        """Get all conversations for a specific week."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM conversations 
            WHERE week = ?
            ORDER BY timestamp
        """, (week,))
        
        rows = cursor.fetchall()
        conn.close()
        
        conversations = []
        for row in rows:
            conversations.append(Conversation(
                id=row[0],
                week=row[1],
                timestamp=datetime.fromisoformat(row[2]),
                agent_id=row[3],
                member_id=row[4],
                conversation_type=ConversationType(row[5]),
                content=row[6],
                actionable_id=row[7],
                handoff_to=row[8],
                created_at=datetime.fromisoformat(row[9])
            ))
        
        return conversations

    def get_conversation_history(self, agent_id: str, limit: int = 10) -> List[Conversation]:
        """Get conversation history for a specific agent."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM conversations 
            WHERE agent_id = ?
            ORDER BY timestamp DESC
            LIMIT ?
        """, (agent_id, limit))
        
        rows = cursor.fetchall()
        conn.close()
        
        conversations = []
        for row in rows:
            conversations.append(Conversation(
                id=row[0],
                week=row[1],
                timestamp=datetime.fromisoformat(row[2]),
                agent_id=row[3],
                member_id=row[4],
                conversation_type=ConversationType(row[5]),
                content=row[6],
                actionable_id=row[7],
                handoff_to=row[8],
                created_at=datetime.fromisoformat(row[9])
            ))
        
        return conversations