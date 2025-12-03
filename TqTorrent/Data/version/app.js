// --- ДАННЫЕ ИНИЦИАЛИЗИРУЮТСЯ PYTHON'ОМ ---
let CNF_DATA = {};
let GAME_DATA = [];

// DOM ELEMENTS for the Modal
const detailModal = document.getElementById('game-detail-modal');
const closeModalBtn = document.getElementById('close-modal-btn');
const detailLaunchBtn = document.getElementById('detail-launch-btn');

// КРИТИЧЕСКАЯ ГЛОБАЛЬНАЯ ФУНКЦИЯ: вызывается Python'ом для передачи данных
window.setConfigData = function(data) {
    if (data && data.CNF_DATA && data.GAME_DATA) {
        CNF_DATA = data.CNF_DATA;
        GAME_DATA = data.GAME_DATA;
        console.log('JavaScript: Конфигурация получена от Python, загружаем UI.');
        loadGameData();
    } else {
        console.error('JavaScript: Получены неполные или некорректные данные от Python. Используем пустую конфигурацию.');
        loadGameData();
    }
}

// --- ФУНКЦИИ ИНТЕРФЕЙСА ---

function loadGameData() {
    const grid = document.getElementById('game-grid');
    grid.innerHTML = '';
    
    document.getElementById('app-title').textContent = CNF_DATA.progr_name || "TqG"; 

    GAME_DATA.forEach((game, index) => {
        const installedIds = CNF_DATA.installed_game_ids || [];
        const runningIds = CNF_DATA.running_game_ids || [];

        const isInstalled = installedIds.includes(game.id);
        const isRunning = runningIds.includes(game.id);
        
        let buttonText = "Установить";
        let buttonClass = "btn-install";
        
        if (isRunning) {
            buttonText = "Игра Запущена";
            buttonClass = "btn-running"; 
        } else if (isInstalled) {
            buttonText = "Запустить";
            buttonClass = "btn-launch";
        }

        const card = document.createElement('div');
        card.className = 'game-card';
        card.setAttribute('data-game-id', game.id);
        
        card.style.animation = `fadeIn 0.5s ease-out ${index * 0.1}s forwards`;
        
        card.innerHTML = `
            <img src="${game.image}" alt="Обложка ${game.title}">
            ${isRunning ? '<span class="game-status">ЗАПУЩЕНА</span>' : ''}
            <div class="card-info">
                <h3>${game.title}</h3>
                <p>${game.description}</p>
            </div>
            <button class="action-btn ${buttonClass}" data-path="${game.launch_path}" data-status="${buttonClass}" data-game-id="${game.id}">
                ${buttonText}
            </button>
        `;
        grid.appendChild(card);
    });
    
    addLaunchListeners();
    addDetailViewListeners(); 
}


