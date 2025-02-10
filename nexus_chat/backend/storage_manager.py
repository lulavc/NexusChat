"""Storage management for chat sessions and messages."""
import aiosqlite
import json
import logging
from typing import List, Optional, Dict, Any
from datetime import datetime
from pathlib import Path

from nexus_chat.models.message import Message, MessageRole, MessageStatus
from nexus_chat.models.chat_session import ChatSession

logger = logging.getLogger(__name__)

class StorageManager:
    """Manages persistent storage of chat data using SQLite."""
    
    def __init__(self, db_path: Optional[str] = None):
        """Initialize storage manager with optional custom db path."""
        if db_path is None:
            db_path = Path.home() / ".config" / "ollama-chat" / "chat.db"
        db_path.parent.mkdir(parents=True, exist_ok=True)
        self.db_path = str(db_path)
        self.initialized = False

    async def _initialize_db(self):
        """Initialize database schema if not already done."""
        if self.initialized:
            return

        async with aiosqlite.connect(self.db_path) as db:
            # Create sessions table
            await db.execute("""
                CREATE TABLE IF NOT EXISTS chat_sessions (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    model TEXT NOT NULL,
                    system_prompt TEXT,
                    active BOOLEAN NOT NULL DEFAULT 1,
                    created_at TIMESTAMP NOT NULL,
                    updated_at TIMESTAMP NOT NULL,
                    metadata TEXT
                )
            """)

            # Create messages table with foreign key
            await db.execute("""
                CREATE TABLE IF NOT EXISTS messages (
                    id TEXT PRIMARY KEY,
                    session_id TEXT NOT NULL,
                    content TEXT NOT NULL,
                    role TEXT NOT NULL,
                    model TEXT NOT NULL,
                    parent_id TEXT,
                    status TEXT NOT NULL DEFAULT 'complete',
                    error TEXT,
                    created_at TIMESTAMP NOT NULL,
                    metadata TEXT,
                    FOREIGN KEY (session_id) REFERENCES chat_sessions (id)
                        ON DELETE CASCADE
                )
            """)

            await db.commit()
        self.initialized = True

    async def save_session(self, session: ChatSession) -> None:
        """Save or update a chat session."""
        await self._initialize_db()
        try:
            async with aiosqlite.connect(self.db_path) as db:
                await db.execute("""
                    INSERT OR REPLACE INTO chat_sessions (
                        id, name, model, system_prompt, active,
                        created_at, updated_at, metadata
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    session.id,
                    session.name,
                    session.model,
                    session.system_prompt,
                    session.active,
                    session.created_at.isoformat(),
                    datetime.now().isoformat(),
                    json.dumps(session.metadata) if session.metadata else None
                ))
                await db.commit()
        except Exception as e:
            logger.error(f"Error saving session: {e}")
            raise

    async def save_message(self, message: Message) -> None:
        """Save or update a message."""
        await self._initialize_db()
        try:
            async with aiosqlite.connect(self.db_path) as db:
                await db.execute("""
                    INSERT OR REPLACE INTO messages (
                        id, session_id, content, role, model,
                        parent_id, status, error,
                        created_at, metadata
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    message.message_id,
                    message.session_id,
                    message.content,
                    message.role.value,
                    message.model,
                    message.parent_id,
                    message.status.value,
                    message.error,
                    message.timestamp.isoformat(),
                    json.dumps(message.metadata) if message.metadata else None
                ))
                await db.commit()
        except Exception as e:
            logger.error(f"Error saving message: {e}")
            raise

    async def get_session(self, session_id: str) -> Optional[ChatSession]:
        """Get a specific chat session with its messages."""
        await self._initialize_db()
        try:
            async with aiosqlite.connect(self.db_path) as db:
                db.row_factory = aiosqlite.Row
                
                # Get session
                async with db.execute(
                    "SELECT * FROM chat_sessions WHERE id = ?",
                    (session_id,)
                ) as cursor:
                    row = await cursor.fetchone()
                    if not row:
                        return None
                    
                    session = ChatSession(
                        id=row["id"],
                        name=row["name"],
                        model=row["model"],
                        system_prompt=row["system_prompt"],
                        active=bool(row["active"]),
                        created_at=datetime.fromisoformat(row["created_at"]),
                        metadata=json.loads(row["metadata"]) if row["metadata"] else {}
                    )
                    
                    # Get messages
                    async with db.execute(
                        "SELECT * FROM messages WHERE session_id = ? ORDER BY created_at",
                        (session_id,)
                    ) as msg_cursor:
                        async for msg_row in msg_cursor:
                            message = Message(
                                message_id=msg_row["id"],
                                session_id=msg_row["session_id"],
                                content=msg_row["content"],
                                role=MessageRole(msg_row["role"]),
                                model=msg_row["model"],
                                parent_id=msg_row["parent_id"],
                                status=MessageStatus(msg_row["status"]),
                                error=msg_row["error"],
                                timestamp=datetime.fromisoformat(msg_row["created_at"]),
                                metadata=json.loads(msg_row["metadata"]) if msg_row["metadata"] else {}
                            )
                            session.messages.append(message)
                    
                    return session
        except Exception as e:
            logger.error(f"Error getting session: {e}")
            raise

    async def list_sessions(self, active_only: bool = True) -> List[ChatSession]:
        """List all chat sessions."""
        await self._initialize_db()
        sessions = []
        try:
            async with aiosqlite.connect(self.db_path) as db:
                db.row_factory = aiosqlite.Row
                query = "SELECT * FROM chat_sessions"
                if active_only:
                    query += " WHERE active = 1"
                query += " ORDER BY updated_at DESC"
                
                async with db.execute(query) as cursor:
                    async for row in cursor:
                        session = ChatSession(
                            id=row["id"],
                            name=row["name"],
                            model=row["model"],
                            system_prompt=row["system_prompt"],
                            active=bool(row["active"]),
                            created_at=datetime.fromisoformat(row["created_at"]),
                            metadata=json.loads(row["metadata"]) if row["metadata"] else {}
                        )
                        sessions.append(session)
            return sessions
        except Exception as e:
            logger.error(f"Error listing sessions: {e}")
            raise
