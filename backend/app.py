import time
import requests
from openai import OpenAI

# Function to check if the vLLM service is ready
def is_vllm_ready(base_url):
    try:
        response = requests.get(f"{base_url}/models")
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False

# Wait for the vLLM service to be ready
base_url = "http://vllm:1370/v1"  # Use "vllm" as the hostname if running inside Docker
max_retries = 30
retry_delay = 5  # seconds

for _ in range(max_retries):
    if is_vllm_ready(base_url):
        print("vLLM service is ready!")
        break
    print("Waiting for vLLM service to start...")
    time.sleep(retry_delay)
else:
    raise Exception("vLLM service did not start in time.")

# Connect to the vLLM service
client = OpenAI(
    base_url=base_url,
    api_key="dummy-key",  # API key is not required for vLLM
)

# Example API call
response = client.completions.create(
    model="deepseek",  # Use the served model name
    prompt="Hello, how are you?",
    max_tokens=50,
)

print(response.choices[0].text)