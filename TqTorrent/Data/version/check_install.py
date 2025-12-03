import json
import os
import time
import subprocess

# --- КОНФИГУРАЦИЯ ---
# Абсолютный путь к вашему файлу данных
CONFIG_FILE_PATH = r"C:\Users\drswa\OneDrive\Documents\TqTorrent\Data\config\data.json"
# --------------------

def is_game_running(process_name):
    # ... (логика проверки процессов остается без изменений) ...
    if not process_name:
        return False
        
    try:
        # tasklist /fi "IMAGENAME eq process_name"
        result = subprocess.run(
            ['tasklist', '/fi', f'IMAGENAME eq {process_name}'], 
            capture_output=True, 
            text=True,
            check=False 
        )
        return process_name.lower() in result.stdout.lower()
    except Exception:
        return False

def check_steam_status(nickname):
    """
    !!! ПЛЕЙСХОЛДЕР ДЛЯ ПРОВЕРКИ НИКНЕЙМА STEAM (Space War) !!!
    
    Для реальной работы требуется Steam SDK, Web API или чтение логов клиента.
    """
    print(f"\n[STEAM CHECK] Ищем пользователя: {nickname}...")
    time.sleep(0.5)
    
    # Имитация: если никнейм присутствует в конфиге, считаем его верифицированным
    if nickname and nickname != "N/A":
        print("[STEAM CHECK] Пользователь найден и верифицирован.")
        return True
    else:
        print("[STEAM CHECK] Пользователь не настроен в config. Проверка пропущена.")
        return False

def check_and_install_missing_games():
    data_path = CONFIG_FILE_PATH
    
    # 1. ЧТЕНИЕ ДАННЫХ
    if not os.path.exists(data_path):
        print(f"ОШИБКА: Файл конфигурации не найден по пути:\n{data_path}\nПроверка отменена.")
        return
    try:
        with open(data_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"ОШИБКА при чтении '{data_path}': {e}")
        return

    cnf_data = data.get("CNF_DATA", {})
    game_data = data.get("GAME_DATA", [])
    
    steam_nickname = cnf_data.get("steam_nickname", "N/A")
    
    # --- ВЫЗОВ ПРОВЕРКИ STEAM ---
    check_steam_status(steam_nickname)
    
    installed_ids = set(cnf_data.get("installed_game_ids", []))
    running_ids = set() 

    # 2. ПРОВЕРКА И ИМИТАЦИЯ УСТАНОВКИ (логика остается прежней)
    missing_games = [g for g in game_data if g.get("id") not in installed_ids]
    # ... (остальная логика установки)

    # 3. ПРОВЕРКА ЗАПУЩЕННЫХ ИГР (логика остается прежней)
    print("\nПроверка запущенных процессов...")
    for game in game_data:
        game_id = game.get("id")
        process_name = game.get("process_name")
        
        if game_id in installed_ids and process_name:
            if is_game_running(process_name):
                running_ids.add(game_id)
                print(f"-> [НАЙДЕНО] Игра '{game['title']}' активна ({process_name}).")
            
    # 4. ОБНОВЛЕНИЕ JSON
    data["CNF_DATA"]["installed_game_ids"] = sorted(list(installed_ids))
    data["CNF_DATA"]["running_game_ids"] = sorted(list(running_ids)) 
    
    try:
        with open(data_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False) 
        print(f"\n[ЗАПИСЬ] Конфигурация обновлена. {len(running_ids)} игр активны.")
    except Exception as e:
        print(f"\n[ОШИБКА] Не удалось обновить '{data_path}': {e}")


if __name__ == "__main__":
    check_and_install_missing_games()