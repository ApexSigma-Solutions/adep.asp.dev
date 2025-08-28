import requests
import json

url = "http://localhost:8002/ingest/text"

payload = {
    "content": "Implemented Graph API endpoints (related, shortest-path, subgraph) and updated Neo4j client in memOS.as.",
    "metadata": {
        "content_type": "text",
        "source": "api",
        "source_url": "session_log"
    },
    "chunk_size": 500,
    "process_async": False
}

headers = {
    'Content-Type': 'application/json'
}

try:
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    response.raise_for_status()  # Raise an exception for HTTP errors
    print("Progress logged successfully to InGest-LLM.as:", response.json())
except requests.exceptions.RequestException as e:
    print(f"Error logging progress to InGest-LLM.as: {e}")
    if hasattr(e, 'response') and e.response is not None:
        print("Response content:", e.response.text)
