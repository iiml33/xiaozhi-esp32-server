# Windows系统构建Docker镜像指南

## 方法1：使用Git Bash（推荐）

如果你已经安装了Git for Windows，可以使用Git Bash运行bash脚本：

### 步骤1：打开Git Bash

1. 在项目文件夹中右键点击
2. 选择 "Git Bash Here"
3. 或者在开始菜单搜索 "Git Bash"

### 步骤2：运行脚本

```bash
# 给脚本添加执行权限（Git Bash中可用）
chmod +x build-and-push.sh

# 运行脚本
./build-and-push.sh
```

## 方法2：使用Windows批处理文件（.bat）

我已经为你创建了Windows版本的脚本 `build-and-push.bat`，可以直接在PowerShell或CMD中运行：

### 步骤1：编辑配置

打开 `build-and-push.bat`，修改以下配置（已根据你的信息预填）：

```batch
set REGISTRY=crpi-mql7znw3gpm4caw8.cn-beijing.personal.cr.aliyuncs.com
set NAMESPACE=aichatbotesp32
set USERNAME=LTAI5t8JLqqiJvm7T69M28b6
```

### 步骤2：运行脚本

在PowerShell或CMD中：

```powershell
# PowerShell
.\build-and-push.bat

# 或CMD
build-and-push.bat
```

## 方法3：使用WSL（Windows Subsystem for Linux）

如果你安装了WSL，可以在WSL中运行：

```bash
# 在WSL中进入项目目录
cd /mnt/e/xiaozhi-server-full-module-onekey/src

# 运行脚本
chmod +x build-and-push.sh
./build-and-push.sh
```

## 当前配置信息

根据你的设置，当前配置为：

- **镜像仓库**: `crpi-mql7znw3gpm4caw8.cn-beijing.personal.cr.aliyuncs.com`
- **命名空间**: `aichatbotesp32`
- **用户名**: `LTAI5t8JLqqiJvm7T69M28b6`

**最终镜像地址将是：**
```
crpi-mql7znw3gpm4caw8.cn-beijing.personal.cr.aliyuncs.com/aichatbotesp32/xiaozhi-esp32-server:server_latest
crpi-mql7znw3gpm4caw8.cn-beijing.personal.cr.aliyuncs.com/aichatbotesp32/xiaozhi-esp32-server:web_latest
```

## 注意事项

1. **确保Docker Desktop正在运行**
   - 检查系统托盘中的Docker图标
   - 确保Docker状态为"Running"

2. **登录时输入密码**
   - 脚本会提示输入AccessKey Secret
   - 输入时不会显示字符（这是正常的）

3. **构建时间**
   - 首次构建可能需要较长时间（下载依赖）
   - 后续构建会更快（使用缓存）

## 常见问题

**Q: PowerShell中提示"无法识别chmod"？**
- 这是正常的，PowerShell不支持chmod命令
- 使用Git Bash或运行.bat文件

**Q: 如何安装Git Bash？**
- 下载Git for Windows：https://git-scm.com/download/win
- 安装时会自动安装Git Bash

**Q: 构建失败怎么办？**
- 检查Docker是否运行
- 检查网络连接
- 查看错误信息，通常是网络或权限问题

## 推荐方式

对于Windows用户，推荐使用：
1. **Git Bash** - 如果已安装Git
2. **.bat文件** - 如果不想安装额外工具

两种方式功能相同，选择你方便的即可。

