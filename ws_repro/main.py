from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
import logging

app = FastAPI()
logging.basicConfig(level=logging.DEBUG)


# class Middleware:
#     def __init__(self, app):
#         self.app = app

#     async def __call__(self, scope, receive, send):
#         if scope["type"] == "http" or scope["type"] == "websocket":
#             headers = dict(scope["headers"])
#             headers.__setitem__("host".encode(), "ws-repros.dbtn.app".encode())
#             scope["headers"] = [(k, v) for k, v in headers.items() if k != b"origin"]
#             await self.app(scope, receive, send)
#         else:
#             await self.app(scope, receive, send)


# app.add_middleware(Middleware)

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var host = window.location.host;
            var protocol = window.location.protocol === 'https:' ? 'wss://' : 'ws://';
            var ws = new WebSocket(protocol + host);
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            ws.onclose = function(evt) {
                console.log(evt)
            };
                
            ws.onerror = function(evt) {
                console.log(evt)
            };

            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""


@app.get("/")
async def hello():
    return HTMLResponse(html)


@app.websocket("/")
async def hello_ws(websocket: WebSocket):
    try:
        await websocket.accept()
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Message text was: {data}")
    except:
        import traceback

        traceback.print_exc()


import uvicorn

uvicorn.run(
    app,
    port=8080,
    log_level="debug",
    host="0.0.0.0",
    debug=True,
    forwarded_allow_ips="*",
    timeout_keep_alive=60 * 30,
    proxy_headers=True,
)
