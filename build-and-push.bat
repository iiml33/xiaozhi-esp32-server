@echo off
chcp 65001 >nul 2>&1
REM Docker Image Build and Push Script (Windows Version)
REM Usage: build-and-push.bat

REM 配置镜像仓库（请根据实际情况修改）
set REGISTRY=crpi-mql7znw3gpm4caw8.cn-beijing.personal.cr.aliyuncs.com
set NAMESPACE=aichatbotesp32
set USERNAME=nick0416011493

REM 构建镜像前缀
if "%NAMESPACE%"=="" (
    set IMAGE_PREFIX=%REGISTRY%/%USERNAME%/xiaozhi-esp32-server
) else (
    set IMAGE_PREFIX=%REGISTRY%/%NAMESPACE%/xiaozhi-esp32-server
)

echo ========================================
echo   Xiaozhi Server Docker Image Build Script
echo ========================================
echo.

REM Check if Docker is running
echo Checking Docker status...
docker info >nul 2>&1
if errorlevel 1 (
    echo.
    echo ========================================
    echo ERROR: Docker is not running
    echo ========================================
    echo.
    echo Please follow these steps:
    echo 1. Start "Docker Desktop" from Start Menu
    echo 2. Wait for Docker Desktop to fully start (system tray icon turns green)
    echo 3. Then run this script again
    echo.
    echo Or run this command to start Docker Desktop:
    echo    Start-Process "C:\Program Files\Docker\Docker\Docker Desktop.exe"
    echo.
    set /p START_DOCKER="Start Docker Desktop now? (y/n): "
    if /i "%START_DOCKER%"=="y" (
        echo Starting Docker Desktop...
        if exist "C:\Program Files\Docker\Docker\Docker Desktop.exe" (
            start "" "C:\Program Files\Docker\Docker\Docker Desktop.exe"
        ) else if exist "%LOCALAPPDATA%\Docker\Docker Desktop.exe" (
            start "" "%LOCALAPPDATA%\Docker\Docker Desktop.exe"
        ) else (
            echo ERROR: Cannot find Docker Desktop.exe
            echo Please start Docker Desktop manually from Start Menu
            exit /b 1
        )
        echo.
        echo Docker Desktop is starting, please wait 1-2 minutes...
        echo Waiting for Docker to be ready...
        timeout /t 10 >nul
        
        REM Wait for Docker to be ready (max 2 minutes)
        setlocal enabledelayedexpansion
        set WAIT_COUNT=0
        :WAIT_LOOP
        docker info >nul 2>&1
        if not errorlevel 1 (
            echo Docker is ready!
            endlocal
            goto DOCKER_READY
        )
        set /a WAIT_COUNT+=1
        if !WAIT_COUNT! GEQ 24 (
            echo.
            echo Docker Desktop is taking longer than expected to start.
            echo Please wait a bit more and run this script again.
            endlocal
            exit /b 1
        )
        echo Waiting... (!WAIT_COUNT! of 24)
        timeout /t 5 >nul
        goto WAIT_LOOP
        
        :DOCKER_READY
        endlocal
        echo.
        echo Docker is ready! Continuing with build...
        echo.
        goto :SKIP_DOCKER_CHECK
    ) else (
        exit /b 1
    )
)
:SKIP_DOCKER_CHECK
echo Docker is running

REM Check if in project root directory
if not exist "Dockerfile-server-base" (
    echo ERROR: Please run this script in the project root directory
    exit /b 1
)
if not exist "Dockerfile-server" (
    echo ERROR: Please run this script in the project root directory
    exit /b 1
)
if not exist "Dockerfile-web" (
    echo ERROR: Please run this script in the project root directory
    exit /b 1
)

REM Display configuration
echo Current configuration:
echo   Registry: %REGISTRY%
if not "%NAMESPACE%"=="" (
    echo   Namespace: %NAMESPACE%
)
echo   Username: %USERNAME%
echo   Image prefix: %IMAGE_PREFIX%
echo.
set /p CONFIRM="Use above configuration? (y/n): "
if /i not "%CONFIRM%"=="y" (
    echo Please edit the script to modify REGISTRY, NAMESPACE and USERNAME variables
    exit /b 1
)

