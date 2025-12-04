// --- КРИТИЧЕСКИ ВАЖНО: ДАННЫЕ ИНИЦИАЛИЗИРУЮТСЯ PYTHON'ОМ ---
let CNF_DATA = {};
let GAME_DATA = [];

// DOM ELEMENTS for the Modal and Panels
const detailModal = document.getElementById('game-detail-modal');
const closeModalBtn = document.getElementById('close-modal-btn');
const detailLaunchBtn = document.getElementById('detail-launch-btn');
const downloadStatusPanel = document.getElementById('download-status-panel');
const gameGrid = document.getElementById('game-grid'); 

// КРИТИЧЕСКАЯ ГЛОБАЛЬНАЯ ФУНКЦИЯ: вызывается Python'ом для передачи данных
window.setConfigData = function(data) {
    if (data && data.CNF_DATA && data.GAME_DATA) {
        CNF_DATA = data.CNF_DATA;
        GAME_DATA = data.GAME_DATA;
        console.log('JavaScript: Конфигурация получена от Python, загружаем UI.');
        
        loadGameData();
        updateDownloadStatusPanel(); 
        setInitialView(CNF_DATA.initial_view); 
        
    } else {
        console.error('JavaScript: Получены неполные или некорректные данные от Python.');
        loadGameData();
    }
}

function updateDownloadStatusPanel() {
    const statusTextElement = document.getElementById('download-status-text');
    const progressBarElement = document.getElementById('download-progress');

    if (CNF_DATA.download_status && CNF_DATA.download_status !== "") {
        downloadStatusPanel.classList.add('is-visible');
        downloadStatusPanel.classList.remove('stack-back');
        
        statusTextElement.textContent = CNF_DATA.download_status;
        
        // Попытка извлечь процент для прогресс-бара
        const match = CNF_DATA.download_status.match(/\((\d+)%\)/);
        const percent = match ? parseInt(match[1]) : 0;
        progressBarElement.style.width = `${percent}%`;

    } else {
        // Задержка исчезновения панели, чтобы избежать мерцания при быстром обновлении
        downloadStatusPanel.classList.add('stack-back'); 
        setTimeout(() => {
            if (!CNF_DATA.download_status) {
                downloadStatusPanel.classList.remove('is-visible');
            }
        }, 500); 
    }
}

function setInitialView(viewName) {
    const defaultView = 'catalog';
    const targetView = viewName || defaultView;

    // Снимаем активность со всех вкладок
    document.querySelectorAll('.nav-item').forEach(nav => nav.classList.remove('active'));
    document.querySelectorAll('.view-section').forEach(section => section.classList.remove('active'));

    // Активируем нужную вкладку и секцию
    const navItem = document.querySelector(`.nav-item[data-view="${targetView}"]`);
    const viewSection = document.getElementById(targetView + '-view');

    if (navItem) navItem.classList.add('active');
    if (viewSection) viewSection.classList.add('active');
}


function getButtonStatus(game) {
    let buttonText = "Установить";
    let buttonClass = "btn-install";
    let statusTag = "НЕ СКАЧЕНО";
    
    // Логика статусов на основе поля 'action' из cache.txt (deisvie)
    switch (game.action) {
        case "установлено":
            buttonText = "Запустить";
            buttonClass = "btn-launch";
            statusTag = "УСТАНОВЛЕНО";
            break;
        case "запущена": 
            buttonText = "Игра Запущена";
            buttonClass = "btn-running"; 
            statusTag = "ЗАПУЩЕНА";
            break;
        case "установка":
            buttonText = "Установка (0%)";
            buttonClass = "btn-launching"; 
            statusTag = "УСТАНОВКА";
            break;
        case "установка_регистрация":
            buttonText = "Регистрация...";
            buttonClass = "btn-launching"; 
            statusTag = "РЕГИСТРАЦИЯ";
            break;
        case "ошибка":
            buttonText = "Ошибка (Журнал)";
            buttonClass = "btn-error";
            statusTag = "ОШИБКА";
            break;
        case "не скачено": 
        default:
            buttonText = "Установить";
            buttonClass = "btn-install";
            statusTag = "НЕ СКАЧЕНО";
    }
    
    return { text: buttonText, class: buttonClass, statusTag: statusTag };
}


