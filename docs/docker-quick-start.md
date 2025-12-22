# Docker镜像构建快速指南

## 快速开始（3步完成）

### 步骤1：选择镜像仓库并注册账号

**推荐选项（按优先级）：**

1. **阿里云ACR**（国内推荐，速度快）
   - 注册：https://cr.console.aliyun.com/
   - 个人版免费，国内速度快
   - 登录：`docker login crpi-xxx.cn-beijing.personal.cr.aliyuncs.com -u ACCESS_KEY_ID -p ACCESS_KEY_SECRET`
   - 详细配置：参考 [aliyun-acr-setup.md](./aliyun-acr-setup.md)

2. **Docker Hub**（全球可用）
   - 注册：https://hub.docker.com/signup
   - 免费，全球CDN
   - 登录：`docker login`

3. **GitHub Container Registry**（与GitHub集成）
   - 需要GitHub账号
   - 免费，私有仓库免费
   - 登录：`echo $GITHUB_TOKEN | docker login ghcr.io -u USERNAME --password-stdin`

4. **腾讯云容器镜像服务**（国内备选）
   - 注册：https://console.cloud.tencent.com/tcr
   - 国内速度快
   - 登录：`docker login ccr.ccs.tencentyun.com -u USERNAME -p PASSWORD`

### 步骤2：修改构建脚本配置

编辑 `build-and-push.sh`，修改以下配置：

**如果使用阿里云ACR：**
```bash
REGISTRY="crpi-mql7znw3gpm4caw8.cn-beijing.personal.cr.aliyuncs.com"  # 你的ACR公网地址
NAMESPACE="your-namespace"  # 替换为你的命名空间名称
USERNAME="your-accesskey-id"  # 替换为你的AccessKey ID
```

**如果使用Docker Hub或其他：**
```bash
REGISTRY="docker.io"  # 或 "ghcr.io" 或 "ccr.ccs.tencentyun.com"
NAMESPACE=""  # Docker Hub不需要命名空间，留空
USERNAME="your-username"  # 替换为你的实际用户名
```

### 步骤3：执行构建脚本

```bash
# 在Linux/Mac上
chmod +x build-and-push.sh
./build-and-push.sh

# 或在Windows上使用Git Bash
bash build-and-push.sh
```

脚本会自动：
1. 构建3个镜像（基础镜像、服务端镜像、Web镜像）
2. 询问是否推送到仓库
3. 显示镜像地址

## 修改部署脚本

构建完成后，修改你的部署脚本，将以下两处：

```bash
# 原镜像地址（在脚本中搜索这两行）：
ghcr.nju.edu.cn/xinnan-tech/xiaozhi-esp32-server:server_latest
ghcr.nju.edu.cn/xinnan-tech/xiaozhi-esp32-server:web_latest

# 替换为你的镜像地址（示例）：
docker.io/your-username/xiaozhi-esp32-server:server_latest
docker.io/your-username/xiaozhi-esp32-server:web_latest
```

## 修改docker-compose文件

在 `main/xiaozhi-server/docker-compose_all.yml` 中修改：

```yaml
services:
  xiaozhi-esp32-server:
    image: docker.io/your-username/xiaozhi-esp32-server:server_latest  # 改这里
    
  xiaozhi-esp32-server-web:
    image: docker.io/your-username/xiaozhi-esp32-server:web_latest  # 改这里
```

## 手动构建（如果脚本不可用）

```bash
# 1. 设置变量
export REGISTRY="docker.io"
export USERNAME="your-username"
export IMAGE_PREFIX="${REGISTRY}/${USERNAME}/xiaozhi-esp32-server"

# 2. 登录
docker login

# 3. 构建基础镜像
docker build -f Dockerfile-server-base -t ${IMAGE_PREFIX}:server-base .

# 4. 构建服务端镜像
docker build -f Dockerfile-server -t ${IMAGE_PREFIX}:server_latest .

# 5. 构建Web镜像
docker build -f Dockerfile-web -t ${IMAGE_PREFIX}:web_latest .

# 6. 推送镜像
docker push ${IMAGE_PREFIX}:server-base
docker push ${IMAGE_PREFIX}:server_latest
docker push ${IMAGE_PREFIX}:web_latest
```

## 常见问题

**Q: 构建很慢怎么办？**
- 使用国内镜像源（已在Dockerfile中配置）
- 使用腾讯云等国内镜像仓库

**Q: 推送失败？**
- 确保已登录：`docker login`
- 检查镜像名称格式
- 确保有推送权限

**Q: 如何更新镜像？**
- 重新构建并推送
- 在服务器上：`docker-compose pull && docker-compose up -d`

## 完整文档

详细说明请参考：[docker-build-and-push.md](./docker-build-and-push.md)

