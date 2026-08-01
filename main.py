import os
from Flask import Flask, render_template_string

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

        p {
            font-size: 1.2rem;
            color: #a6a6a6;
            margin-bottom: 30px;
        }

        .warning {
            color: #ff4d4d;
            font-weight: bold;
            margin-top: 20px;
            font-size: 1rem;
            text-transform: uppercase;
        }

        /* Kirish tugmasi */
        .horror-btn {
            background-color: #5c0000;
            color: #ff1a1a;
            border: 2px solid #ff1a1a;
            padding: 12px 30px;
            font-size: 1.2rem;
            font-family: 'Courier New', Courier, monospace;
            cursor: pointer;
            border-radius: 5px;
            box-shadow: 0 0 15px rgba(255, 0, 0, 0.5);
            transition: 0.3s;
        }

        .horror-btn:hover {
            background-color: #ff1a1a;
            color: #030303;
            box-shadow: 0 0 25px #ff1a1a;
        }

        .hidden {
            display: none;
        }
    </style>
</head>
<body>

    <!-- Fon ovozi uchun audio element -->
    <audio id="creepy-audio" loop>
        <source src="https://actions.google.com/sounds/v1/ambiences/creepy_wind.ogg" type="audio/ogg">
    </audio>

    <div class="container" id="welcome-screen">
        <h1>DIQQAT!</h1>
        <p>Bu sahifa kuchli psixologik muhitga ega.<br>Davom etish uchun yuragingiz sust emasligiga ishonch hosil qiling.</p>
        <button class="horror-btn" onclick="startExperience()">KIRISH</button>
    </div>

    <div class="container hidden" id="main-screen">
        <h1 style="text-shadow: 0 0 20px #ff0000;">SEN TUZAKDASAN</h1>
        <p>Qorong'ulik allaqachon ortingizda turgandek tuyulmayaptimi?..</p>
        <div class="warning">⚠️ Orqaga yo'l yo'q. Qochib qutula olmaysiz.</div>
    </div>

    <script>
        function startExperience() {
            // Ovozni yoqish
            var audio = document.getElementById("creepy-audio");
            audio.play().catch(error => console.log("Audio o'ynashda xatolik:", error));

            // Ekranlarni almashtirish
            document.getElementById("welcome-screen").classList.add("hidden");
            document.getElementById("main-screen").classList.remove("hidden");
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
