# Garmin AI Assistant API 文檔

## 概述
Garmin AI Assistant API 提供了一系列端點，用於管理用戶活動、偏好設定和數據分析。所有 API 請求都需要使用 API Key 進行認證。

## 認證
所有 API 請求都需要在 Header 中包含 `X-API-Key`。

```http
X-API-Key: your-api-key-here
```

## 基礎 URL
- 開發環境：`http://localhost:5000/api`
- 生產環境：`https://your-domain.com/api`

## API 端點

### 活動相關

#### 獲取活動列表
```http
GET /activities
```

**響應**
```json
{
    "status": "success",
    "data": {
        "activities": [
            {
                "id": 1,
                "title": "晨跑",
                "date": "2024-03-20T08:00:00",
                "type": "running",
                "distance": 5.2,
                "duration": 1800
            }
        ]
    }
}
```

#### 創建新活動
```http
POST /activities
```

**請求體**
```json
{
    "title": "晨跑",
    "date": "2024-03-20T08:00:00",
    "type": "running",
    "distance": 5.2,
    "duration": 1800
}
```

### 用戶相關

#### 獲取用戶資料
```http
GET /user
```

**響應**
```json
{
    "status": "success",
    "data": {
        "user": {
            "id": 1,
            "username": "user1",
            "email": "user@example.com",
            "is_admin": false
        }
    }
}
```

#### 更新用戶偏好
```http
POST /user/preferences
```

**請求體**
```json
{
    "language": "zh-TW",
    "theme": "dark",
    "notifications_enabled": true
}
```

### 分析相關

#### 獲取活動分析
```http
POST /analyze
```

**請求體**
```json
{
    "activity_id": 1
}
```

**響應**
```json
{
    "status": "success",
    "data": {
        "formatted": "您的晨跑表現優於平均水準...",
        "suggestions": [
            "建議增加跑步距離",
            "注意心率控制"
        ]
    }
}
```

## 錯誤處理
所有錯誤響應都遵循以下格式：

```json
{
    "status": "error",
    "error": "錯誤描述"
}
```

常見錯誤代碼：
- 400: 請求格式錯誤
- 401: 未授權
- 403: 禁止訪問
- 404: 資源不存在
- 500: 服務器錯誤

## 速率限制
API 請求受到速率限制：
- 一般端點：每分鐘 10 次請求
- 分析端點：每分鐘 5 次請求
- Webhook：每分鐘 20 次請求

## 版本控制
當前 API 版本：v1

## 支持
如有問題，請聯繫：support@example.com 