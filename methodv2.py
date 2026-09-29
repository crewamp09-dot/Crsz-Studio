# Crew Upload Method - Videodaki Tüm Özellikler ve Sayfalar Dahil Tam Flask Kodu
from flask import Flask, render_template_string

app = Flask("crew_upload_full")

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Crew Upload Method - CompressBase</title>
    <style>
        :root {
            --bg-color: #0b0f19;
            --card-bg: #111827;
            --card-hover: #1f2937;
            --accent-color: #eab308;
            --accent-hover: #ca8a04;
            --text-main: #ffffff;
            --text-muted: #94a3b8;
            --border-color: #1e293b;
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
            flex-direction: column;
            align-items: center;
        }

        /* Navigasyon / Header */
        header {
            width: 100%;
            max-width: 600px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 20px;
            border-bottom: 1px solid var(--border-color);
        }

        .logo-area {
            display: flex;
            align-items: center;
            gap: 8px;
            font-weight: 800;
            font-size: 16px;
        }

        .logo-badge {
            background: var(--accent-color);
            color: #000;
            padding: 4px 8px;
            border-radius: 6px;
            font-size: 12px;
        }

        .menu-btn {
            background: none;
            border: none;
            color: var(--text-main);
            font-size: 20px;
            cursor: pointer;
        }

        /* Ana İçerik Alanı */
        .main-container {
            width: 100%;
            max-width: 600px;
            padding: 20px;
            flex: 1;
        }

        /* Modal / Giriş Ekranı (Telegram Doğrulama) */
        #auth-modal {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(11, 15, 25, 0.9);
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
            z-index: 1000;
        }

        .modal-container {
            width: 100%;
            max-width: 420px;
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 16px;
            padding: 24px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.6);
            position: relative;
        }

        .top-bar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 11px;
            color: var(--text-muted);
            margin-bottom: 12px;
            font-weight: 600;
        }

        .progress-line {
            width: 100%;
            height: 2px;
            background: var(--border-color);
            margin-bottom: 20px;
            position: relative;
            overflow: hidden;
        }

        .progress-fill {
            position: absolute;
            top: 0;
            left: 0;
            height: 100%;
            background: var(--accent-color);
            width: 100%;
            transition: width 1s linear;
        }

        .header-content {
            text-align: center;
            margin-bottom: 20px;
        }

        .badge-text {
            font-size: 11px;
            text-transform: uppercase;
            letter-spacing: 1px;
            color: var(--accent-color);
            font-weight: 700;
            margin-bottom: 6px;
            display: block;
        }

        h1 {
            font-size: 18px;
            font-weight: 700;
            margin-bottom: 6px;
            line-height: 1.3;
        }

        p {
            font-size: 12px;
            color: var(--text-muted);
            line-height: 1.4;
        }

        .action-btn {
            display: flex;
            align-items: center;
            justify-content: space-between;
            width: 100%;
            background: rgba(234, 179, 8, 0.08);
            border: 1px solid rgba(234, 179, 8, 0.3);
            color: var(--text-main);
            padding: 12px 16px;
            border-radius: 10px;
            font-size: 13px;
            font-weight: 600;
            cursor: pointer;
            text-decoration: none;
            margin-bottom: 16px;
            transition: background 0.2s;
        }

        .action-btn:hover {
            background: rgba(234, 179, 8, 0.15);
        }

        .divider {
            text-align: center;
            position: relative;
            margin-bottom: 16px;
        }

        .divider span {
            background: var(--card-bg);
            padding: 0 10px;
            font-size: 11px;
            color: var(--text-muted);
            position: relative;
            z-index: 1;
            font-weight: 700;
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
            margin-bottom: 14px;
        }

        .label-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 6px;
        }

        .label-row label {
            font-size: 12px;
            font-weight: 600;
        }

        .find-id-link {
            font-size: 11px;
            color: var(--accent-color);
            text-decoration: none;
            font-weight: 600;
        }

        input[type="text"] {
            width: 100%;
            background: var(--bg-color);
            border: 1px solid var(--border-color);
            padding: 10px 12px;
            border-radius: 8px;
            color: var(--text-main);
            font-size: 13px;
            outline: none;
        }

        input[type="text"]:focus {
            border-color: var(--accent-color);
        }

        .verify-btn {
            width: 100%;
            background: var(--accent-color);
            color: #000;
            border: none;
            padding: 12px;
            border-radius: 10px;
            font-size: 13px;
            font-weight: 700;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
            margin-bottom: 12px;
        }

        .continue-btn {
            display: flex;
            align-items: center;
            justify-content: space-between;
            width: 100%;
            background: transparent;
            border: 1px solid var(--border-color);
            color: var(--text-muted);
            padding: 10px 14px;
            border-radius: 10px;
            font-size: 12px;
            font-weight: 600;
            cursor: pointer;
            text-decoration: none;
        }

        /* Animasyonlu Hesap Doğrulama Overlay */
        #success-overlay {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: var(--card-bg);
            border-radius: 16px;
            display: none;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            z-index: 20;
            padding: 20px;
            text-align: center;
        }

        .spinner {
            width: 40px;
            height: 40px;
            border: 3px solid var(--border-color);
            border-top: 3px solid var(--accent-color);
            border-radius: 50%;
            animation: spin 0.8s linear infinite;
            margin-bottom: 12px;
        }

        @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }

        .account-card {
            background: var(--bg-color);
            border: 1px solid var(--border-color);
            padding: 12px 16px;
            border-radius: 10px;
            margin-top: 10px;
            width: 100%;
            display: flex;
            align-items: center;
            gap: 10px;
            text-align: left;
        }

        .account-avatar {
            width: 32px;
            height: 32px;
            background: var(--accent-color);
            color: #000;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            font-size: 14px;
        }

        /* Web Sitesi Ana Paneli (Videodaki Adımlar) */
        .panel-header {
            margin-bottom: 20px;
        }

        .panel-header h2 {
            font-size: 20px;
            font-weight: 800;
            margin-bottom: 4px;
        }

        .limit-box {
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 16px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
        }

        .get-unlimited-btn {
            background: var(--accent-color);
            color: #000;
            border: none;
            padding: 8px 14px;
            border-radius: 8px;
            font-weight: 700;
            font-size: 12px;
            cursor: pointer;
        }

        .step-card {
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 16px;
            margin-bottom: 16px;
        }

        .step-title {
            font-size: 14px;
            font-weight: 700;
            margin-bottom: 12px;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .step-num {
            background: var(--accent-color);
            color: #000;
            width: 22px;
            height: 22px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 12px;
        }

        .upload-dropzone {
            border: 2px dashed var(--border-color);
            border-radius: 10px;
            padding: 24px;
            text-align: center;
            cursor: pointer;
            background: var(--bg-color);
        }

        .method-option {
            background: var(--bg-color);
            border: 1px solid var(--border-color);
            border-radius: 10px;
            padding: 14px;
            margin-bottom: 10px;
            cursor: pointer;
        }

        .method-option.active {
            border-color: var(--accent-color);
        }

        /* Mini Oyun / Snake Alanı (Videodaki Bekleme Oyunu) */
        .game-container {
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 16px;
            margin-top: 20px;
            text-align: center;
        }

        .game-board {
            width: 100%;
            height: 160px;
            background: #1a1500;
            border-radius: 8px;
            margin-top: 10px;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            color: var(--accent-color);
            font-weight: bold;
        }
    </style>
</head>
<body>

    <!-- TELEGRAM DOĞRULAMA MODALI -->
    <div id="auth-modal">
        <div class="modal-container">
            <div class="top-bar">
                <span>THIS MESSAGE CLOSES AUTOMATICALLY</span>
                <span id="timer">8s</span>
            </div>
            <div class="progress-line">
                <div class="progress-fill" id="progressFill"></div>
            </div>

            <div class="header-content">
                <span class="badge-text">FREE UNLIMITED ACCESS</span>
                <h1>Want unlimited Quality Method uses?</h1>
                <p>Join <strong>Editing News</strong> to support developers and remove daily limits.</p>
            </div>

            <a href="https://t.me/crwandwn4s" target="_blank" class="action-btn">
                <span>Join Editing News</span>
                <span style="font-size: 11px; color: var(--text-muted);">Open Telegram ↗</span>
            </a>

            <div class="divider">
                <span>ALREADY JOINED?</span>
            </div>

            <div class="form-group">
                <div class="label-row">
                    <label for="telegram-id">Telegram user ID</label>
                    <a href="https://t.me/username_to_id_bot" target="_blank" class="find-id-link">Find my ID</a>
                </div>
                <input type="text" id="telegram-id" placeholder="Example: 653760865">
            </div>

            <button class="verify-btn" onclick="verifyUser()">
                <span>Verify</span>
                <span>→</span>
            </button>

            <a href="#" class="continue-btn" onclick="skipAuth(event)">
                <span>Continue with daily use</span>
                <span>→</span>
            </a>

            <!-- Animasyonlu Hesap Gösterim Ekranı -->
            <div id="success-overlay">
                <div class="spinner"></div>
                <h3 id="overlay-title" style="font-size: 15px;">Hesap Doğrulanıyor...</h3>
                <p style="font-size: 11px; margin-top: 4px;">ID sistem ile eşleştiriliyor</p>
                
                <div class="account-card" id="accountCard" style="display: none;">
                    <div class="account-avatar" id="accInitial">C</div>
                    <div>
                        <div id="accName" style="font-size: 13px; font-weight: 700;">Crew User</div>
                        <div id="accIdText" style="font-size: 11px; color: var(--text-muted);">ID: --</div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- ANA PANEL (VİDEODAKİ TÜM ÖZELLİKLER) -->
    <header>
        <div class="logo-area">
            <span class="logo-badge">CB</span>
            <span>COMPRESSBASE</span>
        </div>
        <button class="menu-btn" onclick="alert('Menü açıldı')">☰</button>
    </header>

    <div class="main-container">
        <div class="panel-header">
            <h2>Upload Method</h2>
            <p>Choose a video, pick a method, and download the finished file.</p>
        </div>

        <div class="limit-box">
            <div>
                <div style="font-size: 11px; color: var(--text-muted);">FREE ACCESS • PER DEVICE</div>
                <div style="font-size: 15px; font-weight: 800; margin-top: 2px;">5 of 5 uses left today</div>
            </div>
            <button class="get-unlimited-btn">Get unlimited</button>
        </div>

        <!-- Adım 1: Video Seçimi -->
        <div class="step-card">
            <div class="step-title">
                <div class="step-num">1</div>
                <span>Choose your video</span>
            </div>
            <div class="upload-dropzone" onclick="alert('Video seçme ekranı açıldı (Dosya/Galeri)')">
                <div style="font-size: 24px; margin-bottom: 6px;">📁</div>
                <div style="font-size: 13px; font-weight: 700;">Select video</div>
                <div style="font-size: 11px; color: var(--text-muted); margin-top: 2px;">or drag and drop your file here</div>
            </div>
        </div>

        <!-- Adım 2: Metot Seçimi -->
        <div class="step-card">
            <div class="step-title">
                <div class="step-num">2</div>
                <span>Choose a method</span>
            </div>
            <div class="method-option active">
                <div style="font-size: 13px; font-weight: 700;">MAX QUALITY + FPS METHOD</div>
                <div style="font-size: 11px; color: var(--text-muted); margin-top: 2px;">Preserves as much quality as possible and supports up to 1080p and 120 FPS.</div>
            </div>
            <div class="method-option">
                <div style="font-size: 13px; font-weight: 700;">Optimize file size for TikTok</div>
                <div style="font-size: 11px; color: var(--text-muted); margin-top: 2px;">Optional: Makes large files smaller while keeping good visual quality.</div>
            </div>
        </div>

        <!-- Bekleme Alanı / Mini Oyun (Snake) -->
        <div class="game-container">
            <div style="font-size: 13px; font-weight: 700;">Play while you wait</div>
            <div style="font-size: 11px; color: var(--text-muted);">Your video keeps processing in the background.</div>
            <div class="game-board">
                <span>🐍 Snake Game Active</span>
                <span style="font-size: 10px; color: var(--text-muted); margin-top: 4px;">Tap to play</span>
            </div>
        </div>
    </div>

    <script>
        // Üst Sayaç ve Çubuk
        let timeLeft = 8;
        const timerElement = document.getElementById('timer');
        const progressFill = document.getElementById('progressFill');
        
        const countdown = setInterval(() => {
            timeLeft--;
            timerElement.textContent = timeLeft + 's';
            progressFill.style.width = (timeLeft / 8) * 100 + '%';
            if (timeLeft <= 0) {
                clearInterval(countdown);
            }
        }, 1000);

        function verifyUser() {
            const userId = document.getElementById('telegram-id').value.trim();
            if(!userId) {
                alert('Lütfen Telegram ID giriniz.');
                return;
            }

            const overlay = document.getElementById('success-overlay');
            overlay.style.display = 'flex';

            document.getElementById('accIdText').textContent = 'ID: ' + userId;
            document.getElementById('accName').textContent = 'Crew User (' + userId.slice(-4) + ')';
            document.getElementById('accInitial').textContent = userId.charAt(0);

            setTimeout(() => {
                document.querySelector('.spinner').style.display = 'none';
                document.getElementById('overlay-title').textContent = 'Giriş Başarılı!';
                document.getElementById('accountCard').style.display = 'flex';
            }, 1000);

            setTimeout(() => {
                document.getElementById('auth-modal').style.display = 'none';
            }, 2400);
        }

        function skipAuth(e) {
            e.preventDefault();
            document.getElementById('auth-modal').style.display = 'none';
        }
    </script>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML_TEMPLATE)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

