@echo off
:: Установка кодировки UTF-8 для корректного отображения кириллицы
chcp 65001 > nul 

setlocal

echo =======================================================
echo     ПРОВЕРКА И УСТАНОВКА ЗАВИСИМОСТЕЙ TqG LAUNCHER
echo =======================================================

:: --- 1. ПРОВЕРКА НАЛИЧИЯ PYTHON ---

echo.
echo [1/4] Проверка доступности Python...

:: Запускаем команду python --version и перенаправляем stderr в stdout (2>&1)
python --version 2>&1 | findstr /i "Python" > nul
if errorlevel 1 (
    goto :INSTALL_PYTHON
) else (
    echo [OK] Python установлен и доступен.
)


:: --- 2. УСТАНОВКА БИБЛИОТЕК (PyQt6) ---

echo.
echo [2/4] Установка необходимых библиотек (PyQt6, PyQt6-WebEngine)...
echo (Это может занять некоторое время...)

:: Запускаем pip install.
pip install PyQt6 PyQt6-WebEngine
if errorlevel 0 (
    echo [OK] Все библиотеки успешно установлены.
) else (
    echo [ОШИБКА] Не удалось установить библиотеки. ПРОВЕРЬТЕ ИНТЕРНЕТ И ПРАВА АДМИНИСТРАТОРА.
    pause
    goto :EOF
)


:: --- 3. ВЫПОЛНЕНИЕ ПРОВЕРКИ ИГР (check_install.py) ---

echo.
echo [3/4] Выполнение проверки установленных и запущенных игр...

:: Запускаем Python-скрипт, который обновляет data.json
python check_install.py
if errorlevel 0 (
    echo [ОК] Проверка и обновление конфигурации завершено.
) else (
    echo [ПРЕДУПРЕЖДЕНИЕ] Скрипт проверки вернул ошибку, но продолжим запуск.
)


:: --- 4. ЗАПУСК ПРИЛОЖЕНИЯ ---

:END
echo.
echo [4/4] Запуск каталога...
:: Явно запускаем main_app.py с помощью python, отсоединяя процесс от окна батника
start "" python main_app.py
goto :EOF


:: --- РАЗДЕЛ: PYTHON НЕ НАЙДЕН ---

:INSTALL_PYTHON
echo.
echo [ВНИМАНИЕ] Python не найден в вашей системе.
echo Для работы TqG Launcher требуется Python 3.
echo.

:ASK_INSTALL
set /p ANSWER="Вы хотите получить ссылку для установки Python? (Y/N): "
if /i "%ANSWER%"=="Y" (
    echo.
    echo Открываем ссылку на загрузку Python (https://www.python.org/downloads/windows/).
    echo Пожалуйста, во время установки ОБЯЗАТЕЛЬНО отметьте "Add Python to PATH"!
    start "" "https://www.python.org/downloads/windows/"
    echo.
    echo После установки перезапустите этот файл.
    pause
    goto :EOF
) else if /i "%ANSWER%"=="N" (
    echo.
    echo Установка отменена. Приложение не может быть запущено.
    pause
    goto :EOF
) else (
    echo Некорректный ввод. Пожалуйста, введите Y или N.
    goto :ASK_INSTALL
)

:EOF
endlocal