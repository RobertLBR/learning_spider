# 图片背景消除工具

这是一个基于 Python Flask + Rembg + React 的图片背景消除Web工具。用户可以上传图片，系统会自动去除图片背景，并提供下载功能。

## 功能特点

- 支持多种图片格式（JPEG, PNG, GIF, WebP等）
- 实时预览原图和处理后的图片
- 一键去除图片背景
- 支持处理后图片下载
- 响应式设计，支持移动端访问
- 后端健康检查，确保服务可用性

## 技术栈

- 前端：React.js, Axios
- 后端：Python Flask, Flask-CORS
- 图片处理：Rembg, PIL (Pillow)

## 系统要求

- **操作系统**：Windows 10+、macOS 10.15+、Ubuntu 20.04/22.04
- **Node.js**：14.0.0 或更高版本
- **Python**：3.7 或更高版本
- **浏览器**：Chrome、Firefox、Edge、Safari 最新版本

## 项目结构

```
img_remove/
├── backend/            # Flask后端
│   ├── app.py         # Flask应用主文件
│   ├── requirements.txt # Python依赖
│   └── temp/          # 临时文件目录
├── frontend/          # React前端
│   ├── package.json   # 前端依赖配置
│   ├── public/        # 静态文件
│   └── src/          # React源代码
├── start_app.sh      # Linux/Mac启动脚本
├── start_app.bat     # Windows启动脚本
└── README.md         # 项目说明文档
```

## 快速启动

### Ubuntu 22.04 快速启动

1. **安装系统依赖**

   ```bash
   sudo apt update
   sudo apt install -y python3 python3-pip python3-venv nodejs npm
   ```

2. **运行启动脚本**

   ```bash
   chmod +x start_app.sh
   ./start_app.sh
   ```

   脚本会自动安装所有必要的依赖并启动应用。

3. **访问应用**

   打开浏览器访问：http://localhost:3000

### Windows 快速启动

双击运行 `start_app.bat` 文件，然后在浏览器中访问 http://localhost:3000

## 手动安装和运行

### 后端设置

1. 进入后端目录：
```bash
cd backend
```

2. 创建虚拟环境（可选但推荐）：
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. 安装依赖：
```bash
pip install -r requirements.txt
```

4. 运行后端服务：
```bash
python app.py
```

服务器将在 http://localhost:5000 启动

### 前端设置

1. 进入前端目录：
```bash
cd frontend
```

2. 安装依赖：
```bash
npm install
```

3. 运行开发服务器：
```bash
npm start
```

应用将在 http://localhost:3000 启动

## 使用说明

1. 打开浏览器访问 http://localhost:3000
2. 点击"选择图片"按钮上传需要处理的图片
3. 点击"去除背景"按钮进行处理
4. 处理完成后，可以预览效果并下载处理后的图片

## 常见问题解决

### 后端服务无法启动

- **问题**: 运行`python app.py`时出现错误
- **解决方案**: 
  - 确保已安装所有依赖: `pip install -r requirements.txt`
  - 检查Python版本是否兼容: `python --version`
  - 尝试使用管理员/root权限运行
  - 检查端口5000是否被占用: `sudo lsof -i :5000` (Linux/Mac) 或 `netstat -ano | findstr :5000` (Windows)

### 无法连接到后端服务

- **问题**: 前端显示"后端服务未连接"
- **解决方案**:
  - 确保后端服务正在运行
  - 检查防火墙设置是否阻止了端口5000
  - 尝试访问 http://localhost:5000 确认后端服务可用
  - 在Ubuntu系统上，可能需要配置防火墙: `sudo ufw allow 5000/tcp`

### 图片处理超时

- **问题**: 处理大图片时出现超时错误
- **解决方案**:
  - 尝试使用较小的图片
  - 增加服务器超时限制
  - 确保系统有足够的内存
  - 在低配置系统上，可以尝试关闭其他占用资源的应用

### 404错误

- **问题**: 访问后端API时出现404错误
- **解决方案**:
  - 确保访问的是正确的API端点 `/api/remove-bg`
  - 检查前端代理配置是否正确
  - 如果直接访问后端根路径，会看到API文档页面

## 注意事项

- 支持的图片格式：PNG、JPG、JPEG、GIF、WebP
- 图片大小限制：10MB
- 处理大图片可能需要较长时间，请耐心等待
- 复杂图片的背景去除效果可能不尽如人意
- 在Ubuntu系统上，如果遇到权限问题，可能需要使用sudo运行脚本

## 开发者说明

- 后端API端点：`/api/remove-bg`
- 健康检查端点：`/api/health`
- 开发模式下前端会自动代理API请求到后端
- 可以通过修改后端的`app.py`中的配置来调整上传限制
- 前端代码支持热重载，修改后会自动刷新

## 性能优化建议

- 对于生产环境，建议使用Gunicorn或uWSGI来部署Flask应用
- 考虑使用Nginx作为反向代理服务器
- 对于高流量场景，可以考虑添加图片处理队列
- 在资源受限的系统上，可以降低Rembg的处理质量以提高速度

## 许可证

MIT License