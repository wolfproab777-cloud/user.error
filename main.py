import os
from flask import Flask, render_template_string

app = Flask(__name__)

HORROR_HTML = """
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Qorong'ulik Seni Kutmoqda...</title>
    <style>
        body {
            background-color: #030303;
            color: #ff1a1a;
            font-family: 'Courier New', Courier, monospace;
            text-align: center;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            overflow: hidden;
            animation: flicker 0.15s infinite;
            cursor: crosshair;
        }

        @keyframes flicker {
            0% { opacity: 0.95; }
            50% { opacity: 1; }
            100% { opacity: 0.85; }
        }

        body::after {
            content: " ";
            display: block;
            position: fixed;
            top: 0; left: 0; bottom: 0; right: 0;
            background: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.25) 50%);
            background-size: 100% 4px;
            z-index: 999;
            pointer-events: none;
        }

        .container {
            background: rgba(10, 0, 0, 0.95);
            border: 3px solid #400000;
            padding: 40px;
            border-radius: 12px;
            box-shadow: 0 0 50px rgba(255, 0, 0, 0.4);
            max-width: 650px;
            position: relative;
            z-index: 1000;
            text-align: left;
        }

        h1 {
            text-align: center;
            font-size: 2rem;
            text-shadow: 0 0 15px #ff0000;
            margin-bottom: 20px;
        }

        .checkbox-group {
            margin: 15px 0;
            font-size: 0.95rem;
            color: #d9d9d9;
            display: flex;
            align-items: flex-start;
            gap: 10px;
            cursor: pointer;
        }

        .checkbox-group input {
            transform: scale(1.3);
            accent-color: #ff0000;
            cursor: pointer;
            margin-top: 3px;
        }

        .horror-btn {
            display: block;
            width: 100%;
            background-color: #330000;
            color: #555;
            border: 2px solid #550000;
            padding: 12px;
            font-size: 1.1rem;
            font-family: 'Courier New', Courier, monospace;
            cursor: not-allowed;
            border-radius: 5px;
            margin-top: 25px;
            transition: 0.3s;
            text-align: center;
        }

        .horror-btn.active {
            background-color: #5c0000;
            color: #ff1a1a;
            border: 2px solid #ff1a1a;
            cursor: pointer;
            box-shadow: 0 0 15px rgba(255, 0, 0, 0.5);
        }

        .horror-btn.active:hover {
            background-color: #ff1a1a;
            color: #030303;
            box-shadow: 0 0 25px #ff1a1a;
        }

        .hidden {
            display: none !important;
        }

        .blood-drop {
            position: absolute;
            width: 8px;
            height: 14px;
            background: #ff0000;
            border-radius: 50% 50% 50% 50% / 60% 60% 40% 40%;
            pointer-events: none;
            opacity: 0.8;
            animation: fall-blood 1s linear forwards;
            z-index: 9999;
        }

        @keyframes fall-blood {
            0% { transform: scale(1); opacity: 0.9; }
            100% { transform: translateY(30px) scale(0.5); opacity: 0; }
        }

        #screamer-overlay {
            position: fixed;
            top: 0; left: 0; width: 100vw; height: 100vh;
            background: black;
            display: flex;
            justify-content: center;
            align-items: center;
            z-index: 999999;
            opacity: 0;
            pointer-events: none;
            transition: opacity 0.02s ease-in-out;
        }

        #screamer-overlay img {
            width: 100%;
            height: 100%;
            object-fit: cover;
            filter: contrast(180%) brightness(70%) drop-shadow(0 0 30px red);
        }

        .doors-container {
            display: flex;
            justify-content: space-around;
            margin-top: 30px;
            gap: 15px;
        }

        .door {
            background: #1a0000;
            border: 2px solid #ff0000;
            padding: 25px 15px;
            text-align: center;
            border-radius: 8px;
            cursor: pointer;
            flex: 1;
            transition: 0.3s;
            box-shadow: 0 0 10px rgba(255, 0, 0, 0.2);
        }

        .door:hover {
            background: #4d0000;
            box-shadow: 0 0 25px #ff0000;
            transform: scale(1.05);
        }

        .door h3 {
            margin: 0;
            color: #ff4d4d;
            font-size: 1.2rem;
        }

        /* AI Yordamchi (Kichkina odamcha) dizayni */
        #ai-assistant {
            position: fixed;
            bottom: 20px;
            right: 20px;
            width: 70px;
            height: 70px;
            background: #330000;
            border: 2px solid #ff1a1a;
            border-radius: 50%;
            display: flex;
            justify-content: center;
            align-items: center;
            cursor: grab;
            box-shadow: 0 0 15px #ff0000;
            z-index: 99999;
            user-select: none;
        }

        #ai-assistant:active {
            cursor: grabbing;
        }

        #ai-assistant img {
            width: 50px;
            height: 50px;
            border-radius: 50%;
        }

        /* AI Chat Oynasi */
        #ai-chat-box {
            position: fixed;
            bottom: 100px;
            right: 20px;
            width: 300px;
            background: rgba(10, 0, 0, 0.95);
            border: 2px solid #ff0000;
            border-radius: 10px;
            padding: 15px;
            box-shadow: 0 0 20px rgba(255, 0, 0, 0.5);
            z-index: 99999;
            display: none;
            text-align: left;
        }

        #ai-chat-box h4 {
            margin: 0 0 10px 0;
            color: #ff4d4d;
            font-size: 1rem;
            text-align: center;
        }

        #ai-chat-messages {
            height: 120px;
            overflow-y: auto;
            font-size: 0.85rem;
            color: #ccc;
            margin-bottom: 10px;
            border-bottom: 1px dashed #550000;
            padding-bottom: 5px;
        }

        .ai-input-group {
            display: flex;
            gap: 5px;
        }

        .ai-input-group input {
            flex: 1;
            background: #030303;
            border: 1px solid #ff1a1a;
            color: #fff;
            padding: 5px;
            font-size: 0.85rem;
            border-radius: 3px;
        }

        .ai-input-group button {
            background: #5c0000;
            color: #ff1a1a;
            border: 1px solid #ff1a1a;
            padding: 5px 10px;
            cursor: pointer;
            border-radius: 3px;
            font-family: 'Courier New', Courier, monospace;
        }

        @keyframes lightning {
            0% { background-color: #030303; }
            2% { background-color: #ffffff; }
            4% { background-color: #030303; }
            80% { background-color: #030303; }
            82% { background-color: #ff0000; }
            84% { background-color: #030303; }
            100% { background-color: #030303; }
        }

        .lightning-effect {
            animation: lightning 8s infinite;
        }
    </style>
</head>
<body class="lightning-effect">

    <!-- YouTube orqali fon musiqasi -->
    <div id="youtube-player" style="display:none;">
        <iframe width="560" height="315" src="https://www.youtube.com/embed/6g5fZ8W2ST0?autoplay=1&loop=1&playlist=6g5fZ8W2ST0" frameborder="0" allow="autoplay"></iframe>
    </div>

    <!-- Screamer -->
    <div id="screamer-overlay">
        <img src="https://images.unsplash.com/photo-1518709268805-4e9042af9f23?q=80&w=1000&auto=format&fit=crop" alt="Scary Face">
    </div>

    <!-- 1. OGOHLANTIRISH EKRANI -->
    <div class="container" id="warning-screen">
        <h1>⚠️ OGOHLANTIRISH</h1>
        
        <label class="checkbox-group">
            <input type="checkbox" id="check1" onchange="validateForm()">
            <span>1. QO'RQINCHILI NARSALAR VA RASMLAR CHIQSA QORQMAYSIZMI?</span>
        </label>

        <label class="checkbox-group">
            <input type="checkbox" id="check2" onchange="validateForm()">
            <span>2. SIZ QORQSANGIZ YOKI SIZ BILAN QANDAYDIR KO'NGILSIZLIK YOKI PSIXIKA O'ZGARUVI BO'LSA SAYT BU NARSAGA JAVOB BERMAYDI?</span>
        </label>

        <label class="checkbox-group">
            <input type="checkbox" id="check3" onchange="validateForm()">
            <span>3. SIZ QORQSANGIZ SAYTDAN CHIQIB KETISHINGIZ MUMKUN?</span>
        </label>

        <button class="horror-btn" id="boldi-btn" onclick="enterMenu()">BO'LDI</button>
    </div>

    <!-- 2. 3 TA ESHIK EKRANI -->
    <div class="container hidden" id="main-menu" style="text-align: center;">
        <h1 style="text-shadow: 0 0 20px #ff0000;">TAQDIRINGIZni TANLANG</h1>
        <p style="color: #a6a6a6; font-size: 1rem;">Oldingizda 3 ta eshik turibdi. Ulardan birini tanlang...</p>
        
        <div class="doors-container">
            <div class="door" onclick="chooseDoor(1)">
                <h3>1-ESHIK</h3>
                <p style="font-size:0.8rem; color:#888;">Noma'lum...</p>
            </div>
            <div class="door" onclick="chooseDoor(2)">
                <h3>2-ESHIK</h3>
                <p style="font-size:0.8rem; color:#888;">Qorong'u...</p>
            </div>
            <div class="door" onclick="chooseDoor(3)">
                <h3>3-ESHIK</h3>
                <p style="font-size:0.8rem; color:#888;">Oxirgi...</p>
            </div>
        </div>

        <div style="font-size: 0.8rem; color: #550000; margin-top: 30px;">Status: Trap Activated</div>
    </div>

    <!-- AI YORDAMCHI (Odamcha) -->
    <div id="ai-assistant" title="Yordamchi AI" onclick="toggleAiChat()">
        <img src="https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?q=80&w=200&auto=format&fit=crop" alt="AI">
    </div>

    <!-- AI Chat Oynasi -->
    <div id="ai-chat-box">
        <h4>💀 Qorong'u Yordamchi</h4>
        <div id="ai-chat-messages">
            Salom! Men sening yordamchingman. Qo'rqinchili savollaringni ber, javob beraman...
        </div>
        <div class="ai-input-group">
            <input type="text" id="ai-user-input" placeholder="Savol berish...">
            <button onclick="askAi()">Berish</button>
        </div>
    </div>

    <script>
        let experienceStarted = false;

        function validateForm() {
            let c1 = document.getElementById("check1").checked;
            let c2 = document.getElementById("check2").checked;
            let c3 = document.getElementById("check3").checked;
            let btn = document.getElementById("boldi-btn");

            if (c1 && c2 && c3) {
                btn.classList.add("active");
            } else {
                btn.classList.remove("active");
            }
        }

        function enterMenu() {
            let c1 = document.getElementById("check1").checked;
            let c2 = document.getElementById("check2").checked;
            let c3 = document.getElementById("check3").checked;

            if (!(c1 && c2 && c3)) {
                alert("Iltimos, barcha shartlarga rozilik belgisini qo'ying!");
                return;
            }

            experienceStarted = true;
            document.getElementById("warning-screen").classList.add("hidden");
            document.getElementById("main-menu").classList.remove("hidden");
        }

        function chooseDoor(doorNumber) {
            triggerScreamer();
        }

        // AI Chat oynasini ochish/yopish
        function toggleAiChat() {
            let chat = document.getElementById("ai-chat-box");
            if (chat.style.display === "block") {
                chat.style.display = "none";
            } else {
                chat.style.display = "block";
            }
        }

        // AI ga savol berish va qorqinchili javoblar qaytarish
        function askAi() {
            let inputField = document.getElementById("ai-user-input");
            let msgBox = document.getElementById("ai-chat-messages");
            let question = inputField.value.trim();

            if (question === "") return;

            msgBox.innerHTML += "<br><b style='color:#ff4d4d;'>Sen:</b> " + question;

            let answer = "Bu sirni hech kim bilmaydi...";
            let qLower = question.toLowerCase();

            if (qLower.includes("qayerdaman") || qLower.includes("qayerda")) {
                answer = "Sen qorong'u tuzakdasan, ortingga yo'l yo'q!";
            } else {
                let answers = [
                    "Men sening fikrlaringni o'qiyapman...",
                    "Bu savolga javob berish hayotingga tushishi mumkin.",
                    "Ular seni kuzatib turibdi, ortingga qarama!",
                    "Qo'rqinchli tushlaring haqida o'yla...",
                    "Bu yerdan qochib qutula olmaysan."
                ];
                answer = answers[Math.floor(Math.random() * answers.length)];
            }

            setTimeout(() => {
                msgBox.innerHTML += "<br><b style='color:#ff1a1a;'>Yordamchi:</b> " + answer;
                msgBox.scrollTop = msgBox.scrollHeight;
            }, 500);

            inputField.value = "";
        }

        // Sichqoncha yordamida AI odamchani sudrab yurish (Drag and Drop)
        let ai = document.getElementById("ai-assistant");
        let isDragging = false;
        let offsetX, offsetY;

        ai.addEventListener('mousedown', (e) => {
            isDragging = true;
            offsetX = e.clientX - ai.getBoundingClientRect().left;
            offsetY = e.clientY - ai.getBoundingClientRect().top;
            ai.style.cursor = "grabbing";
        });

        document.addEventListener('mousemove', (e) => {
            if (!isDragging) return;
            ai.style.left = (e.clientX - offsetX) + 'px';
            ai.style.top = (e.clientY - offsetY) + 'px';
            ai.style.bottom = 'auto';
            ai.style.right = 'auto';

            if (experienceStarted && Math.random() > 0.3) {
                let drop = document.createElement('div');
                drop.className = 'blood-drop';
                drop.style.left = e.pageX + 'px';
                drop.style.top = e.pageY + 'px';
                document.body.appendChild(drop);
                setTimeout(() => drop.remove(), 1000);
            }
        });

        document.addEventListener('mouseup', () => {
            isDragging = false;
            ai.style.cursor = "grab";
        });

        function triggerScreamer() {
            let screamer = document.getElementById("screamer-overlay");
            screamer.style.opacity = "1";
            setTimeout(() => {
                screamer.style.opacity = "0";
            }, 1200);
        }
    </script>
</body>
</html>
"""

@app.route('/')
def horror_page():
    return render_template_string(HORROR_HTML)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
