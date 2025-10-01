#!/usr/bin/env python3
"""
Session Manager for ApexSigma Development Sessions

This script provides functionality to manage development sessions,
track progress, and log achievements during active development work.
Integrates with memos.as progress logging system.
"""

import argparse
import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

import requests


class SessionManager:
    """Manages development sessions and progress tracking"""

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.session_dir = project_root / "sessions"
        self.session_dir.mkdir(exist_ok=True)

    def start_session(self, goals: str = "", session_id: Optional[str] = None) -> str:
        """Start a new development session"""
        if not session_id:
            session_id = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        session_file = self.session_dir / f"{session_id}.json"

        session_data = {
            "session_id": session_id,
            "start_time": datetime.now().isoformat(),
            "goals": goals,
            "status": "active",
            "progress_updates": [],
        }

        with open(session_file, "w") as f:
            json.dump(session_data, f, indent=2)

        print(f"Started new session: {session_id}")
        print(f"Goals: {goals}")
        return session_id

    def get_active_sessions(self) -> List[Dict]:
        """Get all active sessions"""
        active_sessions = []
        for session_file in self.session_dir.glob("*.json"):
            try:
                with open(session_file, "r") as f:
                    session_data = json.load(f)
                if session_data.get("status") == "active":
                    active_sessions.append(session_data)
            except Exception:
                continue
        return active_sessions

    def get_session(self, session_id: str) -> Optional[Dict]:
        """Get session data by ID"""
        session_file = self.session_dir / f"{session_id}.json"
        if session_file.exists():
            try:
                with open(session_file, "r") as f:
                    return json.load(f)
            except Exception:
                return None
        return None

    def log_progress(
        self,
        session_id: str,
        completed_work: str,
        current_status: str,
        challenges: str,
        next_steps: str,
    ) -> bool:
        """Log progress for a session and integrate with memos.as"""
        session_data = self.get_session(session_id)
        if not session_data:
            print(f"Session {session_id} not found")
            return False

        progress_entry = {
            "timestamp": datetime.now().isoformat(),
            "completed_work": completed_work,
            "current_status": current_status,
            "challenges": challenges,
            "next_steps": next_steps,
        }

        session_data["progress_updates"].append(progress_entry)

        # Save updated session data
        session_file = self.session_dir / f"{session_id}.json"
        with open(session_file, "w") as f:
            json.dump(session_data, f, indent=2)

        # Integrate with memos.as progress logging system
        self._log_to_memos(session_id, progress_entry)

        print(f"Progress logged for session: {session_id}")
        return True

    def complete_session(self, session_id: str, final_summary: str = "") -> bool:
        """Mark a session as completed and log final achievement to memos.as"""
        session_data = self.get_session(session_id)
        if not session_data:
            print(f"Session {session_id} not found")
            return False

        session_data["end_time"] = datetime.now().isoformat()
        session_data["status"] = "completed"
        session_data["final_summary"] = final_summary

        # Save updated session data
        session_file = self.session_dir / f"{session_id}.json"
        with open(session_file, "w") as f:
            json.dump(session_data, f, indent=2)

        # Log final achievement to memos.as
        self._log_achievement_to_memos(session_id, session_data)

        print(f"Session completed: {session_id}")
        return True

    def list_sessions(self) -> List[Dict]:
        """List all sessions"""
        sessions = []
        for session_file in self.session_dir.glob("*.json"):
            try:
                with open(session_file, "r") as f:
                    sessions.append(json.load(f))
            except Exception:
                continue
        return sessions

    def show_session(self, session_id: str) -> bool:
        """Display session details"""
        session_data = self.get_session(session_id)
        if not session_data:
            print(f"Session {session_id} not found")
            return False

        print(f"\nSession: {session_data['session_id']}")
        print(f"Status: {session_data['status']}")
        print(f"Start Time: {session_data['start_time']}")
        if "end_time" in session_data:
            print(f"End Time: {session_data['end_time']}")
        print(f"Goals: {session_data['goals']}")

        if session_data["progress_updates"]:
            print("\nProgress Updates:")
            for i, update in enumerate(session_data["progress_updates"], 1):
                print(f"\n  Update {i} ({update['timestamp']}):")
                print(f"    Completed: {update['completed_work']}")
                print(f"    Status: {update['current_status']}")
                print(f"    Challenges: {update['challenges']}")
                print(f"    Next Steps: {update['next_steps']}")

        if "final_summary" in session_data:
            print(f"\nFinal Summary: {session_data['final_summary']}")

        return True

    def _log_to_memos(self, session_id: str, progress_entry: Dict) -> None:
        """Log progress entry to memos.as system"""
        try:
            # Try to send progress to memos.as API
            memos_endpoint = "http://localhost:8090/memory/store"
            progress_data = {
                "content": f"Session {session_id} Progress Update",
                "agent_id": "session_manager",
                "metadata": {
                    "session_id": session_id,
                    "timestamp": progress_entry["timestamp"],
                    "completed_work": progress_entry["completed_work"],
                    "current_status": progress_entry["current_status"],
                    "challenges": progress_entry["challenges"],
                    "next_steps": progress_entry["next_steps"],
                    "type": "session_progress",
                },
            }

            # Only try to connect if the endpoint is available
            # This is a fire-and-forget operation - don't block if service is down
            try:
                response = requests.post(memos_endpoint, json=progress_data, timeout=2)
                if response.status_code == 200:
                    print(f"Progress also logged to memos.as")
            except requests.exceptions.RequestException:
                # If memos.as is not available, that's okay - just continue
                pass
        except Exception:
            # If anything goes wrong with memos integration, don't let it stop the main function
            pass

    def _log_achievement_to_memos(self, session_id: str, session_data: Dict) -> None:
        """Log session completion as an achievement to memos.as"""
        try:
            # Try to send achievement to memos.as API
            memos_endpoint = "http://localhost:8090/memory/store"
            achievement_data = {
                "content": f"Session {session_id} Completed",
                "agent_id": "session_manager",
                "metadata": {
                    "session_id": session_id,
                    "end_time": session_data.get("end_time", ""),
                    "goals": session_data.get("goals", ""),
                    "final_summary": session_data.get("final_summary", ""),
                    "progress_updates_count": len(
                        session_data.get("progress_updates", [])
                    ),
                    "type": "session_completion",
                },
            }

            # Only try to connect if the endpoint is available
            try:
                response = requests.post(
                    memos_endpoint, json=achievement_data, timeout=2
                )
                if response.status_code == 200:
                    print(f"Session completion also logged to memos.as")
            except requests.exceptions.RequestException:
                # If memos.as is not available, that's okay
                pass
        except Exception:
            # If anything goes wrong with memos integration, don't let it stop the main function
            pass


