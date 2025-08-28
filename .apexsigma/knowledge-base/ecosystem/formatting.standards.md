 # Unicode Policy for Cross-Platform Compatibility

 ## Problem Statement

 > Unicode characters (especially emojis) in terminal output cause UnicodeEncodeError exceptions and display incorrectly on standard Windows terminals, creating a poor developer experience.
Policy

 **NO UNICODE CHARACTERS** are permitted in any print() statements or logs that are intended for terminal output within the DevEnviro Python application.

 ### Approved Replacements

 * Use the following text-based equivalents for all visual status indicators:

Symbol      Replacement         Usage Context

    ✅          [OK]            General success

    ❌          [FAIL]          General failure or error

    ⚠️          [WARN]          General warning

    💡          [INFO]          General informational message

    🚀          [START]         Service or process startup

    🛑          [STOP]          Service or process shutdown

    🐳          [DOCKER]        Docker-related operations

    🐇          [RABBITMQ]      RabbitMQ queue operations

    🔍          [QDRANT]        Qdrant search/store operations

 ### Implementation

 * This policy is enforced through a pre-commit hook that scans Python files for forbidden characters, ensuring all terminal output remains clean and compatible across all developer environments.

 **Exceptions**

 Unicode characters are permissible in:

 * Documentation files (.md).
 * Comments within code files.
 * String literals that are not used for terminal print() or logging functions (e.g., data being sent to a database).