// Единый обработчик для всех кнопок запуска
function handleLaunchClick(event) {
    const launchPath = event.target.getAttribute('data-path');
    const status = event.target.getAttribute('data-status');

    if (status === 'btn-launch') {
        if (window.qt_bridge) {
            const button = event.target;
            const gameId = parseInt(button.getAttribute('data-game-id'));
            const gameCard = document.querySelector(`.game-card[data-game-id="${gameId}"]`);
            
            button.disabled = true;

            window.qt_bridge.launchGame(launchPath, function(result) {
                button.disabled = false;
                console.log("Результат запуска от Python:", result);
                
                if (result === "SUCCESS") {
                    // 1. Немедленное обновление статуса
                    button.textContent = "Игра Запущена";
                    button.className = 'action-btn btn-running';
                    button.setAttribute('data-status', 'btn-running');
                    
                    // 2. Обновление статуса на главной карточке (если существует)
                    if (gameCard) {
                        if (!gameCard.querySelector('.game-status')) {
                            const statusSpan = document.createElement('span');
                            statusSpan.className = 'game-status';
                            statusSpan.textContent = 'ЗАПУЩЕНА';
                            gameCard.insertBefore(statusSpan, gameCard.children[1]);
                        }
                        // Обновляем кнопку на главной карточке, если она отличается
                        const mainCardButton = gameCard.querySelector('.action-btn');
                        if (mainCardButton && mainCardButton !== button) {
                            mainCardButton.textContent = "Игра Запущена";
                            mainCardButton.className = 'action-btn btn-running';
                            mainCardButton.setAttribute('data-status', 'btn-running');
                        }
                    }
                    
                    // 3. Обновляем данные в памяти
                    if (CNF_DATA.running_game_ids && !CNF_DATA.running_game_ids.includes(gameId)) {
                        CNF_DATA.running_game_ids.push(gameId);
                    }
                    
                    // 4. Если запускали из модала, закрываем его
                    if (detailModal.classList.contains('is-visible')) {
                        detailModal.classList.remove('is-visible');
                    }
                    
                }
            });
        } else {
            console.error("QWebChannel (qt_bridge) не доступен. Запуск невозможен.");
        }
    } else if (status === 'btn-install') {
        console.log(`Попытка установки игры: ${gameCard ? gameCard.querySelector('h3').textContent : 'Неизвестно'}`);
    } else if (status === 'btn-running') {
        console.log('Игра уже запущена. Действие игнорируется.');
    }
}

function showGameDetail(gameId) {
    const game = GAME_DATA.find(g => g.id === gameId);
    if (!game) return;

    // Заполнение модального окна данными
    document.getElementById('detail-image').src = game.image;
    document.getElementById('detail-title').textContent = game.title;
    document.getElementById('detail-description').textContent = game.description;
    document.getElementById('detail-steam-id').textContent = game.steam_app_id || 'N/A';
    document.getElementById('detail-path').textContent = game.launch_path;
    
    // Обновление кнопки запуска в деталях
    const installedIds = CNF_DATA.installed_game_ids || [];
    const runningIds = CNF_DATA.running_game_ids || [];
    const isInstalled = installedIds.includes(game.id);
    const isRunning = runningIds.includes(game.id);
    
    let buttonText = "Установить";
    let buttonClass = "btn-install";
    
    if (isRunning) {
        buttonText = "Игра Запущена";
        buttonClass = "btn-running"; 
    } else if (isInstalled) {
        buttonText = "Запустить";
        buttonClass = "btn-launch";
    }

    detailLaunchBtn.textContent = buttonText;
    detailLaunchBtn.className = `action-btn ${buttonClass}`;
    detailLaunchBtn.setAttribute('data-path', game.launch_path);
    detailLaunchBtn.setAttribute('data-status', buttonClass);
    detailLaunchBtn.setAttribute('data-game-id', game.id); 

    // Показ модального окна с анимацией
    detailModal.classList.add('is-visible');
}

function addDetailViewListeners() {
    // 1. Слушатель для открытия деталей по клику на карточку (исключая кнопку)
    document.querySelectorAll('.game-card').forEach(card => {
        card.addEventListener('click', (event) => {
            // Проверяем, что клик был не на кнопке
            if (!event.target.classList.contains('action-btn')) {
                const gameId = parseInt(card.getAttribute('data-game-id'));
                showGameDetail(gameId);
            }
        });
    });

    // 2. Слушатели закрытия модального окна
    closeModalBtn.addEventListener('click', () => {
        detailModal.classList.remove('is-visible');
    });
    detailModal.addEventListener('click', (event) => {
        if (event.target === detailModal) {
            detailModal.classList.remove('is-visible');
        }
    });

    // 3. Слушатель для кнопки запуска внутри модального окна
    detailLaunchBtn.addEventListener('click', handleLaunchClick);
}

function addLaunchListeners() {
    // Слушатели только для кнопок на ГЛАВНОМ экране
    document.querySelectorAll('.game-grid .action-btn').forEach(button => {
        button.addEventListener('click', handleLaunchClick);
    });
}