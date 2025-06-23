@echo off
SETLOCAL

:: Check for administrative privileges
NET SESSION >NUL 2>&1
IF %ERRORLEVEL% NEQ 0 (
    ECHO This script requires administrative privileges. Please run as administrator.
    PAUSE
    EXIT /B 1
)

ECHO.=====================================================
ECHO.           YouTube到B站智能体 - Windows安装脚本
ECHO.=====================================================
ECHO.

:: --- 1. Install Chocolatey (if not already installed) ---
ECHO.1. 检查并安装 Chocolatey...
WHERE choco >NUL 2>&1
IF %ERRORLEVEL% NEQ 0 (
    ECHO Chocolatey 未安装，正在安装...
    powershell.exe -NoProfile -InputFormat None -ExecutionPolicy Bypass -Command "[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString(\'https://community.chocolatey.org/install.ps1\'))"
    IF %ERRORLEVEL% NEQ 0 (
        ECHO Chocolatey 安装失败，请手动安装后重试。
        PAUSE
        EXIT /B 1
    )
    ECHO Chocolatey 安装成功。
) ELSE (
    ECHO Chocolatey 已安装。
)
ECHO.

:: --- 2. Install Python ---
ECHO.2. 安装 Python...
choco install python --version=3.11.9 -y
IF %ERRORLEVEL% NEQ 0 (
    ECHO Python 安装失败，请检查。
    PAUSE
    EXIT /B 1
)
ECHO Python 安装成功。
ECHO.

:: --- 3. Install Node.js ---
ECHO.3. 安装 Node.js...
choco install nodejs-lts -y
IF %ERRORLEVEL% NEQ 0 (
    ECHO Node.js 安装失败，请检查。
    PAUSE
    EXIT /B 1
)
ECHO Node.js 安装成功。
ECHO.

:: --- 4. Install FFmpeg ---
ECHO.4. 安装 FFmpeg...
choco install ffmpeg -y
IF %ERRORLEVEL% NEQ 0 (
    ECHO FFmpeg 安装失败，请检查。
    PAUSE
    EXIT /B 1
)
ECHO FFmpeg 安装成功。
ECHO.

:: --- 5. Install yt-dlp ---
ECHO.5. 安装 yt-dlp...
choco install yt-dlp -y
IF %ERRORLEVEL% NEQ 0 (
    ECHO yt-dlp 安装失败，请检查。
    PAUSE
    EXIT /B 1
)
ECHO yt-dlp 安装成功。
ECHO.

:: --- 6. Install Python dependencies ---
ECHO.6. 安装 Python 依赖...
pip install -r requirements.txt
IF %ERRORLEVEL% NEQ 0 (
    ECHO Python 依赖安装失败，请检查。
    PAUSE
    EXIT /B 1
)
ECHO Python 依赖安装成功。
ECHO.

:: --- 7. Install Node.js dependencies ---
ECHO.7. 安装 Node.js 依赖...
cd youtube-bilibili-agent
npm install
IF %ERRORLEVEL% NEQ 0 (
    ECHO Node.js 依赖安装失败，请检查。
    PAUSE
    EXIT /B 1
)
ECHO Node.js 依赖安装成功。
cd ..
ECHO.

:: --- 8. ChromeDriver (Manual step, inform user) ---
ECHO.8. ChromeDriver 配置 (手动步骤)
ECHO.   请确保您的Google Chrome浏览器已安装。
ECHO.   1. 检查您Chrome浏览器的版本 (在Chrome浏览器中输入 chrome://version)。
ECHO.   2. 访问 https://chromedriver.chromium.org/downloads 下载与您Chrome浏览器版本对应的ChromeDriver。
ECHO.   3. 将下载的 chromedriver.exe 放到一个系统Path目录中 (例如 C:\Windows)。
ECHO.

ECHO.=====================================================
ECHO.           安装完成！
ECHO.=====================================================
ECHO.
ECHO.请按照上述步骤手动配置ChromeDriver。
ECHO.您现在可以按照使用文档中的说明启动后端和前端服务。
PAUSE


