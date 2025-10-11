from app.services.redis_client import RedisClient

# Create a Redis client instance
client = RedisClient()

# Print methods
print("Methods:", [m for m in dir(client) if not m.startswith("_")])

# Check if client exists
print("Client exists:", client.client is not None)
print("Client type:", type(client.client))
