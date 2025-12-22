# Docker镜像构建和推送指南

## 前置要求

1. 已安装Docker和Docker Compose
2. 已注册镜像仓库账号（推荐选项见下方）
3. 已登录到对应的镜像仓库

## 镜像仓库选择

### 选项1：Docker Hub（推荐，全球可用）
- 地址：https://hub.docker.com
- 优点：全球CDN，速度快，免费
- 注册：https://hub.docker.com/signup
- 登录命令：`docker login`

### 选项2：GitHub Container Registry（推荐，免费）
- 地址：https://github.com/features/packages
- 优点：与GitHub集成，免费，私有仓库免费
- 使用：需要GitHub账号
- 登录命令：`echo $GITHUB_TOKEN | docker login ghcr.io -u USERNAME --password-stdin`

### 选项3：腾讯云容器镜像服务（国内推荐）
- 地址：https://console.cloud.tencent.com/tcr
- 优点：国内速度快，免费额度充足
- 注册：需要腾讯云账号
- 登录命令：`docker login ccr.ccs.tencentyun.com -u USERNAME -p PASSWORD`

## 构建步骤

### 步骤1：设置镜像仓库变量

根据你选择的镜像仓库，设置以下变量：

```bash
# Docker Hub
export REGISTRY="docker.io"
export USERNAME="your-dockerhub-username"
export IMAGE_PREFIX="${USERNAME}/xiaozhi-esp32-server"

# 或 GitHub Container Registry
export REGISTRY="ghcr.io"
export USERNAME="your-github-username"
export IMAGE_PREFIX="${REGISTRY}/${USERNAME}/xiaozhi-esp32-server"

# 或 腾讯云容器镜像服务
export REGISTRY="ccr.ccs.tencentyun.com"
export USERNAME="your-tencent-namespace"
export IMAGE_PREFIX="${REGISTRY}/${USERNAME}/xiaozhi-esp32-server"
```

### 步骤2：登录镜像仓库

```bash
# Docker Hub
docker login

# GitHub Container Registry
echo $GITHUB_TOKEN | docker login ghcr.io -u $USERNAME --password-stdin

# 腾讯云
docker login ccr.ccs.tencentyun.com -u $USERNAME -p $PASSWORD
```

### 步骤3：构建基础镜像

```bash
# 在项目根目录执行
docker build -f Dockerfile-server-base -t ${IMAGE_PREFIX}:server-base .
```

### 步骤4：构建服务端镜像

```bash
# 构建服务端镜像（依赖基础镜像）
docker build -f Dockerfile-server -t ${IMAGE_PREFIX}:server_latest .
```

### 步骤5：构建Web镜像

```bash
# 构建Web镜像（包含前端和后端）
docker build -f Dockerfile-web -t ${IMAGE_PREFIX}:web_latest .
```

### 步骤6：推送镜像到仓库

```bash
# 推送基础镜像
docker push ${IMAGE_PREFIX}:server-base

# 推送服务端镜像
docker push ${IMAGE_PREFIX}:server_latest

# 推送Web镜像
docker push ${IMAGE_PREFIX}:web_latest
```

## 一键构建脚本

创建 `build-and-push.sh` 脚本：

```bash
#!/bin/bash

# 配置镜像仓库（请根据实际情况修改）
REGISTRY="docker.io"  # 或 "ghcr.io" 或 "ccr.ccs.tencentyun.com"
USERNAME="your-username"  # 替换为你的用户名
IMAGE_PREFIX="${REGISTRY}/${USERNAME}/xiaozhi-esp32-server"

# 颜色输出
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}开始构建Docker镜像...${NC}"

# 检查Docker是否运行
if ! docker info > /dev/null 2>&1; then
    echo "错误: Docker未运行，请先启动Docker"
    exit 1
fi

# 构建基础镜像
echo -e "${YELLOW}步骤1/5: 构建基础镜像...${NC}"
docker build -f Dockerfile-server-base -t ${IMAGE_PREFIX}:server-base . || {
    echo "基础镜像构建失败"
    exit 1
}

# 构建服务端镜像
echo -e "${YELLOW}步骤2/5: 构建服务端镜像...${NC}"
docker build -f Dockerfile-server -t ${IMAGE_PREFIX}:server_latest . || {
    echo "服务端镜像构建失败"
    exit 1
}

# 构建Web镜像
echo -e "${YELLOW}步骤3/5: 构建Web镜像...${NC}"
docker build -f Dockerfile-web -t ${IMAGE_PREFIX}:web_latest . || {
    echo "Web镜像构建失败"
    exit 1
}

# 询问是否推送
read -p "是否推送镜像到仓库? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${YELLOW}步骤4/5: 推送基础镜像...${NC}"
    docker push ${IMAGE_PREFIX}:server-base || {
        echo "基础镜像推送失败"
        exit 1
    }
    
    echo -e "${YELLOW}步骤5/5: 推送服务端镜像...${NC}"
    docker push ${IMAGE_PREFIX}:server_latest || {
        echo "服务端镜像推送失败"
        exit 1
    }
    
    echo -e "${YELLOW}推送Web镜像...${NC}"
    docker push ${IMAGE_PREFIX}:web_latest || {
        echo "Web镜像推送失败"
        exit 1
    }
    
    echo -e "${GREEN}所有镜像已成功推送！${NC}"
    echo -e "${GREEN}镜像地址:${NC}"
    echo "  - ${IMAGE_PREFIX}:server-base"
    echo "  - ${IMAGE_PREFIX}:server_latest"
    echo "  - ${IMAGE_PREFIX}:web_latest"
else
    echo "已跳过推送步骤"
fi

echo -e "${GREEN}构建完成！${NC}"
```

