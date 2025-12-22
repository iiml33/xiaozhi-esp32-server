# 阿里云ACR登录详细步骤

## 问题

使用实例ID登录失败，提示 "unauthorized: authentication required"

## 解决方案

### 方法1：从ACR控制台获取登录指令（最简单）

1. **访问ACR控制台**
   - 打开：https://cr.console.aliyun.com/
   - 选择你的实例：`crpi-mql7znw3gpm4caw8`

2. **获取登录指令**
   - 在实例详情页面，找到"登录指令"或"访问凭证"
   - 点击"生成临时登录密码"或"获取登录指令"
   - 会显示类似这样的命令：
     ```
     docker login crpi-mql7znw3gpm4caw8.cn-beijing.personal.cr.aliyuncs.com -u crpi-mql7znw3gpm4caw8 -p <临时密码>
     ```
   - 复制完整的命令并执行

3. **或者直接复制临时密码**
   - 在"访问凭证"页面，会显示临时密码
   - 复制临时密码
   - 使用以下命令登录：
     ```powershell
     docker login crpi-mql7znw3gpm4caw8.cn-beijing.personal.cr.aliyuncs.com -u crpi-mql7znw3gpm4caw8
     ```
   - 粘贴临时密码

### 方法2：使用AccessKey（如果方法1不行）

1. **检查AccessKey权限**
   - 访问：https://ram.console.aliyun.com/manage/ak
   - 找到你的AccessKey：`LTAI5tQxpeqgx5JvWsUV3FjV`
   - 检查是否有"容器镜像服务"的权限
   - 如果没有，需要添加权限

2. **使用AccessKey登录**
   ```powershell
   docker login crpi-mql7znw3gpm4caw8.cn-beijing.personal.cr.aliyuncs.com -u LTAI5tQxpeqgx5JvWsUV3FjV
   ```
   - 输入AccessKey Secret作为密码

### 方法3：创建RAM子账号（推荐用于生产环境）

如果主账号AccessKey有问题，可以创建RAM子账号：

1. **创建RAM子账号**
   - 访问：https://ram.console.aliyun.com/users
   - 创建新用户
   - 授予"容器镜像服务"的权限

2. **为子账号创建AccessKey**
   - 选择创建的子账号
   - 创建AccessKey
   - 使用子账号的AccessKey登录

## 验证登录

登录成功后，可以测试：

```powershell
# 测试拉取（会失败，但能验证登录）
docker pull crpi-mql7znw3gpm4caw8.cn-beijing.personal.cr.aliyuncs.com/aichatbotesp32/test:test

# 如果提示 "unauthorized" 说明登录失败
# 如果提示 "not found" 说明登录成功（只是镜像不存在）
```

## 常见问题

### Q: 为什么使用实例ID登录失败？

**可能原因**：
- 临时密码已过期（临时密码通常24小时有效）
- 密码输入错误
- 需要使用AccessKey ID作为用户名

**解决方案**：
- 重新从ACR控制台获取临时密码
- 或使用AccessKey ID作为用户名

### Q: AccessKey Secret可以用于登录吗？

**答案**：对于个人版ACR，通常需要使用临时登录密码，而不是直接使用AccessKey Secret。

**解决方案**：
- 优先使用临时登录密码
- 如果必须使用AccessKey，确保AccessKey有容器镜像服务的权限

### Q: 如何确认登录成功？

**验证方法**：
```powershell
# 查看Docker登录信息
cat ~/.docker/config.json

# 或在Windows上
type %USERPROFILE%\.docker\config.json
```

如果看到你的ACR地址，说明已登录。

## 推荐流程

1. ✅ 访问ACR控制台获取临时登录密码
2. ✅ 使用临时密码登录
3. ✅ 登录成功后推送镜像
4. ✅ 如果临时密码过期，重新获取

## 下一步

登录成功后，可以推送镜像：

```powershell
docker push crpi-mql7znw3gpm4caw8.cn-beijing.personal.cr.aliyuncs.com/aichatbotesp32/xiaozhi-esp32-server:server-base
docker push crpi-mql7znw3gpm4caw8.cn-beijing.personal.cr.aliyuncs.com/aichatbotesp32/xiaozhi-esp32-server:server_latest
docker push crpi-mql7znw3gpm4caw8.cn-beijing.personal.cr.aliyuncs.com/aichatbotesp32/xiaozhi-esp32-server:web_latest
```

