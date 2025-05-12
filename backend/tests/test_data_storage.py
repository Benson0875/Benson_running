import unittest
import os
import shutil
from datetime import datetime, timedelta
from backend.utils.data_storage import DataStorage
import pandas as pd

class TestDataStorage(unittest.TestCase):
    def setUp(self):
        """測試前的設置"""
        self.test_data_dir = "test_data"
        self.storage = DataStorage(base_path=self.test_data_dir)
        
        # 創建測試數據
        self.test_data = pd.DataFrame({
            'activity_id': ['act1', 'act2'],
            'date': ['2024-03-21', '2024-03-22'],
            'activity_type': ['running', 'running'],
            'duration': [3600, 1800],
            'distance': [10000, 5000],
            'avg_heart_rate': [150, 160],
            'max_heart_rate': [180, 190]
        })

    def tearDown(self):
        """測試後的清理"""
        if os.path.exists(self.test_data_dir):
            shutil.rmtree(self.test_data_dir)

    def test_directory_creation(self):
        """測試目錄創建"""
        self.assertTrue(os.path.exists(self.test_data_dir))
        self.assertTrue(os.path.exists(os.path.join(self.test_data_dir, "users")))
        self.assertTrue(os.path.exists(os.path.join(self.test_data_dir, "backups")))
        self.assertTrue(os.path.exists(os.path.join(self.test_data_dir, "temp")))

    def test_activity_file_path(self):
        """測試活動文件路徑生成"""
        user_id = "test_user"
        activity_type = "running"
        date = datetime(2024, 3, 21)
        
        file_path = self.storage.get_activity_file_path(user_id, activity_type, date)
        expected_path = os.path.join(
            self.test_data_dir,
            "users",
            f"user_{user_id}",
            activity_type,
            "202403.csv"
        )
        
        self.assertEqual(file_path, expected_path)
        self.assertTrue(os.path.exists(os.path.dirname(file_path)))

    def test_save_activity_data(self):
        """測試活動數據保存"""
        user_id = "test_user"
        activity_type = "running"
        
        # 保存數據
        result = self.storage.save_activity_data(user_id, activity_type, self.test_data)
        self.assertTrue(result)
        
        # 驗證文件是否創建
        file_path = self.storage.get_activity_file_path(
            user_id, 
            activity_type, 
            datetime.now()
        )
        self.assertTrue(os.path.exists(file_path))
        
        # 驗證數據是否正確保存
        saved_data = pd.read_csv(file_path)
        self.assertEqual(len(saved_data), len(self.test_data))
        self.assertTrue(all(saved_data['activity_id'] == self.test_data['activity_id']))

    def test_backup_data(self):
        """測試數據備份"""
        # 先保存一些測試數據
        self.storage.save_activity_data("test_user", "running", self.test_data)
        
        # 執行備份
        result = self.storage.backup_data(backup_type="test")
        self.assertTrue(result)
        
        # 驗證備份目錄是否創建
        backup_dirs = [d for d in os.listdir(os.path.join(self.test_data_dir, "backups"))
                      if d.startswith("test_")]
        self.assertTrue(len(backup_dirs) > 0)
        
        # 驗證備份信息文件
        backup_dir = os.path.join(self.test_data_dir, "backups", backup_dirs[0])
        self.assertTrue(os.path.exists(os.path.join(backup_dir, "backup_info.json")))

    def test_validate_activity_data(self):
        """測試數據驗證"""
        # 測試有效數據
        validation_results = self.storage.validate_activity_data(self.test_data)
        self.assertEqual(len(validation_results["errors"]), 0)
        
        # 測試無效數據
        invalid_data = self.test_data.copy()
        invalid_data.loc[0, 'duration'] = 'invalid'
        validation_results = self.storage.validate_activity_data(invalid_data)
        self.assertTrue(len(validation_results["errors"]) > 0)

    def test_cleanup_temp_files(self):
        """測試臨時文件清理"""
        # 創建一些臨時文件
        temp_dir = os.path.join(self.test_data_dir, "temp")
        test_file = os.path.join(temp_dir, "test.txt")
        with open(test_file, "w") as f:
            f.write("test content")
        
        # 執行清理
        self.storage.cleanup_temp_files(max_age_days=0)
        
        # 驗證文件是否被刪除
        self.assertFalse(os.path.exists(test_file))

if __name__ == '__main__':
    unittest.main() 