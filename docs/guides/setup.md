# Garmin AI Assistant 設置指南

## 系統需求
- Python 3.8 或更高版本
- pip（Python 包管理器）
- virtualenv（Python 虛擬環境）
- Redis 服務器（用於緩存和消息隊列）
- SQLite 或 PostgreSQL（數據庫）

## 安裝步驟

### 1. 克隆代碼庫
```bash
git clone https://github.com/your-username/garmin-ai-assistant.git
cd garmin-ai-assistant
```

### 2. 設置虛擬環境
```bash
python3 -m virtualenv venv
source venv/bin/activate  # Linux/Mac
# 或
.\venv\Scripts\activate  # Windows
```

### 3. 安裝依賴
```bash
pip install -r requirements.txt
```

### 4. 配置環境變數
創建 `.env` 文件並設置以下變數：
```env
FLASK_APP=backend.app:app
FLASK_ENV=development  # 或 production
FLASK_DEBUG=1  # 開發環境設為 1，生產環境設為 0
SECRET_KEY=your-secret-key
API_KEY=your-api-key
DATABASE_URL=sqlite:///app.db  # 或 PostgreSQL URL
REDIS_URL=redis://localhost:6379/0
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
JWT_SECRET_KEY=your-jwt-secret-key
```

### 5. 初始化數據庫
```bash
python scripts/init_db.py
```

### 6. 執行數據庫遷移
```bash
flask db init
flask db migrate
flask db upgrade
```

### 7. 啟動服務
使用部署腳本：
```bash
chmod +x scripts/deploy.sh
./scripts/deploy.sh
```

或手動啟動各個服務：

#### 開發環境
```bash
# 啟動 Redis（如果尚未運行）
redis-server

# 啟動 Celery 工作進程
celery -A backend.celery worker --loglevel=info

# 啟動 Flask 應用
flask run
```

#### 生產環境
```bash
# 啟動 Redis
redis-server

# 啟動 Celery 工作進程
celery -A backend.celery worker --loglevel=info

# 啟動 Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 backend.app:app
```

## 目錄結構
```
garmin-ai-assistant/
├── backend/           # 後端代碼
├── frontend/          # 前端代碼
├── scripts/           # 腳本文件
├── docs/             # 文檔
├── tests/            # 測試文件
├── logs/             # 日誌文件
├── data/             # 數據文件
│   ├── backups/      # 備份文件
│   └── temp/         # 臨時文件
└── venv/             # 虛擬環境
```

## 驗證安裝
1. 訪問 http://localhost:5000
2. 使用默認管理員帳號登入：
   - 用戶名：admin
   - 密碼：admin123

## 常見問題

### 1. 數據庫連接錯誤
- 檢查 DATABASE_URL 是否正確
- 確保數據庫服務正在運行
- 檢查數據庫用戶權限

### 2. Redis 連接錯誤
- 確保 Redis 服務正在運行
- 檢查 REDIS_URL 是否正確
- 檢查 Redis 端口是否被佔用

### 3. 模塊導入錯誤
- 確保在正確的虛擬環境中
- 檢查 PYTHONPATH 設置
- 重新安裝依賴：`pip install -r requirements.txt`

## 下一步
- 查看 [用戶指南](user-guide.md)
- 閱讀 [API 文檔](../api/README.md)
- 了解 [維護程序](../maintenance/README.md) 