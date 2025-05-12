from flask import Flask, jsonify, request
from flask_cors import CORS
import jwt
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv, find_dotenv
import logging
from openai import OpenAI

# 自動偵測並載入 .env（專案根目錄或 backend 目錄）
env_path = find_dotenv()
if not env_path:
    # 嘗試 backend 目錄
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(env_path):
        load_dotenv(env_path)
else:
    load_dotenv(env_path)

openai_api_key = os.getenv('OPENAI_API_KEY')
if openai_api_key:
    print("[INFO] OPENAI_API_KEY 已載入")
else:
    print("[WARNING] OPENAI_API_KEY 未設定，AI 分析功能將無法使用")

# 設定 logging 格式
log_dir = os.path.join(os.path.dirname(__file__), 'logs')
os.makedirs(log_dir, exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(log_dir, "app.log"), encoding='utf-8'),
        logging.StreamHandler()
    ]
)

def create_app():
    app = Flask(__name__)
    CORS(app)
    
    # 基本配置
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev')
    
    # 設置 OpenAI API
    client = OpenAI(api_key=openai_api_key)
    
    # 健康檢查端點
    @app.route('/api/health')
    def health_check():
        return jsonify({
            'status': 'healthy',
            'version': '1.0.0'
        })
    
    # 城市運動分析端點
    @app.route('/api/analyze/city', methods=['POST'])
    def analyze_city_sport():
        logging.info('收到 /api/analyze/city 請求')
        data = request.get_json()
        logging.info(f'收到資料: {data}')
        sport = data.get('sport')
        location = data.get('location', '台北市')
        weather = data.get('weather', '晴天')
        time = data.get('time', '早晨')
        
        if not sport:
            logging.warning('未提供運動類型')
            return jsonify({
                'status': 'error',
                'message': '請選擇運動類型'
            }), 400
        
        if not openai_api_key:
            logging.error('AI 金鑰未設定')
            return jsonify({
                'status': 'error',
                'message': 'AI 金鑰未設定，請聯絡管理員'
            }), 500
        try:
            logging.info('呼叫 OpenAI API...')
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "你是一個專業的城市運動分析師，請根據用戶的運動類型、地點、天氣和時間提供專業的分析和建議。"},
                    {"role": "user", "content": f"""
                    請分析以下運動情況：
                    1. 運動類型：{get_sport_name(sport)}
                    2. 地點：{location}
                    3. 天氣：{weather}
                    4. 時間：{time}
                    
                    請提供以下信息：
                    1. 適合的運動路線建議
                    2. 天氣相關注意事項
                    3. 安全建議
                    4. 運動強度建議
                    5. 裝備建議
                    """}
                ]
            )
            logging.info(f'OpenAI 回應: {response}')
            ai_response = response.choices[0].message.content
            
            # 格式化分析結果
            analysis_result = {
                'status': 'success',
                'sport': sport,
                'location': location,
                'weather': weather,
                'time': time,
                'analysis': {
                    'ai_response': ai_response,
                    'timestamp': datetime.now().isoformat()
                }
            }
            logging.info('分析成功，回傳結果')
            return jsonify(analysis_result)
            
        except Exception as e:
            logging.error(f"OpenAI API Error: {str(e)}", exc_info=True)
            return jsonify({
                'status': 'error',
                'message': 'AI 分析服務暫時無法使用，請稍後再試'
            }), 500
    
    # 獲取城市運動熱點
    @app.route('/api/city/hotspots', methods=['GET'])
    def get_city_hotspots():
        location = request.args.get('location', '台北市')
        
        try:
            # 使用 OpenAI API 獲取熱點信息
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "你是一個專業的城市運動規劃師，請提供城市中適合運動的地點和路線建議。"},
                    {"role": "user", "content": f"請提供{location}的運動熱點，包括：\n1. 公園\n2. 運動場\n3. 自行車道\n4. 跑步路線\n5. 每個地點的適合運動類型"}
                ]
            )
            
            # 解析 AI 回應
            ai_response = response.choices[0].message.content
            
            return jsonify({
                'status': 'success',
                'location': location,
                'hotspots': ai_response
            })
            
        except Exception as e:
            logging.error(f"OpenAI API Error: {str(e)}", exc_info=True)
            return jsonify({
                'status': 'error',
                'message': '無法獲取城市運動熱點信息'
            }), 500
    
    return app

def get_sport_name(sport_id):
    sport_names = {
        'running': '跑步',
        'cycling': '自行車',
        'swimming': '游泳',
        'hiking': '健行',
        'gym': '健身房',
        'basketball': '籃球',
        'tennis': '網球',
        'yoga': '瑜伽',
        'dancing': '舞蹈',
        'martial_arts': '武術'
    }
    return sport_names.get(sport_id, sport_id)

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5001)  # 使用不同的端口