function loadGameData() {
    const grid = document.getElementById('game-grid');
    grid.innerHTML = '';
    
    document.getElementById('app-title').textContent = CNF_DATA.progr_name || "TqG"; 
    document.querySelector('.nickname').textContent = CNF_DATA.steam_nickname || "Пользователь";

    // ПРОВЕРКА НА ПУСТОЙ КЭШ: Если нет игр, показываем "Загрузка..."
    if (GAME_DATA.length === 0) {
        gameGrid.innerHTML = `
            <div class="empty-placeholder">
                <h1>Загрузка...</h1>
                <p>Ожидание данных из файла cache.txt. Если это занимает много времени, убедитесь, что файл не пуст или не поврежден.</p>
            </div>
        `;
        return; 
    }


    GAME_DATA.forEach((game, index) => {
        const { text: buttonText, class: buttonClass, statusTag } = getButtonStatus(game);

        const card = document.createElement('div');
        card.className = 'game-card';
        card.setAttribute('data-game-id', game.id);
        
        card.style.animation = `fadeIn 0.5s ease-out ${index * 0.05}s forwards`; 
        
        const statusClass = statusTag.toLowerCase().replace(/\s/g, '-').replace('(', '').replace(')', '');

        card.innerHTML = `
            <img src="${game.image}" alt="Обложка ${game.title}">
            <span class="game-status status-${statusClass}" data-status-tag="${statusTag}">
                ${statusTag}
            </span>
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
    addViewSwitchListeners(); 
}


// Единый обработчик для всех кнопок запуска/установки
function handleLaunchClick(event) {
    const launchPath = event.target.getAttribute('data-path');
    let status = event.target.getAttribute('data-status');
    const gameId = parseInt(event.target.getAttribute('data-game-id'));
    
    const button = event.target.closest('.action-btn');
    const container = event.target.closest('.game-card') || detailModal;
    const statusElement = container.querySelector('.game-status') || container.querySelector('.detail-status');

    if (status === 'btn-launch') {
        if (window.qt_bridge) {
            button.disabled = true;
            
            // Визуальный статус: Запускается
            if (statusElement) {
                statusElement.textContent = "ЗАПУСКАЕТСЯ";
                statusElement.className = statusElement.className.replace(/status-\S+/, 'status-запускается');
            }
            
            // Вызов Python-функции launchGame
            window.qt_bridge.launchGame(launchPath, function(result) {
                
                if (result === "SUCCESS") {
                    // В случае успеха, статус меняется на "Игра Запущена"
                    button.textContent = "Игра Запущена";
                    button.className = button.className.replace(/btn-\S+/, 'btn-running');
                    button.setAttribute('data-status', 'btn-running');
                    
                    if (statusElement) {
                        statusElement.textContent = 'ЗАПУЩЕНА';
                        statusElement.className = statusElement.className.replace(/status-\S+/, 'status-запущена');
                    }
                    detailModal.classList.remove('is-visible');
                    
                } else {
                     // В случае ошибки
                    button.textContent = "Ошибка (Журнал)";
                    button.className = button.className.replace(/btn-\S+/, 'btn-error');
                    button.setAttribute('data-status', 'btn-error');
                    
                    if (statusElement) {
                        statusElement.textContent = 'ОШИБКА';
                        statusElement.className = statusElement.className.replace(/status-\S+/, 'status-ошибка');
                    }
                    alert("Ошибка запуска: " + result);
                }
                button.disabled = false;
            });
        }
    } else if (status === 'btn-install') {
        console.log(`Попытка установки игры ID: ${gameId}`);
        const gameTitle = container.querySelector('h3') ? container.querySelector('h3').textContent : 'Игра';
        
        // Имитация статуса скачивания
        CNF_DATA.download_status = `Скачивание: ${gameTitle} (10%)`;
        updateDownloadStatusPanel();
        
    } else if (status === 'btn-running') {
        // Ничего не делать
        console.log("Игра уже запущена. Отслеживание процесса...");
    } else if (status === 'btn-error') {
         alert('Проверьте журнал ошибок для этой игры.');
    } 
}

function showGameDetail(gameId) {
    const game = GAME_DATA.find(g => g.id === gameId);
    if (!game) return;
    
    const { text: buttonText, class: buttonClass, statusTag } = getButtonStatus(game);
    const statusClass = statusTag.toLowerCase().replace(/\s/g, '-').replace('(', '').replace(')', '');

    // Заполнение модального окна данными
    document.getElementById('detail-image').src = game.image;
    document.getElementById('detail-title').textContent = game.title;
    document.getElementById('detail-description').textContent = game.description;
    
    // Детальный статус
    document.getElementById('detail-game-status').textContent = statusTag;
    document.getElementById('detail-game-status').className = `detail-status status-${statusClass}`;

    document.getElementById('detail-steam-id').textContent = game.steam_app_id || 'N/A';
    document.getElementById('detail-path').textContent = game.launch_path;
    
    // Обновление кнопки запуска в деталях
    detailLaunchBtn.textContent = buttonText;
    detailLaunchBtn.className = `action-btn ${buttonClass}`;
    detailLaunchBtn.setAttribute('data-path', game.launch_path);
    detailLaunchBtn.setAttribute('data-status', buttonClass);
    detailLaunchBtn.setAttribute('data-game-id', game.id); 

    detailModal.classList.add('is-visible');
}

function handleCardClick(event) {
    const card = event.target.closest('.game-card');
    // Проверяем, что клик не был по кнопке
    if (card && !event.target.classList.contains('action-btn')) {
        const gameId = parseInt(card.getAttribute('data-game-id'));
        showGameDetail(gameId);
    }
}

function addLaunchListeners() {
    document.querySelectorAll('.game-grid .action-btn').forEach(button => {
        button.removeEventListener('click', handleLaunchClick);
        button.addEventListener('click', handleLaunchClick);
    });
}

function addDetailViewListeners() {
    const grid = document.getElementById('game-grid');
    grid.removeEventListener('click', handleCardClick);
    grid.addEventListener('click', handleCardClick);

    closeModalBtn.removeEventListener('click', closeModal);
    closeModalBtn.addEventListener('click', closeModal);
    document.removeEventListener('keydown', handleEscapeKey);
    document.addEventListener('keydown', handleEscapeKey);

    detailLaunchBtn.removeEventListener('click', handleLaunchClick); 
    detailLaunchBtn.addEventListener('click', handleLaunchClick);
}

function closeModal() {
    detailModal.classList.remove('is-visible');
}
function handleEscapeKey(event) {
    if (event.key === "Escape") {
        closeModal();
    }
}

function addViewSwitchListeners() {
    document.querySelectorAll('.nav-item').forEach(item => {
        item.removeEventListener('click', handleViewSwitch);
        item.addEventListener('click', handleViewSwitch);
    });
}

function handleViewSwitch(e) {
    e.preventDefault();
    const targetView = this.getAttribute('data-view');
    
    document.querySelectorAll('.nav-item').forEach(nav => nav.classList.remove('active'));
    this.classList.add('active');
    
    document.querySelectorAll('.view-section').forEach(section => {
        section.classList.remove('active');
    });
    const section = document.getElementById(targetView + '-view');
    if (section) {
        section.classList.add('active');
    }
}