import requests
import json

url = 'http://localhost:8090/memory/store'
data = {
    'content': 'Test memory for database initialization verification',
    'agent_id': 'test_agent',
    'metadata': {'test': True}
}

response = requests.post(url, json=data)
print('Status Code:', response.status_code)
print('Response:', response.text)