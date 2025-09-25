import random
import json
import pickle
import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.chat.util import Chat, reflections
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware

# Define chatbot responses using patterns
pairs = [
    # ... your pairs as before ...
]

chatbot = Chat(pairs, reflections)

app = FastAPI()

# Allow CORS for all origins (for development)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", response_class=HTMLResponse)
async def home():
    return """
    <html>
    <head>
        <title>cvrBot Web Chat</title>
        <style>
            body { font-family: Arial; background: #f4f4f4; }
            #chat { width: 400px; margin: 40px auto; background: #fff; padding: 20px; border-radius: 8px; }
            .bot { color: #0074D9; margin: 8px 0; }
            .user { color: #111; margin: 8px 0; text-align: right; }
            input[type=text] { width: 80%; padding: 8px; }
            button { padding: 8px 12px; }
        </style>
    </head>
    <body>
        <div id="chat">
            <div class="bot">cvrBot: Hello! Type your message below.</div>
        </div>
        <input id="msg" type="text" placeholder="Type your message..." autofocus/>
        <button onclick="send()">Send</button>
        <script>
            function addMsg(text, who) {
                let div = document.createElement('div');
                div.className = who;
                div.innerText = (who === 'user' ? 'You: ' : 'cvrBot: ') + text;
                document.getElementById('chat').appendChild(div);
                document.getElementById('chat').scrollTop = document.getElementById('chat').scrollHeight;
            }
            function send() {
                let msg = document.getElementById('msg').value;
                if (!msg) return;
                addMsg(msg, 'user');
                fetch('/chat', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({message: msg})
                })
                .then(r => r.json())
                .then(data => addMsg(data.response, 'bot'));
                document.getElementById('msg').value = '';
            }
            document.getElementById('msg').addEventListener('keydown', function(e) {
                if (e.key === 'Enter') send();
            });
        </script>
    </body>
    </html>
    """

@app.post("/chat")
async def chat_api(request: Request):
    data = await request.json()
    user_input = data.get("message", "")
    if user_input.lower() in ["bye", "exit", "quit"]:
        return JSONResponse({"response": "Goodbye! If you need further assistance, just start a new chat.\nBefore you go, could you please provide feedback about your experience?"})
    response = chatbot.respond(user_input)
    if not response:
        response = "I'm here to help with any laptop service or repair questions. Could you please provide more details?"
    return JSONResponse({"response": response})