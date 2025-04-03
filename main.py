from typing import Union

from fastapi import FastAPI
import uvicorn

import requests
from pydantic import BaseModel

app = FastAPI()

# LLM_BASE_URL = "http://127.0.0.1:11434" # replace with your server address (localhost)
LLM_BASE_URL = "http://ollama_server:11434" # replace with your server address (contains port)
MODEL_NAME = "llama3.2:1b"  # เปลี่ยนเป็นชื่อโมเดลที่ใช้

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.get("/health-check-llm")
def call_health_check_llm():
    # Fetch available models
    response = requests.get(f"{LLM_BASE_URL}/v1/models")
    if response.status_code == 200:
        models = response.json()
        print("Available Models:", models)
        return {"models": models}
    else:
        print(f"Failed to fetch models: {response.status_code} - {response.text}")
        return {"errors": f"Failed to fetch models: {response.status_code} - {response.text}"}

@app.get("/ask")
def call_ask_llm():
    payload = {
        "model": MODEL_NAME,  # Replace with your desired model name
        "prompt": "What are the key benefits of local LLM systems?",
        "max_tokens": 100,
        "temperature": 0.7
    }
    response = requests.post(f"{LLM_BASE_URL}/v1/completions", json=payload)

    if response.status_code == 200:
        data = response.json()
        print("Completion Response:")
        result = data.get("choices", [{}])[0].get("text", "No response")
        print(result)
        return {"data": result}
    else:
        return {"errors": f"Failed to fetch models: {response.status_code} - {response.text}"}

@app.get("/ask/chat")
def call_ask_chat_llm(request):
    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": "คุณคือผู้ช่วยที่สามารถอธิบายเรื่องทางเทคนิคได้อย่างละเอียด"},
            {"role": "user", "content": "ช่วยอธิบายหลักการทำงานของควอนตัมคอมพิวติ้งให้เข้าใจง่ายหน่อย"},
            {"role": "assistant", "content": "แน่นอน! ควอนตัมคอมพิวติ้งคือ..."}  # สามารถใส่ข้อความตอบกลับล่วงหน้าได้
        ],
        "max_tokens": 100,
        "temperature": 0.5
    }

    response = requests.post(f"{LLM_BASE_URL}/v1/chat/completions", json=payload)

    if response.status_code == 200:
        data = response.json()
        print("Chat Response:")
        result = data.get("choices", [{}])[0].get("message", {}).get("content", "No response")
        print(result)
        return {"data": result}
    else:
        print(f"Error: {response.status_code} - {response.text}")

class RequestChat(BaseModel):
    message: str

@app.post('/chat')
async def chat(req: RequestChat):
    user_message = req.message
    print(f"User message: {user_message}")

    if not user_message:
        return {"error": "กรุณาส่งข้อความ"}

    # สร้าง payload สำหรับ LLM
    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": "คุณคือผู้ช่วยอัฉริยที่เป็นมิตรและให้ข้อมูลที่ถูกต้องแม่นยำ"},
            {"role": "user", "content": user_message},
            {"role": "assistant", "content": "ผมมีแนวคิดว่า...."}
        ],
        "max_tokens": 1000,
        "temperature": 0.7
    }

    # ส่งคำขอไปยัง LLM
    response = requests.post(f"{LLM_BASE_URL}/v1/chat/completions", json=payload)

    if response.status_code == 200:
        data = response.json()
        ai_response = data.get("choices", [{}])[0].get("message", {}).get("content", "ไม่มีคำตอบ")
        return {"response": ai_response}
    else:
        return {"error": f"LLM Error: {response.status_code} - {response.text}"}


if __name__ == '__main__':
    uvicorn.run("debug_server:app", host="0.0.0.0", port=80, reload=True)
