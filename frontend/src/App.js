import React, { useState, useEffect } from 'react';
import './App.css';

// API 基礎 URL
const API_BASE_URL = 'http://localhost:5001';

function App() {
  const [apiStatus, setApiStatus] = useState('Checking...');
  const [selectedSport, setSelectedSport] = useState('');
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [analysisResult, setAnalysisResult] = useState(null);

  const sports = [
    { id: 'running', name: '跑步', icon: '🏃' },
    { id: 'cycling', name: '自行車', icon: '🚴' },
    { id: 'swimming', name: '游泳', icon: '🏊' },
    { id: 'hiking', name: '健行', icon: '🥾' },
    { id: 'gym', name: '健身房', icon: '💪' },
    { id: 'basketball', name: '籃球', icon: '🏀' },
    { id: 'tennis', name: '網球', icon: '🎾' },
    { id: 'yoga', name: '瑜伽', icon: '🧘' },
    { id: 'dancing', name: '舞蹈', icon: '💃' },
    { id: 'martial_arts', name: '武術', icon: '🥋' }
  ];

  useEffect(() => {
    // 測試後端 API 連接
    fetch(`${API_BASE_URL}/api/health`)
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then(data => {
        setApiStatus('Connected to API');
        console.log('API Health Check:', data);
      })
      .catch(error => {
        setApiStatus('API Connection Error');
        console.error('API Error:', error);
      });
  }, []);

  const handleSportSelect = (sportId) => {
    setSelectedSport(sportId);
  };

  const handleAnalyze = async () => {
    if (!selectedSport) {
      alert('請先選擇運動類型');
      return;
    }

    setIsAnalyzing(true);
    try {
      const response = await fetch(`${API_BASE_URL}/api/analyze/city`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          sport: selectedSport,
          location: '台北市',
          weather: '晴天',
          time: '早晨'
        }),
      });

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      const data = await response.json();
      setAnalysisResult(data);
      console.log('Analysis result:', data);
    } catch (error) {
      console.error('Analysis error:', error);
      alert('分析過程中發生錯誤');
    } finally {
      setIsAnalyzing(false);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <div className="app-title">
          <h1>Garmin AI Assistant</h1>
          <p className="subtitle">智能運動分析助手</p>
        </div>
        
        <div className="status-bar">
          <span className={`status-indicator ${apiStatus === 'Connected to API' ? 'connected' : 'disconnected'}`}>
            {apiStatus}
          </span>
        </div>

        <div className="sport-selection">
          <h2>選擇運動類型</h2>
          <div className="sport-grid">
            {sports.map(sport => (
              <div
                key={sport.id}
                className={`sport-card ${selectedSport === sport.id ? 'selected' : ''}`}
                onClick={() => handleSportSelect(sport.id)}
              >
                <span className="sport-icon">{sport.icon}</span>
                <span className="sport-name">{sport.name}</span>
              </div>
            ))}
          </div>
        </div>

        <button 
          className={`analyze-button ${selectedSport ? 'active' : ''}`}
          onClick={handleAnalyze}
          disabled={!selectedSport || isAnalyzing}
        >
          {isAnalyzing ? '分析中...' : '開始分析'}
        </button>

        {analysisResult && (
          <div className="analysis-result">
            <h3>分析結果</h3>
            <pre>{JSON.stringify(analysisResult, null, 2)}</pre>
          </div>
        )}
      </header>
    </div>
  );
}

export default App;
