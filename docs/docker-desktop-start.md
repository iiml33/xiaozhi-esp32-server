# 启动Docker Desktop

## 问题

如果看到错误信息：
```
错误: Docker未运行，请先启动Docker
```

或
```
failed to connect to the docker API at npipe:////./pipe/dockerDesktopLinuxEngine
```

这表示Docker Desktop没有运行。

## 解决方法

### 方法1：从开始菜单启动

1. 点击Windows开始菜单
2. 搜索 "Docker Desktop"
3. 点击启动Docker Desktop
4. 等待Docker Desktop完全启动（系统托盘图标不再闪烁）

### 方法2：从系统托盘启动

1. 查看系统托盘（右下角）
2. 如果看到Docker图标，右键点击
3. 选择 "Start Docker Desktop"

### 方法3：命令行启动

在PowerShell中运行：

```powershell
# 启动Docker Desktop
Start-Process "C:\Program Files\Docker\Docker\Docker Desktop.exe"
```

## 验证Docker是否运行

启动后，等待1-2分钟，然后运行：

```powershell
docker info
```

如果看到Docker信息（而不是错误），说明Docker已成功启动。

## 检查Docker Desktop状态

1. 查看系统托盘中的Docker图标
2. 图标状态：
   - 🐳 绿色：Docker正在运行
   - 🐳 黄色：Docker正在启动
   - 🐳 红色：Docker有错误

## 常见问题

**Q: Docker Desktop启动很慢？**
- 首次启动需要初始化，可能需要几分钟
- 确保有足够的内存和磁盘空间

**Q: 启动后仍然提示未运行？**
- 等待更长时间（可能需要2-3分钟）
- 检查系统托盘图标是否变为绿色
- 尝试重启Docker Desktop

**Q: 如何设置Docker Desktop开机自启？**
- 打开Docker Desktop
- Settings -> General
- 勾选 "Start Docker Desktop when you log in"

