import os
import sys
import subprocess
import json
from pathlib import Path
import datetime

def setup_logging():
    """Настройка системы логирования"""
    log_dir = Path.home() / "Documents" / "TqTorrent" / "log"
    log_file = log_dir / "tqtorrent.log"
    
    log_dir.mkdir(parents=True, exist_ok=True)
    
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(f"\n{'='*60}\n")
        f.write(f"TqTorrent запущен: {datetime.datetime.now()}\n")
        f.write(f"Python: {sys.version}\n")
        f.write(f"Платформа: {sys.platform}\n")
    
    return log_file

def check_dependencies():
    """Проверяет и устанавливает зависимости"""
    print("=" * 60)
    print("TqTorrent - Проверка зависимостей")
    print("=" * 60)
    
    # Базовые библиотеки (всегда нужны)
    base_libs = ["requests", "beautifulsoup4", "psutil"]
    
    # Дополнительные библиотеки по категориям
    categories = {
        "web": ["flask", "django", "fastapi"],
        "data": ["pandas", "numpy", "matplotlib"],
        "gui": ["PyQt5", "tkinter", "customtkinter"],
        "automation": ["selenium", "pyautogui", "schedule"],
        "database": ["sqlalchemy", "psycopg2", "pymongo"]
    }
    
    print("\nВыберите категории для установки:")
    print("1. Базовые (уже установлены)")
    for i, (cat, libs) in enumerate(categories.items(), 2):
        print(f"{i}. {cat.capitalize()} ({', '.join(libs)})")
    print(f"{len(categories)+2}. ВСЕ библиотеки")
    print(f"{len(categories)+3}. Только базовые (пропустить)")
    
    try:
        choice = input("\nВаш выбор (через запятую, например: 1,2,3): ")
        choices = [c.strip() for c in choice.split(',')]
        
        libraries_to_install = []
        
        if str(len(categories)+2) in choices:  # Все библиотеки
            for libs in categories.values():
                libraries_to_install.extend(libs)
        elif str(len(categories)+3) in choices:  # Только базовые
            libraries_to_install = []
        else:
            # Добавляем выбранные категории
            for choice_num in choices:
                if choice_num.isdigit():
                    idx = int(choice_num) - 2  # -2 потому что 1=базовые
                    if 0 <= idx < len(categories):
                        cat_name = list(categories.keys())[idx]
                        libraries_to_install.extend(categories[cat_name])
        
        # Установка библиотек
        if libraries_to_install:
            print(f"\nУстанавливаю {len(libraries_to_install)} библиотек...")
            for lib in libraries_to_install:
                print(f"  → {lib}...", end=" ")
                try:
                    subprocess.check_call([sys.executable, "-m", "pip", "install", lib])
                    print("✓")
                except subprocess.CalledProcessError:
                    print("✗")
        else:
            print("\nУстановка библиотек пропущена.")
            
    except Exception as e:
        print(f"\nОшибка: {e}")

def create_project_structure():
    """Создаёт структуру проекта для пользователя"""
    print("\n" + "=" * 60)
    print("Создание структуры проекта")
    print("=" * 60)
    
    project_name = input("Введите имя проекта (или Enter для пропуска): ").strip()
    
    if project_name:
        project_dir = Path.cwd() / project_name
        
        try:
            # Создаём структуру проекта
            (project_dir / "src").mkdir(parents=True, exist_ok=True)
            (project_dir / "data").mkdir(parents=True, exist_ok=True)
            (project_dir / "docs").mkdir(parents=True, exist_ok=True)
            (project_dir / "tests").mkdir(parents=True, exist_ok=True)
            
            # Создаём основные файлы
            files = {
                "README.md": f"# {project_name}\n\nПроект создан с помощью TqTorrent",
                "requirements.txt": "# Зависимости проекта\n\n",
                "main.py": "#!/usr/bin/env python3\n\"\"\"Основной файл проекта\"\"\"\n\nprint('Hello from TqTorrent!')\n",
                ".gitignore": "__pycache__/\n*.pyc\n.env\n"
            }
            
            for filename, content in files.items():
                (project_dir / filename).write_text(content, encoding='utf-8')
            
            print(f"\n✅ Проект '{project_name}' создан в: {project_dir}")
            
        except Exception as e:
            print(f"\n❌ Ошибка при создании проекта: {e}")

def main_menu():
    """Главное меню программы"""
    while True:
        print("\n" + "=" * 60)
        print("TQTORRENT - ГЛАВНОЕ МЕНЮ")
        print("=" * 60)
        print("1. 📦 Установить дополнительные библиотеки")
        print("2. 📁 Создать новый проект")
        print("3. 🔧 Настройки")
        print("4. ℹ️  Информация о системе")
        print("5. 📝 Логи")
        print("6. 🚪 Выход")
        print("=" * 60)
        
        choice = input("\nВыберите действие (1-6): ").strip()
        
        if choice == "1":
            check_dependencies()
        elif choice == "2":
            create_project_structure()
        elif choice == "3":
            print("\nНастройки пока не реализованы")
        elif choice == "4":
            print(f"\nИнформация о системе:")
            print(f"Python: {sys.version}")
            print(f"Платформа: {sys.platform}")
            print(f"Текущая папка: {Path.cwd()}")
        elif choice == "5":
            log_file = Path.home() / "Documents" / "TqTorrent" / "log" / "tqtorrent.log"
            if log_file.exists():
                print(f"\nПоследние записи лога ({log_file}):")
                with open(log_file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()[-20:]  # Последние 20 строк
                    print(''.join(lines))
            else:
                print("\nЛог файл не найден")
        elif choice == "6":
            print("\nДо свидания!")
            break
        else:
            print("\n❌ Неверный выбор. Попробуйте снова.")

def main():
    """Основная функция"""
    print("=" * 60)
    print("TQTORRENT v1.0.0")
    print("=" * 60)
    
    # Настройка логирования
    log_file = setup_logging()
    print(f"Логирование: {log_file}")
    
    # Проверяем структуру
    base_dir = Path.home() / "Documents" / "TqTorrent"
    if not base_dir.exists():
        print("⚠️  Структура TqTorrent не найдена!")
        response = input("Создать структуру? (Y/N): ").strip().lower()
        if response == 'y':
            # Создаём базовую структуру
            (base_dir / "Localsaves_by_TqTorrent" / "saves").mkdir(parents=True, exist_ok=True)
            (base_dir / "log").mkdir(parents=True, exist_ok=True)
            print("✅ Структура создана")
    
    # Главное меню
    main_menu()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nПрограмма прервана пользователем")
    except Exception as e:
        print(f"\n❌ Критическая ошибка: {e}")
        input("Нажмите Enter для выхода...")
