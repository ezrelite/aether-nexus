import json
import logging
from typing import Optional, Dict, Any, List
from redis import asyncio as redis
from redis.exceptions import ConnectionError
from src.config.settings import settings

logger = logging.getLogger(__name__)

class MockRedis:
    """
    In-Memory Redis replacement for standalone mode.
    """
    def __init__(self):
        self.data = {}
        self.lists = {}
        logger.warning("⚠️  Cortex operating in IN-MEMORY MODE (Redis unavailable). Data will be lost on restart.")

    async def close(self):
        pass

    async def set(self, key, value, ex=None):
        self.data[key] = value

    async def get(self, key):
        return self.data.get(key)

    async def rpush(self, key, value):
        if key not in self.lists:
            self.lists[key] = []
        self.lists[key].append(value)

    async def lrange(self, key, start, end):
        if key not in self.lists:
            return []
        if end == -1:
            return self.lists[key][start:]
        return self.lists[key][start:end+1]

class Cortex:
    """
    The Memory System (Cortex).
    Attempts to connect to Redis. Falls back to In-Memory if unavailable.
    """
    def __init__(self):
        self.redis_url = settings.REDIS_URL
        self.client = None
        self.is_mock = False

    async def connect(self):
        """Initializes the connection (Redis or Mock)."""
        if self.client:
            return

        try:
            # Attempt real Redis connection
            client = redis.from_url(self.redis_url, decode_responses=True)
            await client.ping() # Test connection
            self.client = client
            logger.info(f"✅ Connected to Cortex Redis at {self.redis_url}")
        except (ConnectionError, OSError) as e:
            logger.warning(f"❌ Could not connect to Redis: {e}")
            logger.warning("🔄 Switching to In-Memory Cortex.")
            self.client = MockRedis()
            self.is_mock = True

    async def disconnect(self):
        """Closes the connection."""
        if self.client:
            await self.client.close()
            logger.info("Disconnected from Cortex")

    async def save_context(self, session_id: str, key: str, value: Any, ttl: int = 3600):
        if not self.client: await self.connect()
        
        full_key = f"session:{session_id}:{key}"
        serialized_value = json.dumps(value) if isinstance(value, (dict, list)) else str(value)
        await self.client.set(full_key, serialized_value, ex=ttl)

    async def get_context(self, session_id: str, key: str) -> Optional[Any]:
        if not self.client: await self.connect()
            
        full_key = f"session:{session_id}:{key}"
        value = await self.client.get(full_key)
        
        if value:
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                return value
        return None

    async def add_log(self, session_id: str, log_entry: Dict[str, Any]):
        if not self.client: await self.connect()
            
        list_key = f"session:{session_id}:logs"
        await self.client.rpush(list_key, json.dumps(log_entry))

    async def get_logs(self, session_id: str) -> List[Dict[str, Any]]:
        if not self.client: await self.connect()
            
        list_key = f"session:{session_id}:logs"
        logs = await self.client.lrange(list_key, 0, -1)
        return [json.loads(log) for log in logs]

cortex = Cortex()
