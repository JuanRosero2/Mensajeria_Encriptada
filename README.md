# ChatLab — Mensajería Cifrada vs. No Cifrada

Chat multiusuario por **salas** que permite comparar comunicación **sin cifrado** (`ws://`) y **cifrada** (`wss://` con TLS) para analizar el tráfico de red con Wireshark.

## Descripción

Cada usuario crea una sala, comparte el link con un compañero y ambos conversan en tiempo real. La barra superior permite alternar entre **UNENCRYPTED** y **ENCRYPTED** según el canal sobre el que se quiere transmitir.

## Requisitos previos

- Python 3.10+
- OpenSSL (para generar certificados)
- Navegador moderno
- Wireshark (para capturar tráfico)

## Instalación

```bash
git clone <repositorio>
cd Mensajeria_Encriptada
python -m venv venv
source venv/bin/activate        # Linux/Mac
pip install -r requirements.txt
```

### Generar certificados autofirmados

```bash
openssl req -x509 -newkey rsa:2048 -keyout key.pem -out cert.pem \
  -days 365 -nodes -subj "/CN=127.0.0.1"
```

## Ejecución

```bash
python server.py
```

- **No cifrado:** `http://127.0.0.1:8000`
- **Cifrado:** `https://127.0.0.1:8443`

Antes de usar el modo cifrado, visita `https://127.0.0.1:8443` y acepta la advertencia de certificado autofirmado.

## Uso

1. Abre `http://127.0.0.1:8000` → serás redirigido a una sala nueva.
2. Escribe tu **nombre de usuario** y entra.
3. Pulsa **[ copiar link ]** en la barra superior y compártelo con un compañero.
4. El compañero abre el link, pone su nombre y entra a la misma sala.
5. Usa el toggle de la barra superior para cambiar entre `UNENCRYPTED` (ws://) y `ENCRYPTED` (wss://).

> Ambos participantes pueden usar distintos modos a la vez. Cada mensaje muestra la etiqueta del canal por el que viajó (`⚠ plain` / `🔒 TLS`).

## Acceso desde otro dispositivo

El botón **[ copiar link ]** genera un link con la **IP LAN del servidor** (detectada automáticamente por el backend), lista para enviar por WhatsApp/mensajería a un compañero en la misma red.

- En modo `UNENCRYPTED` el link será `http://IP-LAN:8000/index.html?room=…`
- En modo `ENCRYPTED` el link será `https://IP-LAN:8443/index.html?room=…`

El certificado autofirmado solo está emitido para `127.0.0.1`, por lo que al acceder desde otro equipo por `https` el navegador mostrará una advertencia de seguridad. Para verificar la identidad, cada demo puede aceptarla manualmente o regenerar el certificado incluyendo la IP como SAN:

```bash
openssl req -x509 -newkey rsa:2048 -keyout key.pem -out cert.pem \
  -days 365 -nodes -addext "subjectAltName=IP:127.0.0.1,IP:192.168.1.50"
```
(reemplaza `192.168.1.50` por tu IP LAN real, visible en `sudo ip addr`)

## Uso con Wireshark

1. Inicia Wireshark y captura en la interfaz **Loopback** (`lo`).
2. Aplica el filtro `tcp.port == 8000` para ver tráfico **no cifrado**: el contenido del mensaje aparece en texto plano.
3. Aplica el filtro `tcp.port == 8443` para ver tráfico **cifrado**: los datos aparecen como `Application Data` cifrado por TLS.

## API

| Ruta                     | Descripción                                       |
| ------------------------ | -------------------------------------------------- |
| `GET /new-room`        | Crea una sala y redirige a `/?room=<id>` |
| `GET /api/rooms/{id}`  | Lista de usuarios conectados en una sala           |
| `WS /ws/{room}/{user}` | WebSocket de la sala (recibe/emite JSON)           |
