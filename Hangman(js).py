<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Advanced Hangman Royale</title>
    <style>
        :root {
            --bg-color: #0f172a;
            --card-color: #1e293b;
            --accent-color: #38bdf8;
            --accent-hover: #0ea5e9;
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --success: #22c55e;
            --error: #ef4444;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }

        body {
            background-color: var(--bg-color);
            color: var(--text-main);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            padding: 20px;
            overflow-x: hidden;
        }

        .game-container {
            background-color: var(--card-color);
            border-radius: 16px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.3);
            width: 100%;
            max-width: 800px;
            padding: 30px;
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 30px;
            position: relative;
        }

        @media (max-width: 768px) {
            .game-container {
                grid-template-columns: 1fr;
            }
        }

        /* Left Column: Visuals */
        .visual-panel {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: space-between;
        }

        header h1 {
            color: var(--accent-color);
            font-size: 1.8rem;
            margin-bottom: 5px;
            text-align: center;
            letter-spacing: 2px;
        }

        .category-badge {
            background: rgba(56, 189, 248, 0.1);
            color: var(--accent-color);
            padding: 6px 16px;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 600;
            margin-bottom: 20px;
            border: 1px solid rgba(56, 189, 248, 0.2);
        }

        canvas {
            background: #111827;
            border-radius: 12px;
            max-width: 100%;
            box-shadow: inset 0 4px 10px rgba(0,0,0,0.5);
        }

        /* Right Column: Game Logic Space */
        .game-panel {
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            gap: 25px;
        }

        .word-display {
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
            justify-content: center;
            min-height: 50px;
            align-items: center;
        }

        .letter-slot {
            border-bottom: 4px solid var(--text-muted);
            width: 32px;
            height: 45px;
            font-size: 2rem;
            font-weight: bold;
            text-align: center;
            text-transform: uppercase;
            color: var(--text-main);
            transition: all 0.2s ease;
        }

        .letter-slot.revealed {
            border-bottom-color: var(--success);
            color: var(--accent-color);
            animation: popIn 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        }

        .status-message {
            font-size: 1.1rem;
            font-weight: 500;
            min-height: 24px;
            text-align: center;
            transition: color 0.3s;
        }

        .keyboard {
            display: grid;
            grid-template-columns: repeat(7, 1fr);
            gap: 8px;
            width: 100%;
        }

        .key {
            background-color: #334155;
            color: var(--text-main);
            border: none;
            padding: 12px 0;
            font-size: 1.1rem;
            font-weight: bold;
            border-radius: 6px;
            cursor: pointer;
            text-transform: uppercase;
            transition: all 0.15s ease;
        }

        .key:hover:not(:disabled) {
            background-color: var(--accent-color);
            transform: translateY(-2px);
        }

        .key:disabled {
            opacity: 0.25;
            cursor: not-allowed;
        }

        .key.correct {
            background-color: var(--success) !important;
            opacity: 0.7;
        }

        .key.wrong {
            background-color: var(--error) !important;
            opacity: 0.4;
        }

        /* Modal Overlay Screens */
        .screen-overlay {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(15, 23, 42, 0.95);
            border-radius: 16px;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            z-index: 10;
            padding: 20px;
            text-align: center;
            opacity: 0;
            pointer-events: none;
            transition: opacity 0.3s ease;
        }

        .screen-overlay.active {
            opacity: 1;
            pointer-events: auto;
        }

        .screen-overlay h2 {
            font-size: 2.5rem;
            margin-bottom: 15px;
        }

        .screen-overlay p {
            color: var(--text-muted);
            margin-bottom: 30px;
            font-size: 1.1rem;
        }

        .btn {
            background-color: var(--accent-color);
            color: #000;
            border: none;
            padding: 12px 30px;
            font-size: 1.1rem;
            font-weight: bold;
            border-radius: 8px;
            cursor: pointer;
            transition: background 0.2s, transform 0.1s;
        }

        .btn:hover {
            background-color: var(--accent-hover);
            transform: scale(1.05);
        }

        .category-select-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
            width: 100%;
            max-width: 400px;
        }

        /* Keyframes */
        @keyframes popIn {
            0% { transform: scale(0.5); opacity: 0; }
            100% { transform: scale(1); opacity: 1; }
        }
    </style>
