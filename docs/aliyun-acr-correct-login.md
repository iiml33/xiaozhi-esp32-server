# 阿里云ACR正确登录方式

## 正确的登录信息

根据ACR控制台显示：

### 用户名
```
nick0416011493
```

### 登录命令格式
```powershell
docker login --username=nick0416011493 crpi-mql7znw3gpm4caw8.cn-beijing.personal.cr.aliyuncs.com
```

### 密码
使用**固定密码（固定密码）**，从ACR控制台获取：
1. 访问：https://cr.console.aliyun.com/
2. 选择实例：`crpi-mql7znw3gpm4caw8`
3. 进入：**访问凭证**
4. 设置或获取：**固定密码**
5. 使用固定密码登录

## 完整登录步骤

### 步骤1：获取固定密码

1. 访问ACR控制台：https://cr.console.aliyun.com/
2. 选择你的实例：`crpi-mql7znw3gpm4caw8`
3. 点击左侧菜单：**访问凭证**
4. 在"固定密码"部分：
   - 如果还没有设置，点击"设置固定密码"
   - 如果已设置，点击"查看"或"重置"获取密码
5. 复制固定密码

### 步骤2：登录

```powershell
docker login --username=nick0416011493 crpi-mql7znw3gpm4caw8.cn-beijing.personal.cr.aliyuncs.com
```

输入固定密码。

### 步骤3：验证登录

```powershell
# 查看登录信息
type %USERPROFILE%\.docker\config.json
```

如果看到你的ACR地址，说明登录成功。

## 推送镜像

登录成功后，推送镜像：

```powershell
# 推送基础镜像
docker push crpi-mql7znw3gpm4caw8.cn-beijing.personal.cr.aliyuncs.com/aichatbotesp32/xiaozhi-esp32-server:server-base

# 推送服务端镜像
docker push crpi-mql7znw3gpm4caw8.cn-beijing.personal.cr.aliyuncs.com/aichatbotesp32/xiaozhi-esp32-server:server_latest

# 推送Web镜像
docker push crpi-mql7znw3gpm4caw8.cn-beijing.personal.cr.aliyuncs.com/aichatbotesp32/xiaozhi-esp32-server:web_latest
```

## 重要提示

1. **用户名**：使用 `nick0416011493`，不是AccessKey ID
2. **密码**：使用固定密码（固定密码），不是AccessKey Secret
3. **命令格式**：使用 `--username=` 参数，不是 `-u`
4. **固定密码**：没有时效限制，请妥善保管

## 常见错误

### 错误1：使用AccessKey ID作为用户名
```
错误：使用 LTAI5tQxpeqgx5JvWsUV3FjV 作为用户名
正确：使用 nick0416011493 作为用户名
```

### 错误2：使用AccessKey Secret作为密码
```
错误：使用AccessKey Secret作为密码
正确：使用固定密码（从ACR控制台获取）
```

### 错误3：命令格式错误
```
错误：docker login -u nick0416011493 ...
正确：docker login --username=nick0416011493 ...
```

## 快速参考

```powershell
# 1. 获取固定密码（从ACR控制台）
# 2. 登录
docker login --username=nick0416011493 crpi-mql7znw3gpm4caw8.cn-beijing.personal.cr.aliyuncs.com

# 3. 推送镜像
docker push crpi-mql7znw3gpm4caw8.cn-beijing.personal.cr.aliyuncs.com/aichatbotesp32/xiaozhi-esp32-server:server-base
docker push crpi-mql7znw3gpm4caw8.cn-beijing.personal.cr.aliyuncs.com/aichatbotesp32/xiaozhi-esp32-server:server_latest
docker push crpi-mql7znw3gpm4caw8.cn-beijing.personal.cr.aliyuncs.com/aichatbotesp32/xiaozhi-esp32-server:web_latest
```

