import openai
import os
from typing import Dict, Any

class AIAnalyzer:
    def __init__(self, api_key: str = None, model: str = "gpt-4"):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = model
        openai.api_key = self.api_key

    def build_prompt(self, user_profile: Dict[str, Any], activity_summary: Dict[str, Any], goal: str = None) -> str:
        """
        根據用戶資料與活動摘要生成分析提示
        """
        prompt = f"""
你是一位專業運動教練與數據分析師，請根據以下用戶資料與運動摘要，給出個性化的訓練建議：

[用戶資料]
{user_profile}

[活動摘要]
{activity_summary}
"""
        if goal:
            prompt += f"\n[目標]\n{goal}\n"
        prompt += "\n請以條列式給出建議，並簡要說明分析依據。"
        return prompt

    def analyze(self, user_profile: Dict[str, Any], activity_summary: Dict[str, Any], goal: str = None) -> Dict[str, Any]:
        """
        呼叫 OpenAI API 進行分析，並解析回應
        """
        prompt = self.build_prompt(user_profile, activity_summary, goal)
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "你是一位專業運動教練與數據分析師。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=512
            )
            return self.parse_response(response)
        except Exception as e:
            return {"error": str(e)}

    def parse_response(self, response: Any) -> Dict[str, Any]:
        """
        解析 OpenAI API 回應內容，並產生結構化回應
        """
        try:
            content = response["choices"][0]["message"]["content"]
            return self.create_structured_response(content)
        except Exception as e:
            return {"error": f"Response parsing failed: {str(e)}"}

    # ----------- 分析模板區 -----------
    def template_performance_trends(self, user_profile, activity_summary):
        return f"""
請根據以下運動數據，分析近期表現趨勢，指出進步與待加強之處：\n[用戶資料]\n{user_profile}\n[活動摘要]\n{activity_summary}\n請條列說明趨勢與建議。
"""

    def template_training_load(self, user_profile, activity_summary):
        return f"""
請根據以下運動數據，分析訓練負荷是否適當，並給出調整建議：\n[用戶資料]\n{user_profile}\n[活動摘要]\n{activity_summary}\n請條列說明訓練負荷與建議。
"""

    def template_recovery(self, user_profile, activity_summary):
        return f"""
請根據以下運動數據，分析恢復狀態，並給出恢復建議：\n[用戶資料]\n{user_profile}\n[活動摘要]\n{activity_summary}\n請條列說明恢復狀態與建議。
"""

    def template_goal_progress(self, user_profile, activity_summary, goal):
        return f"""
請根據以下運動數據，分析目標達成進度，指出目前進展與後續建議：\n[用戶資料]\n{user_profile}\n[活動摘要]\n{activity_summary}\n[目標]\n{goal}\n請條列說明進度與建議。
"""

    # ----------- 洞察生成邏輯 -----------
    def generate_insight(self, insight_type: str, user_profile: Dict[str, Any], activity_summary: Dict[str, Any], goal: str = None, personalization: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        根據 insight_type 產生不同主題的分析洞察，並可加入個人化參數
        """
        # 個人化處理
        user_profile = self._personalize_profile(user_profile, personalization)
        
        if insight_type == "performance_trends":
            prompt = self.template_performance_trends(user_profile, activity_summary)
        elif insight_type == "training_load":
            prompt = self.template_training_load(user_profile, activity_summary)
        elif insight_type == "recovery":
            prompt = self.template_recovery(user_profile, activity_summary)
        elif insight_type == "goal_progress":
            prompt = self.template_goal_progress(user_profile, activity_summary, goal or "")
        else:
            prompt = self.build_prompt(user_profile, activity_summary, goal)
        
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "你是一位專業運動教練與數據分析師。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=512
            )
            return self.parse_response(response)
        except Exception as e:
            return {"error": str(e)}

    def _personalize_profile(self, user_profile: Dict[str, Any], personalization: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        根據個人化參數調整用戶資料
        """
        if not personalization:
            return user_profile
        profile = user_profile.copy()
        for k, v in personalization.items():
            profile[k] = v
        return profile

    # ----------- 回應格式化區 -----------
    def format_response(self, raw_content: str, use_markdown: bool = True, use_emoji: bool = True) -> str:
        """
        將原始回應內容格式化，支援 Markdown 與 emoji
        """
        if not raw_content:
            return ""
        content = raw_content
        if use_markdown:
            content = self._apply_markdown(content)
        if use_emoji:
            content = self._add_emoji(content)
        return content

    def _apply_markdown(self, content: str) -> str:
        """
        將條列式內容轉為 Markdown 格式
        """
        lines = content.split("\n")
        formatted_lines = []
        for line in lines:
            line = line.strip()
            if line.startswith("- "):
                formatted_lines.append(f"* {line[2:]}")
            else:
                formatted_lines.append(line)
        return "\n".join(formatted_lines)

    def _add_emoji(self, content: str) -> str:
        """
        根據關鍵字加入 emoji
        """
        emoji_map = {
            "進步": "🚀",
            "建議": "💡",
            "注意": "⚠️",
            "目標": "🎯",
            "恢復": "🔄",
            "訓練": "💪",
            "分析": "📊",
            "總結": "📝"
        }
        for keyword, emoji in emoji_map.items():
            content = content.replace(keyword, f"{emoji} {keyword}")
        return content

    def create_structured_response(self, raw_content: str, use_markdown: bool = True, use_emoji: bool = True) -> Dict[str, Any]:
        """
        產生結構化回應物件，包含原始內容、格式化內容與建議列表
        """
        formatted_content = self.format_response(raw_content, use_markdown, use_emoji)
        suggestions = []
        for line in raw_content.split("\n"):
            line = line.strip("- ")
            if line:
                suggestions.append(line)
        return {
            "raw": raw_content,
            "formatted": formatted_content,
            "suggestions": suggestions
        }
