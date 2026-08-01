import os
from flask import Flask, render_template_string

app = Flask(__name__)

# Barcha dahshatli effektlar jamlangan tayyor HTML/CSS va JS kodi
HORROR_HTML = """
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Qorong'ulik Seni Kutmoqda...</title>
    <style>
        /* CRT Eski Televizor va Miltillash effekti */
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
        }

        @keyframes flicker {
            0% { opacity: 0.95; }
            50% { opacity: 1; }
            100% { opacity: 0.85; }
        }

        /* Monitor chiziqlari effekti */
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
            background: rgba(10, 0, 0, 0.9);
            border: 3px solid #400000;
            padding: 50px;
            border-radius: 12px;
            box-shadow: 0 0 50px rgba(255, 0, 0, 0.3);
            max-width: 650px;
            position: relative;
            z-index: 1000;
        }

        h1 {
            font-size: 2.8rem;
            text-shadow: 0 0 15px #ff0000;
            margin-bottom: 20px;
            letter-spacing: 2px;
        }

        .typewriter {
            font-size: 1.2rem;
            color: #a6a6a6;
            border-right: 2px solid #ff1a1a;
            white-space: nowrap;
            overflow: hidden;
            margin: 0 auto;
            animation: blink-caret 0.75s step-end infinite;
        }

        @keyframes blink-caret {
            from, to { border-color: transparent }
            50% { border-color: #ff1a1a; }
        }

        .warning {
            color: #ff4d4d;
            font-weight: bold;
            margin-top: 30px;
            font-size: 1.1rem;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        .pulse {
            animation: pulse-glow 2s infinite;
        }

        @keyframes pulse-glow {
            0% { text-shadow: 0 0 5px #ff0000; }
            50% { text-shadow: 0 0 25px #ff0000, 0 0 10px #ff3333; }
            100% { text-shadow: 0 0 5px #ff0000; }
        }
    </style>
</head>
<body>

    <!-- Fon uchun qo'rqinchili muhit musiqasi / ambient ovoz -->
    <audio autoplay loop>
        <source src="https://actions.google.com/sounds/v1/ambiences/creepy_wind.ogg" type="audio/ogg">
    </audio>

    <div class="container">
        <h1 class="pulse">OGOHLANTIRISH</h1>
        <p class="typewriter" id="typing-text">Siz bu eshikni ochmasligingiz kerak edi...</p>
        <div class="warning">⚠️ Orqaga qaytish uchun juda kech. Ular seni ko'rib turibdi.</div>
    </div>

    <script>
        // Yozuv effekti uchun matnni sekin chiqarish
        const textElement = document.getElementById("typing-text");
        const originalText = textElement.innerHTML;
        textElement.innerHTML = "";
        
        let i = 0;
        function typeWriter() {
            if (i < originalText.length) {
                textElement.innerHTML += originalText.charAt(i);
                i++;
                setTimeout(typeWriter, 80);
            }
        }
        setTimeout(typeWriter, 1000);
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
