#!/bin/bash

# 獲取腳本所在目錄的絕對路徑
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# 啟動後端服務
echo "Starting backend service..."
cd "$SCRIPT_DIR/backend"
flask run --port=5001 &
BACKEND_PID=$!

# 啟動前端服務
echo "Starting frontend service..."
cd "$SCRIPT_DIR/frontend"
npm start &
FRONTEND_PID=$!

# 等待用戶按下 Ctrl+C
echo "Services are running. Press Ctrl+C to stop all services."
trap "kill $BACKEND_PID $FRONTEND_PID; exit" INT

# 保持腳本運行
wait 