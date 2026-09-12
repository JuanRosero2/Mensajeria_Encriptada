import asyncio
import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Chat Seguro e Inseguro")

# Evitar problemas de CORS si abrimos el HTML desde otra parte
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: str, sender_mode: str):
        for connection in self.active_connections:
            # Enviamos el mensaje en formato JSON para que el frontend lo maneje fácilmente
            await connection.send_json({"text": message, "mode": sender_mode})

manager_unencrypted = ConnectionManager()
manager_encrypted = ConnectionManager()

@app.websocket("/ws/unencrypted")
async def websocket_unencrypted(websocket: WebSocket):
    await manager_unencrypted.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            print(f"[No Cifrado] Recibido: {data}")
            await manager_unencrypted.broadcast(data, "UNENCRYPTED")
    except WebSocketDisconnect:
        manager_unencrypted.disconnect(websocket)
        print("[No Cifrado] Cliente desconectado")

@app.websocket("/ws/encrypted")
async def websocket_encrypted(websocket: WebSocket):
    await manager_encrypted.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            print(f"[Cifrado] Recibido: {data}")
            await manager_encrypted.broadcast(data, "ENCRYPTED")
    except WebSocketDisconnect:
        manager_encrypted.disconnect(websocket)
        print("[Cifrado] Cliente desconectado")

async def main():
    print("Iniciando servidores...")
    
    # Configuración servidor NO CIFRADO (ws://) en puerto 8000
    config_unencrypted = uvicorn.Config(app, host="0.0.0.0", port=8000)
    server_unencrypted = uvicorn.Server(config_unencrypted)
    
    # Configuración servidor CIFRADO (wss://) en puerto 8443
    # Requiere cert.pem y key.pem en la misma carpeta
    try:
        config_encrypted = uvicorn.Config(
            app, 
            host="0.0.0.0", 
            port=8443, 
            ssl_keyfile="key.pem", 
            ssl_certfile="cert.pem"
        )
        server_encrypted = uvicorn.Server(config_encrypted)
        
        print("=> Servidor No Cifrado escuchando en ws://127.0.0.1:8000/ws/unencrypted")
        print("=> Servidor Cifrado escuchando en wss://127.0.0.1:8443/ws/encrypted")
        
        await asyncio.gather(
            server_unencrypted.serve(),
            server_encrypted.serve(),
        )
    except FileNotFoundError:
        print("\n[ERROR] No se encontraron los certificados 'cert.pem' y 'key.pem'.")
        print("Por favor, genéralos usando OpenSSL antes de iniciar el servidor cifrado.\n")
        
if __name__ == "__main__":
    asyncio.run(main())
