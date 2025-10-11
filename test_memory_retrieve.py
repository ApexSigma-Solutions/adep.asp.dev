import requests

# Test retrieving the memory we just stored
memory_id = 1
url = f"http://localhost:8090/memory/{memory_id}"

response = requests.get(url)
print("Status Code:", response.status_code)
print("Response:", response.json())
