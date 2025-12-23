# Docker容器中猫叫声功能修复指南

## 问题描述

本地部署可以发出猫叫，但构建Docker镜像推送到阿里云后不能发出猫叫。

## 问题原因

Docker容器中缺少 `config/cat_sounds` 目录的挂载。猫叫声音频文件存储在 `main/xiaozhi-server/config/cat_sounds/` 目录下，但容器内无法访问这些文件。

## 解决方案

### 方案1：在docker-compose.yml中添加挂载（推荐）

在 `docker-compose_all.yml` 的 `xiaozhi-esp32-server` 服务的 `volumes` 部分添加：

```yaml
volumes:
  # 配置文件目录
  - ./data:/opt/xiaozhi-esp32-server/data
  # 模型文件挂接，很重要
  - ./models/SenseVoiceSmall/model.pt:/opt/xiaozhi-esp32-server/models/SenseVoiceSmall/model.pt
  # 猫叫声文件目录（重要：用于猫语功能）
  - ./main/xiaozhi-server/config/cat_sounds:/opt/xiaozhi-esp32-server/config/cat_sounds
```

### 方案2：将音频文件打包进镜像（不推荐）

如果不想使用挂载，可以修改 `Dockerfile-server`，确保复制了 `config/cat_sounds` 目录：

```dockerfile
FROM ghcr.io/xinnan-tech/xiaozhi-esp32-server:server-base

COPY main/xiaozhi-server .
# 确保config/cat_sounds目录被复制
# COPY main/xiaozhi-server/config/cat_sounds /opt/xiaozhi-esp32-server/config/cat_sounds

CMD ["python", "app.py"]
```

**注意**：这种方式不推荐，因为：
1. 镜像会变得很大
2. 更新音频文件需要重新构建镜像
3. 不够灵活

## 验证修复

修复后，可以通过以下方式验证：

### 1. 检查容器内目录

```bash
docker exec -it xiaozhi-esp32-server ls -la /opt/xiaozhi-esp32-server/config/cat_sounds
```

应该能看到各个猫叫声类型的文件夹（Meow, Purr, Trill等）。

### 2. 检查音频文件

```bash
docker exec -it xiaozhi-esp32-server ls -la /opt/xiaozhi-esp32-server/config/cat_sounds/Meow
```

应该能看到音频文件（.wav, .mp3等）。

### 3. 查看日志

```bash
docker logs xiaozhi-esp32-server | grep -i "cat_sound\|猫叫"
```

如果看到类似 "为猫叫声类型 meow 选择了文件: ..." 的日志，说明功能正常。

## 目录结构

正确的目录结构应该是：

```
/opt/xiaozhi-esp32-server/
├── config/
│   └── cat_sounds/
│       ├── Meow/          # 喵
│       ├── Purr/          # 呼噜
│       ├── Trill/         # 咕噜咕噜/颤音
│       ├── Chattering/    # 咔咔/啾啾
│       ├── Hiss/          # 哈气
│       ├── Growl/         # 低吼/咆哮
│       ├── Yowl/          # 嚎叫/长嗷
│       ├── Scream/        # 尖叫/惨叫
│       └── Mutter/        # 嘟嘟嘟不满声/咕哝
```

## 常见问题

### Q1: 挂载后仍然没有声音？

**检查清单**：
1. ✅ 确认本地 `main/xiaozhi-server/config/cat_sounds/` 目录存在且有音频文件
2. ✅ 确认挂载路径正确
3. ✅ 重启容器：`docker-compose restart xiaozhi-esp32-server`
4. ✅ 检查容器内文件权限

### Q2: 权限问题？

如果遇到权限问题，可以：

```bash
# 设置本地目录权限
chmod -R 755 main/xiaozhi-server/config/cat_sounds

# 或者在容器内设置
docker exec -it xiaozhi-esp32-server chmod -R 755 /opt/xiaozhi-esp32-server/config/cat_sounds
```

### Q3: 路径大小写问题？

注意：代码中使用的是小写（如 `meow`），但实际文件夹可能是首字母大写（如 `Meow`）。

如果遇到路径不匹配，可以：
1. 重命名文件夹为小写
2. 或者在代码中处理大小写不敏感

## 部署到阿里云

如果使用阿里云部署，确保：

1. **本地有音频文件**：`main/xiaozhi-server/config/cat_sounds/` 目录下有音频文件
2. **挂载配置正确**：`docker-compose_all.yml` 中已添加挂载
3. **服务器上有对应目录**：在服务器上创建对应的目录结构
4. **文件同步**：将音频文件同步到服务器

### 服务器部署步骤

```bash
# 1. 在服务器上创建目录
mkdir -p /path/to/project/main/xiaozhi-server/config/cat_sounds

# 2. 将音频文件上传到服务器（使用scp、rsync等）
scp -r main/xiaozhi-server/config/cat_sounds/* user@server:/path/to/project/main/xiaozhi-server/config/cat_sounds/

# 3. 启动容器
docker-compose -f docker-compose_all.yml up -d
```

## 总结

**根本原因**：Docker容器中缺少 `config/cat_sounds` 目录的挂载。

**解决方法**：在 `docker-compose_all.yml` 中添加目录挂载。

**验证方法**：检查容器内目录和日志。

