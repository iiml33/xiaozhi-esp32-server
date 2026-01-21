#!/bin/bash

# 快速推送镜像脚本
# 使用方法: ./push-images.sh

REGISTRY="crpi-mql7znw3gpm4caw8.cn-beijing.personal.cr.aliyuncs.com"
NAMESPACE="aichatbotesp32"
IMAGE_PREFIX="${REGISTRY}/${NAMESPACE}/xiaozhi-esp32-server"

# 颜色输出
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  推送镜像到阿里云 ACR${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""

# 检查登录状态
echo "检查登录状态..."
# 不再隐藏 docker 的错误输出，方便排查问题
if ! docker pull ${REGISTRY}/test:test; then
    echo -e "${YELLOW}未登录或登录已过期，需要先登录${NC}"
    echo ""
    echo "请执行以下命令登录："
    echo "  docker login ${REGISTRY} -u nick0416011493"
    echo ""
    echo "或者使用实例ID登录："
    echo "  docker login ${REGISTRY} -u crpi-mql7znw3gpm4caw8"
    echo ""
    read -p "是否现在登录? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        docker login ${REGISTRY} -u nick0416011493
        if [ $? -ne 0 ]; then
            echo -e "${RED}登录失败，请手动登录后重新运行此脚本${NC}"
            exit 1
        fi
    else
        echo "请先登录后再运行此脚本"
        exit 1
    fi
fi

echo -e "${GREEN}登录状态正常${NC}"
echo ""

# 定义一个函数：如果镜像存在则推送，不存在就跳过
push_if_exists() {
  local TAG="$1"
  if docker image inspect "${IMAGE_PREFIX}:${TAG}" > /dev/null 2>&1; then
    echo -e "${YELLOW}正在推送镜像: ${IMAGE_PREFIX}:${TAG} ...${NC}"
    if docker push "${IMAGE_PREFIX}:${TAG}"; then
      echo -e "${GREEN}✓ 镜像推送成功: ${IMAGE_PREFIX}:${TAG}${NC}"
    else
      echo -e "${RED}✗ 镜像推送失败: ${IMAGE_PREFIX}:${TAG}${NC}"
      exit 1
    fi
    echo ""
  else
    echo -e "${YELLOW}跳过: 本地未找到镜像 ${IMAGE_PREFIX}:${TAG}，不推送${NC}"
    echo ""
  fi
}

# 按顺序尝试推送三种镜像（不存在的会自动跳过）
push_if_exists "server-base"
push_if_exists "server_latest"
push_if_exists "web_latest"

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}镜像推送流程完成！${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo "镜像地址："
echo "  - ${IMAGE_PREFIX}:server-base   (如本地存在)"
echo "  - ${IMAGE_PREFIX}:server_latest (如本地存在)"
echo "  - ${IMAGE_PREFIX}:web_latest    (如本地存在)"
echo ""

