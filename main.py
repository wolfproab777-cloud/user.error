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
            z-index: 99999;
            opacity: 0;
            pointer-events: none;
            transition: opacity 0.1s ease-in-out;
        }

        #screamer-overlay img {
            width: 100%;
            height: 100%;
            object-fit: cover;
        }

        /* 3 ta eshik dizayni */
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
            box-shadow: 0 0 20px #ff0000;
            transform: scale(1.05);
        }

        .door h3 {
            margin: 0;
            color: #ff4d4d;
            font-size: 1.2rem;
        }
    </style>
</head>
<body>

    <!-- YouTube orqali fon musiqasi -->
    <div id="youtube-player" style="display:none;">
        <iframe width="560" height="315" src="https://www.youtube.com/embed/6g5fZ8W2ST0?autoplay=1&loop=1&playlist=6g5fZ8W2ST0" frameborder="0" allow="autoplay"></iframe>
    </div>

    <!-- Screamer -->
    <div id="screamer-overlay">
        <img src="https://images.unsplash.com/photo-1509198397868-475647b2a1e5?q=80&w=1000&auto=format&fit=crop" alt="Scary">
    </div>

    <!-- 1. OGOHLANTIRISH VA SHARTLAR EKRANI -->
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

    <!-- 2. ASOSIY MENYU EKRANI (3 ta eshik bilan) -->
    <div class="container hidden" id="main-menu" style="text-align: center;">
        <h1 style="text-shadow: 0 0 20px #ff0000;">TAQDIRINGIZNI TANLANG</h1>
        <p style="color: #a6a6a6; font-size: 1rem;">Oldingizda 3 ta eshik turibdi. Ulardan birini tanlang, lekin ehtiyot bo'ling...</p>
        
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

        // Eshiklardan birini tanlaganda screamer chiqishi
        function chooseDoor(doorNumber) {
            triggerScreamer();
            setTimeout(() => {
                alert("Siz " + doorNumber + "-eshikni tanladingiz va tuzakka tushdingiz!");
            }, 500);
        }

        document.addEventListener('mousemove', function(e) {
            if (!experienceStarted) return;
            
            if (Math.random() > 0.3) {
                let drop = document.createElement('div');
                drop.className = 'blood-drop';
                drop.style.left = e.pageX + 'px';
                drop.style.top = e.pageY + 'px';
                document.body.appendChild(drop);

                setTimeout(() => {
                    drop.remove();
                }, 1000);
            }
        });

        function triggerScreamer() {
            let screamer = document.getElementById("screamer-overlay");
            screamer.style.opacity = "1";
            setTimeout(() => {
                screamer.style.opacity = "0";
            }, 600);
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
