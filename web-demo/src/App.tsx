import { useState, useEffect, useRef } from 'react';
import VERTC, { IRTCEngine, MediaType, RoomProfileType } from '@volcengine/rtc';

// 日志类型
interface LogEntry {
  time: string;
  message: string;
  type: 'info' | 'success' | 'error';
}

function App() {
  // 配置状态
  const [appId, setAppId] = useState('67890xxxxx'); // 填入你的 AppId
  const [roomId, setRoomId] = useState('test_room_001');
  const [userId] = useState(() => `user_${Math.random().toString(36).substr(2, 6)}`);
  const [token, setToken] = useState('');

  // 状态
  const [isJoined, setIsJoined] = useState(false);
  const [logs, setLogs] = useState<LogEntry[]>([]);
  const [videoEnabled, setVideoEnabled] = useState(false);
  const [audioEnabled, setAudioEnabled] = useState(false);

  // Refs
  const engineRef = useRef<IRTCEngine | null>(null);
  const localVideoRef = useRef<HTMLDivElement>(null);
  const remoteVideoRef = useRef<HTMLDivElement>(null);

  // 日志函数
  const addLog = (message: string, type: 'info' | 'success' | 'error' = 'info') => {
    const time = new Date().toLocaleTimeString();
    setLogs(prev => [...prev, { time, message, type }]);
    console.log(`[${type}] ${message}`);
  };

  // 初始化引擎
  const initEngine = () => {
    if (engineRef.current) return;

    try {
      // 创建引擎
      const engine = VERTC.createEngine(appId, {
        roomProfileType: RoomProfileType.meeting
      });
      engineRef.current = engine;

      addLog('RTC 引擎初始化成功', 'success');
    } catch (error) {
      addLog(`引擎初始化失败: ${error}`, 'error');
    }
  };

  // 加入房间
  const joinRoom = async () => {
    if (!engineRef.current) {
      initEngine();
    }

    try {
      addLog(`加入房间: ${roomId}`, 'info');
      addLog(`用户: ${userId}`, 'info');
      
      // 加入房间
      await engineRef.current?.joinRoom(
        token || null,
        roomId,
        { userId },
        { roomProfileType: RoomProfileType.meeting }
      );
      
      setIsJoined(true);
      addLog('加入房间成功', 'success');
      
      // 自动开启视频
      await engineRef.current?.startVideoCapture();
      setVideoEnabled(true);
      addLog('视频采集已开启', 'info');
      
    } catch (error) {
      addLog(`加入房间失败: ${error}`, 'error');
    }
  };

  // 离开房间
  const leaveRoom = async () => {
    try {
      await engineRef.current?.leaveRoom();
      engineRef.current?.destroy();
      engineRef.current = null;
      setIsJoined(false);
      setVideoEnabled(false);
      setAudioEnabled(false);
      addLog('离开房间成功', 'success');
    } catch (error) {
      addLog(`离开房间失败: ${error}`, 'error');
    }
  };

  // 发布流
  const publishStream = async () => {
    if (!engineRef.current) return;

    try {
      await engineRef.current?.publishStream(MediaType.VIDEO);
      addLog('已发布本地视频流', 'success');
    } catch (error) {
      addLog(`发布流失败: ${error}`, 'error');
    }
  };

  // 开启/关闭视频
  const toggleVideo = async () => {
    if (!engineRef.current) return;

    try {
      if (videoEnabled) {
        await engineRef.current?.stopVideoCapture();
        setVideoEnabled(false);
        addLog('视频已关闭', 'info');
      } else {
        await engineRef.current?.startVideoCapture();
        setVideoEnabled(true);
        addLog('视频已开启', 'info');
      }
    } catch (error) {
      addLog(`视频切换失败: ${error}`, 'error');
    }
  };

  // 开启/关闭音频
  const toggleAudio = async () => {
    if (!engineRef.current) return;

    try {
      if (audioEnabled) {
        await engineRef.current?.stopAudioCapture();
        setAudioEnabled(false);
        addLog('音频已关闭', 'info');
      } else {
        await engineRef.current?.startAudioCapture();
        setAudioEnabled(true);
        addLog('音频已开启', 'info');
      }
    } catch (error) {
      addLog(`音频切换失败: ${error}`, 'error');
    }
  };

  // 清理
  useEffect(() => {
    return () => {
      if (engineRef.current) {
        engineRef.current.destroy();
      }
    };
  }, []);

  return (
    <div className="app">
      <header className="header">
        <h1>火山 RTC Web Demo</h1>
        <p>基于 @volcengine/rtc SDK</p>
      </header>

      <div className="main">
        {/* 配置面板 */}
        <div className="config-panel">
          <h2>配置</h2>
          
          <div className="form-group">
            <label>App ID:</label>
            <input
              type="text"
              value={appId}
              onChange={e => setAppId(e.target.value)}
              placeholder="输入火山 App ID"
            />
          </div>

          <div className="form-group">
            <label>Room ID:</label>
            <input
              type="text"
              value={roomId}
              onChange={e => setRoomId(e.target.value)}
              placeholder="输入房间 ID"
            />
          </div>

          <div className="form-group">
            <label>User ID:</label>
            <input
              type="text"
              value={userId}
              readOnly
              placeholder="自动生成"
            />
          </div>

          <div className="form-group">
            <label>Token:</label>
            <input
              type="text"
              value={token}
              onChange={e => setToken(e.target.value)}
              placeholder="测试环境可留空"
            />
          </div>

          <div className="buttons">
            {!isJoined ? (
              <button onClick={joinRoom} disabled={!appId || !roomId}>
                加入房间
              </button>
            ) : (
              <>
                <button onClick={publishStream}>发布流</button>
                <button onClick={toggleVideo}>
                  {videoEnabled ? '关闭视频' : '开启视频'}
                </button>
                <button onClick={toggleAudio}>
                  {audioEnabled ? '关闭音频' : '开启音频'}
                </button>
                <button onClick={leaveRoom} className="danger">
                  离开房间
                </button>
              </>
            )}
          </div>

          {isJoined && (
            <div className="status">
              <span className="badge success">已加入</span>
              <span>Room: {roomId}</span>
              <span>User: {userId}</span>
            </div>
          )}
        </div>

        {/* 视频区域 */}
        <div className="video-area">
          <div className="video-container">
            <h3>本地预览</h3>
            <div className="video-wrapper local">
              <div ref={localVideoRef} />
              {videoEnabled && <span className="label">本地</span>}
            </div>
          </div>

          <div className="video-container">
            <h3>远端视频</h3>
            <div className="video-wrapper remote">
              <div ref={remoteVideoRef} />
            </div>
          </div>
        </div>

        {/* 日志区域 */}
        <div className="log-area">
          <h2>日志</h2>
          <div className="logs">
            {logs.map((log, i) => (
              <div key={i} className={`log ${log.type}`}>
                <span className="time">[{log.time}]</span>
                <span className="message">{log.message}</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
