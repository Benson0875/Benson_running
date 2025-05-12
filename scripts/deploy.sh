#!/bin/bash

# 設定顏色輸出
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# 設定日誌檔案
LOG_FILE="logs/deploy_$(date +%Y%m%d_%H%M%S).log"

# 日誌函數
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

log_debug() {
    echo -e "${BLUE}[DEBUG]${NC} $1"
}

# 錯誤處理函數
handle_error() {
    log_error "$1"
    exit 1
}

# 進度顯示函數
show_progress() {
    echo -e "${GREEN}[PROGRESS]${NC} $1"
}

# 完成提示函數
show_complete() {
    echo -e "\n${GREEN}✓ $1${NC}\n"
}

# 檢查命令是否存在
check_command() {
    if ! command -v $1 &> /dev/null; then
        handle_error "$1 未安裝"
    fi
    log_info "$1 已安裝"
}

# 建立日誌目錄
mkdir -p logs

log_info "開始部署流程..."

# 檢查必要的命令
log_info "檢查必要的命令..."
check_command python3
check_command pip3
check_command virtualenv

# 檢查環境變數
if [ -z "$ENV" ]; then
    log_warning "未設定 ENV 環境變數，使用開發環境"
    export ENV=development
else
    log_info "使用 $ENV 環境"
fi

# 建立並啟動虛擬環境
if [ ! -d "venv" ]; then
    log_info "建立虛擬環境..."
    python3 -m virtualenv venv || handle_error "建立虛擬環境失敗"
    log_debug "虛擬環境建立完成"
else
    log_info "虛擬環境已存在"
fi

log_info "啟動虛擬環境..."
source venv/bin/activate || handle_error "啟動虛擬環境失敗"
log_debug "虛擬環境啟動成功"

# 建立必要的目錄
log_info "建立必要的目錄..."
mkdir -p logs
mkdir -p data/backups
mkdir -p data/temp
log_debug "目錄建立完成"

# 安裝依賴
log_info "安裝 Python 依賴..."
pip install --upgrade pip || handle_error "更新 pip 失敗"
log_debug "pip 更新完成"

# 安裝額外需要的套件
log_info "安裝額外依賴..."
pip install flask-cors || handle_error "安裝 flask-cors 失敗"
log_debug "額外依賴安裝完成"

pip install -r requirements.txt || handle_error "安裝依賴失敗"
log_debug "依賴安裝完成"

# 設定環境變數
log_info "設定環境變數..."
if [ "$ENV" = "production" ]; then
    export FLASK_ENV=production
    export FLASK_DEBUG=0
    export FLASK_APP=backend.app:app
    log_debug "設定為生產環境"
else
    export FLASK_ENV=development
    export FLASK_DEBUG=1
    export FLASK_APP=backend.app:app
    log_debug "設定為開發環境"
fi

# 設定 Python 路徑
export PYTHONPATH=$PYTHONPATH:$(pwd)
log_debug "Python 路徑設定完成: $PYTHONPATH"

# 檢查 .env 檔案
if [ ! -f ".env" ]; then
    log_warning "未找到 .env 檔案，使用預設設定"
    cat > .env << EOL
FLASK_APP=backend.app:app
FLASK_ENV=$FLASK_ENV
FLASK_DEBUG=$FLASK_DEBUG
SECRET_KEY=dev-secret-key
API_KEY=dev-api-key
DATABASE_URL=sqlite:///app.db
REDIS_URL=redis://localhost:6379/0
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
JWT_SECRET_KEY=jwt-secret-key
EOL
    log_debug ".env 檔案建立完成"
else
    log_info ".env 檔案已存在"
fi

# 初始化資料庫
log_info "初始化資料庫..."
python scripts/init_db.py || handle_error "資料庫初始化失敗"
log_debug "資料庫初始化完成"

# 執行資料庫遷移
log_info "執行資料庫遷移..."
flask db init || log_warning "資料庫初始化失敗，可能已經初始化"
log_debug "資料庫遷移初始化完成"

flask db migrate || log_warning "資料庫遷移失敗，可能沒有變更"
log_debug "資料庫遷移腳本生成完成"

flask db upgrade || log_warning "資料庫升級失敗"
log_debug "資料庫升級完成"

# 啟動監控服務
log_info "啟動監控服務..."
python scripts/monitor.py &
MONITOR_PID=$!
log_debug "監控服務啟動完成 (PID: $MONITOR_PID)"

# 啟動備份服務
log_info "啟動備份服務..."
python scripts/backup.py &
BACKUP_PID=$!
log_debug "備份服務啟動完成 (PID: $BACKUP_PID)"

# 啟動應用程式
log_info "啟動應用程式..."
if [ "$ENV" = "production" ]; then
    if ! command -v gunicorn &> /dev/null; then
        log_info "安裝 gunicorn..."
        pip install gunicorn || handle_error "安裝 gunicorn 失敗"
    fi
    log_debug "使用 gunicorn 啟動應用程式"
    gunicorn -w 4 -b 0.0.0.0:5000 backend.app:app &
    APP_PID=$!
else
    log_debug "使用 flask run 啟動應用程式"
    flask run &
    APP_PID=$!
fi

# 顯示完成訊息
echo -e "\n${GREEN}部署完成！${NC}"
echo -e "應用運行在: http://localhost:5000"
echo -e "監控服務 PID: $MONITOR_PID"
echo -e "備份服務 PID: $BACKUP_PID"
echo -e "應用服務 PID: $APP_PID"

# 清理程序
trap "kill $MONITOR_PID $BACKUP_PID $APP_PID 2>/dev/null" EXIT 