REM Prompt for login
echo.
echo Preparing to login to image registry...
echo.
echo Aliyun ACR Login Instructions:
echo   Login command: docker login %REGISTRY% -u %USERNAME%
echo.
echo How to get login credentials:
echo   1. Visit: https://cr.console.aliyun.com/
echo   2. Click avatar in top right -^> AccessKey Management
echo   3. Create AccessKey (if you don't have one)
echo   4. Use AccessKey ID as username, AccessKey Secret as password
echo.
echo Alternative: Use temporary login password from ACR console
echo   - Go to ACR console -^> Access Credentials
echo   - Copy temporary password and use it
echo.
set /p LOGIN="Login now? (y/n): "
if /i "%LOGIN%"=="y" (
    echo.
    echo Note: Use Fixed Password (固定密码) from ACR console
    echo   - Go to: https://cr.console.aliyun.com/
    echo   - Instance -^> Access Credentials -^> Fixed Password
    echo.
    set /p PASSWORD="Enter Fixed Password (固定密码): "
    echo %PASSWORD% | docker login --username=%USERNAME% %REGISTRY% --password-stdin
    if errorlevel 1 (
        echo.
        echo ========================================
        echo Login failed!
        echo ========================================
        echo.
        echo Troubleshooting:
        echo 1. Check if AccessKey ID and Secret are correct
        echo 2. Try using temporary login password from ACR console
        echo 3. Try using instance ID as username: crpi-mql7znw3gpm4caw8
        echo 4. Check AccessKey permissions in RAM console
        echo.
        echo Manual login command:
        echo   docker login --username=%USERNAME% %REGISTRY%
        echo.
        set /p RETRY="Try again? (y/n): "
        if /i "%RETRY%"=="y" (
            set /p PASSWORD2="Enter Fixed Password again: "
            echo %PASSWORD2% | docker login --username=%USERNAME% %REGISTRY% --password-stdin
            if errorlevel 1 (
                echo Login failed again. Please check credentials and try manually.
                exit /b 1
            )
            echo Login successful!
        ) else (
            echo Login skipped. You can login manually later.
            echo Command: docker login --username=%USERNAME% %REGISTRY%
        )
    ) else (
        echo Login successful!
    )
) else (
    echo Login skipped. If push fails later, please login manually first.
)

REM Build base image
echo.
echo ========================================
echo Step 1/5: Building base image...
echo ========================================
docker build -f Dockerfile-server-base -t %IMAGE_PREFIX%:server-base .
if errorlevel 1 (
    echo Base image build failed
    exit /b 1
)
echo Base image build successful

REM Build server image
echo.
echo ========================================
echo Step 2/5: Building server image...
echo ========================================
docker build -f Dockerfile-server -t %IMAGE_PREFIX%:server_latest .
if errorlevel 1 (
    echo Server image build failed
    exit /b 1
)
echo Server image build successful

REM Build Web image
echo.
echo ========================================
echo Step 3/5: Building Web image...
echo ========================================
docker build -f Dockerfile-web -t %IMAGE_PREFIX%:web_latest .
if errorlevel 1 (
    echo Web image build failed
    exit /b 1
)
echo Web image build successful

REM Ask if push
echo.
echo ========================================
set /p PUSH="Push images to registry? (y/n): "
if /i "%PUSH%"=="y" (
    REM Check if logged in before pushing
    echo.
    echo Checking login status...
    docker pull %REGISTRY%/test:test >nul 2>&1
    if errorlevel 1 (
        echo.
        echo WARNING: Not logged in or login expired!
        echo You need to login before pushing images.
        echo.
        echo Please login manually:
        echo   docker login --username=%USERNAME% %REGISTRY%
        echo.
        echo Get Fixed Password from ACR console:
        echo   https://cr.console.aliyun.com/ -^> Instance -^> Access Credentials
        echo.
        set /p LOGIN_NOW="Login now? (y/n): "
        if /i "%LOGIN_NOW%"=="y" (
            docker login --username=%USERNAME% %REGISTRY%
            if errorlevel 1 (
                echo Login failed. Please login manually and try pushing again.
                echo.
                echo Get Fixed Password from: https://cr.console.aliyun.com/
                echo Then run: docker login --username=%USERNAME% %REGISTRY%
                echo.
                echo You can push manually later using:
                echo   docker push %IMAGE_PREFIX%:server-base
                echo   docker push %IMAGE_PREFIX%:server_latest
                echo   docker push %IMAGE_PREFIX%:web_latest
                exit /b 1
            )
        ) else (
            echo Push cancelled. Please login first.
            exit /b 1
        )
    )
    REM Push base image
    echo.
    echo ========================================
    echo Step 4/5: Pushing base image...
    echo ========================================
    docker push %IMAGE_PREFIX%:server-base
    if errorlevel 1 (
        echo Base image push failed
        exit /b 1
    )
    echo Base image push successful
    
    REM Push server image
    echo.
    echo ========================================
    echo Step 5/5: Pushing server image...
    echo ========================================
    docker push %IMAGE_PREFIX%:server_latest
    if errorlevel 1 (
        echo Server image push failed
        exit /b 1
    )
    echo Server image push successful
    
    REM Push Web image
    echo.
    echo ========================================
    echo Pushing Web image...
    echo ========================================
    docker push %IMAGE_PREFIX%:web_latest
    if errorlevel 1 (
        echo Web image push failed
        exit /b 1
    )
    echo Web image push successful
    
    echo.
    echo ========================================
    echo All images pushed successfully!
    echo ========================================
    echo.
    echo Image addresses:
    echo   - %IMAGE_PREFIX%:server-base
    echo   - %IMAGE_PREFIX%:server_latest
    echo   - %IMAGE_PREFIX%:web_latest
    echo.
    echo Please update the following image addresses in your deployment script:
    echo   ghcr.nju.edu.cn/xinnan-tech/xiaozhi-esp32-server:server_latest
    echo   Replace with: %IMAGE_PREFIX%:server_latest
    echo.
    echo   ghcr.nju.edu.cn/xinnan-tech/xiaozhi-esp32-server:web_latest
    echo   Replace with: %IMAGE_PREFIX%:web_latest
) else (
    echo Push step skipped
    echo Images are built but not pushed. You can push manually later:
    echo   docker push %IMAGE_PREFIX%:server-base
    echo   docker push %IMAGE_PREFIX%:server_latest
    echo   docker push %IMAGE_PREFIX%:web_latest
)

echo.
echo Build completed!
pause

