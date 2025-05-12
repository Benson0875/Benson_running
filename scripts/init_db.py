import os
import sys

# 添加專案根目錄到 Python 路徑
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from backend.app import create_app
from backend.extensions import db
from backend.models.user import User, UserPreference
import logging

# 設定日誌
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/init_db.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def init_db():
    """初始化資料庫並創建管理員用戶"""
    try:
        # 創建應用實例
        app = create_app()
        
        with app.app_context():
            # 創建所有資料表
            db.create_all()
            logger.info("資料表創建完成")

            # 檢查是否已存在管理員用戶
            admin = User.query.filter_by(username='admin').first()
            if not admin:
                # 創建管理員用戶
                admin = User(
                    username='admin',
                    email='admin@example.com',
                    is_admin=True
                )
                admin.set_password('admin123')  # 請在生產環境中更改此密碼
                db.session.add(admin)

                # 創建管理員偏好設定
                admin_prefs = UserPreference(
                    user=admin,
                    language='zh-TW',
                    theme='light',
                    notifications_enabled=True
                )
                db.session.add(admin_prefs)

                db.session.commit()
                logger.info("管理員用戶創建完成")
            else:
                logger.info("管理員用戶已存在")

    except Exception as e:
        logger.error(f"資料庫初始化失敗: {e}")
        raise

if __name__ == '__main__':
    init_db() 