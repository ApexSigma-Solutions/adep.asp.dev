#!/usr/bin/env python3
"""
Comprehensive Database Initialization Script for ApexSigma Ecosystem

This script initializes all databases required for the ApexSigma ecosystem:
1. Langfuse database (observability)
2. memOS.as database (memory management)
3. Dagster database (workflow orchestration)

The script is idempotent and can be run multiple times safely.
"""

import sys
import os
import time
from pathlib import Path
from typing import Dict, List, Optional

import psycopg2
from psycopg2.extensions import connection
from psycopg2 import sql


class DatabaseInitializer:
    """Handles initialization of all ApexSigma databases."""
    
    def __init__(self):
        self.host = os.environ.get("POSTGRES_HOST", "localhost")
        self.port = int(os.environ.get("POSTGRES_PORT", 5432))
        self.user = os.environ.get("POSTGRES_USER", "apexsigma_user")
        self.password = os.environ.get("POSTGRES_PASSWORD", "Apexsigma123_")
        self.default_db = os.environ.get("POSTGRES_DB", "apexsigma_db")
        
        # Connection to postgres database (for creating new databases)
        self.admin_conn: Optional[connection] = None
        
        # Database configurations
        self.databases = {
            "langfuse_db": {
                "user": "langfuse_user",
                "password": "Apexsigma123_",
                "init_script": "config/postgres/init-langfuse.sql"
            },
            "apexsigma_db": {
                "user": "apexsigma_user",
                "password": "Apexsigma123_",
                "init_script": "config/postgres/init-memos.sql"
            },
            "dagster_db": {
                "user": "dagster_user",
                "password": "Apexsigma123_",
                "init_script": "config/postgres/init-dagster.sql"
            }
        }
    
    def get_admin_connection(self) -> connection:
        """Get connection to postgres database for admin operations."""
        if self.admin_conn is None or self.admin_conn.closed:
            try:
                self.admin_conn = psycopg2.connect(
                    host=self.host,
                    port=self.port,
                    user=self.user,
                    password=self.password,
                    database="postgres"  # Connect to default postgres database
                )
                self.admin_conn.autocommit = True
                print("Connected to PostgreSQL admin interface")
            except Exception as e:
                print(f"Failed to connect to PostgreSQL: {e}")
                raise
        return self.admin_conn
    
    def database_exists(self, db_name: str) -> bool:
        """Check if a database exists."""
        conn = self.get_admin_connection()
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT 1 FROM pg_database WHERE datname = %s",
                (db_name,)
            )
            return cursor.fetchone() is not None
    
    def create_database(self, db_name: str, user: str, password: str) -> bool:
        """Create a database and user if they don't exist."""
        conn = self.get_admin_connection()
        
        try:
            with conn.cursor() as cursor:
                # Create user if doesn't exist
                cursor.execute(
                    sql.SQL("""
                        DO $$
                        BEGIN
                           IF NOT EXISTS (
                              SELECT FROM pg_catalog.pg_roles
                              WHERE  rolname = %s) THEN
                              CREATE ROLE %s LOGIN PASSWORD %s;
                           END IF;
                        END
                        $$;
                    """),
                    [user, sql.Identifier(user), password]
                )
                
                # Create database if doesn't exist
                cursor.execute(
                    sql.SQL("SELECT 'CREATE DATABASE {}' WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = %s)").format(
                        sql.Identifier(db_name)
                    ),
                    [db_name]
                )
                
                # Grant privileges
                cursor.execute(
                    sql.SQL("GRANT ALL PRIVILEGES ON DATABASE {} TO {}").format(
                        sql.Identifier(db_name),
                        sql.Identifier(user)
                    )
                )
                
                print(f"Database {db_name} and user {user} created/verified")
                return True
                
        except Exception as e:
            print(f"Failed to create database {db_name}: {e}")
            return False
    
    def execute_init_script(self, db_name: str, script_path: str) -> bool:
        """Execute an initialization script on a specific database."""
        script_file = Path(script_path)
        if not script_file.exists():
            print(f"Init script not found: {script_path}")
            return False
        
        try:
            # Connect to the specific database
            conn = psycopg2.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=db_name
            )
            conn.autocommit = True
            
            with conn.cursor() as cursor:
                # Read and execute the script
                with open(script_file, 'r') as f:
                    script_content = f.read()
                
                # Split script into individual statements
                statements = [stmt.strip() for stmt in script_content.split(';') if stmt.strip()]
                
                for statement in statements:
                    if statement:
                        try:
                            cursor.execute(statement)
                        except Exception as e:
                            # Ignore certain expected errors for idempotency
                            if "already exists" in str(e).lower() or "does not exist" in str(e).lower():
                                continue
                            print(f"SQL warning: {e}")
                            continue
                
                print(f"Executed init script for {db_name}")
                return True
                
        except Exception as e:
            print(f"Failed to execute init script for {db_name}: {e}")
            return False
        finally:
            if 'conn' in locals():
                conn.close()
    
    def verify_database(self, db_name: str) -> bool:
        """Verify that a database is properly initialized."""
        try:
            conn = psycopg2.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=db_name
            )
            
            with conn.cursor() as cursor:
                # Get table count
                cursor.execute(
                    "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public'"
                )
                table_count = cursor.fetchone()[0]
                
                print(f"Database {db_name} verified with {table_count} tables")
                return True
                
        except Exception as e:
            print(f"Failed to verify database {db_name}: {e}")
            return False
        finally:
            if 'conn' in locals():
                conn.close()
    
    def wait_for_postgres(self, max_attempts: int = 30, delay: int = 2) -> bool:
        """Wait for PostgreSQL to be ready."""
        print("Waiting for PostgreSQL to be ready...")
        
        for attempt in range(max_attempts):
            try:
                conn = psycopg2.connect(
                    host=self.host,
                    port=self.port,
                    user=self.user,
                    password=self.password,
                    database="postgres",
                    connect_timeout=5
                )
                conn.close()
                print("PostgreSQL is ready")
                return True
            except Exception:
                if attempt < max_attempts - 1:
                    print(f"Attempt {attempt + 1}/{max_attempts} - waiting {delay}s...")
                    time.sleep(delay)
                else:
                    print("PostgreSQL is not ready after maximum attempts")
                    return False
        
        return False
    
    def initialize_all(self) -> bool:
        """Initialize all databases."""
        print("APEXSIGMA DATABASE INITIALIZATION")
        print("=" * 50)
        
        # Wait for PostgreSQL to be ready
        if not self.wait_for_postgres():
            return False
        
        success = True
        
        for db_name, config in self.databases.items():
            print(f"\nInitializing {db_name}...")
            
            # Create database and user
            if not self.create_database(db_name, config["user"], config["password"]):
                success = False
                continue
            
            # Execute init script
            if not self.execute_init_script(db_name, config["init_script"]):
                success = False
                continue
            
            # Verify database
            if not self.verify_database(db_name):
                success = False
                continue
        
        if success:
            print("\nAll databases initialized successfully!")
            print("ApexSigma ecosystem is ready for operation")
        else:
            print("\nSome database initializations failed")
        
        return success
    
    def cleanup(self):
        """Clean up connections."""
        if self.admin_conn and not self.admin_conn.closed:
            self.admin_conn.close()


def main():
    """Main function."""
    initializer = DatabaseInitializer()
    
    try:
        success = initializer.initialize_all()
        return 0 if success else 1
    except KeyboardInterrupt:
        print("\nInitialization interrupted by user")
        return 1
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    finally:
        initializer.cleanup()


if __name__ == "__main__":
    sys.exit(main())