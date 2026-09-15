# Actividad de Ciberseguridad: Chat cifrado vs. no cifrado

## 1. Objetivo

En esta actividad deberán desarrollar una aplicación de chat que permita comparar, de manera práctica, la comunicación **sin cifrado** y la comunicación **cifrada**.

El objetivo es comprender:

* Qué diferencia existe entre una comunicación cifrada y una no cifrada.
* Qué información puede observar un tercero que capture el tráfico de red.
* Cómo se comporta el tráfico de una aplicación cuando utiliza cifrado.
* Cómo utilizar **Wireshark** para analizar tráfico de red.
* Por qué el cifrado es importante para proteger la confidencialidad de las comunicaciones.

---

# 2. Producto final

Cada grupo deberá desarrollar una aplicación de chat funcional que permita enviar mensajes utilizando **dos modalidades**:

### Modo 1 — Comunicación no cifrada

Los mensajes deberán transmitirse utilizando un canal que permita observar el contenido del mensaje en el tráfico capturado.

Por ejemplo:

* TCP
* HTTP
* WebSocket (`ws://`)
* Otro protocolo apropiado para demostrar comunicación sin cifrado.

### Modo 2 — Comunicación cifrada

Los mensajes deberán transmitirse mediante un canal protegido mediante cifrado.

Por ejemplo:

* HTTPS
* Secure WebSocket (`wss://`)
* TLS
* Otro mecanismo equivalente.

> **Importante:** No es necesario implementar un algoritmo criptográfico desde cero. El objetivo principal es comprender y demostrar la diferencia entre una comunicación protegida y una comunicación sin protección.

---

# 3. Requisitos mínimos de la aplicación

La aplicación debe contar como mínimo con:

### Interfaz de usuario

El frontend puede desarrollarse utilizando la tecnología que prefieran.

Algunas opciones:

* HTML/CSS/JavaScript
* React
* Vue
* Angular
* Svelte
* Otra tecnología equivalente.

La interfaz debe permitir:

1. Escribir un mensaje.
2. Enviar el mensaje.
3. Recibir mensajes.
4. Identificar claramente si actualmente se está utilizando:

   * **UNENCRYPTED**
   * **ENCRYPTED**
5. Cambiar entre los dos modos de comunicación.

Por ejemplo:

```text
┌──────────────────────────────────────────┐
│             SECURE CHAT                  │
├──────────────────────────────────────────┤
│ Mode: [ ENCRYPTED ▼ ]                    │
│                                          │
│ Alice: Hello Bob!                        │
│ Bob:   Hello Alice!                      │
│                                          │
│ Message: [________________________]      │
│                                          │
│             [ SEND ]                     │
└──────────────────────────────────────────┘
```

---

# 4. Backend

Pueden utilizar **Python** para desarrollar el backend.

Algunas tecnologías posibles:

* Python + Flask
* Python + FastAPI
* Python + WebSockets
* Python + Socket programming
* Otra tecnología que permita implementar los dos tipos de comunicación.

No es obligatorio utilizar Python si el grupo prefiere otra tecnología, pero la implementación debe permitir demostrar claramente los dos escenarios.

---

# 5. Escenario de comunicación no cifrada

Deberán implementar un canal donde el contenido de los mensajes pueda ser observado mediante una captura de tráfico.

Por ejemplo:

```text
Client ──────── TCP / HTTP / WS ────────> Server
                   │
                   │
                Wireshark
                   │
                   ▼
            "Hello, Bob!"
```

Realicen una captura utilizando Wireshark y demuestren que, dependiendo del protocolo utilizado, es posible identificar información relacionada con la comunicación y, en el escenario diseñado para la práctica, observar el contenido del mensaje.

---

# 6. Escenario de comunicación cifrada

Posteriormente deberán implementar un canal protegido mediante TLS.

Un ejemplo sería:

```text
Client ───────── TLS / WSS ─────────> Server
                   │
                   │
                Wireshark
                   │
                   ▼
             Encrypted data
```

La aplicación debe continuar funcionando normalmente:

```text
Alice → "Hello Bob!"
              ↓
          TLS / WSS
              ↓
           Server
              ↓
          Bob recibe
          "Hello Bob!"
```

Sin embargo, al capturar el tráfico con Wireshark, el contenido de la comunicación no debería aparecer como texto plano.

---

# 7. Prueba con Wireshark

Una parte fundamental de la actividad consiste en realizar una comparación utilizando **Wireshark**.

Deberán realizar al menos dos capturas:

### Captura A — Comunicación no cifrada

Enviar varios mensajes, por ejemplo:

```text
Hello Bob
This is a secret message
My password is 123456
```

> Utilicen únicamente información ficticia. **Nunca utilicen contraseñas reales, información personal real o datos sensibles.**

Posteriormente deberán analizar la captura con Wireshark.

Intenten identificar:

* IP de origen.
* IP de destino.
* Protocolo utilizado.
* Puertos.
* Tamaño de los paquetes.
* Contenido de los mensajes, cuando el protocolo lo permita.

---

### Captura B — Comunicación cifrada

Repitan exactamente una prueba equivalente utilizando el modo cifrado.

Por ejemplo:

```text
Hello Bob
This is a secret message
My password is 123456
```

Analicen nuevamente el tráfico utilizando Wireshark.

Intenten identificar:

* IP de origen.
* IP de destino.
* Puerto.
* Protocolo.
* Información relacionada con TLS.
* Datos cifrados.

---

# 8. Comparación

