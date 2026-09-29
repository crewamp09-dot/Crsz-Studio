<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Crew Upload Method</title>
    <style>
        :root {
            --bg-color: #0c0915;
            --card-bg: #151122;
            --accent-color: #8b5cf6;
            --accent-hover: #7c3aed;
            --text-main: #ffffff;
            --text-muted: #9ca3af;
            --border-color: #2e2442;
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        }

        body {
            background-color: var(--bg-color);
            color: var(--text-main);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }

        .modal-container {
            width: 100%;
            max-width: 440px;
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 16px;
            padding: 24px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
            position: relative;
        }

        .timer-bar {
            text-align: right;
            font-size: 13px;
            color: var(--text-muted);
            margin-bottom: 16px;
            font-weight: 600;
        }

        .header-content {
            text-align: center;
            margin-bottom: 24px;
        }

        .icon-box {
            width: 48px;
            height: 48px;
            background: rgba(139, 92, 246, 0.15);
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto 16px auto;
            color: var(--accent-color);
            font-size: 24px;
        }

        .badge {
            font-size: 11px;
            text-transform: uppercase;
            letter-spacing: 1px;
            color: var(--accent-color);
            font-weight: 700;
            margin-bottom: 8px;
            display: block;
        }

        h1 {
            font-size: 20px;
            font-weight: 700;
            margin-bottom: 8px;
            line-height: 1.3;
        }

        p {
            font-size: 13px;
            color: var(--text-muted);
            line-height: 1.5;
        }

        .action-btn {
            display: flex;
            align-items: center;
            justify-content: space-between;
            width: 100%;
            background: rgba(139, 92, 246, 0.1);
            border: 1px solid rgba(139, 92, 246, 0.3);
            color: var(--text-main);
            padding: 12px 16px;
            border-radius: 10px;
            font-size: 14px;
            font-weight: 600;
            cursor: pointer;
            text-decoration: none;
            margin-bottom: 24px;
            transition: background 0.2s;
        }

        .action-btn:hover {
            background: rgba(139, 92, 246, 0.2);
        }

        .divider {
            text-align: center;
            position: relative;
            margin-bottom: 20px;
        }

        .divider span {
            background: var(--card-bg);
            padding: 0 10px;
            font-size: 12px;
            color: var(--text-muted);
            position: relative;
            z-index: 1;
        }

        .divider::after {
            content: "";
            position: absolute;
            top: 50%;
            left: 0;
            width: 100%;
            height: 1px;
            background: var(--border-color);
            z-index: 0;
        }

        .form-group {
            margin-bottom: 16px;
        }

        .label-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 8px;
        }

        .label-row label {
            font-size: 13px;
            font-weight: 600;
        }

        .find-id-link {
            font-size: 12px;
            color: var(--accent-color);
            text-decoration: none;
            font-weight: 600;
        }

        .find-id-link:hover {
            text-decoration: underline;
        }

        input[type="text"] {
            width: 100%;
            background: #0c0915;
            border: 1px solid var(--border-color);
            padding: 12px;
            border-radius: 10px;
            color: var(--text-main);
            font-size: 14px;
            outline: none;
            transition: border-color 0.2s;
        }

        input[type="text"]:focus {
            border-color: var(--accent-color);
        }

        .verify-btn {
            width: 100%;
            background: var(--accent-color);
            color: white;
            border: none;
            padding: 12px;
            border-radius: 10px;
            font-size: 14px;
            font-weight: 600;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
            transition: background 0.2s;
            margin-bottom: 16px;
        }

        .verify-btn:hover {
            background: var(--accent-hover);
        }

        .continue-btn {
            display: flex;
            align-items: center;
            justify-content: space-between;
            width: 100%;
            background: transparent;
            border: 1px solid var(--border-color);
            color: var(--text-muted);
            padding: 12px 16px;
            border-radius: 10px;
            font-size: 13px;
            font-weight: 600;
            cursor: pointer;
            text-decoration: none;
            transition: all 0.2s;
        }

        .continue-btn:hover {
            border-color: var(--text-muted);
            color: var(--text-main);
        }
    </style>
</head>
<body>

    <div class="modal-container">
        <div class="timer-bar" id="timer">8s</div>

        <div class="header-content">
            <div class="icon-box">
                ✈️
            </div>
            <span class="badge">CREW UPLOAD METHOD</span>
            <h1>Sınırsız Kalite Moduna Hoş Geldiniz</h1>
            <p>Devam etmek ve günlük sınırları kaldırmak için duyurular kanalımıza katılın.</p>
        </div>

        <a href="https://t.me/" target="_blank" class="action-btn">
            <span>Duyuru Kanalına Katıl</span>
            <span>↗</span>
        </a>

        <div class="divider">
            <span>ZATEN KATILDINIZ MI?</span>
        </div>

        <div class="form-group">
            <div class="label-row">
                <label for="telegram-id">Telegram User ID</label>
                <a href="https://t.me/username_to_id_bot" target="_blank" class="find-id-link">ID'mi Bul</a>
            </div>
            <input type="text" id="telegram-id" placeholder="Örnek: 653760865">
        </div>

        <button class="verify-btn" onclick="verifyUser()">
            <span>Doğrula</span>
            <span>→</span>
        </button>

        <a href="#" class="continue-btn" onclick="skipVerification(event)">
            <span>Normal kullanım ile devam et</span>
            <span>→</span>
        </a>
    </div>

    <script>
        // Geri sayım sayacı
        let timeLeft = 8;
        const timerElement = document.getElementById('timer');
        
        const countdown = setInterval(() => {
            timeLeft--;
            timerElement.textContent = timeLeft + 's';
            if (timeLeft <= 0) {
                clearInterval(countdown);
            }
        }, 1000);

        function verifyUser() {
            const userId = document.getElementById('telegram-id').value;
            if(!userId) {
                alert('Lütfen Telegram ID giriniz.');
                return;
            }
            alert('ID doğrulandı: ' + userId);
        }

        function skipVerification(e) {
            e.preventDefault();
            alert('Normal mod ile devam ediliyor...');
        }
    </script>
</body>
</html>