</head>
<body>

    <div class="game-container">
        
        <div class="visual-panel">
            <header>
                <h1>HANGMAN ROYALE</h1>
            </header>
            <div class="category-badge" id="categoryName">Category: -</div>
            <canvas id="hangmanCanvas" width="230" height="230"></canvas>
        </div>

        <div class="game-panel">
            <div class="word-display" id="wordDisplay"></div>
            <div class="status-message" id="statusMessage">Pick a letter to begin...</div>
            <div class="keyboard" id="keyboard"></div>
        </div>

        <div class="screen-overlay active" id="startScreen">
            <h2>Select a Category</h2>
            <p>Challenge yourself in specialized terminology arenas.</p>
            <div class="category-select-grid" id="categoryOptions"></div>
        </div>

        <div class="screen-overlay" id="endScreen">
            <h2 id="endTitle">Result</h2>
            <p id="endSubtext">The word was...</p>
            <button class="btn" id="restartBtn">Play Again</button>
        </div>

    </div>

    <script>
        // --- GAME ASSETS & DATA ---
        const CATEGORIES = {
            "Programming": ["javascript", "developer", "algorithm", "compiler", "database", "frontend"],
            "Animals": ["kangaroo", "chameleon", "platypus", "leopard", "dolphin", "elephant"],
            "Countries": ["switzerland", "australia", "madagascar", "brazil", "japan", "canada"],
            "Sci-Fi Movies": ["inception", "gladiator", "interstellar", "avengers", "parasite", "matrix"]
        };

        // --- STATE VARIABLES ---
        let selectedWord = "";
        let selectedCategory = "";
        let guessedLetters = new Set();
        let wrongGuesses = 0;
        const maxLives = 6;

        // --- DOM ELEMENTS ---
        const canvas = document.getElementById('hangmanCanvas');
        const ctx = canvas.getContext('2d');
        const wordDisplay = document.getElementById('wordDisplay');
        const keyboard = document.getElementById('keyboard');
        const statusMessage = document.getElementById('statusMessage');
        const categoryNameBadge = document.getElementById('categoryName');
        
        const startScreen = document.getElementById('startScreen');
        const endScreen = document.getElementById('endScreen');
        const categoryOptions = document.getElementById('categoryOptions');
        const endTitle = document.getElementById('endTitle');
        const endSubtext = document.getElementById('endSubtext');
        const restartBtn = document.getElementById('restartBtn');

        // --- INTERFACE BUILDERS ---
        function initCategoryMenu() {
            categoryOptions.innerHTML = '';
            Object.keys(CATEGORIES).forEach(cat => {
                const btn = document.createElement('button');
                btn.className = 'btn';
                btn.textContent = cat;
                btn.onclick = () => startGame(cat);
                categoryOptions.appendChild(btn);
            });
        }

        function createKeyboard() {
            keyboard.innerHTML = '';
            for (let i = 97; i <= 122; i++) {
                const letter = String.fromCharCode(i);
                const button = document.createElement('button');
                button.className = 'key';
                button.textContent = letter;
                button.setAttribute('data-key', letter);
                button.onclick = () => handleGuess(letter);
                keyboard.appendChild(button);
            }
        }

        // --- CANVAS RENDERING ENGINE ---
        function resetCanvas() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            ctx.lineWidth = 4;
            ctx.strokeStyle = "#f8fafc"; // Text color compatibility
            
            // Base/Gallows baseline (Drawn immediately)
            ctx.beginPath();
            ctx.moveTo(20, 210); ctx.lineTo(180, 210);
            ctx.moveTo(50, 210); ctx.lineTo(50, 20);
            ctx.lineTo(140, 20); ctx.lineTo(140, 50);
            ctx.stroke();
        }

        function drawHangman(stage) {
            ctx.strokeStyle = "#ef4444"; // Death red lines
            ctx.lineWidth = 4;
            ctx.beginPath();
            
            switch(stage) {
                case 1: // Head
                    ctx.arc(140, 65, 15, 0, Math.PI * 2);
                    break;
                case 2: // Torso
                    ctx.moveTo(140, 80); ctx.lineTo(140, 140);
                    break;
                case 3: // Left Arm
                    ctx.moveTo(140, 95); ctx.lineTo(110, 115);
                    break;
                case 4: // Right Arm
                    ctx.moveTo(140, 95); ctx.lineTo(170, 115);
                    break;
                case 5: // Left Leg
                    ctx.moveTo(140, 140); ctx.lineTo(115, 185);
                    break;
                case 6: // Right Leg
                    ctx.moveTo(140, 140); ctx.lineTo(165, 185);
                    break;
            }
            ctx.stroke();
        }

        // --- CORE GAME LOGIC ---
        function startGame(category) {
            selectedCategory = category;
            const words = CATEGORIES[category];
            selectedWord = words[Math.floor(Math.random() * words.length)];
            guessedLetters.clear();
            wrongGuesses = 0;

            // DOM Adjustments
            categoryNameBadge.textContent = `Category: ${selectedCategory}`;
            statusMessage.textContent = "Make your opening move!";
            statusMessage.style.color = "var(--text-muted)";
            startScreen.classList.remove('active');
            endScreen.classList.remove('active');

            resetCanvas();
            createKeyboard();
            renderWordDisplay();
        }

        function renderWordDisplay() {
            wordDisplay.innerHTML = '';
            let won = true;

            [...selectedWord].forEach(letter => {
                const slot = document.createElement('div');
                slot.className = 'letter-slot';
                
                if (guessedLetters.has(letter)) {
                    slot.textContent = letter;
                    slot.classList.add('revealed');
                } else {
                    slot.textContent = '';
                    won = false;
                }
                wordDisplay.appendChild(slot);
            });

            if (won && selectedWord.length > 0) {
                endGame(true);
            }
        }

        function handleGuess(letter) {
            if (guessedLetters.has(letter) || wrongGuesses >= maxLives) return;

            guessedLetters.add(letter);
            const keyButton = document.querySelector(`.key[data-key="${letter}"]`);
            if (keyButton) keyButton.disabled = true;

            if (selectedWord.includes(letter)) {
                if (keyButton) keyButton.classList.add('correct');
                statusMessage.textContent = `Good strike! "${letter.toUpperCase()}" is correct.`;
                statusMessage.style.color = "var(--success)";
                renderWordDisplay();
            } else {
                if (keyButton) keyButton.classList.add('wrong');
                wrongGuesses++;
                statusMessage.textContent = `Miss! "${letter.toUpperCase()}" is not in the word.`;
                statusMessage.style.color = "var(--error)";
                drawHangman(wrongGuesses);
                
                if (wrongGuesses >= maxLives) {
                    endGame(false);
                }
            }
        }

        function endGame(isWin) {
            setTimeout(() => {
                endScreen.classList.add('active');
                if (isWin) {
                    endTitle.textContent = "VICTORY! 🎉";
                    endTitle.style.color = "var(--success)";
                    endSubtext.innerHTML = `Brilliant deduction! You survived with <strong>${maxLives - wrongGuesses}</strong> remaining lives.`;
                } else {
                    endTitle.textContent = "DEFEAT 💀";
                    endTitle.style.color = "var(--error)";
                    endSubtext.innerHTML = `The hangman claimed this round.<br>The mystery word was: <strong style="color:var(--accent-color); font-size:1.4rem">${selectedWord.toUpperCase()}</strong>`;
                }
            }, 500);
        }

        // --- HARDWARE KEYBOARD ATTACHMENT ---
        window.addEventListener('keydown', (e) => {
            // Ignore keystrokes if a modal menu overlay is visible
            if (startScreen.classList.contains('active') || endScreen.classList.contains('active')) return;
            
            const key = e.key.toLowerCase();
            if (key >= 'a' && key <= 'z') {
                handleGuess(key);
            }
        });

        restartBtn.onclick = () => {
            endScreen.classList.remove('active');
            startScreen.classList.add('active');
        };

        // Initialize App
        initCategoryMenu();
    </script>
</body>
</html>
