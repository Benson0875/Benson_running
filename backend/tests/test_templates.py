import unittest
import os
from bs4 import BeautifulSoup

class TestTemplates(unittest.TestCase):
    def setUp(self):
        self.templates_dir = os.path.join(os.path.dirname(__file__), '../../frontend/templates')
        
    def read_template(self, filename):
        with open(os.path.join(self.templates_dir, filename), 'r', encoding='utf-8') as f:
            return f.read()

    def test_index_template(self):
        """測試首頁模板結構"""
        html = self.read_template('index.html')
        soup = BeautifulSoup(html, 'html.parser')
        
        # 測試基本結構
        self.assertIsNotNone(soup.find('html'))
        self.assertIsNotNone(soup.find('head'))
        self.assertIsNotNone(soup.find('body'))
        
        # 測試導航欄
        nav = soup.find('nav')
        self.assertIsNotNone(nav)
        nav_links = nav.find_all('a')
        self.assertEqual(len(nav_links), 4)  # 首頁、活動、洞察、個人資料
        
        # 測試登入表單
        login_form = soup.find('form', {'id': 'login-form'})
        self.assertIsNotNone(login_form)
        self.assertIsNotNone(login_form.find('input', {'type': 'text'}))
        self.assertIsNotNone(login_form.find('input', {'type': 'password'}))

    def test_activities_template(self):
        """測試活動頁面模板結構"""
        html = self.read_template('activities.html')
        soup = BeautifulSoup(html, 'html.parser')
        
        # 測試過濾表單
        filter_form = soup.find('form', {'id': 'filter-form'})
        self.assertIsNotNone(filter_form)
        self.assertIsNotNone(filter_form.find('input', {'type': 'date'}))
        self.assertIsNotNone(filter_form.find('select', {'id': 'activity-type'}))
        
        # 測試活動列表
        activity_list = soup.find('section', {'id': 'activity-list'})
        self.assertIsNotNone(activity_list)

    def test_insights_template(self):
        """測試洞察頁面模板結構"""
        html = self.read_template('insights.html')
        soup = BeautifulSoup(html, 'html.parser')
        
        # 測試圖表容器
        chart_containers = soup.find_all('div', {'class': 'chart-container'})
        self.assertEqual(len(chart_containers), 2)  # 表現趨勢和訓練負荷圖表
        
        # 測試 AI 回應區塊
        ai_response = soup.find('section', {'id': 'ai-response'})
        self.assertIsNotNone(ai_response)
        
        # 測試進度追蹤區塊
        progress_tracking = soup.find('section', {'id': 'progress-tracking'})
        self.assertIsNotNone(progress_tracking)
        self.assertIsNotNone(progress_tracking.find('div', {'class': 'progress-bar'}))

if __name__ == '__main__':
    unittest.main() 