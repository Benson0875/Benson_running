import unittest
from unittest.mock import patch, MagicMock
from backend.models.ai_analyzer import AIAnalyzer

class TestAIAnalyzer(unittest.TestCase):
    def setUp(self):
        self.analyzer = AIAnalyzer()
        self.test_user_profile = {
            "name": "測試用戶",
            "age": 30,
            "fitness_level": "中級",
            "preferred_activities": ["跑步", "游泳"]
        }
        self.test_activity_summary = {
            "type": "跑步",
            "distance": 5000,
            "duration": 1800,
            "avg_heart_rate": 150
        }

    @patch('openai.ChatCompletion.create')
    def test_analyze(self, mock_create):
        # 模擬 OpenAI API 回應
        mock_response = MagicMock()
        mock_response.choices = [MagicMock(message={'content': '分析結果'})]
        mock_create.return_value = mock_response

        # 測試分析數據
        result = self.analyzer.analyze(self.test_user_profile, self.test_activity_summary)
        self.assertIsInstance(result, dict)
        self.assertIn('formatted', result)

    def test_build_prompt(self):
        # 測試提示詞生成
        prompt = self.analyzer.build_prompt(self.test_user_profile, self.test_activity_summary)
        self.assertIn("測試用戶", prompt)
        self.assertIn("跑步", prompt)
        self.assertIn("5000", prompt)

    def test_template_performance_trends(self):
        # 測試表現趨勢模板
        template = self.analyzer.template_performance_trends(
            self.test_user_profile, 
            self.test_activity_summary
        )
        self.assertIn("表現趨勢", template)
        self.assertIn("測試用戶", template)

    def test_template_training_load(self):
        # 測試訓練負荷模板
        template = self.analyzer.template_training_load(
            self.test_user_profile, 
            self.test_activity_summary
        )
        self.assertIn("訓練負荷", template)
        self.assertIn("5000", template)

    def test_personalize_profile(self):
        # 測試個人化功能
        personalization = {
            "fitness_level": "高級",
            "new_goal": "馬拉松"
        }
        personalized = self.analyzer._personalize_profile(
            self.test_user_profile, 
            personalization
        )
        self.assertEqual(personalized["fitness_level"], "高級")
        self.assertEqual(personalized["new_goal"], "馬拉松")

    def test_format_response(self):
        # 測試格式化回應
        raw_response = '• 建議1\n• 建議2'
        formatted = self.analyzer.format_response(raw_response)
        self.assertIn('建議1', formatted)
        self.assertIn('建議2', formatted)

    def test_create_structured_response(self):
        # 測試創建結構化回應
        raw_content = '• 建議1\n• 建議2'
        structured = self.analyzer.create_structured_response(raw_content)
        self.assertEqual(structured['raw'], raw_content)
        self.assertIn('建議1', structured['formatted'])
        self.assertIn('建議2', structured['formatted'])
        self.assertIsInstance(structured['suggestions'], list)

if __name__ == '__main__':
    unittest.main() 