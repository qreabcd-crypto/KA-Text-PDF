from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Optional
from google import genai
import base64
import io
from PIL import Image

app = FastAPI(title="Gemini Pro Ultimate App")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = genai.Client()

class ChatRequest(BaseModel):
    prompt: str
    image: Optional[str] = None

@app.post("/api/chat")
def chat_with_ai(request: ChatRequest):
    try:
        contents = []
        if request.image:
            image_data = request.image.split(",")[1] if "," in request.image else request.image
            image_bytes = base64.b64decode(image_data)
            pil_image = Image.open(io.BytesIO(image_bytes))
            contents.append(pil_image)

        if request.prompt:
            contents.append(request.prompt)
        elif request.image and not request.prompt:
            contents.append("ఈ ఫోటోలో ఏముంది? దీని గురించి వివరించండి.")

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=contents,
        )
        return {"response": response.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/", response_class=HTMLResponse)
def get_gemini_ui():
    html_content = """
    <!DOCTYPE html>
    <html lang="te">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Google Gemini - Ultimate</title>
        <script src="https://cdn.jsdelivr.net/npm/marked/marked.js"></script>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/atom-one-dark.min.css">
        <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>
        
        <style>
            * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
            body { background-color: #131314; color: #e3e3e3; display: flex; flex-direction: column; height: 100vh; }
            header { background: #131314; padding: 15px 20px; font-size: 1.3rem; font-weight: 500; display: flex; align-items: center; justify-content: space-between; border-bottom: 1px solid #222; }
            .left-header { display: flex; align-items: center; gap: 10px; }
            .sparkle { color: #8ab4f8; font-size: 1.4rem; }
            .clear-btn { background: #2b2c2f; border: none; color: #aaa; font-size: 0.85rem; padding: 6px 12px; border-radius: 12px; cursor: pointer; }
            .clear-btn:hover { background: #333; color: #fff; }
            .chat-container { flex: 1; overflow-y: auto; padding: 20px; display: flex; flex-direction: column; gap: 24px; max-width: 800px; width: 100%; margin: 0 auto; }
            .message { display: flex; flex-direction: column; gap: 10px; max-width: 90%; line-height: 1.6; font-size: 1.05rem; }
            .message.user { align-self: flex-end; background: #2b2c2f; padding: 14px 20px; border-radius: 20px 20px 4px 20px; color: #fff; white-space: pre-wrap; }
            .message.ai { align-self: flex-start; background: transparent; padding: 10px 0; color: #e3e3e3; width: 100%; }
            
            .message.ai p { margin-bottom: 10px; }
            .message.ai pre { background: #1e1f20; padding: 15px; border-radius: 8px; overflow-x: auto; margin: 10px 0; border: 1px solid #333; position: relative; }
            .message.ai code { font-family: 'Courier New', Courier, monospace; font-size: 0.95rem; background: rgba(255,255,255,0.1); padding: 2px 5px; border-radius: 4px; }
            .message.ai pre code { background: transparent; padding: 0; }
            .message.ai ul, .message.ai ol { margin-left: 20px; margin-bottom: 10px; }

            .copy-code-btn { position: absolute; top: 8px; right: 8px; background: #333; color: #fff; border: none; padding: 4px 8px; font-size: 0.75rem; border-radius: 4px; cursor: pointer; }
            .copy-code-btn:hover { background: #444; }

            .chat-img { max-width: 200px; border-radius: 10px; }
            .preview-container { padding: 0 20px; max-width: 800px; margin: 0 auto; width: 100%; display: none; align-items: center; gap: 10px; }
            .preview-img { width: 50px; height: 50px; object-fit: cover; border-radius: 8px; border: 1px solid #444; }
            
            .input-area { padding: 20px; background: #131314; display: flex; flex-direction: column; gap: 10px; }
            .input-box { display: flex; background: #1e1f20; width: 100%; max-width: 800px; margin: 0 auto; border-radius: 30px; padding: 10px 20px; align-items: center; border: 1px solid #333; gap: 10px; }
            input[type="text"] { flex: 1; background: transparent; border: none; color: white; font-size: 1rem; outline: none; padding: 8px; }
            
            .icon-btn { background: transparent; border: none; color: #aaa; cursor: pointer; font-size: 1.2rem; padding: 5px; display: flex; align-items: center; justify-content: center; }
            .icon-btn:hover { color: #fff; }
            .icon-btn.listening { color: #ea4335; animation: pulse 1.5s infinite; }
            
            .send-btn { background: #8ab4f8; border: none; color: #131314; width: 38px; height: 38px; border-radius: 50%; cursor: pointer; display: flex; align-items: center; justify-content: center; font-weight: bold; font-size: 1rem; }
            .send-btn:hover { background: #aecbfa; }

            @keyframes pulse { 0% { opacity: 1; } 50% { opacity: 0.4; } 100% { opacity: 1; } }
        </style>
    </head>
    <body>
        <header>
            <div class="left-header">
                <span class="sparkle">✨</span>
                <span>Gemini Pro</span>
            </div>
            <button class="clear-btn" onclick="clearHistory()">చాట్ క్లియర్ చేయి</button>
        </header>
        
        <div class="chat-container" id="chatContainer">
            <div class="message ai">నమస్కారం! మైక్ ద్వారా మాట్లాడవచ్చు, ఫోటోలు పెట్టవచ్చు లేదా కోడ్ అడగవచ్చు.</div>
        </div>

        <div class="preview-container" id="previewContainer">
            <img id="previewImg" class="preview-img" src="" alt="Preview">
            <span style="font-size: 0.9rem; color: #aaa;" id="fileName">ఫోటో అటాచ్ చేయబడింది</span>
            <button onclick="removeImage()" style="background:none; border:none; color:#ea4335; cursor:pointer; font-weight:bold; margin-left:auto;">✕ తొలగించు</button>
        </div>

        <div class="input-area">
            <div class="input-box">
                <button class="icon-btn" id="micBtn" onclick="toggleVoiceInput()" title="మాట్లాడి అడగండి">🎤</button>
                <input type="file" id="imageInput" accept="image/*" style="display: none;" onchange="handleImageSelect(event)">
                <button class="icon-btn" onclick="document.getElementById('imageInput').click()" title="ఫోటో అప్లోడ్ చేయండి">➕</button>
                <input type="text" id="userInput" placeholder="Gemini ని అడగండి..." onkeydown="handleKeyDown(event)">
                <button class="send-btn" onclick="sendMessage()">⬆</button>
            </div>
        </div>

        <script>
            let base64Image = null;
            let recognition;
            let isListening = false;

            if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
                const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
                recognition = new SpeechRecognition();
                recognition.continuous = false;
                recognition.interimResults = false;
                recognition.lang = 'te-IN';

                recognition.onstart = function() {
                    isListening = true;
                    document.getElementById('micBtn').classList.add('listening');
                    document.getElementById('userInput').placeholder = "వింటున్నాను మాట్లాడండి...";
                };

                recognition.onresult = function(event) {
                    const transcript = event.results[0][0].transcript;
                    document.getElementById('userInput').value = transcript;
                    stopVoiceInput();
                    sendMessage();
                };

                recognition.onerror = function() { stopVoiceInput(); };
                recognition.onend = function() { stopVoiceInput(); };
            }

            function toggleVoiceInput() {
                if (!recognition) {
                    alert("మీ బ్రౌజర్ వాయిస్ రికగ్నిషన్‌ని సపోర్ట్ చేయడం లేదు.");
                    return;
                }
                if (isListening) { recognition.stop(); } 
                else { recognition.start(); }
            }

            function stopVoiceInput() {
                isListening = false;
                document.getElementById('micBtn').classList.remove('listening');
                document.getElementById('userInput').placeholder = "Gemini ని అడగండి...";
            }

            window.onload = function() {
                const savedChat = localStorage.getItem('gemini_ultimate_chat');
                if (savedChat) {
                    document.getElementById('chatContainer').innerHTML = savedChat;
                    hljs.highlightAll();
                    addCopyButtons();
                    const container = document.getElementById('chatContainer');
                    container.scrollTop = container.scrollHeight;
                }
            };

            function saveChatHistory() {
                const container = document.getElementById('chatContainer');
                localStorage.setItem('gemini_ultimate_chat', container.innerHTML);
            }

            function clearHistory() {
                if(confirm("మీరు చాట్ హిస్టరీ డిలీట్ చేయాలనుకుంటున్నారా?")) {
                    localStorage.removeItem('gemini_ultimate_chat');
                    document.getElementById('chatContainer').innerHTML = `<div class="message ai">చాట్ క్లియర్ చేయబడింది.</div>`;
                }
            }

            function handleImageSelect(event) {
                const file = event.target.files[0];
                if (file) {
                    const reader = new FileReader();
                    reader.onload = function(e) {
                        base64Image = e.target.result;
                        document.getElementById('previewImg').src = base64Image;
                        document.getElementById('fileName').innerText = file.name;
                        document.getElementById('previewContainer').style.display = 'flex';
                    };
                    reader.readAsDataURL(file);
                }
            }

            function removeImage() {
                base64Image = null;
                document.getElementById('imageInput').value = '';
                document.getElementById('previewContainer').style.display = 'none';
            }

            function handleKeyDown(event) {
                if (event.key === 'Enter') {
                    sendMessage();
                }
            }

            function addCopyButtons() {
                document.querySelectorAll('pre').forEach(pre => {
                    if (!pre.querySelector('.copy-code-btn')) {
                        const button = document.createElement('button');
                        button.className = 'copy-code-btn';
                        button.innerText = 'కాపీ';
                        button.onclick = () => {
                            const code = pre.querySelector('code').innerText;
                            navigator.clipboard.writeText(code);
                            button.innerText = 'కాపీ అయింది!';
                            setTimeout(() => button.innerText = 'కాపీ', 2000);
                        };
                        pre.appendChild(button);
                    }
                });
            }

            async function sendMessage() {
                const input = document.getElementById('userInput');
                const container = document.getElementById('chatContainer');
                const text = input.value.trim();
                
                if (!text && !base64Image) return;

                let userHtml = `<div class="message user">`;
                if (base64Image) {
                    userHtml += `<img src="${base64Image}" class="chat-img">`;
                }
                if (text) {
                    userHtml += `<span>${text}</span>`;
                }
                userHtml += `</div>`;
                container.innerHTML += userHtml;

                const currentImage = base64Image;
                input.value = '';
                removeImage();
                container.scrollTop = container.scrollHeight;
                saveChatHistory();

                const loadingId = 'loading_' + Date.now();
                container.innerHTML += `<div class="message ai" id="${loadingId}">యోచిస్తోంది...</div>`;
                container.scrollTop = container.scrollHeight;

                try {
                    const res = await fetch('/api/chat', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ prompt: text, image: currentImage })
                    });
                    const data = await res.json();
                    
                    const parsedHtml = marked.parse(data.response || "సమాధానం పొందడంలో లోపం ఏర్పడింది.");
                    const aiMsgDiv = document.getElementById(loadingId);
                    aiMsgDiv.innerHTML = parsedHtml;
                    
                    hljs.highlightAll();
                    addCopyButtons();

                } catch(err) {
                    document.getElementById(loadingId).innerText = "కనెక్షన్ ఎర్రర్ వచ్చింది.";
                }
                container.scrollTop = container.scrollHeight;
                saveChatHistory();
            }
        </script>
    </body>
    </html>
    """
    return html_content
    
