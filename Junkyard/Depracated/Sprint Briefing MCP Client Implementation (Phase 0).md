---
tags:
  - ApexSigma
  - MCP
  - Protocol
  - Python
  - Abandoned
  - Client
---
Date: 2025-09-10

Objective: To produce a functional, tested, and reusable MCPClient Python class, enabling the first successful agent communication with the live memOS.as server.

End State: A standalone test script can successfully use the client to store a memory and then recall it from the server.

## Phase 1: Foundation & Setup
The goal here is to establish the boilerplate and project structure.

[ ] TASK-01: In the memos.as project root, create a new directory named mcp_client.

[ ] TASK-02: Download or copy the client.py file from the vanzan01/taskmaster-agent-claude-code GitHub repository.

[ ] TASK-03: Place the file inside the new mcp_client directory and rename it to core.py.

[ ] TASK-04: Create an empty __init__.py file inside the mcp_client directory to make it a proper Python package.

## Phase 2: Adaptation & Refactoring
The goal is to transform the boilerplate into our specific client.

[ ] TASK-05: Open mcp_client/core.py and rename the class from TaskMasterClient to MCPClient.

[ ] TASK-06: Refactor the __init__ method. It should accept base_url and an agent_id string, which will be stored for later use in request headers or bodies.

[ ] TASK-07: Delete all existing TaskMaster-specific methods (e.g., add_task, get_next_task, set_task_status). We want a clean slate.

[ ] TASK-08: Implement the store(self, memory_payload: dict) -> dict method. This method will make a POST request to the /store endpoint of the memOS.as server, sending the memory_payload as the JSON body. It should return the server's JSON response.

[ ] TASK-09: Implement the recall(self, query: str) -> dict method. This method will make a POST request to the /recall endpoint, sending a JSON body like {"query": query}. It should return the server's JSON response containing the retrieved memories.

## Phase 3: Integration & End-to-End Testing
The goal is to prove the client works against the live server.

[ ] TASK-10: In the memos.as project root, create a new file named test_client_e2e.py. This file will not be part of the mcp_client package.

[ ] TASK-11: In this test script, import the MCPClient class.

[ ] TASK-12: Instantiate the client, pointing it to the live memOS.as server URL (http://localhost:8090 or whatever the correct mapping is).

[ ] TASK-13: Write a simple execution block:

Define a sample memory dictionary (e.g., {'type': 'test', 'content': 'The client works.'}).

Call the .store() method with this dictionary.

Print the response to confirm the memory was stored successfully.

Call the .recall() method with a relevant query (e.g., "client test").

Print the response and visually confirm that the original memory was returned.