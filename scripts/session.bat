@echo off
REM Session Management Commands for ApexSigma Development

if "%1" == "start" (
    python %~dp0\session_manager.py start --goals "%2"
) else if "%1" == "progress" (
    python %~dp0\session_manager.py progress --session-id "%2" --completed "%3" --status "%4" --challenges "%5" --next "%6"
) else if "%1" == "complete" (
    python %~dp0\session_manager.py complete --session-id "%2" --summary "%3"
) else if "%1" == "list" (
    python %~dp0\session_manager.py list
) else if "%1" == "show" (
    python %~dp0\session_manager.py show --session-id "%2"
) else (
    echo Usage:
    echo   session-start [goals] - Start a new session
    echo   session-progress ^<session-id^> ^<completed^> ^<status^> ^<challenges^> ^<next^> - Log progress
    echo   session-complete ^<session-id^> [summary] - Complete a session
    echo   session-list - List all sessions
    echo   session-show ^<session-id^> - Show session details
)