import os
import sys
from pathlib import Path
import datetime

def create_tqtorrent_structure():
    """Создаёт структуру папок и файлов для TqTorrent"""
    
    # Основная папка в Документах
    base_dir = Path.home() / "Documents" / "TqTorrent"
    
    # Подпапки
    localsaves_dir = base_dir / "Localsaves_by_TqTorrent"
    log_dir = base_dir / "log"
    tqmanager_dir = base_dir / "TqManager"
    version_dir = base_dir / "Version"
    
    # Папка saves внутри Localsaves_by_TqTorrent
    saves_dir = localsaves_dir / "saves"
    
    print("=" * 50)
    print("Создание структуры TqTorrent")
    print("=" * 50)
    
    try:
        # Создаём основную папку
        base_dir.mkdir(exist_ok=True)
        print(f"[✓] Основная папка: {base_dir}")
        
        # Создаём Localsaves_by_TqTorrent
        localsaves_dir.mkdir(exist_ok=True)
        print(f"[✓] Папка Localsaves_by_TqTorrent создана")
        
        # Создаём папку saves
        saves_dir.mkdir(exist_ok=True)
        print(f"[✓] Папка saves создана")
        
        # Создаём файлы в папке saves
        config_file = saves_dir / "config"
        config_file.touch(exist_ok=True)
        print(f"[✓] Файл config создан")
        
        cnf_file = saves_dir / "cnf.txt"
        if not cnf_file.exists():
            with open(cnf_file, 'w', encoding='utf-8') as f:
                f.write("# Конфигурационный файл TqTorrent\n")
                f.write(f"created_at: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("version: 1.0\n")
            print(f"[✓] Файл cnf.txt создан и заполнен")
        else:
            print(f"[✓] Файл cnf.txt уже существует")
        
        # Создаём папку log
        log_dir.mkdir(exist_ok=True)
        print(f"[✓] Папка log создана")
        
        # Создаём log.txt с начальной записью
        log_file = log_dir / "log.txt"
        if not log_file.exists():
            with open(log_file, 'w', encoding='utf-8') as f:
                f.write("=" * 50 + "\n")
                f.write(f"Лог TqTorrent - {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("=" * 50 + "\n\n")
                f.write("[INIT] Структура папок создана успешно\n")
                f.write(f"[INFO] Путь: {base_dir}\n")
            print(f"[✓] Файл log.txt создан и заполнен")
        else:
            # Добавляем запись в существующий лог
            with open(log_file, 'a', encoding='utf-8') as f:
                f.write(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Структура проверена/создана\n")
            print(f"[✓] Запись добавлена в существующий log.txt")
        
        # Создаём папку TqManager
        tqmanager_dir.mkdir(exist_ok=True)
        print(f"[✓] Папка TqManager создана")
        
        # Создаём базовый файл в TqManager
        manager_file = tqmanager_dir / "manager_config.ini"
        if not manager_file.exists():
            with open(manager_file, 'w', encoding='utf-8') as f:
                f.write("[TqManager]\n")
                f.write(f"created = {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("active = true\n")
            print(f"[✓] Файл manager_config.ini создан в TqManager")
        
        # Создаём папку Version
        version_dir.mkdir(exist_ok=True)
        print(f"[✓] Папка Version создана")
        
        # Создаём файл версии
        version_file = version_dir / "version.txt"
        if not version_file.exists():
            with open(version_file, 'w', encoding='utf-8') as f:
                f.write("TqTorrent v1.0.0\n")
                f.write(f"Build date: {datetime.datetime.now().strftime('%Y-%m-%d')}\n")
                f.write("Structure created\n")
            print(f"[✓] Файл version.txt создан")
        
        print("\n" + "=" * 50)
        print("СТРУКТУРА УСПЕШНО СОЗДАНА!")
        print("=" * 50)
        print(f"\nСозданные папки и файлы:")
        print(f"📁 {base_dir}/")
        print(f"  📁 Localsaves_by_TqTorrent/")
        print(f"    📁 saves/")
        print(f"      📄 config")
        print(f"      📄 cnf.txt")
        print(f"  📁 log/")
        print(f"    📄 log.txt")
        print(f"  📁 TqManager/")
        print(f"    📄 manager_config.ini")
        print(f"  📁 Version/")
        print(f"    📄 version.txt")
        
        # Записываем путь в отдельный файл для использования другими скриптами
        path_info = base_dir / "path_info.txt"
        with open(path_info, 'w', encoding='utf-8') as f:
            f.write(str(base_dir))
        
        return True, str(base_dir)
        
    except Exception as e:
        print(f"\n[✗] ОШИБКА: Не удалось создать структуру")
        print(f"Ошибка: {e}")
        return False, str(e)

def check_existing_structure():
    """Проверяет существующую структуру"""
    base_dir = Path.home() / "Documents" / "TqTorrent"
    
    if base_dir.exists():
        print("\n" + "=" * 50)
        print("ПРОВЕРКА СУЩЕСТВУЮЩЕЙ СТРУКТУРЫ")
        print("=" * 50)
        
        required_items = [
            (base_dir / "Localsaves_by_TqTorrent", "папка"),
            (base_dir / "Localsaves_by_TqTorrent" / "saves", "папка"),
            (base_dir / "Localsaves_by_TqTorrent" / "saves" / "config", "файл"),
            (base_dir / "Localsaves_by_TqTorrent" / "saves" / "cnf.txt", "файл"),
            (base_dir / "log", "папка"),
            (base_dir / "log" / "log.txt", "файл"),
            (base_dir / "TqManager", "папка"),
            (base_dir / "Version", "папка"),
        ]
        
        missing_items = []
        
        for item_path, item_type in required_items:
            if item_path.exists():
                print(f"[✓] {item_type.capitalize()} существует: {item_path.name}")
            else:
                print(f"[✗] {item_type.capitalize()} отсутствует: {item_path.name}")
                missing_items.append((item_path, item_type))
        
        return missing_items
    return []

if __name__ == "__main__":
    print("TqTorrent Structure Creator")
    print("Скрипт создаст структуру папок и файлов для TqTorrent")
    
    # Проверяем существующую структуру
    missing = check_existing_structure()
    
    if missing:
        print(f"\nНайдено отсутствующих элементов: {len(missing)}")
        response = input("Хотите создать отсутствующие элементы? (Y/N): ")
        
        if response.lower() == 'y':
            success, result = create_tqtorrent_structure()
        else:
            print("Операция отменена пользователем.")
            success = False
            result = "Отменено пользователем"
    else:
        print("\nВся структура уже создана!")
        response = input("Хотите пересоздать структуру? (Y/N): ")
        
        if response.lower() == 'y':
            success, result = create_tqtorrent_structure()
        else:
            print("Структура оставлена без изменений.")
            success = True
            result = "Структура уже существует"
    
    # Ждём нажатия Enter перед закрытием
    print("\n" + "=" * 50)
    if success:
        print("✅ СТРУКТУРА ГОТОВА К ИСПОЛЬЗОВАНИЮ")
    else:
        print("❚ ПРОИЗОШЛА ОШИБКА")
    print("=" * 50)
    
    input("\nНажмите Enter для выхода...")
