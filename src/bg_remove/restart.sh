#!/usr/bin/bash

# 定义目录
PROJECT_DIR=$(pwd)

# 清理进程
netstat -tnlp| egrep ':5000|:3000' | awk '{print $NF}' | awk -F / '{print $1}' | xargs kill -9

# 加载环境
eval "$(~/anaconda3/bin/conda shell.bash hook)"
conda activate bg_remove

# 启动项目
cd ${PROJECT_DIR}/backend && nohup python app.py >> ${PROJECT_DIR}/start.log &
cd ${PROJECT_DIR}/frontend && nohup npm start >> ${PROJECT_DIR}/start.log &

# 查看进程
sleep 2
netstat -tnlp| egrep ':5000|:3000' 
