import requests
import json
import time
def create_agent(task, llm_api_key):
    url = "https://api.example-llm.com/v1/completions"
    headers = {"Authorization": f"Bearer {llm_api_key}","Content-Type":"application/json"}
    prompt=f"Ты - агент, выполни задачу: {task}"
    data={"model":"gpt-4","prompt":prompt,"max_tokens":150}
    response = requests.post(url, headers=headers, json=data)
    if response.status_code==200:
        result = response.json()["choices"][0]["text"]
        return result
    else:
        return "Ошибка при вызове LLM"

def run_multiple_tasks(tasks,api_key):
    results=[]
    for task in tasks:
        result = create_agent(task,api_key)
        results.append(result)
        time.sleep(3)  # искусственная задержка, чтобы "не спамить"
    return results

if __name__ == "__main__":
    tasks = ["задача 1", "задача 2", "задача 3"]
    api_key = "your-secret-api-key-here"
    outputs = run_multiple_tasks(tasks,api_key)
    for output in outputs:print(output)