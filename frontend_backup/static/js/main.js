// 活動選擇處理
function handleActivitySelect(activityId) {
    // 觸發活動詳情顯示或分析
    window.location.href = `/activities/${activityId}`;
}

// 分析請求按鈕
function requestAnalysis(insightType) {
    const activityId = document.querySelector('.activity-item.selected')?.dataset.id;
    if (!activityId) {
        alert('請先選擇一個活動！');
        return;
    }
    fetch(`/api/analyze`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ activity_id: activityId, insight_type: insightType })
    })
    .then(res => res.json())
    .then(data => {
        document.getElementById('ai-response-content').innerHTML = data.formatted;
        updateSuggestions(data.suggestions);
    });
}

// 資料刷新機制
function refreshActivities() {
    fetch('/api/activities')
        .then(res => res.json())
        .then(data => {
            renderActivityList(data.activities);
        });
}

function renderActivityList(activities) {
    const list = document.getElementById('activity-list-ul');
    list.innerHTML = '';
    activities.forEach(act => {
        const li = document.createElement('li');
        li.className = 'activity-item';
        li.dataset.id = act.id;
        li.innerHTML = `<h3>${act.title}</h3><p>日期：${act.date}</p><p>類型：${act.type}</p>`;
        li.onclick = () => handleActivitySelect(act.id);
        list.appendChild(li);
    });
}

// 用戶偏好設定
function saveUserPreferences() {
    const prefs = {
        theme: document.getElementById('theme-select').value,
        language: document.getElementById('language-select').value
    };
    fetch('/api/user/preferences', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(prefs)
    }).then(() => alert('偏好設定已儲存！'));
}

// 即時更新（WebSocket 範例）
let ws;
function setupRealtimeUpdates() {
    ws = new WebSocket('ws://' + window.location.host + '/ws/updates');
    ws.onmessage = function(event) {
        const data = JSON.parse(event.data);
        if (data.type === 'activity_update') {
            refreshActivities();
        }
        if (data.type === 'analysis_update') {
            document.getElementById('ai-response-content').innerHTML = data.formatted;
            updateSuggestions(data.suggestions);
        }
    };
}

function updateSuggestions(suggestions) {
    const ul = document.getElementById('suggestions-list');
    ul.innerHTML = '';
    suggestions.forEach(s => {
        const li = document.createElement('li');
        li.textContent = s;
        ul.appendChild(li);
    });
}

document.addEventListener('DOMContentLoaded', () => {
    // 初始化活動列表與即時更新
    refreshActivities();
    setupRealtimeUpdates();
    // 綁定偏好設定儲存
    const prefBtn = document.getElementById('save-preferences-btn');
    if (prefBtn) prefBtn.onclick = saveUserPreferences;
});
