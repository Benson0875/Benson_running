import os
import shutil
import datetime
import logging
import subprocess
import zipfile
from pathlib import Path
from config.config import Config

# 設定日誌
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/backup.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def create_backup():
    """建立資料庫和檔案備份"""
    try:
        # 建立備份目錄
        backup_dir = Path(Config.BACKUP_DIR)
        backup_dir.mkdir(parents=True, exist_ok=True)
        
        # 產生備份名稱
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_name = f'backup_{timestamp}'
        backup_path = backup_dir / backup_name
        backup_path.mkdir(exist_ok=True)
        
        logger.info(f"開始建立備份: {backup_name}")
        
        # 備份資料庫
        if Config.SQLALCHEMY_DATABASE_URI.startswith('sqlite'):
            # SQLite 備份
            db_path = Config.SQLALCHEMY_DATABASE_URI.replace('sqlite:///', '')
            if os.path.exists(db_path):
                shutil.copy2(db_path, backup_path / 'database.db')
                logger.info("SQLite 資料庫備份完成")
            else:
                logger.warning(f"找不到 SQLite 資料庫檔案: {db_path}")
        else:
            # PostgreSQL 備份
            try:
                subprocess.run([
                    'pg_dump',
                    '-h', os.getenv('DB_HOST', 'localhost'),
                    '-U', os.getenv('DB_USER', 'postgres'),
                    '-d', os.getenv('DB_NAME', 'postgres'),
                    '-f', str(backup_path / 'database.sql')
                ], check=True, env=dict(os.environ, PGPASSWORD=os.getenv('DB_PASSWORD', '')))
                logger.info("PostgreSQL 資料庫備份完成")
            except subprocess.CalledProcessError as e:
                logger.error(f"PostgreSQL 備份失敗: {e}")
                raise
        
        # 備份上傳的檔案
        upload_dir = Path(Config.UPLOAD_FOLDER)
        if upload_dir.exists():
            shutil.copytree(upload_dir, backup_path / 'uploads')
            logger.info("上傳檔案備份完成")
        else:
            logger.warning(f"找不到上傳目錄: {upload_dir}")
        
        # 壓縮備份
        zip_path = backup_dir / f'{backup_name}.zip'
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, _, files in os.walk(backup_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, backup_path)
                    zipf.write(file_path, arcname)
        
        # 刪除未壓縮的備份目錄
        shutil.rmtree(backup_path)
        logger.info(f"備份壓縮完成: {zip_path}")
        
        # 清理舊備份
        cleanup_old_backups()
        
        return str(zip_path)
    
    except Exception as e:
        logger.error(f"備份過程發生錯誤: {e}")
        raise

def cleanup_old_backups():
    """清理超過保留期限的備份"""
    try:
        backup_dir = Path(Config.BACKUP_DIR)
        retention_days = Config.BACKUP_RETENTION_DAYS
        cutoff_date = datetime.datetime.now() - datetime.timedelta(days=retention_days)
        
        for backup_file in backup_dir.glob('backup_*.zip'):
            try:
                # 從檔名解析日期
                date_str = backup_file.stem.split('_')[1]
                backup_date = datetime.datetime.strptime(date_str, '%Y%m%d')
                
                if backup_date < cutoff_date:
                    backup_file.unlink()
                    logger.info(f"刪除舊備份: {backup_file}")
            except (ValueError, IndexError) as e:
                logger.warning(f"無法解析備份檔名 {backup_file}: {e}")
                continue
        
        logger.info("清理舊備份完成")
    
    except Exception as e:
        logger.error(f"清理舊備份時發生錯誤: {e}")
        raise

if __name__ == '__main__':
    try:
        backup_path = create_backup()
        logger.info(f"備份成功完成: {backup_path}")
    except Exception as e:
        logger.error(f"備份失敗: {e}")
        exit(1) 