El grupo deberá responder experimentalmente preguntas como:

### Comunicación no cifrada

* ¿Se puede identificar quién se está comunicando?
* ¿Se puede identificar el servidor?
* ¿Se puede observar el contenido del mensaje?
* ¿Qué información queda expuesta?
* ¿Qué podría hacer un atacante que pudiera capturar ese tráfico?

### Comunicación cifrada

* ¿Se puede identificar que existe una comunicación?
* ¿Se pueden identificar las IPs?
* ¿Se puede identificar el uso de TLS?
* ¿Se puede leer directamente el contenido del mensaje?
* ¿Qué información continúa siendo visible?
* ¿Qué información deja de estar disponible para un observador de red?

---

# 9. Entregables

Cada grupo deberá entregar:

### 1. Código fuente

Repositorio o carpeta que contenga:

* Frontend.
* Backend.
* Configuración necesaria.
* Instrucciones para ejecutar el proyecto.
* `README` con los pasos de instalación y ejecución.

El proyecto debe poder ser ejecutado por el docente.

---

### 2. Evidencia de funcionamiento

Incluyan capturas de pantalla que demuestren:

* Chat funcionando en modo no cifrado.
* Chat funcionando en modo cifrado.
* Captura de Wireshark del tráfico no cifrado.
* Captura de Wireshark del tráfico cifrado.
* Comparación de ambos escenarios.

---

### 3. Video explicativo

El video debe realizarse **completamente en inglés**.

**Duración máxima: 10–15 minutos.**

**Todos los integrantes del grupo deben aparecer y participar en el video.**

El video debe incluir una demostración de la aplicación y una explicación de los resultados obtenidos.

---

# 10. Contenido obligatorio del video

El video debe cubrir como mínimo los siguientes puntos:

## A. Introduction

Presentar:

* Nombre del proyecto.
* Integrantes del grupo.
* Objetivo de la actividad.

---

## B. Application demonstration

Mostrar la aplicación funcionando.

Demostrar:

1. Comunicación no cifrada.
2. Comunicación cifrada.
3. Cambio entre ambos modos.
4. Envío y recepción de mensajes.

---

## C. Unencrypted communication

Explicar:

* Qué protocolo utilizaron.
* Cómo funciona su implementación.
* Qué ocurre con el mensaje cuando se transmite.
* Qué información pudieron observar utilizando Wireshark.

---

## D. Encrypted communication

Explicar:

* Qué mecanismo de cifrado/protocolo utilizaron.
* Cómo cambia la comunicación.
* Qué observaron en Wireshark.
* Por qué el contenido del mensaje ya no puede observarse directamente como texto plano.

---

## E. Wireshark comparison

Mostrar ambas capturas y compararlas.

Por ejemplo:

```text
UNENCRYPTED

Packet → Message
         "Hello Bob!"


ENCRYPTED

Packet → Encrypted/TLS data
         [unreadable data]
```

Los estudiantes deben explicar **qué cambió y qué no cambió**.

Es importante entender que el cifrado no necesariamente oculta toda la información de una conexión. Por ejemplo, dependiendo del protocolo y configuración, ciertos metadatos como IPs, puertos o el hecho de que existe una conexión pueden seguir siendo observables.

---

## F. Importance of encryption

Explicar por qué el cifrado es importante en situaciones reales.

Pueden mencionar ejemplos como:

* Online banking.
* Messaging applications.
* Login credentials.
* E-commerce.
* Public Wi-Fi.
* Personal information.
* Corporate communications.

---

## G. Conclusion

El grupo deberá explicar brevemente:

* Qué aprendieron.
* Cuál es la diferencia principal entre ambos escenarios.
* Por qué una aplicación debería proteger las comunicaciones.
* Qué riesgos existen al transmitir información sin cifrado.

---

# 11. Recomendación de estructura del video

Una posible distribución de los 10–15 minutos:

| Tiempo       | Contenido                  |
| ------------ | -------------------------- |
| 0:00–1:00   | Introduction + integrantes |
| 1:00–3:00   | Application demonstration  |
| 3:00–5:00   | Unencrypted communication  |
| 5:00–7:00   | Encrypted communication    |
| 7:00–10:00  | Wireshark analysis         |
| 10:00–12:00 | Comparison                 |
| 12:00–14:00 | Importance of encryption   |
| 14:00–15:00 | Conclusion                 |

La distribución es solamente una recomendación; pueden organizar el video de otra manera siempre que cubran todos los puntos requeridos.

---

# 12. Consideraciones de seguridad

Esta actividad debe realizarse únicamente en un entorno controlado.

* Utilicen equipos, servidores y redes bajo su control o con autorización.
* No capturen tráfico de otras personas.
* No utilicen contraseñas reales.
* No capturen conversaciones reales.
* No intenten interceptar comunicaciones de terceros.
* Para las demostraciones, utilicen únicamente mensajes ficticios.

El objetivo es **aprender cómo funciona la protección de las comunicaciones**, no interceptar comunicaciones reales.

---

## Aspectos importantes

No se evaluará únicamente que "el chat funcione". El grupo debe ser capaz de **explicar qué ocurre con los datos durante la comunicación y demostrarlo mediante Wireshark**.

La parte más importante de la actividad es conectar:

**Código → Comunicación → Tráfico de red → Wireshark → Seguridad**

El uso de frameworks, lenguajes o tecnologías diferentes no será penalizado siempre que permitan demostrar claramente los conceptos solicitados.

 a