def main():
    parser = argparse.ArgumentParser(
        description="ApexSigma Development Session Manager"
    )
    parser.add_argument(
        "command",
        choices=["start", "progress", "complete", "list", "show"],
        help="Command to execute",
    )
    parser.add_argument("--session-id", help="Session ID")
    parser.add_argument("--goals", help="Session goals")
    parser.add_argument("--completed", help="Completed work")
    parser.add_argument("--status", help="Current status")
    parser.add_argument("--challenges", help="Challenges encountered")
    parser.add_argument("--next", help="Next steps")
    parser.add_argument("--summary", help="Final summary")

    args = parser.parse_args()

    project_root = Path.cwd()
    session_manager = SessionManager(project_root)

    if args.command == "start":
        session_id = session_manager.start_session(args.goals or "")
        print(f"\nSession started: {session_id}")
        print("Use this session ID for progress updates:")
        print(
            f"  python session_manager.py progress --session-id {session_id} --completed '...' --status '...' --challenges '...' --next '...'"
        )

    elif args.command == "progress":
        if not args.session_id:
            print("Error: --session-id is required for progress command")
            return 1

        success = session_manager.log_progress(
            args.session_id,
            args.completed or "",
            args.status or "",
            args.challenges or "",
            args.next or "",
        )

        if success:
            print("\nProgress logged successfully!")
            print("Next steps:")
            print(f"  - Continue working on your tasks")
            print(
                f"  - Run this command again to log more progress: session-progress --session-id {args.session_id}"
            )
            print(
                f"  - When finished, complete the session: session-complete --session-id {args.session_id}"
            )
        else:
            return 1

    elif args.command == "complete":
        if not args.session_id:
            print("Error: --session-id is required for complete command")
            return 1

        success = session_manager.complete_session(args.session_id, args.summary or "")
        if success:
            print(f"Session {args.session_id} completed successfully!")
        else:
            return 1

    elif args.command == "list":
        sessions = session_manager.list_sessions()
        if not sessions:
            print("No sessions found")
            return 0

        print("Sessions:")
        for session in sessions:
            status = session.get("status", "unknown")
            print(f"  {session['session_id']} - {status}")

    elif args.command == "show":
        if not args.session_id:
            print("Error: --session-id is required for show command")
            return 1

        session_manager.show_session(args.session_id)

    return 0


if __name__ == "__main__":
    sys.exit(main())
