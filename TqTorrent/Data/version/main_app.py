import sys
import os # Стандартная библиотека
import json # Стандартная библиотека
import subprocess # Стандартная библиотека
import time # Стандартная библиотека
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import QUrl, QObject, pyqtSlot, QTimer 
from PyQt6.QtWebChannel import QWebChannel 
import re # Стандартная библиотека

# --- КОНФИГУРАЦИЯ (Проверьте пути!) ---
BASE_CONFIG_PATH = r"C:\Users\drswa\OneDrive\Documents\TqTorrent\Data\config"
DATA_FILE_PATH = os.path.join(BASE_CONFIG_PATH, "data.json")
CACHE_FILE_PATH = os.path.join(BASE_CONFIG_PATH, "cache.txt")
PLUS_FILE_PATH = os.path.join(BASE_CONFIG_PATH, "plus_file.txt") 
# --------------------

# ----------------- КЛАСС-МОСТ (PYTHON -> JAVASCRIPT) -----------------
class GameLauncherBridge(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent 
        
    @pyqtSlot(str, result=str)
    def launchGame(self, launch_path):
        """Запускает игру, используя Popen с правильным рабочим каталогом."""
        print(f"Python: Попытка запустить: {launch_path}")
        try:
            # Получаем каталог, в котором находится исполняемый файл, для установки как working directory (cwd)
            working_dir = os.path.dirname(launch_path)
            
            # Запуск исполняемого файла напрямую, без shell=True
            subprocess.Popen([launch_path], cwd=working_dir) 
            
            print(f"Python: Успешно запущено. Рабочий каталог: {working_dir}")
            return "SUCCESS"
        except Exception as e:
            error_message = f"ОШИБКА запуска игры: {e}"
            print(error_message)
            return error_message

# ---------------------------------------------------------------------

class GameCatalogApp(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("TqG — Каталог Игр")
        self.setGeometry(100, 100, 1400, 900) 
        
        self.browser = QWebEngineView()
        self.channel = QWebChannel(self.browser.page())
        
        self.bridge = GameLauncherBridge(self) 
        self.channel.registerObject('qt_bridge', self.bridge)
        self.browser.page().setWebChannel(self.channel)
        
        current_dir = os.path.dirname(os.path.abspath(__file__))
        html_file_path = os.path.join(current_dir, 'index.html')
        local_url = QUrl.fromLocalFile(html_file_path)
        self.browser.setUrl(local_url)

        # Передача данных в JS после загрузки страницы
        self.last_cache_mtime = 0 
        self.browser.page().loadFinished.connect(self.send_data_to_js)
        self.browser.page().loadFinished.connect(self.setup_update_timer) 
        
        self.setCentralWidget(self.browser)
        
    def setup_update_timer(self):
        """Настраивает таймер для периодической проверки cache.txt."""
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.check_for_updates) 
        self.timer.start(5000) 
        print("Python: Запущен таймер проверки обновлений (5 сек).")

    def check_for_updates(self):
        """Проверяет, был ли изменен файл cache.txt, и обновляет UI, если да."""
        if not os.path.exists(CACHE_FILE_PATH):
            return

        try:
            current_mtime = os.path.getmtime(CACHE_FILE_PATH)
        except Exception as e:
            print(f"ОШИБКА при получении mtime: {e}")
            return
            
        if self.last_cache_mtime == 0:
            # Игнорируем первое сравнение, только устанавливаем начальное время
            self.last_cache_mtime = current_mtime
            return

        if current_mtime > self.last_cache_mtime:
            print("Python: Обнаружено изменение файла cache.txt. Обновление данных...")
            self.send_data_to_js()
            self.last_cache_mtime = current_mtime

    def read_plus_file(self):
        """Читает плюс_file.txt для определения начальной вкладки."""
        if not os.path.exists(PLUS_FILE_PATH):
            return "catalog" 
        try:
            with open(PLUS_FILE_PATH, 'r', encoding='utf-8') as f:
                view_name = f.readline().strip().lower()
                # Маппинг для соответствия data-view атрибутам
                if view_name == "установленные":
                    return "installed"
                elif view_name == "загрузки":
                    return "downloads"
                elif view_name == "моды":
                    return "mods"
                elif view_name == "настройки":
                    return "settings"
                else:
                    return "catalog"
        except Exception as e:
            print(f"ОШИБКА при чтении plus_file.txt: {e}")
            return "catalog"
            
    def parse_cache_txt(self):
        """Читает и парсит cache.txt, используя поле deisvie (Действие)."""
        game_data = []
        if not os.path.exists(CACHE_FILE_PATH):
            return game_data
        
        try:
            with open(CACHE_FILE_PATH, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            print(f"ОШИБКА при чтении cache.txt: {e}")
            return game_data

        # Ищет блоки, начинающиеся с g# = ...
        game_blocks = re.findall(r'(g\d+\s*=\s*.+)', content, re.DOTALL)
        
        game_id_counter = 1
        for block in game_blocks:
            match_name = re.search(r'name\((.*?)\)', block, re.DOTALL)
            match_priwie = re.search(r'priwie\((.*?)\)', block, re.DOTALL)
            match_opisan = re.search(r'opisan\((.*?)\)', block, re.DOTALL)
            match_url_ins = re.search(r'url_ins\((.*?)\)', block, re.DOTALL)
            match_dowanloadin = re.search(r'dowanloadin\((.*?)\)', block, re.DOTALL)
            match_starting = re.search(r'starting\((.*?)\)', block, re.DOTALL)
            match_deisvie = re.search(r'deisvie\((.*?)\)', block, re.DOTALL)
            
            title = match_name.group(1).strip() if match_name else "Без названия"
            image = match_priwie.group(1).strip() if match_priwie else ""
            description = match_opisan.group(1).strip() if match_opisan else ""
            url_install = match_url_ins.group(1).strip() if match_url_ins else "" 
            process_name = match_dowanloadin.group(1).strip() if match_dowanloadin else ""
            launch_path = match_starting.group(1).strip() if match_starting else ""
            initial_action = match_deisvie.group(1).strip().lower() if match_deisvie else "не скачено" 

            game_obj = {
                "id": game_id_counter,
                "title": title,
                "description": description,
                "image": image,
                "steam_app_id": None, 
                "process_name": process_name,
                "launch_path": launch_path,
                "url_install": url_install,
                "action": initial_action
            }
            game_data.append(game_obj)
            game_id_counter += 1
            
        return game_data

    def load_config_data(self):
        """Читает CNF_DATA из data.json и объединяет с GAME_DATA из cache.txt."""
        cnf_data = {
            "progr_name": "TqG", 
            "steam_nickname": "Drswa", 
            "installed_game_ids": [], 
            "running_game_ids": [],
            "download_status": "", 
            "initial_view": self.read_plus_file()
        }

        if os.path.exists(DATA_FILE_PATH):
            try:
                with open(DATA_FILE_PATH, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    cnf_data.update(data.get("CNF_DATA", {}))
            except Exception as e:
                print(f"ОШИБКА при чтении data.json: {e}")

        game_data = self.parse_cache_txt()

        return {
            "CNF_DATA": cnf_data,
            "GAME_DATA": game_data
        }

    def send_data_to_js(self):
        """Передает данные из Python в JavaScript."""
        config_data = self.load_config_data()
        
        if config_data:
            json_str = json.dumps(config_data, ensure_ascii=False)
            
            js_code = f"if (typeof setConfigData === 'function') {{ setConfigData({json_str}); }} else {{ console.error('JS function setConfigData is not defined.'); }}"
            self.browser.page().runJavaScript(js_code)
            print("Python: Конфигурационные данные успешно переданы в JavaScript.")
        else:
            print("Python: Не удалось загрузить или передать данные в JavaScript.")

def run_app():
    app = QApplication(sys.argv)
    main_window = GameCatalogApp()
    main_window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    run_app()