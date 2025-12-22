# 镜像推送问题排查

## 当前问题

从日志看到推送失败，错误信息：
```
failed to copy: failed to do request: Put "https://...": write tcp 192.168.65.3:41982->192.168.65.1:3128: use of closed network connection
```

## 可能原因

### 1. 未登录或登录过期

**症状**：推送时提示 "unauthorized" 或网络连接错误

**解决方案**：
```powershell
# 先登录
docker login crpi-mql7znw3gpm4caw8.cn-beijing.personal.cr.aliyuncs.com -u LTAI5tQxpeqgx5JvWsUV3FjV

# 或使用实例ID作为用户名（推荐）
docker login crpi-mql7znw3gpm4caw8.cn-beijing.personal.cr.aliyuncs.com -u crpi-mql7znw3gpm4caw8
```

### 2. 网络连接问题（代理/防火墙）

**症状**：推送大文件时连接中断

**解决方案**：

#### 检查Docker代理设置

1. 打开Docker Desktop
2. Settings -> Resources -> Proxies
3. 检查是否有代理设置导致问题
4. 如果不需要代理，可以禁用

#### 使用专有网络地址（如果在阿里云服务器上）

如果在阿里云服务器上，可以使用专有网络地址：
```
crpi-mql7znw3gpm4caw8-vpc.cn-beijing.personal.cr.aliyuncs.com
```

### 3. 镜像太大，上传超时

**症状**：推送大镜像时失败

**解决方案**：
- 使用分片上传（Docker自动处理）
- 增加超时时间
- 检查网络稳定性

### 4. 命名空间或权限问题

**症状**：提示 "denied: requested access to the resource is denied"

**解决方案**：
- 检查命名空间 `aichatbotesp32` 是否存在
- 检查是否有推送权限
- 确认AccessKey有容器镜像服务的权限

## 手动推送步骤

如果脚本推送失败，可以手动推送：

### 步骤1：登录

```powershell
# 方式1：使用AccessKey ID
docker login crpi-mql7znw3gpm4caw8.cn-beijing.personal.cr.aliyuncs.com -u LTAI5tQxpeqgx5JvWsUV3FjV

# 方式2：使用实例ID（推荐，使用临时密码）
docker login crpi-mql7znw3gpm4caw8.cn-beijing.personal.cr.aliyuncs.com -u crpi-mql7znw3gpm4caw8
```

### 步骤2：推送镜像

```powershell
# 推送基础镜像
docker push crpi-mql7znw3gpm4caw8.cn-beijing.personal.cr.aliyuncs.com/aichatbotesp32/xiaozhi-esp32-server:server-base

# 推送服务端镜像
docker push crpi-mql7znw3gpm4caw8.cn-beijing.personal.cr.aliyuncs.com/aichatbotesp32/xiaozhi-esp32-server:server_latest

# 推送Web镜像
docker push crpi-mql7znw3gpm4caw8.cn-beijing.personal.cr.aliyuncs.com/aichatbotesp32/xiaozhi-esp32-server:web_latest
```

## 获取临时登录密码

1. 访问：https://cr.console.aliyun.com/
2. 选择实例 `crpi-mql7znw3gpm4caw8`
3. 点击"访问凭证"或"登录指令"
4. 复制临时密码
5. 使用临时密码登录

## 验证推送

推送成功后，在ACR控制台查看：
1. 访问：https://cr.console.aliyun.com/
2. 选择你的实例
3. 进入"镜像仓库"
4. 选择命名空间 `aichatbotesp32`
5. 应该能看到推送的镜像

## 常见错误

### "unauthorized: authentication required"
- 未登录或登录过期
- 重新登录

### "denied: requested access to the resource is denied"
- 命名空间不存在
- 没有推送权限
- 检查命名空间和权限

### "use of closed network connection"
- 网络连接中断
- 可能是代理问题
- 检查Docker代理设置
- 重试推送

### "context deadline exceeded"
- 上传超时
- 网络不稳定
- 重试推送

## 快速修复

1. **先登录**（使用临时密码）：
   ```powershell
   docker login crpi-mql7znw3gpm4caw8.cn-beijing.personal.cr.aliyuncs.com -u crpi-mql7znw3gpm4caw8
   ```

2. **然后推送**：
   ```powershell
   docker push crpi-mql7znw3gpm4caw8.cn-beijing.personal.cr.aliyuncs.com/aichatbotesp32/xiaozhi-esp32-server:server-base
   docker push crpi-mql7znw3gpm4caw8.cn-beijing.personal.cr.aliyuncs.com/aichatbotesp32/xiaozhi-esp32-server:server_latest
   docker push crpi-mql7znw3gpm4caw8.cn-beijing.personal.cr.aliyuncs.com/aichatbotesp32/xiaozhi-esp32-server:web_latest
   ```

