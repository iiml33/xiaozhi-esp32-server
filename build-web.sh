#!/bin/bash

# Docker镜像构建脚本（仅本地构建 web，不推送）
# 使用方法: ./build-web.sh

# 确保输出不被缓冲，所有错误信息可见
export PYTHONUNBUFFERED=1
# 确保错误输出也显示在终端
exec 2>&1

# 配置镜像仓库（请根据实际情况修改）
# 阿里云ACR配置（如果只是本地测试，其实不强依赖这些变量）
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
echo -e "${GREEN}  小智服务端 Web Docker镜像构建脚本${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""

# 检查Docker是否运行
if ! docker info > /dev/null 2>&1; then
    echo -e "${RED}错误: Docker未运行，请先启动Docker${NC}"
    exit 1
fi

# 检查是否在项目根目录
if [ ! -f "Dockerfile-web" ]; then
    echo -e "${RED}错误: 请在项目根目录执行此脚本${NC}"
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
read -p "是否使用以上配置? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "请编辑脚本修改 REGISTRY、NAMESPACE 和 USERNAME 变量"
    exit 1
fi

echo -e "${YELLOW}说明: 本脚本现在只负责本地构建 web 镜像，不会执行登录和推送操作。${NC}"

# 构建Web镜像（前端 + Java 后端）
echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${YELLOW}步骤1/1: 构建Web镜像...${NC}"
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
echo -e "${GREEN}web 镜像已在本地构建完成（未推送）！${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""

echo -e "${GREEN}构建流程结束！${NC}"

