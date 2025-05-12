# Garmin Training AI Assistant

## 專案說明
這是一個結合 Garmin Connect 數據分析和 AI 訓練建議的應用程式。

## 環境需求
- Python 3.8+
- Ubuntu 20.04+

## 安裝步驟
1. 建立虛擬環境：
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

2. 安裝依賴套件：
   ```bash
   pip install -r requirements.txt
   ```

3. 設置環境變數：
   - 複製 .env.example 為 .env
   - 填入必要的環境變數

## 使用說明
1. 啟動應用程式：
   ```bash
   python backend/app.py
   ```

2. 開啟瀏覽器訪問：
   http://localhost:5000
