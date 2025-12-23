# Simple Docker Image Test Script
param(
    [string]$ImageName = "crpi-mql7znw3gpm4caw8.cn-beijing.personal.cr.aliyuncs.com/aichatbotesp32/xiaozhi-esp32-server:web_latest"
)

Write-Host "Testing Docker Image: $ImageName" -ForegroundColor Cyan
Write-Host ""

# Test 1: Check if image exists
Write-Host "[1] Checking if image exists..." -ForegroundColor Yellow
$img = docker images $ImageName --format "{{.Repository}}:{{.Tag}}" 2>$null
if ($img) {
    Write-Host "[OK] Image found" -ForegroundColor Green
} else {
    Write-Host "[FAIL] Image not found" -ForegroundColor Red
    exit 1
}

# Test 2: Check /start.sh exists
Write-Host "[2] Checking /start.sh file..." -ForegroundColor Yellow
$result = docker run --rm $ImageName ls -l /start.sh 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "[OK] /start.sh exists" -ForegroundColor Green
    Write-Host "File info: $result" -ForegroundColor Gray
} else {
    Write-Host "[FAIL] /start.sh not found" -ForegroundColor Red
}

# Test 3: Check file permissions
Write-Host "[3] Checking file permissions..." -ForegroundColor Yellow
$perm = docker run --rm $ImageName ls -l /start.sh 2>&1
if ($perm -match "-rwx") {
    Write-Host "[OK] File has execute permission" -ForegroundColor Green
} else {
    Write-Host "[WARN] File may not have execute permission" -ForegroundColor Yellow
}

# Test 4: Check first line (shebang)
Write-Host "[4] Checking shebang line..." -ForegroundColor Yellow
$first = docker run --rm $ImageName head -c 20 /start.sh 2>&1
if ($first -match "#!/bin/bash") {
    Write-Host "[OK] Shebang is correct: $first" -ForegroundColor Green
} else {
    Write-Host "[WARN] Shebang may be wrong: $first" -ForegroundColor Yellow
}

# Test 5: Try to run container
Write-Host "[5] Testing container startup..." -ForegroundColor Yellow
$testName = "test-$(Get-Random)"
docker run -d --name $testName $ImageName 2>&1 | Out-Null
Start-Sleep -Seconds 2
$status = docker inspect $testName --format '{{.State.Status}}' 2>$null
if ($status -eq "running") {
    Write-Host "[OK] Container is running" -ForegroundColor Green
    Write-Host "Logs:" -ForegroundColor Gray
    docker logs --tail=5 $testName 2>&1
} else {
    Write-Host "[FAIL] Container status: $status" -ForegroundColor Red
    Write-Host "Logs:" -ForegroundColor Red
    docker logs $testName 2>&1
}
docker stop $testName 2>&1 | Out-Null
docker rm $testName 2>&1 | Out-Null

Write-Host ""
Write-Host "Test completed!" -ForegroundColor Cyan

