#!/usr/bin/env python3
"""Test database connectivity and schema"""

import os

import psycopg2


def test_database():
    """Test database connection and schema"""

    # Connect to PostgreSQL
    conn = psycopg2.connect(
        host=os.environ.get("POSTGRES_HOST", "localhost"),
        port=int(os.environ.get("POSTGRES_PORT", 5432)),
        user=os.environ.get("POSTGRES_USER", "apexsigma_user"),
        password=os.environ.get("POSTGRES_PASSWORD", "Apexsigma123_"),
        database="apexsigma_db",
    )

    try:
        with conn.cursor() as cursor:
            # Check if memories table exists
            cursor.execute(
                """
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public' 
                ORDER BY table_name
            """
            )

            tables = cursor.fetchall()
            print(f"Tables in apexsigma_db: {[t[0] for t in tables]}")

            # Check if memories table has data
            if any("memories" in t for t in tables):
                cursor.execute("SELECT COUNT(*) FROM memories")
                count = cursor.fetchone()[0]
                print(f"Memories table has {count} rows")

                # Get sample memory if exists
                if count > 0:
                    cursor.execute("SELECT id, content, tier FROM memories LIMIT 1")
                    memory = cursor.fetchone()
                    print(
                        f"Sample memory: ID={memory[0]}, tier={memory[2]}, content={memory[1][:50]}..."
                    )

            # Check registered_tools table
            if any("registered_tools" in t for t in tables):
                cursor.execute("SELECT COUNT(*) FROM registered_tools")
                count = cursor.fetchone()[0]
                print(f"Registered tools table has {count} rows")

                if count > 0:
                    cursor.execute(
                        "SELECT name, description FROM registered_tools LIMIT 3"
                    )
                    tools = cursor.fetchall()
                    for tool in tools:
                        print(f"  Tool: {tool[0]} - {tool[1][:30]}...")

            # Check knowledge sharing tables
            for table_name in ["knowledge_share_requests", "knowledge_share_offers"]:
                if any(table_name in t for t in tables):
                    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                    count = cursor.fetchone()[0]
                    print(f"{table_name} table has {count} rows")

            print("\nDatabase schema verification completed successfully!")
            return True

    except Exception as e:
        print(f"Error testing database: {e}")
        return False
    finally:
        conn.close()


if __name__ == "__main__":
    test_database()
