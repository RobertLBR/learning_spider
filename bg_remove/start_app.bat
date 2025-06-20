@echo off
echo 图片背景消除工具启动脚本 - Windows版

echo 1. 启动后端服务...
start cmd /k "cd backend && python -m venv venv && venv\Scripts\activate && pip install -r requirements.txt && python app.py"

echo 2. 等待后端服务启动...
timeout /t 5

echo 3. 启动前端应用...
start cmd /k "cd frontend && npm install && npm start"

echo 应用启动中，请稍候...
echo 前端将在浏览器中自动打开: http://localhost:3000