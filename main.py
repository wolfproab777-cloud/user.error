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
            padding: 30px;
            border-radius: 12px;
            box-shadow: 0 0 50px rgba(255, 0, 0, 0.4);
            max-width: 650px;
            width: 90%;
            position: relative;
            z-index: 1000;
            text-align: left;
        }

        h1 {
            text-align: center;
            font-size: 1.8rem;
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

        /* Test / Savollar dizayni */
        .question-text {
            font-size: 1.1rem;
            color: #ff4d4d;
            margin-bottom: 20px;
            text-align: center;
        }

        .options-container {
            display: flex;
            flex-direction: column;
            gap: 12px;
        }

        .option-btn {
            background: #1a0000;
            border: 2px solid #ff0000;
            color: #ffcccc;
            padding: 12px 15px;
            text-align: left;
            border-radius: 8px;
            cursor: pointer;
            transition: 0.3s;
            font-family: 'Courier New', Courier, monospace;
            font-size: 0.95rem;
        }

        .option-btn:hover {
            background: #4d0000;
            box-shadow: 0 0 15px #ff0000;
            color: #ffffff;
        }

        /* AI Yordamchi (Odamcha) dizayni */
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
            width: 320px;
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
            height: 140px;
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

    <!-- 1. BOSHLANG'ICH OGOHLANTIRISH EKRANI -->
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

        <button class="horror-btn" id="boldi-btn" onclick="startQuestions()">BO'LDI</button>
    </div>

    <!-- 2. 20 TA QO'RQINCHILI SAVOL EKRANI -->
    <div class="container hidden" id="game-screen">
        <h1 id="question-counter" style="font-size: 1.3rem; text-shadow: 0 0 10px #ff0000;">SAVOL 1 / 20</h1>
        <div class="question-text" id="question-title">Savol yuklanmoqda...</div>
        <div class="options-container" id="options-box"></div>
    </div>

    <!-- 3. EKSTRIMAL ROZILIK EKRANI (Savollardan keyin) -->
    <div class="container hidden" id="extreme-screen" style="text-align: center;">
        <h1 style="color: #ff0000; text-shadow: 0 0 20px #ff0000;">⚠️ OXIRGI SINOV</h1>
        <p style="color: #d9d9d9; font-size: 1rem; margin-bottom: 25px;">
            SAYT SIZNI QORQITISHI UCHUN EKSTRIMAL REJIMGA ROZIMISIZ?
        </p>

        <label class="checkbox-group" style="justify-content: center; margin-bottom: 20px;">
            <input type="checkbox" id="extreme-check" onchange="validateExtremeForm()">
            <span style="color: #ff4d4d; font-weight: bold;">HA, MEN BARCHASIGA TAYYORMAN!</span>
        </label>

        <button class="horror-btn" id="extreme-btn" onclick="triggerExtremeChaos()">BOSHQA ILoji YO'Q</button>
        <p id="timer-text" style="color: #888; font-size: 0.9rem; margin-top: 15px;"></p>
    </div>

    <!-- AI YORDAMCHI (Odamcha) -->
    <div id="ai-assistant" title="Yordamchi AI (Meni sudrashingiz mumkin)" onclick="toggleAiChat()">
        <img src="https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?q=80&w=200&auto=format&fit=crop" alt="AI">
    </div>

    <!-- AI Chat Oynasi -->
    <div id="ai-chat-box">
        <h4>💀 Qorong'u Yordamchi AI</h4>
        <div id="ai-chat-messages">
            Salom! Men sinovdagi sirlar bo'yicha yordamchingman. Savolingni ber, javob beraman...
        </div>
        <div class="ai-input-group">
            <input type="text" id="ai-user-input" placeholder="Savol berish...">
            <button onclick="askAi()">Berish</button>
        </div>
    </div>

    <script>
        let experienceStarted = false;
        let currentQuestionIndex = 0;
        let extremeInterval = null;

        const questions = [
            { q: "1. Tunda derazangiz ortidan kimdir pichirlab ismingizni aytsa, nima qilasiz?", options: ["A) Derazani ochib qarayman", "B) Ko'rpa ostiga berkinib, ovoz chiqarmayman", "C) Ism noto'g'ri aytildi deb o'ylayman", "D) O'sha yoqqa qarab baqiraman"] },
            { q: "2. Uyda yolg'iz ekansiz, kimsasiz koridordan qadam tovushlari eshitila boshladi. Ilk reaksiyangiz?", options: ["A) Eshikni qulflab, devorga tayanib o'tiraman", "B) Chiroqni yoqib tekshirib chiqaman", "C) Kulgili musiqa qo'yib ovoz chiqaraman", "D) Joyimdan jilmay qotib qolaman"] },
            { q: "3. Ko'zguga qaraganingizda, o'zingizning aksingiz sizdan bir soniya kech harakat qilsa?", options: ["A) Ko'zni yumib ochaman", "B) Ko'zguni sindirib tashlayman", "C) Dahshatdan hushimdan ketaman", "D) O'sha aks begona ekanini tushunaman"] },
            { q: "4. Telefoningizga o'zingizning uxlayotgan holatingizdagi surat kelib tushdi. Kim yuborgan?", options: ["A) Xonadagi ko'rinmas mavjudot", "B) O'zim tushimda rasmga tushganman", "C) Hazilakam do'stlarim", "D) Bilishni ham istamayman"] },
            { q: "5. Tunda tushingizda qora soyalar sizni o'rab olib, 'Sen biznikisan' deyishsa?", options: ["A) Uyg'onishga harakat qilaman, lekin qimirlay olmayman", "B) Ularga qarshi kurashaman", "C) Baqirib yuboraman", "D) Jim qabul qilaman"] },
            { q: "6. Qorong'u yerto'ladan g'alati qichqiriq eshitildi va eshik o'z-o'zidan ochildi. Nima qilasiz?", options: ["A) Ichkariga qarab yuraman", "B) Eshikni qalin temir bilan berkitaman", "C) Qochib ketishga harakat qilaman", "D) Qotib qolaman"] },
            { q: "7. Hech kim yo'q xonada telefoningizdan 'Seni ko'rib turibman' degan quruq ovoz kelsa?", options: ["A) Telefonni o'chirib tashlayman", "B) Atrofga alanglayman", "C) Javob qaytarib gaplashaman", "D) Uyda kim borligini qidiraman"] },
            { q: "8. Ko'chada ketayotib, ortingizdan qadam tovushlari eshitildi. O'girilib qarasangiz — hech kim yo'q, lekin tovush yaqinlashmoqda...", options: ["A) Yugura boshlayman", "B) Joyimda to'xtab turaman", "C) Ko'chani o'zgartiraman", "D) Ko'zlarimni yumib olaman"] },
            { q: "9. Tun yarmida kompyuteringiz o'z-o'zidan yoqilib, veb-kamirasi sizga qaray boshlasa?", options: ["A) Rozetkadan sug'urib tashlayman", "B) Ekrandagi narsaga tikilib qarayman", "C) Stol ostiga berkinaman", "D) Vahimaga tushaman"] },
            { q: "10. Yotoqxonangiz burchagida qora siluet paydo bo'ldi va u asta-sekin sizga qarab yura boshladi?", options: ["A) O'rnimdan turib qochishga urinaman", "B) Qimirlay olmay qotib qolaman", "C) Yorug'likni yoqishga intilaman", "D) Unga taslim bo'laman"] },
            { q: "11. Liftda yolg'iz ketayotgansiz, u kimsasiz qavatda to'xtadi va hech kim kirmadi, lekin eshik yopilmayapti...", options: ["A) Eshikni tepsib yopishga harakat qilaman", "B) 1-qavat tugmasini qayta-qayta bosaman", "C) Lift ichidagi burchakka o'tib olaman", "D) Qichqirib yuboraman"] },
            { q: "12. Tunda eshik taqilladi. Ochib qarasangiz hech kim yo'q, lekin polda qonli izlar turibdi...", options: ["A) Izlar ortidan yura boshlayman", "B) Eshikni tezda qulflayman", "C) Politsiyaga qo'ng'iroq qilaman", "D) Dahshatdan qotib qolaman"] },
            { q: "13. Ko'chada ketayotib hamma odamlar to'xtab qolganini va faqat siz harakatlanayotganingizni sezsangiz?", options: ["A) Boshqalarni qimirlatishga urinaman", "B) Uyga qarab yuguraman", "C) Bu qanday tush ekanini o'ylayman", "D) Vahimaga tushaman"] },
            { q: "14. Soyangiz sizdan alohida mustaqil ravishda qo'lini ko'tarsa?", options: ["A) Qo'limni pastga tushirib sinab ko'raman", "B) Chiroqni o'chirib yuboraman", "C) Qichqirib yuboraman", "D) Ko'zimga ko'rinyapti deb o'ylayman"] },
            { q: "15. Eski suratlar albomini varaqlayotgansiz, lekin avval hech qachon ko'rmagan o'zingizning suratingiz chiqib kelsa va u qabristonda olingan bo'lsa?", options: ["A) Albobni yopib tashlayman", "B) Suratlarni yirtib tashlayman", "C) Kim buni qo'yganini qidiraman", "D) Qotib qolaman"] },
            { q: "16. Tunda tushingizdan uyg'ongach, xonangizda g'alati hid va qandaydir nafas olish ovozini eshitsangiz?", options: ["A) Chiroqni yoqishga harakat qilaman", "B) Nafas olmay yotaveraman", "C) Ko'rpani boshimgacha yopaman", "D) Sekin o'rnimdan turaman"] },
            { q: "17. Qorong'u o'rmonda ketayotib, daraxt ortidan sizning ovozingiz bilan kimdir yordam so'rayotganini eshitsangiz?", options: ["A) O'sha ovoz tomonga boraman", "B) Teskari tomonga qarab qochaman", "C) Ovozni e'tiborsiz qoldirib tez yuraman", "D) Joyimda to'xtab qolaman"] },
            { q: "18. Yotoqxonangizdagi shkaf eshigi o'z-o'zidan jich-jich ochilib, ichidan yaltiroq ko'zlar qarab tursa?", options: ["A) Shkafni borib yopaman", "B) Ko'rpaga berkinib olaman", "C) Xonadan otilib chiqib ketaman", "D) Qotib qolaman"] },
            { q: "19. Kompyuter ekranida noma'lum fayl paydo bo'ldi va uning nomi sizning ism-sharifingiz bo'lsa?", options: ["A) Faylni ochib ko'raman", "B) Darhol o'chirib tashlayman", "C) Antivirus tekshiruvini yoqaman", "D) O'chib ketishini kutaman"] },
            { q: "20. Oxirgi sinov: Siz bu dunyoda yolg'iz emassiz va kimdir sizni o'z olib ketishini aytsa, nima deysiz?", options: ["A) Qarshilik ko'rsataman", "B) Taslim bo'laman", "C) Qochib qutulishga harakat qilaman", "D) Men tayyorman"] }
        ];

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

        function startQuestions() {
            let c1 = document.getElementById("check1").checked;
            let c2 = document.getElementById("check2").checked;
            let c3 = document.getElementById("check3").checked;

            if (!(c1 && c2 && c3)) {
                alert("Iltimos, barcha shartlarga rozilik belgisini qo'ying!");
                return;
            }

            experienceStarted = true;
            document.getElementById("warning-screen").classList.add("hidden");
            document.getElementById("game-screen").classList.remove("hidden");
            loadQuestion();
        }

        function loadQuestion() {
            if (currentQuestionIndex >= questions.length) {
                // 20 ta savol tugadi, endi Ekstremal rozilik ekraniga o'tamiz
                document.getElementById("game-screen").classList.add("hidden");
                document.getElementById("extreme-screen").classList.remove("hidden");
                return;
            }

            let qData = questions[currentQuestionIndex];
            document.getElementById("question-counter").innerText = "SAVOL " + (currentQuestionIndex + 1) + " / 20";
            document.getElementById("question-title").innerText = qData.q;

            let optionsBox = document.getElementById("options-box");
            optionsBox.innerHTML = "";

            qData.options.forEach((opt) => {
                let btn = document.createElement("button");
                btn.className = "option-btn";
                btn.innerText = opt;
                btn.onclick = () => {
                    if (Math.random() > 0.4) {
                        triggerScreamer();
                    }
                    currentQuestionIndex++;
                    loadQuestion();
                };
                optionsBox.appendChild(btn);
            });
        }

        function validateExtremeForm() {
            let chk = document.getElementById("extreme-check").checked;
            let btn = document.getElementById("extreme-btn");
            if (chk) {
                btn.classList.add("active");
            } else {
                btn.classList.remove("active");
            }
        }

        // Galchka bosilmasa yoki orqaga bosilgach 10 sekund ketib o'zi boshlanish funksiyasi
        function triggerExtremeChaos() {
            let chk = document.getElementById("extreme-check").checked;
            let timerText = document.getElementById("timer-text");
            let btn = document.getElementById("extreme-btn");

            btn.style.pointerEvents = "none";

            let countdown = 10;
            timerText.innerText = "Rozilik belgisi qo'yilmadi! Xavfli rejim " + countdown + " sekunddan keyin majburiy boshlanadi...";

            extremeInterval = setInterval(() => {
                countdown--;
                if (countdown > 0) {
                    timerText.innerText = "Xavfli rejim " + countdown + " sekunddan keyin majburiy boshlanadi...";
                } else {
                    clearInterval(extremeInterval);
                    startExtremeLoop();
                }
            }, 1000);
        }

        function startExtremeLoop() {
            document.getElementById("extreme-screen").classList.add("hidden");
            
            // Sichqonchani bloklash, oynani tizish va ekranni kichraytirib-kattalashtirish harakati
            setInterval(() => {
                triggerScreamer();
                // Ekranni o'lchamini o'zgartirib vahima qo'shish
                document.body.style.transform = Math.random() > 0.5 ? "scale(0.95)" : "scale(1.05)";
                
                // Ko'plab yangi oyna ochish simulyatsiyasi (ekranni to'ldirish)
                let newWindow = window.open(window.location.href, "_blank", "width=300,height=300,left=" + Math.random()*window.innerWidth + ",top=" + Math.random()*window.innerHeight);
            }, 1500);

            // To'xtatish uchun yashirin buyruq (Ctrl + C bosib turilganda to'xtashi uchun fon tinglovchisi)
            document.addEventListener('keydown', function(e) {
                if (e.ctrlKey && e.key.toLowerCase() === 'c') {
                    alert("Tizim to'xtatildi.");
                    location.reload();
                }
            });
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

        // AI ga savol berish va qo'rqinchili javoblar qaytarish
        function askAi() {
            let inputField = document.getElementById("ai-user-input");
            let msgBox = document.getElementById("ai-chat-messages");
            let question = inputField.value.trim();

            if (question === "") return;

            msgBox.innerHTML += "<br><b style='color:#ff4d4d;'>Sen:</b> " + question;

            let answer = "Bu savolning javobi qorong'ulikda yashiringan...";
            let qLower = question.toLowerCase();

            if (qLower.includes("qayerdaman") || qLower.includes("joy")) {
                answer = "Sen 20 ta qo'rqinchili sinov labirintidasan, oxirida esa dahshat seni kutmoqda!";
            } else if (qLower.includes("yordam") || qLower.includes("qanday")) {
                answer = "Senga faqat o'z sezgilaring yordam berishi mumkin, ehtiyot bo'l...";
            } else {
                let answers = [
                    "Men sening fikrlaringni o'qiyapman...",
                    "Bu savolga javob berish hayotingga tushishi mumkin.",
                    "Ular seni kuzatib turibdi, savollarga tezroq javob ber!",
                    "Bu yerdan qochib qutula olmaysan.",
                    "Har bir bosgan qadaming seni oxirga yaqinlashtiradi."
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
