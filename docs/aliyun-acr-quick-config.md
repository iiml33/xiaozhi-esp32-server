# 阿里云ACR快速配置指南

## 你的ACR信息

根据你提供的信息：
- **实例ID**: `crpi-mql7znw3gpm4caw8`
- **地域**: `华北2（北京）`
- **公网地址**: `crpi-mql7znw3gpm4caw8.cn-beijing.personal.cr.aliyuncs.com`

## 快速配置步骤

### 步骤1：创建命名空间

1. 访问阿里云ACR控制台：https://cr.console.aliyun.com/
2. 选择你的实例
3. 进入"命名空间"页面
4. 点击"创建命名空间"
5. 输入命名空间名称（例如：`xiaozhi`）
6. 保存命名空间名称，稍后需要用到

### 步骤2：获取AccessKey

1. 点击右上角头像 -> **AccessKey管理**
2. 如果没有AccessKey，点击**创建AccessKey**
3. 保存以下信息：
   - **AccessKey ID**（例如：`LTAI5t...`）
   - **AccessKey Secret**（例如：`xxx...`，只显示一次！）

⚠️ **重要**：AccessKey Secret只显示一次，请立即保存！

### 步骤3：修改构建脚本

编辑 `build-and-push.sh`，修改以下三行：

```bash
REGISTRY="crpi-mql7znw3gpm4caw8.cn-beijing.personal.cr.aliyuncs.com"
NAMESPACE="xiaozhi"  # 替换为你在步骤1中创建的命名空间名称
USERNAME="LTAI5t..."  # 替换为你的AccessKey ID
```

### 步骤4：运行构建脚本

```bash
chmod +x build-and-push.sh
./build-and-push.sh
```

脚本会：
1. 提示你输入AccessKey Secret（密码）
2. 自动构建3个镜像
3. 询问是否推送到ACR
4. 显示最终的镜像地址

### 步骤5：修改部署脚本

构建完成后，在你的部署脚本中搜索并替换：

```bash
# 原镜像地址：
ghcr.nju.edu.cn/xinnan-tech/xiaozhi-esp32-server:server_latest
ghcr.nju.edu.cn/xinnan-tech/xiaozhi-esp32-server:web_latest

# 替换为（假设命名空间是xiaozhi）：
crpi-mql7znw3gpm4caw8.cn-beijing.personal.cr.aliyuncs.com/xiaozhi/xiaozhi-esp32-server:server_latest
crpi-mql7znw3gpm4caw8.cn-beijing.personal.cr.aliyuncs.com/xiaozhi/xiaozhi-esp32-server:web_latest
```

### 步骤6：修改docker-compose文件

在 `main/xiaozhi-server/docker-compose_all.yml` 中修改：

```yaml
services:
  xiaozhi-esp32-server:
    image: crpi-mql7znw3gpm4caw8.cn-beijing.personal.cr.aliyuncs.com/xiaozhi/xiaozhi-esp32-server:server_latest
    
  xiaozhi-esp32-server-web:
    image: crpi-mql7znw3gpm4caw8.cn-beijing.personal.cr.aliyuncs.com/xiaozhi/xiaozhi-esp32-server:web_latest
```

## 完整配置示例

假设你的命名空间是 `xiaozhi`，AccessKey ID是 `LTAI5tABC123`，那么：

**build-and-push.sh 配置：**
```bash
REGISTRY="crpi-mql7znw3gpm4caw8.cn-beijing.personal.cr.aliyuncs.com"
NAMESPACE="xiaozhi"
USERNAME="LTAI5tABC123"
```

**最终镜像地址：**
```
crpi-mql7znw3gpm4caw8.cn-beijing.personal.cr.aliyuncs.com/xiaozhi/xiaozhi-esp32-server:server_latest
crpi-mql7znw3gpm4caw8.cn-beijing.personal.cr.aliyuncs.com/xiaozhi/xiaozhi-esp32-server:web_latest
```

## 验证镜像

推送完成后，可以在ACR控制台查看：

1. 访问：https://cr.console.aliyun.com/
2. 选择你的实例
3. 进入"镜像仓库"
4. 选择命名空间 `xiaozhi`
5. 应该能看到3个镜像：
   - `xiaozhi-esp32-server:server-base`
   - `xiaozhi-esp32-server:server_latest`
   - `xiaozhi-esp32-server:web_latest`

## 常见问题

**Q: 登录时提示"unauthorized"？**
- 检查AccessKey ID和Secret是否正确
- 确认AccessKey未被禁用

**Q: 推送时提示"denied"？**
- 检查命名空间名称是否正确
- 确认命名空间已创建

**Q: 如何查看命名空间？**
- 在ACR控制台的"命名空间"页面查看

## 下一步

1. ✅ 创建命名空间
2. ✅ 获取AccessKey
3. ✅ 修改构建脚本
4. ✅ 运行构建脚本
5. ✅ 修改部署脚本
6. ✅ 在阿里云服务器上部署

详细说明请参考：[aliyun-acr-setup.md](./aliyun-acr-setup.md)