使用脚本：

```bash
chmod +x build-and-push.sh
./build-and-push.sh
```

## 修改部署脚本

修改你的部署脚本，将镜像地址替换为你自己的镜像：

```bash
# 在脚本中找到以下行并替换：
# 原镜像地址：
# ghcr.nju.edu.cn/xinnan-tech/xiaozhi-esp32-server:server_latest
# ghcr.nju.edu.cn/xinnan-tech/xiaozhi-esp32-server:web_latest

# 替换为你的镜像地址（示例）：
# docker.io/your-username/xiaozhi-esp32-server:server_latest
# docker.io/your-username/xiaozhi-esp32-server:web_latest
```

## 修改docker-compose_all.yml

在 `main/xiaozhi-server/docker-compose_all.yml` 中修改镜像地址：

```yaml
services:
  xiaozhi-esp32-server:
    image: docker.io/your-username/xiaozhi-esp32-server:server_latest  # 修改这里
    # ... 其他配置保持不变

  xiaozhi-esp32-server-web:
    image: docker.io/your-username/xiaozhi-esp32-server:web_latest  # 修改这里
    # ... 其他配置保持不变
```

## 使用GitHub Actions自动构建（可选）

如果使用GitHub，可以创建 `.github/workflows/docker-build.yml`：

```yaml
name: Build and Push Docker Images

on:
  push:
    branches: [ main ]
    tags:
      - 'v*'

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v2
      
      - name: Login to Docker Hub
        uses: docker/login-action@v2
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_PASSWORD }}
      
      - name: Build and push base image
        uses: docker/build-push-action@v4
        with:
          context: .
          file: ./Dockerfile-server-base
          push: true
          tags: ${{ secrets.DOCKER_USERNAME }}/xiaozhi-esp32-server:server-base
      
      - name: Build and push server image
        uses: docker/build-push-action@v4
        with:
          context: .
          file: ./Dockerfile-server
          push: true
          tags: ${{ secrets.DOCKER_USERNAME }}/xiaozhi-esp32-server:server_latest
      
      - name: Build and push web image
        uses: docker/build-push-action@v4
        with:
          context: .
          file: ./Dockerfile-web
          push: true
          tags: ${{ secrets.DOCKER_USERNAME }}/xiaozhi-esp32-server:web_latest
```

## 常见问题

### Q1: 构建时网络慢怎么办？

**解决方案：**
1. 使用国内镜像源（已在Dockerfile中配置）
2. 使用代理：`export HTTP_PROXY=http://proxy:port`
3. 使用腾讯云等国内镜像仓库

### Q2: 推送时提示权限不足？

**解决方案：**
1. 确保已登录：`docker login`
2. 检查镜像名称格式是否正确
3. 确保有推送权限

### Q3: 如何更新镜像？

**解决方案：**
1. 重新构建镜像
2. 推送新版本
3. 在服务器上执行：`docker-compose pull && docker-compose up -d`

## 验证镜像

推送后，可以通过以下方式验证：

```bash
# 查看镜像列表
docker images | grep xiaozhi-esp32-server

# 测试运行
docker run --rm ${IMAGE_PREFIX}:server_latest --help

# 从仓库拉取测试
docker pull ${IMAGE_PREFIX}:server_latest
```

## 下一步

1. 修改部署脚本中的镜像地址
2. 在阿里云服务器上运行部署脚本
3. 验证服务是否正常运行

