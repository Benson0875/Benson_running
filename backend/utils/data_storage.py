import os
import shutil
import pandas as pd
from datetime import datetime
import logging
from typing import Optional, Dict, List
import json

class DataStorage:
    def __init__(self, base_path: str = "data"):
        self.base_path = base_path
        self.users_path = os.path.join(base_path, "users")
        self.backups_path = os.path.join(base_path, "backups")
        self.temp_path = os.path.join(base_path, "temp")
        
        # 確保所有必要的目錄存在
        self._ensure_directories()
        
        # 設置日誌
        logging.basicConfig(
            filename=os.path.join(base_path, 'data_storage.log'),
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)

    def _ensure_directories(self):
        """確保所有必要的目錄存在"""
        for path in [self.users_path, self.backups_path, self.temp_path]:
            os.makedirs(path, exist_ok=True)

    def get_activity_file_path(self, user_id: str, activity_type: str, date: datetime) -> str:
        """
        根據命名規範生成活動文件路徑
        
        Args:
            user_id: 用戶ID
            activity_type: 活動類型 (running/cycling/swimming)
            date: 活動日期
            
        Returns:
            str: 完整的文件路徑
        """
        # 確保用戶目錄存在
        user_dir = os.path.join(self.users_path, f"user_{user_id}", activity_type)
        os.makedirs(user_dir, exist_ok=True)
        
        # 生成文件名 (YYYYMM.csv)
        filename = f"{date.strftime('%Y%m')}.csv"
        return os.path.join(user_dir, filename)

    def save_activity_data(self, user_id: str, activity_type: str, data: pd.DataFrame) -> bool:
        """
        保存活動數據到CSV文件
        
        Args:
            user_id: 用戶ID
            activity_type: 活動類型
            data: 活動數據DataFrame
            
        Returns:
            bool: 是否成功保存
        """
        try:
            # 獲取當前日期
            current_date = datetime.now()
            file_path = self.get_activity_file_path(user_id, activity_type, current_date)
            
            # 如果文件已存在，讀取並合併數據
            if os.path.exists(file_path):
                existing_data = pd.read_csv(file_path)
                data = pd.concat([existing_data, data], ignore_index=True)
                data = data.drop_duplicates(subset=['activity_id'])
            
            # 保存數據
            data.to_csv(file_path, index=False)
            self.logger.info(f"Successfully saved activity data for user {user_id}, type {activity_type}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error saving activity data: {str(e)}")
            return False

    def backup_data(self, backup_type: str = "daily") -> bool:
        """
        執行數據備份
        
        Args:
            backup_type: 備份類型 (daily/weekly)
            
        Returns:
            bool: 是否成功備份
        """
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_dir = os.path.join(self.backups_path, f"{backup_type}_{timestamp}")
            
            # 創建備份目錄
            os.makedirs(backup_dir, exist_ok=True)
            
            # 複製用戶數據
            shutil.copytree(self.users_path, os.path.join(backup_dir, "users"))
            
            # 記錄備份信息
            backup_info = {
                "timestamp": timestamp,
                "type": backup_type,
                "size": self._get_directory_size(backup_dir)
            }
            
            with open(os.path.join(backup_dir, "backup_info.json"), "w") as f:
                json.dump(backup_info, f)
            
            self.logger.info(f"Successfully created {backup_type} backup at {backup_dir}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error creating backup: {str(e)}")
            return False

    def validate_activity_data(self, data: pd.DataFrame) -> Dict[str, List[str]]:
        """
        驗證活動數據的完整性和有效性
        
        Args:
            data: 要驗證的DataFrame
            
        Returns:
            Dict[str, List[str]]: 驗證結果，包含錯誤和警告信息
        """
        validation_results = {
            "errors": [],
            "warnings": []
        }
        
        # 檢查必要欄位
        required_columns = [
            "activity_id", "date", "activity_type", "duration", 
            "distance", "avg_heart_rate", "max_heart_rate"
        ]
        
        missing_columns = [col for col in required_columns if col not in data.columns]
        if missing_columns:
            validation_results["errors"].append(f"Missing required columns: {', '.join(missing_columns)}")
        
        # 檢查數據類型
        if "duration" in data.columns and not pd.to_numeric(data["duration"], errors="coerce").notnull().all():
            validation_results["errors"].append("Duration contains invalid values")
            
        if "distance" in data.columns and not pd.to_numeric(data["distance"], errors="coerce").notnull().all():
            validation_results["errors"].append("Distance contains invalid values")
        
        # 檢查數值範圍
        if "avg_heart_rate" in data.columns:
            if (data["avg_heart_rate"] < 0).any() or (data["avg_heart_rate"] > 250).any():
                validation_results["warnings"].append("Average heart rate contains values outside normal range")
        
        # 檢查日期格式
        if "date" in data.columns:
            try:
                pd.to_datetime(data["date"])
            except:
                validation_results["errors"].append("Invalid date format")
        
        return validation_results

    def _get_directory_size(self, path: str) -> int:
        """獲取目錄大小（字節）"""
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                total_size += os.path.getsize(fp)
        return total_size

    def cleanup_temp_files(self, max_age_days: int = 7) -> None:
        """
        清理臨時文件
        
        Args:
            max_age_days: 臨時文件最大保留天數
        """
        try:
            current_time = datetime.now()
            for filename in os.listdir(self.temp_path):
                file_path = os.path.join(self.temp_path, filename)
                if not os.path.isfile(file_path):
                    continue
                    
                file_age = current_time - datetime.fromtimestamp(os.path.getctime(file_path))
                
                if file_age.days >= max_age_days:  # 修改為 >= 以包含當天
                    os.remove(file_path)
                    self.logger.info(f"Cleaned up temp file: {filename}")
                    
        except Exception as e:
            self.logger.error(f"Error cleaning up temp files: {str(e)}") 