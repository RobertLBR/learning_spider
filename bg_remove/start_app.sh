#!/bin/bash

# 设置颜色输出
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# 错误处理函数
handle_error() {
    echo -e "${RED}错误: $1${NC}"
    exit 1
}

# 检查依赖是否已安装
check_dependency() {
    if ! command -v $1 &> /dev/null; then
        echo -e "${YELLOW}警告: 未找到 $1${NC}"
        echo -e "正在尝试安装 $1..."
        
        if command -v apt-get &> /dev/null; then
            sudo apt-get update
            sudo apt-get install -y $2 || handle_error "无法安装 $1"
        elif command -v yum &> /dev/null; then
            sudo yum install -y $2 || handle_error "无法安装 $1"
        else
            handle_error "无法安装 $1，请手动安装后再运行此脚本"
        fi
    fi
}

echo -e "${GREEN}图片背景消除工具启动脚本 - Ubuntu版${NC}"

# 检查必要的依赖
echo -e "${YELLOW}检查系统依赖...${NC}"
check_dependency python3 "python3 python3-pip python3-venv"
check_dependency pip3 "python3-pip"
check_dependency npm "nodejs npm"

# 获取脚本所在目录的绝对路径
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# 启动后端
echo -e "${GREEN}1. 启动后端服务...${NC}"
cd "$SCRIPT_DIR/backend" || handle_error "无法进入后端目录"

# 创建并激活虚拟环境
if [ ! -d "venv" ]; then
    echo "创建Python虚拟环境..."
    python3 -m venv venv || handle_error "无法创建Python虚拟环境"
fi

echo "激活虚拟环境..."
source venv/bin/activate || handle_error "无法激活虚拟环境"

echo "安装Python依赖..."
pip install --upgrade pip
pip install -r requirements.txt || handle_error "无法安装Python依赖"

echo "启动Flask服务器..."
python app.py > backend.log 2>&1 &
BACKEND_PID=$!

# 检查后端是否成功启动
echo -e "${YELLOW}2. 等待后端服务启动...${NC}"
sleep 3
if ! ps -p $BACKEND_PID > /dev/null; then
    echo -e "${RED}后端服务启动失败，请检查backend.log文件${NC}"
    cat backend.log
    exit 1
fi

# 启动前端
echo -e "${GREEN}3. 启动前端应用...${NC}"
cd "$SCRIPT_DIR/frontend" || handle_error "无法进入前端目录"

echo "安装Node.js依赖..."
npm install || handle_error "无法安装Node.js依赖"

echo "启动React开发服务器..."
npm start > frontend.log 2>&1 &
FRONTEND_PID=$!

# 检查前端是否成功启动
sleep 5
if ! ps -p $FRONTEND_PID > /dev/null; then
    echo -e "${RED}前端应用启动失败，请检查frontend.log文件${NC}"
    cat frontend.log
    exit 1
fi

echo -e "${GREEN}应用启动成功!${NC}"
echo -e "后端API服务器: ${YELLOW}http://localhost:5000${NC}"
echo -e "前端应用界面: ${YELLOW}http://localhost:3000${NC}"
echo -e "日志文件位置:"
echo -e "  - 后端日志: ${YELLOW}$SCRIPT_DIR/backend/backend.log${NC}"
echo -e "  - 前端日志: ${YELLOW}$SCRIPT_DIR/frontend/frontend.log${NC}"
echo -e "${GREEN}按 Ctrl+C 停止应用${NC}"

# 等待用户按Ctrl+C
trap "echo -e '${YELLOW}正在停止应用...${NC}'; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; echo -e '${GREEN}应用已停止${NC}'; exit" INT
wait