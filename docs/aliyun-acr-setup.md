# 阿里云ACR镜像仓库配置指南

## 前提条件

1. 已开通阿里云容器镜像服务（ACR）
2. 已创建命名空间
3. 已获取AccessKey（用于Docker登录）

## 获取必要信息

### 1. 实例信息

从你的ACR控制台获取：
- **实例ID**: `crpi-mql7znw3gpm4caw8`
- **地域**: `华北2（北京）`
- **公网地址**: `crpi-mql7znw3gpm4caw8.cn-beijing.personal.cr.aliyuncs.com`

### 2. 命名空间

1. 登录阿里云ACR控制台：https://cr.console.aliyun.com/
2. 选择你的实例
3. 进入"命名空间"页面
4. 查看或创建命名空间（例如：`xiaozhi`）

### 3. AccessKey（用于Docker登录）

1. 点击右上角头像 -> **AccessKey管理**
2. 如果没有AccessKey，点击**创建AccessKey**
3. 保存以下信息：
   - **AccessKey ID**（作为Docker登录用户名）
   - **AccessKey Secret**（作为Docker登录密码）

⚠️ **重要**：AccessKey Secret只显示一次，请妥善保存！

## 配置构建脚本

编辑 `build-and-push.sh`，修改以下配置：

```bash
# 阿里云ACR配置
REGISTRY="crpi-mql7znw3gpm4caw8.cn-beijing.personal.cr.aliyuncs.com"  # 你的ACR公网地址
NAMESPACE="xiaozhi"  # 替换为你的命名空间名称
USERNAME="your-accesskey-id"  # 替换为你的AccessKey ID
```

## 登录阿里云ACR

### 方法1：使用脚本自动登录

运行构建脚本时，脚本会提示你输入密码（AccessKey Secret）

### 方法2：手动登录

```bash
# 登录命令
docker login crpi-mql7znw3gpm4caw8.cn-beijing.personal.cr.aliyuncs.com \
  -u your-accesskey-id \
  -p your-accesskey-secret
```

### 方法3：使用阿里云CLI（推荐，更安全）

```bash
# 安装阿里云CLI（如果还没有）
# 下载地址：https://help.aliyun.com/document_detail/110341.html

# 配置CLI
aliyun configure

# 获取临时登录密码
aliyun cr GetAuthorizationToken --region cn-beijing

# 使用返回的临时密码登录
docker login crpi-mql7znw3gpm4caw8.cn-beijing.personal.cr.aliyuncs.com \
  -u crpi-mql7znw3gpm4caw8 \
  -p <临时密码>
```

## 构建和推送镜像

```bash
# 执行构建脚本
chmod +x build-and-push.sh
./build-and-push.sh
```

脚本会自动：
1. 构建3个镜像
2. 推送到你的ACR仓库

## 镜像地址格式

构建完成后，镜像地址格式为：

```
crpi-mql7znw3gpm4caw8.cn-beijing.personal.cr.aliyuncs.com/xiaozhi/xiaozhi-esp32-server:server_latest
crpi-mql7znw3gpm4caw8.cn-beijing.personal.cr.aliyuncs.com/xiaozhi/xiaozhi-esp32-server:web_latest
```

## 修改部署脚本

在你的部署脚本中，将镜像地址替换为：

```bash
# 原镜像地址：
ghcr.nju.edu.cn/xinnan-tech/xiaozhi-esp32-server:server_latest
ghcr.nju.edu.cn/xinnan-tech/xiaozhi-esp32-server:web_latest

# 替换为你的ACR镜像地址：
crpi-mql7znw3gpm4caw8.cn-beijing.personal.cr.aliyuncs.com/xiaozhi/xiaozhi-esp32-server:server_latest
crpi-mql7znw3gpm4caw8.cn-beijing.personal.cr.aliyuncs.com/xiaozhi/xiaozhi-esp32-server:web_latest
```

## 修改docker-compose文件

在 `main/xiaozhi-server/docker-compose_all.yml` 中修改：

```yaml
services:
  xiaozhi-esp32-server:
    image: crpi-mql7znw3gpm4caw8.cn-beijing.personal.cr.aliyuncs.com/xiaozhi/xiaozhi-esp32-server:server_latest
    
  xiaozhi-esp32-server-web:
    image: crpi-mql7znw3gpm4caw8.cn-beijing.personal.cr.aliyuncs.com/xiaozhi/xiaozhi-esp32-server:web_latest
```

## 在阿里云服务器上配置镜像加速（可选）

如果部署在阿里云服务器上，可以配置镜像加速：

1. 登录服务器
2. 编辑 `/etc/docker/daemon.json`：

```json
{
  "registry-mirrors": [
    "https://crpi-mql7znw3gpm4caw8.cn-beijing.personal.cr.aliyuncs.com"
  ]
}
```

3. 重启Docker：
```bash
systemctl restart docker
```

## 常见问题

### Q1: 登录时提示"unauthorized: authentication required"

**解决方案：**
- 检查AccessKey ID和Secret是否正确
- 确认AccessKey未被禁用
- 尝试使用临时登录密码（通过阿里云CLI获取）

### Q2: 推送时提示"denied: requested access to the resource is denied"

**解决方案：**
- 检查命名空间名称是否正确
- 确认有推送权限
- 检查镜像名称格式是否正确

### Q3: 如何查看已推送的镜像？

**解决方案：**
1. 登录ACR控制台
2. 选择你的实例
3. 进入"镜像仓库"页面
4. 选择对应的命名空间
5. 查看镜像列表

### Q4: 如何设置镜像为公开或私有？

**解决方案：**
1. 在ACR控制台的镜像仓库页面
2. 点击镜像名称
3. 在"基本信息"中修改可见性

## 安全建议

1. **不要将AccessKey提交到代码仓库**
2. **使用环境变量存储敏感信息**：
   ```bash
   export ALIYUN_ACCESS_KEY_ID="your-id"
   export ALIYUN_ACCESS_KEY_SECRET="your-secret"
   ```
3. **定期轮换AccessKey**
4. **使用RAM子账号和最小权限原则**

## 下一步

1. 在ACR控制台创建命名空间
2. 获取AccessKey
3. 修改构建脚本配置
4. 运行构建脚本
5. 修改部署脚本中的镜像地址
6. 在阿里云服务器上部署

