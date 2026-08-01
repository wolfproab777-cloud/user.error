import os
from flask import Flask, render_template_string

app = Flask(__name__)

# Qo'rqinchili va mistik dizayndagi HTML/CSS kodlari
HORROR_HTML = """
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Sirlar Dunyosi...</title>
    <style>
        body {
            background-color: #050505;
            color: #b30000;
            font-family: 'Courier New', Courier, monospace;
            text-align: center;
            padding-top: 100px;
            overflow: hidden;
            margin: 0;
        }
        .container {
            background: rgba(20, 0, 0, 0.8);
            border: 2px solid #550000;
            display: inline-block;
            padding: 40px;
            border-radius: 10px;
            box-shadow: 0 0 30px rgba(255, 0, 0, 0.4);
            max-width: 600px;
        }
        h1 {
            font-size: 3rem;
            text-shadow: 2px 2px 10px #ff0000;
            animation: glitch 1s infinite alternate;
        }
        p {
            color: #8c8c8c;
            font-size: 1.2rem;
            margin-top: 20px;
        }
        .warning {
            color: #ff3333;
            font-weight: bold;
            margin-top: 30px;
            font-size: 1.1rem;
        }
        @keyframes glitch {
            0% { text-shadow: 2px 2px 10px #ff0000; }
            50% { text-shadow: -2px -2px 20px #8b0000; }
            100% { text-shadow: 2px -2px 10px #ff0000; }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>DIQQAT QILMAGAN BO'LSANGIZ...</h1>
        <p>Siz bu sahifaga kirmasligingiz kerak edi. Qorong'ulik allaqachon sizni kuzatmoqda...</p>
        <div class="warning">⚠️ Orqaga yo'l yo'q. Bu yerda hamma narsa sirga boy.</div>
    </div>
</body>
</html>
"""

@app.route('/')
def horror_page():
    return render_template_string(HORROR_HTML)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
