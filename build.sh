#!/bin/bash

# Docker镜像构建脚本（仅本地构建，不推送）
# 使用方法: ./build.sh
# 在 Windows 上使用 Git Bash 或 WSL 运行: bash build.sh

# 确保输出不被缓冲，所有错误信息可见
export PYTHONUNBUFFERED=1
# 确保错误输出也显示在终端
exec 2>&1

# 调试信息：显示脚本开始执行
echo "[DEBUG] 脚本开始执行..."
echo "[DEBUG] 当前目录: $(pwd)"
echo "[DEBUG] 当前用户: $(whoami)"
echo ""

# 配置镜像仓库（请根据实际情况修改）
# 阿里云ACR配置
REGISTRY="crpi-mql7znw3gpm4caw8.cn-beijing.personal.cr.aliyuncs.com"  # 你的ACR公网地址
NAMESPACE="aichatbotesp32"  # 替换为你的命名空间名称（在ACR控制台查看，例如：xiaozhi）
USERNAME="nick0416011493"  # 替换为你的用户名（用于登录）
# 如果使用Docker Hub或其他不需要命名空间的仓库，将NAMESPACE设为空字符串 ""
# 例如：NAMESPACE=""

# 构建镜像前缀
if [ -n "$NAMESPACE" ]; then
    IMAGE_PREFIX="${REGISTRY}/${NAMESPACE}/xiaozhi-esp32-server"
else
    IMAGE_PREFIX="${REGISTRY}/${USERNAME}/xiaozhi-esp32-server"
fi

# 颜色输出
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  小智服务端 Docker镜像构建脚本${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""

# 检查Docker是否运行
if ! command -v docker > /dev/null 2>&1; then
    echo -e "${RED}错误: 未找到 Docker 命令，请先安装 Docker${NC}"
    exit 1
fi
if ! docker info > /dev/null 2>&1; then
    echo -e "${RED}错误: Docker未运行，请先启动Docker${NC}"
    exit 1
fi

# 检查是否在项目根目录
if [ ! -f "Dockerfile-server-base" ] || [ ! -f "Dockerfile-server" ] || [ ! -f "Dockerfile-web" ]; then
    echo -e "${RED}错误: 请在项目根目录执行此脚本${NC}"
    echo -e "${RED}当前目录: $(pwd)${NC}"
    echo -e "${RED}缺少文件: Dockerfile-server-base, Dockerfile-server 或 Dockerfile-web${NC}"
    exit 1
fi

# 提示用户配置信息
echo -e "${YELLOW}当前配置:${NC}"
echo "  镜像仓库: ${REGISTRY}"
if [ -n "$NAMESPACE" ]; then
    echo "  命名空间: ${NAMESPACE}"
fi
echo "  用户名: ${USERNAME}"
echo "  镜像前缀: ${IMAGE_PREFIX}"
echo ""

# 检查是否在交互式环境中，或者是否设置了跳过确认的环境变量
if [ -t 0 ] && [ -z "$SKIP_CONFIRM" ]; then
    read -p "是否使用以上配置? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "请编辑脚本修改 REGISTRY、NAMESPACE 和 USERNAME 变量"
        exit 1
    fi
else
    echo -e "${YELLOW}非交互式环境，自动使用以上配置${NC}"
    echo ""
fi

echo -e "${YELLOW}说明: 本脚本现在只负责构建本地镜像，不会执行登录和推送操作。${NC}"

# 构建基础镜像
echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${YELLOW}步骤1/5: 构建基础镜像...${NC}"
echo -e "${GREEN}========================================${NC}"
echo "开始构建基础镜像..."
if ! docker build -f Dockerfile-server-base -t ${IMAGE_PREFIX}:server-base . 2>&1; then
    echo ""
    echo -e "${RED}========================================${NC}"
    echo -e "${RED}基础镜像构建失败！${NC}"
    echo -e "${RED}========================================${NC}"
    exit 1
fi
echo -e "${GREEN}✓ 基础镜像构建成功${NC}"

# 构建服务端镜像
echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${YELLOW}步骤2/5: 构建服务端镜像...${NC}"
echo -e "${GREEN}========================================${NC}"
echo "开始构建服务端镜像..."
if ! docker build -f Dockerfile-server -t ${IMAGE_PREFIX}:server_latest . 2>&1; then
    echo ""
    echo -e "${RED}========================================${NC}"
    echo -e "${RED}服务端镜像构建失败！${NC}"
    echo -e "${RED}========================================${NC}"
    exit 1
fi
echo -e "${GREEN}✓ 服务端镜像构建成功${NC}"

# 构建Web镜像
echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${YELLOW}步骤3/5: 构建Web镜像...${NC}"
echo -e "${GREEN}========================================${NC}"
echo "开始构建Web镜像..."
if ! docker build -f Dockerfile-web -t ${IMAGE_PREFIX}:web_latest . 2>&1; then
    echo ""
    echo -e "${RED}========================================${NC}"
    echo -e "${RED}Web镜像构建失败！${NC}"
    echo -e "${RED}========================================${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Web镜像构建成功${NC}"

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}所有镜像已在本地构建完成（未推送）！${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo -e "${YELLOW}如需手动推送，可执行:${NC}"
echo "  docker push ${IMAGE_PREFIX}:server-base"
echo "  docker push ${IMAGE_PREFIX}:server_latest"
echo "  docker push ${IMAGE_PREFIX}:web_latest"

echo ""
echo -e "${GREEN}构建流程结束！${NC}"
