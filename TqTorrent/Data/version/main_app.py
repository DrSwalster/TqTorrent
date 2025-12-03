import sys
import os
import json
import subprocess
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import QUrl, QObject, pyqtSlot 
from PyQt6.QtWebChannel import QWebChannel 
import re 

# --- КОНФИГУРАЦИЯ ---
BASE_CONFIG_PATH = r"C:\Users\drswa\OneDrive\Documents\TqTorrent\Data\config"
DATA_FILE_PATH = os.path.join(BASE_CONFIG_PATH, "data.json")
CACHE_FILE_PATH = os.path.join(BASE_CONFIG_PATH, "cache.txt")
# --------------------

# ----------------- КЛАСС-МОСТ (PYTHON -> JAVASCRIPT) -----------------
class GameLauncherBridge(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)
        
    @pyqtSlot(str, result=str)
    def launchGame(self, launch_path):
        """
        Запускает игру с помощью команды 'start' для надежной обработки ярлыков (.url/.lnk) и steam://.
        """
        print(f"Python: Попытка запустить: {launch_path}")
        try:
            # Используем команду 'start' через shell=True
            subprocess.Popen(f'start "" "{launch_path}"', shell=True) 
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
        self.setGeometry(100, 100, 1200, 800) 
        
        self.browser = QWebEngineView()
        self.channel = QWebChannel(self.browser.page())
        self.bridge = GameLauncherBridge()
        self.channel.registerObject('qt_bridge', self.bridge)
        self.browser.page().setWebChannel(self.channel)
        
        current_dir = os.path.dirname(os.path.abspath(__file__))
        html_file_path = os.path.join(current_dir, 'index.html')
        local_url = QUrl.fromLocalFile(html_file_path)
        self.browser.setUrl(local_url)

        self.browser.page().loadFinished.connect(self.send_data_to_js)
        
        self.setCentralWidget(self.browser)
        
    def parse_cache_txt(self):
        """Читает и парсит cache.txt в список объектов Game Data."""
        game_data = []
        if not os.path.exists(CACHE_FILE_PATH):
            print(f"ОШИБКА: Файл кэша не найден по пути: {CACHE_FILE_PATH}")
            return game_data
        
        try:
            with open(CACHE_FILE_PATH, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            print(f"ОШИБКА при чтении cache.txt: {e}")
            return game_data

        # Регулярное выражение для поиска блоков gN = ...
        game_blocks = re.findall(r'(g\d+\s*=\s*.+)', content)
        
        game_id_counter = 1
        for block in game_blocks:
            # Извлечение полей
            match_name = re.search(r'name\((.*?)\)', block)
            match_priwie = re.search(r'priwie\((.*?)\)', block)
            match_opisan = re.search(r'opisan\((.*?)\)', block)
            match_url_ins = re.search(r'url_ins\((.*?)\)', block)
            match_dowanloadin = re.search(r'dowanloadin\((.*?)\)', block)
            # НОВЫЙ КЛЮЧ: starting()
            match_starting = re.search(r'starting\((.*?)\)', block)
            
            # Извлекаем значения
            title = match_name.group(1).strip() if match_name else "Без названия"
            image = match_priwie.group(1).strip() if match_priwie else ""
            description = match_opisan.group(1).strip() if match_opisan else ""
            # url_install теперь не launch_path
            url_install = match_url_ins.group(1).strip() if match_url_ins else "" 
            process_name = match_dowanloadin.group(1).strip() if match_dowanloadin else ""
            # launch_path берется из нового ключа starting()
            launch_path = match_starting.group(1).strip() if match_starting else ""

            # Создаем объект игры
            game_obj = {
                "id": game_id_counter,
                "title": title,
                "description": description,
                "image": image,
                "steam_app_id": None, 
                "process_name": process_name,
                "launch_path": launch_path, # Используем значение из starting()
                "url_install": url_install  # Можно использовать для кнопки "Установить"
            }
            game_data.append(game_obj)
            game_id_counter += 1
            
        return game_data

    def load_config_data(self):
        """Читает CNF_DATA из data.json и объединяет с GAME_DATA из cache.txt."""
        cnf_data = {"progr_name": "TqG", "installed_game_ids": [], "running_game_ids": []}

        # 1. Чтение CNF_DATA из data.json
        if os.path.exists(DATA_FILE_PATH):
            try:
                with open(DATA_FILE_PATH, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    cnf_data.update(data.get("CNF_DATA", {}))
            except json.JSONDecodeError:
                print("КРИТИЧЕСКАЯ ОШИБКА: Неверный синтаксис JSON в data.json!")
            except Exception as e:
                print(f"ОШИБКА при чтении data.json: {e}")

        # 2. Парсинг GAME_DATA из cache.txt
        game_data = self.parse_cache_txt()

        return {
            "CNF_DATA": cnf_data,
            "GAME_DATA": game_data
        }

    def send_data_to_js(self):
        """Передает данные из Python в JavaScript после загрузки страницы."""
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