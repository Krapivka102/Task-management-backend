from fastapi import FastAPI, WebSocket
import asyncio
from apps.web_socket_fastapi.init_django import *

app = FastAPI()
active_connections = set()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_connections.add(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await broadcast(data)
    except:
        active_connections.remove(websocket)

async def broadcast(message: str):
    for connection in active_connections:
        await connection.send_text(message)