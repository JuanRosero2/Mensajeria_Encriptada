import asyncio
import secrets
import socket
import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, RedirectResponse

app = FastAPI(title="ChatLab")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Room manager ──────────────────────────────────────────────

class Room:
    def __init__(self, room_id: str):
        self.room_id = room_id
        self.connections: dict[WebSocket, str] = {}  # ws -> username

    async def connect(self, ws: WebSocket, username: str):
        await ws.accept()
        self.connections[ws] = username
        await self.broadcast({"type": "join", "sender": username}, exclude=ws)
        print(f"[{self.room_id}] {username} joined ({len(self.connections)} users)")

    async def disconnect(self, ws: WebSocket):
        username = self.connections.pop(ws, None)
        if username:
            await self.broadcast({"type": "leave", "sender": username})
            print(f"[{self.room_id}] {username} left ({len(self.connections)} users)")

    async def broadcast(self, message: dict, exclude: WebSocket | None = None):
        for ws in list(self.connections):
            if ws is not exclude:
                try:
                    await ws.send_json(message)
                except Exception:
                    pass

    @property
    def usernames(self) -> list[str]:
        return list(self.connections.values())


rooms: dict[str, Room] = {}


def get_or_create_room(room_id: str) -> Room:
    if room_id not in rooms:
        rooms[room_id] = Room(room_id)
    return rooms[room_id]


def get_lan_ip() -> str:
    """Descubre la IP de red local sin enviar paquetes (connect UDP NO envía datos)."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("10.255.255.255", 1))
        return s.getsockname()[0]
    except OSError:
        return "127.0.0.1"
    finally:
        s.close()


# ── Routes ────────────────────────────────────────────────────

@app.get("/")
async def root():
    return FileResponse("index.html")


@app.get("/index.html")
async def index_alias():
    return FileResponse("index.html")


@app.get("/new-room")
async def new_room():
    room_id = secrets.token_urlsafe(6)
    return RedirectResponse(url=f"/?room={room_id}")


@app.get("/api/rooms/{room_id}")
async def room_info(room_id: str):
    room = get_or_create_room(room_id)
    return {"room_id": room_id, "users": room.usernames}


@app.get("/api/host")
async def host_info():
    return {"host": get_lan_ip()}


# ── WebSocket ─────────────────────────────────────────────────

@app.websocket("/ws/{room_id}/{username}")
async def websocket_room(ws: WebSocket, room_id: str, username: str):
    room = get_or_create_room(room_id)
    await room.connect(ws, username)
    try:
        while True:
            data = await ws.receive_text()
            sender_mode = "ENCRYPTED" if "wss" in str(ws.url) else "UNENCRYPTED"
            await room.broadcast(
                {"type": "message", "sender": username, "text": data, "mode": sender_mode},
                exclude=ws,
            )
    except WebSocketDisconnect:
        await room.disconnect(ws)


# ── Servers ───────────────────────────────────────────────────

async def main():
    print("Iniciando servidores...")

    config_plain = uvicorn.Config(app, host="0.0.0.0", port=8000)
    server_plain = uvicorn.Server(config_plain)

    try:
        config_tls = uvicorn.Config(
            app,
            host="0.0.0.0",
            port=8443,
            ssl_keyfile="key.pem",
            ssl_certfile="cert.pem",
        )
        server_tls = uvicorn.Server(config_tls)

        print("=> http://127.0.0.1:8000/new-room  (unencrypted ws://)")
        print("=> https://127.0.0.1:8443/new-room  (encrypted wss://)")

        await asyncio.gather(
            server_plain.serve(),
            server_tls.serve(),
        )
    except FileNotFoundError:
        print("\n[ERROR] cert.pem / key.pem not found.")
        print("Generate with: openssl req -x509 -newkey rsa:2048 -keyout key.pem -out cert.pem -days 365 -nodes -subj /CN=127.0.0.1\n")
        print("=> Running UNENCRYPTED ONLY on http://127.0.0.1:8000")
        await server_plain.serve()


if __name__ == "__main__":
    asyncio.run(main())
