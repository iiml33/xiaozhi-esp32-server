#!/bin/bash

# Docker镜像构建和推送脚本
# 使用方法: ./build-and-push.sh

# 配置镜像仓库（请根据实际情况修改）
# 阿里云ACR配置
REGISTRY="crpi-mql7znw3gpm4caw8.cn-beijing.personal.cr.aliyuncs.com"  # 你的ACR公网地址
NAMESPACE="aichatbotesp32"  # 替换为你的命名空间名称（在ACR控制台查看，例如：xiaozhi）
USERNAME="LTAI5t8JLqqiJvm7T69M28b6"  # 替换为你的AccessKey ID（用于登录）
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
if ! docker info > /dev/null 2>&1; then
    echo -e "${RED}错误: Docker未运行，请先启动Docker${NC}"
    exit 1
fi

# 检查是否在项目根目录
if [ ! -f "Dockerfile-server-base" ] || [ ! -f "Dockerfile-server" ] || [ ! -f "Dockerfile-web" ]; then
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

# 检查并提示登录
echo -e "${YELLOW}准备登录镜像仓库...${NC}"

# 根据不同的仓库类型显示不同的登录说明
if [[ "$REGISTRY" == *"aliyuncs.com"* ]]; then
    echo -e "${YELLOW}阿里云ACR登录说明:${NC}"
    echo "  登录命令: docker login ${REGISTRY} -u ${USERNAME}"
    echo ""
    echo -e "${YELLOW}获取登录凭证的方法:${NC}"
    echo "  1. 访问: https://cr.console.aliyun.com/"
    echo "  2. 点击右上角头像 -> AccessKey管理"
    echo "  3. 创建AccessKey（如果还没有）"
    echo "  4. 使用AccessKey ID作为用户名，AccessKey Secret作为密码"
    echo ""
    read -p "是否现在登录? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        read -sp "请输入AccessKey Secret（密码）: " password
        echo
        docker login ${REGISTRY} -u ${USERNAME} -p ${password} || {
            echo -e "${RED}登录失败，请检查用户名和密码${NC}"
            echo -e "${YELLOW}提示: 如果登录失败，可以手动执行: docker login ${REGISTRY} -u ${USERNAME}${NC}"
            exit 1
        }
        echo -e "${GREEN}登录成功！${NC}"
    else
        echo -e "${YELLOW}已跳过登录，如果后续推送失败，请先手动登录${NC}"
    fi
elif [ "$REGISTRY" = "ghcr.io" ]; then
    echo "  echo \$GITHUB_TOKEN | docker login ghcr.io -u $USERNAME --password-stdin"
    read -p "是否现在登录? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        read -sp "请输入GitHub Token: " token
        echo
        echo $token | docker login ghcr.io -u $USERNAME --password-stdin || {
            echo -e "${RED}登录失败${NC}"
            exit 1
        }
    fi
elif [ "$REGISTRY" = "ccr.ccs.tencentyun.com" ]; then
    echo "  docker login ccr.ccs.tencentyun.com -u $USERNAME -p \$PASSWORD"
    read -p "是否现在登录? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        read -sp "请输入密码: " password
        echo
        docker login ccr.ccs.tencentyun.com -u $USERNAME -p $password || {
            echo -e "${RED}登录失败${NC}"
            exit 1
        }
    fi
else
    echo "  登录命令: docker login"
    read -p "是否现在登录? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        docker login || {
            echo -e "${RED}登录失败${NC}"
            exit 1
        }
    fi
fi

# 构建基础镜像
echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${YELLOW}步骤1/5: 构建基础镜像...${NC}"
echo -e "${GREEN}========================================${NC}"
docker build -f Dockerfile-server-base -t ${IMAGE_PREFIX}:server-base . || {
    echo -e "${RED}基础镜像构建失败${NC}"
    exit 1
}
echo -e "${GREEN}✓ 基础镜像构建成功${NC}"

# 构建服务端镜像
echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${YELLOW}步骤2/5: 构建服务端镜像...${NC}"
echo -e "${GREEN}========================================${NC}"
docker build -f Dockerfile-server -t ${IMAGE_PREFIX}:server_latest . || {
    echo -e "${RED}服务端镜像构建失败${NC}"
    exit 1
}
echo -e "${GREEN}✓ 服务端镜像构建成功${NC}"

# 构建Web镜像
echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${YELLOW}步骤3/5: 构建Web镜像...${NC}"
echo -e "${GREEN}========================================${NC}"
docker build -f Dockerfile-web -t ${IMAGE_PREFIX}:web_latest . || {
    echo -e "${RED}Web镜像构建失败${NC}"
    exit 1
}
echo -e "${GREEN}✓ Web镜像构建成功${NC}"

# 询问是否推送
echo ""
echo -e "${GREEN}========================================${NC}"
read -p "是否推送镜像到仓库? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 推送基础镜像
    echo ""
    echo -e "${GREEN}========================================${NC}"
    echo -e "${YELLOW}步骤4/5: 推送基础镜像...${NC}"
    echo -e "${GREEN}========================================${NC}"
    docker push ${IMAGE_PREFIX}:server-base || {
        echo -e "${RED}基础镜像推送失败${NC}"
        exit 1
    }
    echo -e "${GREEN}✓ 基础镜像推送成功${NC}"
    
    # 推送服务端镜像
    echo ""
    echo -e "${GREEN}========================================${NC}"
    echo -e "${YELLOW}步骤5/5: 推送服务端镜像...${NC}"
    echo -e "${GREEN}========================================${NC}"
    docker push ${IMAGE_PREFIX}:server_latest || {
        echo -e "${RED}服务端镜像推送失败${NC}"
        exit 1
    }
    echo -e "${GREEN}✓ 服务端镜像推送成功${NC}"
    
    # 推送Web镜像
    echo ""
    echo -e "${GREEN}========================================${NC}"
    echo -e "${YELLOW}推送Web镜像...${NC}"
    echo -e "${GREEN}========================================${NC}"
    docker push ${IMAGE_PREFIX}:web_latest || {
        echo -e "${RED}Web镜像推送失败${NC}"
        exit 1
    }
    echo -e "${GREEN}✓ Web镜像推送成功${NC}"
    
    echo ""
    echo -e "${GREEN}========================================${NC}"
    echo -e "${GREEN}所有镜像已成功推送！${NC}"
    echo -e "${GREEN}========================================${NC}"
    echo ""
    echo -e "${YELLOW}镜像地址:${NC}"
    echo "  - ${IMAGE_PREFIX}:server-base"
    echo "  - ${IMAGE_PREFIX}:server_latest"
    echo "  - ${IMAGE_PREFIX}:web_latest"
    echo ""
    echo -e "${YELLOW}请在部署脚本中修改以下镜像地址:${NC}"
    echo "  ghcr.nju.edu.cn/xinnan-tech/xiaozhi-esp32-server:server_latest"
    echo "  替换为: ${IMAGE_PREFIX}:server_latest"
    echo ""
    echo "  ghcr.nju.edu.cn/xinnan-tech/xiaozhi-esp32-server:web_latest"
    echo "  替换为: ${IMAGE_PREFIX}:web_latest"
else
    echo "已跳过推送步骤"
    echo -e "${YELLOW}镜像已构建但未推送，可以稍后手动推送:${NC}"
    echo "  docker push ${IMAGE_PREFIX}:server-base"
    echo "  docker push ${IMAGE_PREFIX}:server_latest"
    echo "  docker push ${IMAGE_PREFIX}:web_latest"
fi

echo ""
echo -e "${GREEN}构建完成！${NC}"

