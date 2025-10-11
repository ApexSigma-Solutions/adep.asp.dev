from app.services.postgres_client import get_postgres_client

client = get_postgres_client()
with client.get_session() as session:
    result = session.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' ORDER BY table_name")
    tables = [row[0] for row in result.fetchall()]
    print(f"Tables: {tables}")
    
    # Check memories table
    if "memories" in tables:
        result = session.execute("SELECT COUNT(*) FROM memories")
        count = result.fetchone()[0]
        print(f"Memories table has {count} rows")
    
    # Check registered_tools table
    if "registered_tools" in tables:
        result = session.execute("SELECT COUNT(*) FROM registered_tools")
        count = result.fetchone()[0]
        print(f"Registered tools table has {count} rows")