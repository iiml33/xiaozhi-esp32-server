# Docker 镜像检验脚本
# 用法: .\test-docker-image.ps1 [镜像名]

param(
    [string]$ImageName = "crpi-mql7znw3gpm4caw8.cn-beijing.personal.cr.aliyuncs.com/aichatbotesp32/xiaozhi-esp32-server:web_latest"
)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   Docker 镜像检验工具" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 检查 Docker 是否运行
Write-Host "[1/6] 检查 Docker 状态..." -ForegroundColor Yellow
$dockerCheck = docker info 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "[OK] Docker 正在运行" -ForegroundColor Green
} else {
    Write-Host "[ERROR] Docker 未运行，请先启动 Docker Desktop" -ForegroundColor Red
    exit 1
}
Write-Host ""

# 检查镜像是否存在
Write-Host "[2/6] 检查镜像是否存在..." -ForegroundColor Yellow
$imageExists = docker images $ImageName --format "{{.Repository}}:{{.Tag}}" 2>$null
if ($imageExists) {
    Write-Host "[OK] 镜像存在: $ImageName" -ForegroundColor Green
} else {
    Write-Host "[ERROR] 镜像不存在: $ImageName" -ForegroundColor Red
    Write-Host "   请先构建镜像: docker build -f Dockerfile-web -t $ImageName ." -ForegroundColor Yellow
    exit 1
}
Write-Host ""

# 检查镜像的启动命令
Write-Host "[3/6] 检查镜像启动命令..." -ForegroundColor Yellow
$inspect = docker inspect $ImageName --format '{{.Config.Cmd}}' 2>$null
if ($inspect -match "start.sh") {
    Write-Host "[OK] 启动命令包含 /start.sh" -ForegroundColor Green
    Write-Host "   启动命令: $inspect" -ForegroundColor Gray
} else {
    Write-Host "[WARN] 启动命令可能不正确: $inspect" -ForegroundColor Yellow
}
Write-Host ""

# 检查 /start.sh 文件是否存在
Write-Host "[4/6] 检查 /start.sh 文件..." -ForegroundColor Yellow
$containerName = "test-image-check-$(Get-Random)"
$null = docker run --rm --name $containerName $ImageName ls -l /start.sh 2>&1
$checkSuccess = $LASTEXITCODE -eq 0

if ($checkSuccess) {
    Write-Host "[OK] /start.sh 文件存在" -ForegroundColor Green
    
    # 检查文件权限
    $fileInfo = docker run --rm $ImageName ls -l /start.sh 2>&1
    if ($fileInfo -match "-rwx") {
        Write-Host "[OK] /start.sh 有执行权限" -ForegroundColor Green
    } else {
        Write-Host "[WARN] /start.sh 可能没有执行权限" -ForegroundColor Yellow
        Write-Host "   文件信息: $fileInfo" -ForegroundColor Gray
    }
    
    # 检查换行符
    Write-Host ""
    Write-Host "   检查换行符..." -ForegroundColor Gray
    $firstLine = docker run --rm $ImageName head -c 20 /start.sh 2>&1
    if ($firstLine -match "#!/bin/bash") {
        Write-Host "[OK] 第一行正确: $firstLine" -ForegroundColor Green
    } else {
        Write-Host "[WARN] 第一行可能有问题: $firstLine" -ForegroundColor Yellow
    }
} else {
    Write-Host "[ERROR] /start.sh 文件不存在！" -ForegroundColor Red
}
Write-Host ""

# 检查其他关键文件
Write-Host "[5/6] 检查其他关键文件..." -ForegroundColor Yellow
$files = @("/app/xiaozhi-esp32-api.jar", "/etc/nginx/nginx.conf", "/usr/share/nginx/html")

foreach ($file in $files) {
    $null = docker run --rm $ImageName test -e $file 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "[OK] $file 存在" -ForegroundColor Green
    } else {
        Write-Host "[ERROR] $file 不存在" -ForegroundColor Red
    }
}
Write-Host ""

# 尝试实际运行容器
Write-Host "[6/6] 尝试启动容器（5秒测试）..." -ForegroundColor Yellow
$testContainer = "test-run-$(Get-Random)"
Write-Host "   启动测试容器: $testContainer" -ForegroundColor Gray

$null = docker run -d --name $testContainer $ImageName 2>&1
Start-Sleep -Seconds 2

$status = docker inspect $testContainer --format '{{.State.Status}}' 2>$null
if ($status -eq "running") {
    Write-Host "[OK] 容器成功启动并运行中" -ForegroundColor Green
    Write-Host ""
    Write-Host "   容器日志（最后10行）:" -ForegroundColor Gray
    docker logs --tail=10 $testContainer 2>&1 | ForEach-Object { Write-Host "   $_" -ForegroundColor Gray }
} elseif ($status -eq "exited") {
    Write-Host "[WARN] 容器已退出" -ForegroundColor Yellow
    $exitCode = docker inspect $testContainer --format '{{.State.ExitCode}}' 2>$null
    Write-Host "   退出码: $exitCode" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "   错误日志:" -ForegroundColor Red
    docker logs $testContainer 2>&1 | ForEach-Object { Write-Host "   $_" -ForegroundColor Red }
} else {
    Write-Host "[WARN] 容器状态: $status" -ForegroundColor Yellow
}

# 清理测试容器
docker stop $testContainer 2>&1 | Out-Null
docker rm $testContainer 2>&1 | Out-Null
Write-Host ""

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   检验完成" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "如果所有检查都通过 [OK]，镜像应该可以正常使用" -ForegroundColor Green
Write-Host "如果有 [ERROR] 或 [WARN]，请检查 Dockerfile 和构建过程" -ForegroundColor Yellow
