# ChatLab — Mensajería Cifrada vs. No Cifrada

## Descripción

Aplicación de chat que permite comparar comunicación **sin cifrado** (`ws://`) y **cifrada** (`wss://` con TLS) para analizar el tráfico de red con Wireshark.

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

- **No cifrado:** `ws://127.0.0.1:8000`
- **Cifrado:** `wss://127.0.0.1:8443`

Abre `index.html` en tu navegador. Antes de usar el modo cifrado, visita `https://127.0.0.1:8443` y acepta la advertencia de certificado autofirmado.

## Uso con Wireshark

1. Inicia Wireshark y captura en la interfaz **Loopback** (`lo`).
2. Aplica el filtro `tcp.port == 8000` para ver tráfico **no cifrado**: el contenido del mensaje aparecerá en texto plano.
3. Aplica el filtro `tcp.port == 8443` para ver tráfico **cifrado**: los datos aparecerán como `Application Data` cifrado por TLS.
